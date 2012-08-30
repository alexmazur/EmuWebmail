# EMU::POP3 object
package EMU::POP3;

use vars qw(@ISA);
use strict;
use Net::POP3;

@ISA = qw(Net::POP3);

my ($emu_cached, $emu_cacheduidl, %emu_cacheduids);

$emu_cached=0;
$emu_cacheduidl={};

sub login
{
    my $me = shift;
    my $noapop = @_ == 3 ? $_[2] : "";
    my ($ret);
    my ($host);

    EMU::debug("noapop: $noapop");
    $host = ${*$me}{'net_pop3_host'};

# login scheme.
# if the pop server supports APOP then we try to login with apop. If that initial
# apop attempt fails then we try to login normally.
    if ( $noapop ne "" && (${*$me}{'net_pop3_banner'} =~ /(<.*>)/)[0] )
    {
	# this is an apop login..
      EMU::debug("logging in with APOP @_");
	# fall back on the normal login..
	if ( ($ret = $me->SUPER::apop(@_)) eq undef )
        {
	  EMU::debug("Failed login with apop, falling back to normal login... @_");
#	      $me = ref($me)->new($host);
	    $ret = $me->SUPER::login(@_);
            unless ($ret)
	    {
		#Hmm, maybe the host dropped the connection on us!
		$me = $me->new($host); 
		$ret = $me->SUPER::login(@_);
            }
	    ${*$me}{'net_cmd_resp'}->[0] = ${*$me}{'net_cmd_resp'}->[0] || "Failed APOP and Normal authentication.";
        }
    }
    else
    { 
	# this is a normal login..
      EMU::debug("logging in normally: @_");
	$ret = $me->SUPER::login(@_);
    }
EMU::debug("login returning $ret");
return($ret);
}

sub uidl
{
 @_ == 1 || @_ == 2 or return;
 my $me = shift;
 my $uidl;

EMU::debug("Got here"); 

 $me->SUPER::_UIDL(@_) or
    return undef;           
EMU::debug("Got here2"); 

 if(@_)   
  {
#   $uidl = ($me->message =~ /\d+\s+([\041-\176]+)/)[0];
   $uidl = ($me->message =~ /\d+\s+([\S]*)$/)[0];
  }
 else
  {
   my $ref = $me->SUPER::read_until_dot
        or return undef;
   my $ln;
   $uidl = {};  
   foreach $ln (@$ref) {
#     my($msg,$uid) = $ln =~ /^\s*(\d+)\s+([\041-\176]+)/;
     my($msg,$uid) = $ln =~ /^\s*(\d+)\s+([\S]*)$/;
#EMU::debug("ERRORLINE: $ln");
     $uidl->{$msg} = $uid;
   }
  }
 return $uidl;
}

sub errcode
{
    my ($cmd, $err);
    
    $cmd = shift;
    $err = ${*$cmd}{'net_cmd_resp'}->[0];

    $err =~ s/^[-+]\w+//;

    return $err;
}

sub get_header
{
    my $cmd = shift;
    my ($uid) = @_;
    my $msg = $cmd->uid_2_msg($uid);
    return ($msg eq ""  or $msg eq undef) ? "" : $cmd->top($msg);
}

sub del_with_uid
{
    my $cmd = shift;
    my ($uid) = @_;
EMU::debug("deleting msg $uid");

    my $msg = $cmd->uid_2_msg($uid);
EMU::debug("$uid is msg $msg");
    if ($msg ne "" and $msg ne undef) {
        return ($cmd->delete($msg));
    }
}

sub del_oldstyle
{
    my $me = shift;
    my ($msg) = @_;
    my ($total, $count, $digest, $ra_header);
    
    $total = $count = ($me->popstat)[0] || scalar(keys(%{$me->list}));
EMU::debug("count $count");

    while ($count > ($total/2))
    {
	$ra_header = $me->top($count,0);
EMU::debug("header $ra_header");
	$digest    = EMU::md5_lines($ra_header);

	if ($digest eq $msg)
	{
	  EMU::debug("Removing $count...");
	    $me->delete($count);
	    last;
	}
	
	$ra_header = $me->top($total - $count + 1, 0);
EMU::debug("header $ra_header");
	$digest    = EMU::md5_lines($ra_header);

	if ($digest eq $msg)
	{
	  EMU::debug("2) Removing $count...");
	    $me->delete($total - $count + 1);
	    last;
	}
	
	$count--;
    }
    
}

sub get_rfc822_size
{
    my $cmd = shift;

    my ($uid) = @_;
    my $msg = $cmd->uid_2_msg($uid);

    return ($msg eq "" or $msg eq undef) ? 0 : $cmd->list($msg);
}

sub get_no_uid
{
    my $cmd = shift;
    my ($uid) = @_;

    my ($total, $count, $digest, $ra_header);
    
    $total = $count = ($cmd->popstat)[0] || scalar(keys(%{$cmd->list}));
EMU::debug("count $count");

    while ($count > ($total/2))
    {
	$ra_header = $cmd->top($count,0);
	$digest    = EMU::md5_lines($ra_header);
EMU::debug("uid $uid digest $digest count $count");

	if ($digest eq $uid)
	{
	  EMU::debug("downloading $count...");
            return ($cmd->get($count));
	}
	
	$ra_header = $cmd->top($total - $count + 1, 0);
	$digest    = EMU::md5_lines($ra_header);
EMU::debug("uid $uid digest $digest count $count");

	if ($digest eq $uid)
	{
	  EMU::debug("2) downloading $count...");
            return ($cmd->get($total-$count+1));
	}
	
	$count--;
    }
    
}


sub get_with_uid
{
    my $cmd = shift;
    my ($uid) = @_;
    my $msg = $cmd->uid_2_msg($uid);

    return ($msg eq "" or $msg eq undef) ? "" : $cmd->get($msg);
}

# uidl command that also caches requests
sub auidl
{
    my ($cmd) = shift;

    # if the difference is greater than 10 seconds then reget it
    if ( abs(time - $emu_cached) > 10 )
    {
	$emu_cacheduidl = $cmd->SUPER::uidl(@_);
      EMU::debug("caching... cached=$emu_cacheduidl");
    }
    else
    {
      EMU::debug("using cached=$emu_cacheduidl");
#	map { EMU::debug("$_ = " . $emu_cacheduidl->{$_}) } keys %$emu_cacheduidl;
    }

    $emu_cached = time;

    return($emu_cacheduidl);
}

sub uid_2_msg
{
    my $cmd = shift;
    my ($uid) = @_;
    my ($total, $count, $tmpuid);

#    $total = $count = ($cmd->popstat)[0] || scalar(keys(%{$cmd->list}));

    $uid = EMU::desafe($uid);

    # we have the uid but are not sure of the correct msg index...
    # mailbox may change frequently so we must search for the index
#    while ($count > ($total/2)) {
#        if (($tmpuid = $cmd->uidl($count)) eq $uid) {
#            return $count;
#        }
#EMU::debug("looking for $uid found $tmpuid count $count");

#        if (($tmpuid = $cmd->uidl($total-$count+1)) eq $uid) {
#            return ($total-$count+1);
#        }
#EMU::debug("looking for $uid found $tmpuid count ".($total-$count+1));

#        if ($tmpuid eq undef) {
#            EMU::error("uid_2_msg but no uid command!!");
#            EMU::debug("uid_2_msg but no uid command!!");
#        }
#        $count--;
#    }

    if (abs(time - $emu_cached) > 10)
    {
	$emu_cacheduidl = $cmd->uidl;
	if ($emu_cacheduidl eq undef)
	{
	  EMU::error("uid_2_msg but no uid command!!");
	  EMU::debug("uid_2_msg but no uid command!!");
	    return;
	}
	else
	{
	    %{$emu_cacheduidl} = reverse(%{$emu_cacheduidl});
	}
      EMU::debug("caching...");
    }
    else
    {
      EMU::debug("using cached...");
    }

    # update timestamp
    $emu_cached = time;

    if (ref($emu_cacheduidl) ne "HASH")
    {
      EMU::error("uid_2_msg but the emu_cacheduidl is not a hash!!");
      EMU::debug("uid_2_msg but the emu_cacheduidl is not a hash!!");
	return;
    }

    return $emu_cacheduidl->{$uid};
}

# Check to see if this object is connected and authenticated
sub isValid
{
   return shift->_NOOP;
}
1;
