# Revision = q$Id: Locks.pm,v 1.10 2003/05/06 09:39:05 ruslan Exp $;
# Date = q$Date: 2003/05/06 09:39:05 $;

package EMU::Locks;
use strict;
use Fcntl qw(:DEFAULT :flock);
use Symbol;

sub new
{
	my ($proto, %options) = @_;
	my $class = ref($proto) || $proto;
	my $self  = 
        	{
        	'lockdb'	=> {},
        	'timeout'	=> 0,
        	'initsub'	=> undef,
        	'waitingsub'=> undef,
        	'type'		=> 'flock',
        	};
	bless $self, $class;
        
    $self->timeout($options{'timeout'}) if ($options{'timeout'});
    $self->initsub($options{'initsub'}) if ($options{'initsub'});
    $self->waitingsub($options{'waitingsub'}) if ($options{'waitingsub'});
    $self->{type} = $options{'type'} if ( $options{'type'} );
        
    return $self;
}

sub initsub
{
	my ($self, $r_intsub) = @_;
	$self->{'initsub'} = $r_intsub if ($r_intsub && ref($r_intsub) eq 'CODE');
	return $self->{'initsub'};
}

sub waitingsub
{
	my ($self, $r_wsub) = @_;
	$self->{'waitingsub'} = $r_wsub if ($r_wsub && ref($r_wsub) eq 'CODE');
	return $self->{'waitingsub'};
}

sub timeout
{
	my ($self, $value) = @_;
	$self->{'timeout'} = $value if (defined $value);
	
	return $self->{'timeout'};
}

sub _normalize_id
{
	my ($self, $id) = @_;
	$id = "" . $id;
	$id =~ s/^[^=]+=//;
	
	return $id;
}

sub lock_check
{
	my ($self, $id) = @_;
	return $self->{'lockdb'}->{$self->_normalize_id($id)}->{'fh'};
}

sub lock_search
{
	my ($self, $value, $criteria, $excludepostfix) = @_;
	return 0 unless $value;
	$criteria ||= 'path';
	if ($criteria eq 'path')
	{
		$value = "$value.lock" unless ($excludepostfix);
	}
	
	for my $key ( keys %{$self->{lockdb}} )
	{
		return $key if ($self->{lockdb}->{$key}->{$criteria} eq $value);
	}
	
	return 0;
}

sub lock_remove
{
	my ($self, $id) = @_;
	return 0 unless $id;

	$id = $self->_normalize_id($id);
	
	my $lock = $self->{'lockdb'}->{$id};
	if ($lock && ref $lock eq 'HASH')
	{
		my $refid;
		if ( $refid = $lock->{'reference_id'} )
		{
			# it's ghost lock, and we should kick its ass, decrease refcount of 
			# the real lock to which our ghost lock is referencing
			$self->{'lockdb'}->{$refid}->{refcnt} && $self->{'lockdb'}->{$refid}->{refcnt}--;
			# delete lock with zero refcounts (i.e. it's zombie)
			$self->lock_remove($refid) if ( $self->{'lockdb'}->{$refid}->{refcnt} == 0 &&
											$refid ne $id); # infinite loop
			
			delete $self->{'lockdb'}->{$id};
			EMU::debug("ID: $id; Removed ghost lock");
			return 1;
		}
		
		if ( $self->{lockdb}->{$id}->{refcnt} && --$self->{lockdb}->{$id}->{refcnt} )
		{
			# there are references still, can't release lock
			EMU::debug("PATH: " . $lock->{'path'} . "; can't remove lock - we have " . $lock->{refcnt} . " lock reference(s) still");
			return 0;
		}
		
		EMU::debug("removing lock $id for " . $lock->{'path'} . ' called from ' . (caller(1))[3]);
		close $lock->{'fh'};
		unlink $lock->{'path'};
		delete $self->{'lockdb'}->{$id};
		return 1;
	}
	
	EMU::debug("ID: $id; no lock to remove, called from " . (caller(1))[3]);
	return 0;
}

sub locks_clean
{
	my ($self) = @_;
	EMU::debug( "Locks to remove: ", (join ', ', keys %{$self->{'lockdb'}}) );
	for my $key ( keys %{$self->{'lockdb'}} )
	{
		$self->lock_remove( $key );
	}
}

sub lock_create
{
	my ($self, @params) = @_;
	if ( !$self->{type} || lc $self->{type} eq 'flock' )
	{
		return $self->lock_create_flock(@params);
	} 
	else
	{
		return $self->lock_create_file(@params);
	}
}

sub lock_create_file
{
	my ($self, $name, $id, $type, $excludepostfix) = @_;
	return undef unless( $name || $id );
	
	$id = $self->_normalize_id($id);

	my $res = $self->has_cached_lock($id, $name);
	return $res if $res; # return cached lock
	
	my $fh = Symbol::gensym;
	my $fname = ($excludepostfix) ? $name : "$name.lock";
	
	if ($self->initsub)
	{
		&{$self->initsub};
		EMU::debug("PATH: $fname; init sub");
	}

	my $timeout = $self->timeout;
	
	WAIT_LOCK:
	{
		if ( -e $fname )
		{
			if ( defined $timeout &&  $timeout > 0 )
			{
				$timeout--;
				EMU::debug("PATH: $fname; can't lock. timeout: $timeout second(s).");
				if ($self->waitingsub)
				{
					&{$self->waitingsub};
					EMU::debug("PATH: $fname; waiting sub");
				}
				
				sleep 1;
				redo WAIT_LOCK;
			}
			EMU::debug("PATH: $fname; taking over lock after timeout");
		}
	}
	
	unless ( $self->_sysopen_file($fh, $fname) )
	{
		EMU::debug("PATH: $fname; can't sysopen lockfile: $!");
		return undef;
	}
	
	$self->_store_lock($id, $fh, $fname);
	return $self->{'lockdb'}->{$id};
}

sub lock_create_flock
{
	my ($self, $name, $id, $type, $excludepostfix) = @_;
	return undef unless( $name || $id );
	
	my $mode = LOCK_EX;
	my $nonblocking = 0;
	
	if ($type && ref($type) eq 'HASH')
	{
		if ($type->{'mode'})
		{
			$mode = ($type->{'mode'} eq 'read') ? LOCK_SH : LOCK_EX;
		}
		if ($type->{'nb'})
		{
			$mode |= LOCK_NB;
			$nonblocking = 1;
		}
	}

	$id = $self->_normalize_id($id);
	
	my $res = $self->has_cached_lock($id, $name);
	return $res if $res; # return cached lock
	
	my $fh = Symbol::gensym;
	my $fname = ($excludepostfix) ? $name : "$name.lock";

	unless ( $self->_sysopen_file($fh, $fname) )
	{
		EMU::debug("PATH: $fname; can't sysopen lockfile: $!");
		return undef;
	}
		
	if ($self->initsub)
	{
		&{$self->initsub};
		EMU::debug("init sub was called for flock named $fname");
	}
	
	my $timeout = $self->timeout;
	
	WAIT_LOCK:
	{
		unless ( flock $fh, $mode )
		{
			if ( $nonblocking )
			{
				if ( defined $timeout &&  $timeout > 0 )
				{
					$timeout--;
					EMU::debug("can't get lock on $fname. i'll try $timeout second(s).");
					if ($self->waitingsub)
					{
						&{$self->waitingsub};
						EMU::debug("waiting sub was called for flock named $fname");
					}
					
					sleep 1;
					redo WAIT_LOCK;
				}
			}
			close $fh;
			EMU::debug("give up: can't get lock $fname");
			return 0;
		}
	}
	
	$self->_store_lock($id, $fh, $fname);
	return $self->{'lockdb'}->{$id};
}

sub has_cached_lock
{
	my ($self, $id, $name) = @_;
	
	# Well, ok. Maybe it will solve this timeout problem.
	# If we have local lock (local - in the scope of current process/thread)
	# then we should return cached handle, and do not try to create new one.
	
	my $bCanCache = 1;
	my $lock_type = lc $self->{type};
	# Windows is off with flock cache.
	$bCanCache = 0 if ( $^O =~ /Win32/i && $lock_type eq 'flock' );
	if ( $bCanCache )
	{
		my $prevLock_key = $self->lock_search($name, 'path');
		if ( $prevLock_key && $prevLock_key ne $id)
		{
			$self->{lockdb}->{$prevLock_key}->{refcnt}++;
			$self->_store_lock($id, '', '', 0, $prevLock_key);
			EMU::debug("PATH: $name; ID: $id using cached lock (refid $prevLock_key), refcount = " . $self->{lockdb}->{$prevLock_key}->{refcnt});
			return $self->{lockdb}->{$prevLock_key};
		} elsif ( $prevLock_key ) {
			# we have such lock and it's the same id!
			# perphaps someone is trying to lock the same object twice
			# let's return to him the same object and increase refcount
			$self->{lockdb}->{$id}->{refcnt}++;
			return $self->{lockdb}->{$id};
		}
	}
	return undef;
}

sub _sysopen_file
{
	my ($self, $fh, $fname) = @_;
	return undef if (!$fh || !$fname);
	return ( sysopen($fh, $fname, O_RDONLY|O_CREAT, 0644) ) ? 1 : 0;
}

sub _store_lock
{
	my ($self, $id, $fh, $path, $refcnt, $reference_id) = @_;
	$refcnt = 1 if (! defined $refcnt);
	
	$self->{lockdb}->{$id} = {
								'fh'	=> $fh || undef,
								'path'	=> $path || undef,
								'refcnt'=> $refcnt,
								'reference_id' => $reference_id || undef,
							 };
	EMU::debug("PATH: $path; ID: $id; set lock, called from " . (caller(1))[3]) if ($id && $path);
}

1;
