#!/usr/bin/perl
# Revision = q$Id: IMAP.pm,v 1.56 2006/07/13 11:38:39 ruslan Exp $;
# Date = q$Date: 2006/07/13 11:38:39 $;

package EMU::IMAP;

use IO::Select;

my $err = eval { use IO::Socket::SSL };
if ($err eq undef)
{
EMU::debug("IO::Socket::SSL module is not loaded. You may not use IMAPs");
}

use Unicode::IMAPUtf7;

use vars qw(@ISA);

@ISA = qw(IO::Socket::INET);

sub _port         { 993               }
sub _sock_from    { 'IO::Socket::SSL' }

my $sel = new IO::Select;
my $debug = 0;

sub new
{
    my ($class,$host,%arg) = @_;

    $sel = new IO::Select;
     
    EMU::debug("host $host port $arg{Port} timeout $arg{Timeout}");
    
    my $channel = undef;

    if ($arg{Port} == 143)
    {

    $channel = new IO::Socket::INET(PeerAddr => $host,
                                    PeerPort => $arg{Port},
                                    Proto    => 'tcp',
                                    Timeout  => 60
                                    )
        or return undef;
    }else
    {
        $channel = new IO::Socket::SSL( PeerAddr => $host,
                                        PeerPort => $arg{Port},
                                        Proto    => 'tcp',
                                        Timeout  => 60
                                       )
        or return undef;

    }
    

    return undef unless defined $channel;

  EMU::debug("errors? $@");
    $channel->autoflush(1);

    do {warn "Fatal: couldn't make socket object"; return undef;} unless $channel;

    $sel->add($channel);
    # until (scalar $sel->can_read) { }
    if (!$sel->can_read(30)) {
       &EMU::debug("Didn't hear back from '$host' after 30 seconds. Aborting.");
       return undef;
    }

    my $imap = {
	"host" => $host,
	"port" => $arg{Port},
	"token" => "aa100",
	"_errcode" => 1,  #1 == OK, 0 == NO, undef == BAD PROTO
	"channel" => $channel,
	"folder" => "INBOX",
        "response" => $channel->getline
	};

    bless $imap, $class;

    return $imap;
}

sub DESTROY
{
 #Try to cleanup after self
#    &quit;
}

sub _LOGIN { $_[0]->cmd("LOGIN", "\"$_[1]\"", "\"$_[2]\"") }

sub login
{
 # Execute the login command 
    my ($imap) = shift;
    my ($user,$pass) = @_;

    $imap->{"user"} = $user;
    $imap->{"pass"} = $pass;
    #$imap->{folder} = "";

    $imap->_LOGIN($user, $pass);
    $imap->get_response;
    $imap->interpret_response;

    return undef if (!$imap->_errcode);

    $imap->{"need_to_expunge"} = 0;
    $imap->_errcode;
}

sub uid_validity
{
 #gets the uid validity of a folder
    my ($imap) = shift;
    my ($folder) = @_;

    return $imap->{"uidvalidity"} unless ($folder);

    $folder = safe($folder);

    $imap->select( $imap->massage($folder) );

    return $imap->{uidvalidity};
}

sub create_folder
{
    my ($imap, $folder) = @_;

  EMU::debug("creating IMAP folder $folder");
    die "Usage: EMU::IMAP->create_folder(FOLDER_NAME)" unless ($folder);

    $folder = safe($folder);
    # $imap->cmd("create \"$folder\"");
    my $string = "CREATE " . $imap->massage($folder);
	$imap->cmd($string);
	    
    $imap->get_response();
    $imap->interpret_response();

    return ($imap->{'_errcode'});
}

sub delete_folder
{
    my ($imap, $folder) = @_;

  EMU::debug("deleting IMAP folder $folder");
    die "Usage: EMU::IMAP->delete_folder(FOLDER_NAME)" unless ($folder);

    $imap->select("INBOX"); # So we have access to do the delete!

    $folder = safe($folder);

    $imap->cmd("DELETE " . $imap->massage($folder));
    $imap->get_response();
    $imap->interpret_response();

    return ($imap->{'_errcode'});
}

sub _SELECT { $_[0]->cmd("SELECT", $_[1]) }
sub select
{
    #Selects a current folder
    my ($imap) = shift;
    my ($folder) = @_;

    my ($response,@lines,$line);

    $folder = $folder || "INBOX";

    $folder = safe($folder);

  	EMU::debug("(SELECT) folder is $folder");
    $imap->_SELECT( $imap->massage($folder) );
    $response = $imap->get_response();

    @lines =  map { "$_\n" } split(/\r?\n/,$response);    

    $imap->interpret_response($lines[$#lines]);

    my ($set) = 0; #Do any messages exist?

    # Return the number of messages in the folder
    foreach $line (@lines)
    {
	if ($line =~ /^\*\sOK\s\[UIDVALIDITY\s(\d+)\]/i)
	{
            if ($1 eq '0') {
               $imap->{uidvalidity} = '0E0';
            } else {
               $imap->{uidvalidity} = $1;
            }
	}
	if ($line =~ /^\* \s (\d+) \s exists/xi)
	{
	    $imap->{"exists"} = $1;
	    $set = 1;
	}
	if ($line =~ /^\* \s (\d+) \s recent/xi)
	{
	    $imap->{"recent"} = $1;
	}

    }

    EMU::debug("set $set  exists $imap->{exists}");

    $imap->{folder} = unsafe($folder);
    $imap->{read_only} = 0;

    return $set ? $imap->{'exists'} : undef;
}

#sub _EXAMINE { $_[0]->cmd("EXAMINE", "\"$_[1]\"") }
sub examine
{
    #Selects a current folder read only
    my ($imap) = shift;
    my ($folder) = @_;

    my ($response,@lines,$line);

    $folder = $folder || "INBOX";

    $folder = safe($folder);

  EMU::debug("(EXAMINE) folder is $folder");
    $imap->cmd("EXAMINE " . $imap->massage($folder));
    $response = $imap->get_response();

    @lines =  map { "$_\n" } split(/\r?\n/,$response);    

    if (@lines) {
       $imap->interpret_response($lines[$#lines]);
    } else {
       &EMU::debug("No response received from server?");
       return;
    }

    my ($set) = 0; #Do any messages exist?

    # Return the number of messages in the folder
    foreach $line (@lines)
    {
	if ($line =~ /^\*\sOK\s\[UIDVALIDITY\s(\d+)\]/i)
	{
           if ($1 eq '0') {
              $imap->{uidvalidity} = '0E0';
           } else {
              $imap->{uidvalidity} = $1;
           }
	}
	if ($line =~ /^\* \s (\d+) \s exists/xi)
	{
	    $imap->{"exists"} = $1;
	    $set = 1;
	}
	if ($line =~ /^\* \s (\d+) \s recent/xi)
	{
	    $imap->{"recent"} = $1;
	}

    }

    EMU::debug("examine set $set  exists $imap->{exists}");

    $imap->{folder} = unsafe($folder);
    $imap->{read_only} = 1;

    return $set ? $imap->{'exists'} : undef;
}

#sub _STATUS { $_[0]->cmd("STATUS", '"'.$_[1]."\" (MESSAGES UIDNEXT)") }
sub status
{
    #Gets the UID next from the status command
    # Also save the # of messages, can be used for the next msg #
    my ($imap) = shift;
    my ($folder) = @_;

    my ($response,@lines,$line);

    $folder = $folder || "INBOX";

    $folder = safe($folder);

    #$imap->_STATUS($folder);
    $imap->cmd("STATUS " . $imap->massage($folder) . " (MESSAGES UIDNEXT)");
    $imap->get_response();

    @lines =  map { "$_\n" } split(/\r?\n/,$imap->{response});    

    $imap->interpret_response($lines[$#lines]);

    my ($set) = 0;

    foreach $line (@lines)
    {
		if ($line =~ /^\*\s*STATUS\s*.*MESSAGES\s*(\d+)/i)
		{
		    $imap->{'num_msgs'} = $1;
		    $set = 1;
		}
		if ($line =~ /^\*\s*STATUS\s*.*UIDNEXT\s*(\d+)/i)
		{
		    $imap->{'uidnext'} = $1;
		    $set = 1;
		}
    }
    
    return $set ? $imap->{'uidnext'} : $imap->{'_errcode'};
}

sub popstat
{
    my ($imap) = shift;
    return ($imap->{"exists"});
}

sub interpret_response
{
 # Try to interpret a line of response
    my $self = shift; 
    my $response = $_[0] || $self->{'last'};

    EMU::debug("Interpretting: $response");

    if ($response =~ /^\S+ (\S+) (.*)$/) {
       my ($code, $msg) = ($1, $2);

       EMU::debug("code: $code ; msg: $msg");

       if (uc($code) eq 'OK') {
          EMU::debug("Got 'OK'. Setting _errcode to 1.");
          $self->{'_errcode'} = 1;
       } 
       elsif (uc($code) eq 'NO') {
          EMU::debug("Got 'NO'. Setting _errcode to 0.");
          $self->{'_errcode'} = 0;
       } 
       elsif (uc($code) =~ 'BAD') {
          # Assigning to undef here is flawed logic. What if we've just
          # never called interpret_reponse before?
          EMU::debug("Got 'BAD'. Setting _errcode to undef.");
          $self->{'_errcode'} = undef;
       } else {
          EMU::debug("Unable to interpret code '$code'!");
          $self->{'_errcode'} = undef;
          return;
       }
       
       # external (textual) error code - only place it if we got a NO or a BAD
       $self->{'errcode'} = $msg if ($self->{'_errcode'} != 1);

    } else {
       EMU::debug("Unable to locate code in response value!");
       $self->{'_errcode'} = undef;
       return;
    }

    return $self->{'_errcode'};
}

sub get_response
{
 # Read Server Response
    my ($imap) = shift;
    my ($channel) = $imap->{channel};
    my ($token) = $imap->{token};
    my ($response,$line);

    EMU::debug("Waiting up to 30 seconds to get some data from the server...");
                          
    # until (scalar $sel->can_read) { }
    if (!$sel->can_read(30)) {
       &EMU::debug("Didn't hear back from '$imap->{host}' after 30 seconds. Aborting.");
       return $imap->{response}  = "* BAD NO RESPONSE FROM SERVER!";
       
    }

    EMU::debug("Data available! Entering line by line read.");
    while ($line = $channel->getline)
    {
	#Read until "TOKEN ..."
	$response .= $line;

	if ($line =~ /^$token\s/i)
	{
            EMU::debug $line;
            chomp $line;
            $imap->{last} = $line;
	    last;
	}
    } 

    EMU::debug("Finished reading from server.");

    $imap->{"response"} = $response;

    return ($response);
}

#Execute a command
#Automatically adds the token
sub cmd
{
    my ($imap) = shift;

    my $token = $imap->token;

  EMU::debug( "\n$token " . join(" ", @_) . "\n");

    $imap->{'channel'}->print($token . " " . join(" ", @_) . "\r\n");
    EMU::debug("Done sending.");
}

sub do_msg
{
 #Send a message to the IMAP server
 # Usually used as a continuation of another command
 # ex. after a + Ready for additional text

    my ($imap) = shift;
    my ($cmd) = @_;

    my ($channel) = $imap->{channel};

    $channel->print ("$cmd\r\n");
}

sub token
{
 #set and increment the token "aaa", "aab", "aac"...

    my ($imap) = shift;
    my ($token) = ++$imap->{token};

    return $token;
}

sub errcode { $_[0]->{'errcode'} }
# OK=1, NO=0, BAD=undef
sub _errcode { $_[0]->{'_errcode'} }


sub expunge
{
    my ($imap) = shift;
    my (@lines,$line,$response);

    return unless ($imap->{"need_to_expunge"});

    EMU::debug("folder is ".$imap->{folder});
    $imap->cmd("EXPUNGE");
    $response = $imap->get_response();
    @lines =  map { "$_\n" } split(/\r?\n/,$response);    
    $imap->interpret_response($lines[$#lines]);
    foreach $line (@lines) {
        if ($line =~ /^\* \s (\d+) \s exists/xi)
        {
            $imap->{"exists"} = $1;
        }
    }

    $imap->{"need_to_expunge"} = 0;
}

sub quit
{
 # Sends server the logout command
    my ($imap) = shift;

    EMU::debug("expunge? ".$imap->{"need_to_expunge"});
    EMU::debug("folder is ".$imap->{folder});
    EMU::debug("read only? ".$imap->{read_only});

    if ($imap->{"need_to_expunge"})
    {
        if ($imap->{read_only}) {
            $imap->select($imap->{folder});
        }

	$imap->cmd("EXPUNGE");

	$imap->{"need_to_expunge"} = 0;
	$imap->get_response;
	$imap->interpret_response;
    }
    
    $imap->cmd("logout");
    $imap->get_response;
    
    $imap->{channel}->close;

    undef $imap;
}

sub list_folders
{
 # Imap specific function.
 # Returns a folder list of terminating nodes (folders, presumably)
 # starting from the argument passed to the function
 #
 # list_folders("mail") -> Array

    my ($imap) = shift;
    my ($base_folder) = @_;

    my (@folders,@dirs);

    $imap->cmd('LIST ""', $imap->massage("$base_folder*") || '""' );

    my @lines = split(/\r?\n/,$imap->get_response);
    for (my $i=0; $i<@lines; $i++) {
       
       $lines[$i] =~ /^\* LIST \(([^)]*)\) "([^"]*)" (?:{(\d+)}|"?(.*?)"?)$/ or next;
       
       my %flags = map { substr($_, 1) => 1 } split(' ', $1);
       my $delim = $2;
       my $item;
       
       if ($3) {
          $item = $lines[++$i];
       } else {
          $item = $4;
       }
       
       if ($flags{NoSelect} || $flags{HasChildren}) {
          push(@dirs, unsafe($item));
       }  else {
          push(@folders, unsafe($item));
       }
    }
    
    $imap->{folders} = \@folders;
    $imap->{dirs} = \@dirs;

    return @folders;
}

sub list_subscribed_folders
{
   my $self = shift;
   my ($base, $force) = @_;
   my @folders;

# Before enabling this, I need to go fix emumail.cgi to use 'force' in the
# right places so that we don't get stale listings, like after subscribing a
# folder.
#   if (!$force && exists $self->{cache}{subscribed_folders}{$base}) {
#      return @{$self->{cache}{subscribed_folders}{$base}};
#   }
   
   $self->cmd('LSUB ""', $self->massage("$base*") || '"*"');
   
   my @lines = split(/\r?\n/,$self->get_response);
   for (my $i=0; $i<@lines; $i++) {
   
      $lines[$i] =~ /^\* LSUB \([^)]*\) "[^"]*" (?:{(\d+)}|"?(.*?)"?)$/ or next;
      
      if ($1) {
         push (@folders, unsafe($lines[++$i]));
      } else {
         push (@folders, unsafe($2));
      }
   }
   
   $self->{cache}{subscribed_folders}{$base} = \@folders;
   
   return @folders;
}

sub subscribe_folder
{
   my $self = shift;
   my ($folder) = @_;

   $folder = safe($folder);
   #$self->cmd(qq[SUBSCRIBE "$folder"]);
   $self->cmd("SUBSCRIBE " . $self->massage($folder));

   $self->get_response();
   $self->interpret_response();
   return $self->{'_errcode'};
}

sub unsubscribe_folder
{
   my $self = shift;
   my ($folder) = @_;
   
   $folder = safe($folder);
   #$self->cmd(qq[UNSUBSCRIBE "$folder"]);
   $self->cmd("UNSUBSCRIBE " . $self->massage($folder));
   $self->get_response();
   $self->interpret_response();
   return $self->{'_errcode'};
}

sub list_folders_nodes
{
 # Imap specific function.
 # Returns a folder list of terminating nodes (folders, presumably)
 # starting from the argument passed to the function
 #
 # list_folders("mail") -> Array

    my ($imap) = shift;
    my ($base_folder,$no_kleany) = @_;

    my ($response,$line,@lines,@folders);

    unless ( ($base_folder eq "INBOX") || ($base_folder =~ /^$imap->{"prefix"}/) )
    {
        $base_folder = $imap->{"prefix"}.$base_folder;
    }

	if ($no_kleany)
	{
		$imap->cmd('LIST ""', $imap->massage($base_folder) || '""');
	}
	else
	{
    	$imap->cmd('LIST ""', $imap->massage("$base_folder*") || '""');
    }
    

    $response = $imap->get_response($imap);
    @lines =  map { "$_\n" } split(/\r?\n/,$response);

    foreach $line (@lines)
    {
     if ($line =~ /\(.*\\NoInferiors.*\)\s\"(.)\"\s\"?([^\r|\n]*)/i)
     {
         $imap->{delimit} = $1;
         my $f = $2;
         $f =~ s/(.*)\"$/$1/;
         push (@folders,unsafe($f));
     }
     elsif ($line =~ /\(.*\\NoSelect.*\)\s\".\"\s\"?([^\r|\n]*)/i)
     {
         my $f = $1;
         $f =~ s/(.*)\"$/$1/;
         push (@folders,unsafe($f));
     }
 }

    my (@ff,$ff);
    foreach $ff (@folders)
    {
        push(@ff,$ff) if ($ff ne $imap->{"prefix"});
    }

    $imap->{folders} = \@ff;

    return @ff;
}

sub check_folder_existence
{
 # Imap specific function.
 # Returns true if folder exists
 # starting from the argument passed to the function

    my ($imap) = shift;
    my ($base_folder) = @_;

    $base_folder = safe($base_folder);

    my ($err) = $imap->check_node_existence($base_folder);

    unless ($err)
    {
	# Maybe it's a directory, check:
	$err = $imap->list_folders_nodes($base_folder);
    }

    return ($err);
}

sub check_node_existence
{
 # Imap specific function.
 # Returns true if folder exists
 # starting from the argument passed to the function

    my ($imap) = shift;
    my ($base_folder) = @_;

    $base_folder = safe($base_folder);

    &cmd($imap, "STATUS " . $imap->massage($base_folder) . " (MESSAGES)");

    &get_response($imap);
    $imap->interpret_response;    

    my ($err) = $imap->{"_errcode"};

    return ($err);
}

sub list_uids
{
 # Gets all the UIDs for a given folder (or message)
 # Returns a scalar or hash, like the list() function

    my ($imap) = shift;
    my ($start,$end) = @_;

    my ($uid);

    # 2000/09/19 - Added the ability to fetch a range of Message IDs
    # backwards compatible with old single parameter fetch

    if (!($start))
    {
	# If we don't specify a range, that means we want "all" existing UIDs

	if ($imap->{"exists"})
	{
	    $imap->cmd("FETCH 1:".$imap->{"exists"}." UID");
	}
	else
	{
	    $imap->cmd("NOOP"); #Do nothing?
	}
    }
    elsif ( ( ($start) && (!($end)) ) || ($start == $end) )
    {
	# If we have a Starting, but no end, that means that we only want ONE message's UID
	# Also if we're really only selecting one message, use this way
	$imap->cmd("FETCH $start UID"); #some servers are picky and don't like 1:1, but need 1 
    }
    else
    {
	# We have specified both a Start and End message ID.  Let's use this to build a range.
	if ($imap->{"exists"})
	{
	    $imap->cmd("FETCH $start:$end UID");
	}
	else
	{
	    $imap->cmd("NOOP"); #Do nothing?
	}

    }

    my $response = $imap->get_response;

    my @lines =  map { "$_\n" } split(/\r?\n/,$response);    

    $imap->interpret_response($lines[$#lines]);

    my ($line,@uids);

    foreach $line (@lines)
    {
	if ($line =~ /^\*\s(\d+)\sFETCH\s\(UID\s(\d+)\)/i)
	{
	    push(@uids,$2);
	}
    }
    
#    return (@uids) if ( ($start) && (!$end) );
    return (\@uids);
}

sub list
{
 # Emulates the POP list function
 # Returns the size in octets of a message if called with an argument
 # or a hash of all message sizes in octets if called with no argument
    my ($imap) = shift;
    my ($start,$end) = @_;

    my ($response,$line,@lines,%msgs,$cur_size);

    # 2000/09/19 - Added the ability to fetch a range of Messages SIZES
    # backwards compatible with old single parameter fetch

    if (!($start))
    {
	# If we don't specify a range, that means we want "all" existing SIZES

	if ($imap->{"exists"})
	{
	    $imap->cmd("FETCH 1:".$imap->{"exists"}." RFC822.SIZE");
	}
	else
	{
	    $imap->cmd("NOOP"); #Do nothing?
	}
    }
    elsif ( ( ($start) && (!($end)) ) || ($start == $end) )
    {
	# If we have a Starting, but no end, that means that we only want ONE message's Size
	$imap->cmd("FETCH $start RFC822.SIZE"); #some servers are picky and don't like 1:1, but need 1 
    }
    else
    {
	# We have specified both a Start and End message ID.  Let's use this to build a range.
	if ($imap->{"exists"})
	{
	    $imap->cmd("FETCH $start:$end RFC822.SIZE");
	}
	else
	{
	    $imap->cmd("NOOP"); #Do nothing?
	}

    }
    
    $response = $imap->get_response;

    @lines =  map { "$_\n" } split(/\r?\n/,$response);    

    $imap->interpret_response($lines[$#lines]);

    # Return the number of messages in the folder
    foreach $line (@lines)
    {
	if ($line =~ /^\*\s(\d+)\sFETCH\s\(RFC822\.SIZE\s(\d+)\)/i)
	{
	    $cur_size = $msgs{$1} = $2;
	}
    }
    
    return $cur_size if ( ($start) && (!$end));
    return \%msgs;
}

sub top
{
 # This emulates part of the POP "top" function
 # It does not support the 2 parameter mode where the N
 # lines from the message body is returned with the head

    my ($imap) = shift;
    my ($msg_num,$num_lines) = @_;
    my ($amt);
    my ($response,$line,@lines,%msgs,$octets,$count,@header);

    &cmd($imap, "FETCH $msg_num BODY[HEADER]");

    $response = $imap->get_response;

    # Just added the following two lines...10/1/99 ?
    my $hr = get_octets('BODY\[HEADER\]\s\{(\d*)\}',\$response);
    return $hr;

    @lines = split(/\015?\012/, $response);

    $imap->interpret_response($lines[$#lines]);

    # Return the Header
    foreach $line (@lines)
    {
      EMU::debug $line;

	if ($line =~ /^\*\s$msg_num\sFETCH\s\(.*BODY\[HEADER\]\s\{(\d*)\}/i)
	{
	    $octets = $1;
	    next;
	}

	if ($octets) # Read into Buffer
	{
	    if ( (length($line) + $count) <= $octets)
	    {
		push(@header, $line);
	    }
	    elsif ( ($octets - $count) > 0)
	    {
		push(@header,substr($line,0,($octets-$count)));
	    }
	    else
	    {
		last;
	    }
	    $count += (length($line) + $amt);
	}
    }
    
    return \@header;
}

sub get_subject
{
    my ($imap, $msg_num) = @_;

    $imap->cmd("UID FETCH $msg_num BODY[HEADER.FIELDS (SUBJECT)]");

    my $response = $imap->get_response;
    my @lines = split(/\015?\012/, $response);

	my $subject = '';
	my $count = 0;
	my @response;

    if ( $imap->interpret_response($lines[$#lines]) )
    {
    	# Return the Header
    	my $octets = 0;
    	foreach my $line (@lines)
    	{
      		if ($line =~ /^\* \d+ FETCH \(UID $msg_num BODY\[HEADER.FIELDS \("SUBJECT"\)\] {(\d*)}/i)
			{
	    		$octets = $1;
	    		next;
			}

			if ($octets) # Read into Buffer
			{
	    		if ( (length($line) + $count) <= $octets)
	    		{
					push(@response, $line);
	    		}
	    		elsif ( ($octets - $count) > 0)
	    		{
					push(@response, substr($line, 0, $octets-$count));
	    		}
	    		else { last; }
	    		$count += length($line);
			}
    	}
    	
    	foreach my $line2 (@response)
    	{
    		$subject = $1 if ($line2 =~ /^Subject:\s+(.+)/i);
    	}
    }
    
    return $subject;
}

sub get_flags
{
    my ($imap) = shift;
    my ($uid) = @_;
    my ($line, @lines, $flags);

    $imap->cmd("UID FETCH $uid (FLAGS)");

    my $response = $imap->get_response;
    EMU::debug("response $response");

    @lines =  map { "$_\n" } split(/\r?\n/,$response);

    $imap->interpret_response($lines[$#lines]);

    foreach $line (@lines)
    {
#* 1 FETCH (FLAGS (\Seen))
        if ($line =~ /^\*\s(\d+)\sFETCH\s\(UID\s$uid\sFLAGS\s(.*)\)/i)
        {
            $flags = $2;
        }
    }

    return $flags;
}

sub get_header
{
 # This returns the header of a message
 # Takes a UID as an input

    my ($imap) = shift;
    my ($uid) = @_;

    my ($response,$line,@lines,%msgs,$octets,$count,@header,$amt);
    
    # 08/28/98: using BODY.PEEK so that the message isn't marked as READ
    # We also grab the flags at this point 
    #
    # 09/19/00: but apparently we aren't doing anything with the "FLAGS"??

    $imap->cmd("UID FETCH $uid (FLAGS BODY.PEEK[HEADER])");

    $response = $imap->get_response;
    my $body = $imap->get_octets('BODY\[HEADER\]\s\{(\d*)\}',\$response);

    return $body;
}

sub delete
{
    my ($imap) = shift;
    my ($msg_num) = @_;

    my ($response);

    $imap->cmd("STORE $msg_num:$msg_num +FLAGS (\\Deleted)");

    $imap->{"need_to_expunge"} = 1;
    EMU::debug("folder is ".$imap->{folder});
    $response = $imap->get_response;
    $imap->interpret_response;    
    return ($imap->{"_errcode"});
}

sub copy
{
    my ($imap) = shift;
    my ($msg_num,$new_folder) = @_;

    my ($response,$uid_list);
    my $start_uid = 0;
    my $uid = "";

    $new_folder = safe($new_folder);

    my ($validity) = length($imap->uid_validity());
    my $uidvalidity = $imap->uid_validity();

    if ($msg_num ne "*")
    {
	$msg_num =~ s/^$uidvalidity//;
	$start_uid = $uid = $msg_num;
  EMU::debug("$msg_num $uidvalidity");
    }
    else
    {
	$start_uid = 1;
	$uid = "*"; #Copy all msgs.
    }

    $uid_list = "$start_uid:$uid";

    $imap->cmd("UID COPY", $uid_list, $imap->massage($new_folder));
    $response = $imap->get_response;
    
    $imap->interpret_response;	
  EMU::debug("_errcode=",$imap->{'_errcode'});
    return ($imap->{"_errcode"});
}


sub set_flag
{
    my ($imap) = shift;
    my ($msg_num,$flag) = @_;
    my ($status) = "";

    my ($response);

    my ($validity) = length($imap->uid_validity());
    my ($uid) = $msg_num =~ /^.{$validity}(.*)/;
	 EMU::debug("setting flag for $msg_num to $flag");

    if ($flag == EMU::STAT_ANS) {
		  $status = "(\\Answered)";
	 }
	 elsif ($flag == EMU::STAT_READ) {
		  $status = "(\\Seen)";
    }

    if ($status) {
        $imap->cmd("UID STORE $uid:$uid +FLAGS $status");
        $response = $imap->get_response;
	 }
 $imap->interpret_response;
    return ($imap->{"_errcode"});
}

sub delete_uid
{
    my ($imap) = shift;
    my ($msg_num) = @_;

    my ($response);

#    $imap->cmd("STORE $msg_num:$msg_num +FLAGS (\\Deleted)");

    $imap->{"need_to_expunge"} = 1;
    EMU::debug("folder is ".$imap->{folder});
    EMU::debug("deleting $msg_num");
    $imap->cmd("UID STORE $msg_num +FLAGS (\\Deleted)");
    $response = $imap->get_response;
    
    return ($imap->{"_errcode"});
}

sub get
{
    my ($imap) = shift;
    my ($msg_num) = @_;

    &cmd($imap, "FETCH $msg_num RFC822");

    my $response = $imap->get_response();

  EMU::debug "Look response in get is $response";

    my $body = $imap->get_octets('^\*\s'.$msg_num.'\sFETCH\s\(.*RFC822\s\{(\d*)\}',\$response);

    return $body;
}

sub get_octets
{
    my ($imap) = shift;
    my ($regex, $response_ref) = @_;

    my ($response,$line,@lines,%msgs,$octets,$line_num,@body,$body,$amt,$count);

    @lines = split(/\012/, $$response_ref);

  EMU::debug "Got ".scalar(@lines)."  lines.";
    
    foreach $line (@lines)
    {
	if ( (!$octets) && ($line =~ /$regex/io) )
	{
	    $octets = $1;
	  EMU::debug "Oh look, I'm supposed to read $octets how quaint";
	}
	elsif ( ($octets) && ($octets > 0) )# Read into Buffer
	{
	    $octets = $octets - (length($line) + 1);
	    if ($octets < 0 )
	    {
		my $over = abs($octets);
		$line = substr($line, 0, $over);
	    }
	    push (@body, "$line\n");
	}
    }
  EMU::debug "body is ".scalar(@body);
    return \@body;
}

sub get_with_uid
{
    my ($imap) = shift;
    my ($msg_num,$peek) = @_;

	if ( $peek )
	{
		&cmd($imap, "UID FETCH $msg_num RFC822.PEEK");
	}
	else
	{
    	&cmd($imap, "UID FETCH $msg_num RFC822");
    }

    my $response = &get_response($imap);

    #* 2 FETCH (UID 20 RFC822 {762}

    my $body = $imap->get_octets(qr/^\* \d+ FETCH \(.*RFC822.* \{(\d+)\}/,\$response);

    return $body;
}

sub get_rfc822_size
{
 # This returns the header of a message
 # Takes a UID as an input

    my ($imap) = shift;
    my ($uid) = @_;

    my ($response,$line,@lines,$cur_size);

    &cmd($imap, "UID FETCH $uid RFC822.SIZE");

    $response = $imap->get_response;

    @lines =  map { "$_\n" } split(/\r?\n/,$response);

    $imap->interpret_response($lines[$#lines]);

    foreach $line (@lines)
    {
        if ($line =~ /^\*\s(\d+)\sFETCH\s\(UID\s$uid\sRFC822\.SIZE\s(\d+)\)/)
        {
            $cur_size = $2;
        }
    }

    return $cur_size;
}

sub safe
{
    my ($folder) = @_;
    return &Unicode::IMAPUtf7::imap_utf7_encode($folder);
}

sub unsafe
{
    my ($folder) = @_;
    return &Unicode::IMAPUtf7::imap_utf7_decode($folder);
}

sub massage {
	# stolen from Mail::IMAPClient
	my $self = shift;
	my $arg = shift;
	my $notFolder = shift;
	return unless $arg;
	my $escaped_arg = $arg; $escaped_arg =~ s/"/\\"/g;
	$arg = substr($arg, 1, length($arg)-2) if ( $arg =~ /^".*"$/ and !$notFolder);

	if ($arg =~ /["\\]/) {
		$arg = "{" . length($arg) . "}\x0d\x0a$arg" ;
	} elsif ($arg =~ /\s|[{}()]/) {
		$arg = qq("${arg}") unless $arg =~ /^"/;
	} 

	return $arg;
}

sub _APPEND { $_[0]->cmd("APPEND", $_[1], "(".$_[2].")", "{$_[3]}") }
sub append
{
 #Add a message to a mailbox
 # NOT POP compliant, IMAP feature
 # &append(FOLDERNAME, $message);

    my ($imap) = shift;
    my ($folder, $message, $flags) = @_;

    my $response;

    $message =~ s/(?<!\r)\n/\r\n/g;
    my $length = (length($message));

  EMU::debug "Trying to append $length to $folder with flags $flags";

    $folder = safe($folder);

    $imap->_APPEND($imap->massage($folder), $flags, $length);
    
    my ($channel) = $imap->{channel};

    $response = $channel->getline();

    if ($response =~ /^\+/) #Server is ready for us to continue
    {
	$imap->do_msg($message);
    }
    $response = $imap->get_response;
    
    return ($imap->{"_errcode"});
}

#sub _RENAME { $_[0]->cmd("RENAME", '"'.$_[1].'"', '"'.$_[2].'"') }
sub rename
{
 # Rename a mailbox
 # NOT POP compliant, IMAP feature
 # &rename(OLDFOLDERNAME, NEWFOLDERNAME);

    my ($imap) = shift;
    my ($folder, $new_folder) = @_;
    my $prefix = $imap->{"prefix"};

    unless ($folder eq "INBOX")
    {
        $folder = $prefix.$folder if ($folder !~ /^$prefix/);
        $new_folder = $prefix.$new_folder if ($new_folder !~ /^$prefix/);
    }

  EMU::debug("trying to rename $folder to $new_folder");

    my $response;

    $folder = safe($folder);
    $new_folder = safe($new_folder);

    $imap->cmd("RENAME", $imap->massage($folder), $imap->massage($new_folder));

    $response = $imap->get_response;
    return ($imap->{"_errcode"});
}

sub fetch_delimiter
{
   my $self = shift;
   my ($base) = @_;
   
   $self->cmd('LIST ""', $self->massage($base) || '""' );

   my $response = $self->get_response($self);

   if ($response =~ /^\* LIST \(\\NoSelect\) "(.*)" ""/i)
   {
      $self->{delimit} = $1;
      return $self->{delimit};
   }
   else
   {
      return;
   }
}

sub get_msg_quickview
{
    # A quick view of a message is just the flags, size, and headers, so you can basically
    # get an idea of what the message is about.  Sort of like an envelope, I guess.
    #
    # This is all wrapped up into one IMAP command to make it faster (hopefully!)
    # The tricky part is parsing the somewhat complex gob of text it sends back to us.
    #
    # I'm wondering if all this belongs in this module?
    #
    # MM - 2000/09/20

    my ($imap) = shift;
    
    my ($start,$end) = @_;

    my $head_fields = "FROM REPLY-TO SUBJECT CC TO DATE CONTENT-TYPE PRIORITY X-STATUS STATUS";
    $head_fields .= " ".join(" ", @EMU::custom_headers)
        if (scalar(@EMU::custom_headers) > 0);

    if ( ($start ne $end) && ($end) )
    {
	$imap->cmd(qq{UID FETCH $start}.qq{:$end (RFC822.SIZE FLAGS BODY.PEEK[HEADER.FIELDS ($head_fields)])});
    }
    else
    {
	$imap->cmd(qq{UID FETCH $start (RFC822.SIZE FLAGS BODY.PEEK[HEADER.FIELDS ($head_fields)])});
    }

    my $response = $imap->get_response;
    
#   EMU::debug("response $response");

    # Set status
    $imap->interpret_response;

    # Trim off the status line
    $response =~ s/\n.*$//;

    return $imap->parse_fetch(\$response);
}

sub parse_fetch
{
    # In this stream:
    #
    # * denotes that the response is untagged (meaning the command is not finished)
    #
    # We have a general syntax:
    #
    #  * $UID FETCH (VALUE)
    #
    #    The RFC says:
    #
    #  The FETCH response returns data about a message to the client.
    #  The data are pairs of data item names and their values in
    #  parentheses.  This response occurs as the result of a FETCH or
    #  STORE command, as well as by unilateral server decision (e.g. flag
    #  updates).
    #
    # This means that things can come back to us in any order, including giving us information
    # we didn't even request.  Great.
    #
    # From a draft explaining all this (http://www.cis.ohio-state.edu/htbin/rfc/rfc2683.html)
    #
    #   When a client asks for certain information in a FETCH command, the
    #   server may return the requested information in any order, not
    #   necessarily in the order that it was requested.  Further, the server
    #   may return the information in separate FETCH responses and may also
    #   return information that was not explicitly requested (to reflect to
    #   the client changes in the state of the subject message).  Some
    #     examples:
    #
    #     C: 001 FETCH 1 UID FLAGS INTERNALDATE
    #       S: * 5 FETCH (FLAGS (\Deleted)) 
    #	 S: * 1 FETCH (FLAGS (\Seen) INTERNALDATE "..." UID 345)
    #	   S: 001 OK done
    #
    #   (In this case, the responses are in a different order.  Also, the
    #   server returned a flag update for message 5, which wasn't part of the
    #   client's request.)
    #
    #  C: 002 FETCH 2 UID FLAGS INTERNALDATE
    #    S: * 2 FETCH (INTERNALDATE "...")
    #      S: * 2 FETCH (UID 399)
    #	S: * 2 FETCH (FLAGS ())
    #	  S: 002 OK done
    #
    #   (In this case, the responses are in a different order and were
    #   returned in separate responses.)
    #
    #     C: 003 FETCH 2 BODY[1]
    #       S: * 2 FETCH (FLAGS (\Seen) BODY[1] {14}
    #		   S: Hello world!
    #		   S: )
    #	 S: 003 OK done
    #
    #   (In this case, the FLAGS response was added by the server, since
    #   fetching the body part caused the server to set the \Seen flag.)
    #
    #   Because of this characteristic a client must be ready to receive any
    #   FETCH response at any time and should use that information to update
    #   its local information about the message to which the FETCH response
    #   refers.  A client must not assume that any FETCH responses will come
    #   in any particular order, or even that any will come at all.  If after
    #   receiving the tagged response for a FETCH command the client finds
    #   that it did not get all of the information requested, the client
    #   should send a NOOP command to the server to ensure that the server
    #   has an opportunity to send any pending EXPUNGE responses to the
    #   client (see [RFC-2180]).

    # Ok, so what strategy do we use?
    #
    # We'll develop a multi dimensional data structure so that accessing 
    # this information is semi-easy...
    # [sounds good, eh?]
    #
    # $response{"MESSAGE NUMBER"} = $VALUES{"SUBSECTION"}
    #
    # so: keys %response = array of message numbers
    #     keys %values   = array of response values for a message number
    #
    # cool.

    # Expect a stream of untagged responses like:
    #* 1 FETCH (UID 5089 FLAGS (\Seen) RFC822.SIZE 4394 BODY[HEADER.FIELDS ("FROM" "REPLY-TO" "SUBJECT" "CC" "TO" "DATE" "CONTENT-TYPE" "PRIORITY" "X-STATUS" "STATUS")] {232}
    #Date: Tue, 25 Jan 2000 10:32:36 -0500 (EST)
    #From: Stefan Eguizabal <stefan@emumail.com>
    #To: Matt Mankins <matt@emumail.com>
    #Subject: Re: Notes
    #Type: MULTIPART/MIXED; BOUNDARY="-1311767869-1700213930-948814356=:29025"

    my ($self) = shift;
    my ($ss_ref) = @_;

    my ($server_sais) = ${ $ss_ref };

    my (@messages) = (split(/^\* \d+ FETCH \(/im,$server_sais)); # Is this dangerous if people embed imap stuff in messages? probably

    my (%response);

    my $counter;
    foreach my $msg (@messages)
    {
	next unless $msg; #Skip null entry at start
        $msg =~ s/\)\s*$//;

	$counter++;

	my @m;
	# Were getting undef value in array ref... ?
	my  $m_ref = parse_fields($msg);
	@m = @{ $m_ref } if $m_ref;
	
	my $i;
	my %r;

	foreach my $item (@m)
	{
	  STANDARDIZE:
	    {
		$item = uc $item; # make sure the case is consistent for hash lookups?
		$item = "HEADER" if ($item =~ /\[HEADER/);
	    }
	    
	    $r{$item} = $m[$i + 1] if ($i%2 == 0);
	    $i++;
	}

	# Rearrange with the key being the UID instead of the counter
        foreach my $k (keys %r)
        {   
            $response{$r{"UID"}}{$k} = $r{$k} unless ($k eq "UID");
        }

    }

    return \%response;
}

sub parse_fields
{
  my $str = shift;
  return undef unless defined($str);
  my @list;
  my @stack = ([]);

  my $pos = 0;
  my $len = length($str);

  while ($pos < $len) {
    my $c = substr($str, $pos, 1);
    if ($c eq ' ') {
        $pos++;
    }
    elsif ($c =~ /\s/) 
    {
        # If we're encountering a non space whitepace (as in ne ' ', like a
        # tab or newline) then we've either hit the newline at the end of
        # our buffer, or we're about to hit an untagged response. Either way
        # it means we're done.
	return $stack[0];
    } 
    elsif ($c eq '(') 
    {
	push @{$stack[-1]}, [];
	push @stack, $stack[-1]->[-1];
	$pos++;
    } 
    elsif ($c eq ')') 
    {
	pop(@stack);
	$pos++;
    } 
    elsif (substr($str, $pos) =~ /^(\"(?:[^\\\"]|\\\")*\")/) 
    { # qstring
	my $str = substr($1, 1, -1);
	$pos += length $1;
	$str =~ s/\\([\\\"])/$1/g;
	push @{$stack[-1]}, $str;
    } 
    elsif (substr($str, $pos) =~ /^\{(\d+)\}/) 
    { # literal
        $pos = index($str, "\n", $pos) + 1;
	push @{$stack[-1]}, substr($str, $pos, $1);
	$pos += $1;
    } 
    elsif (substr($str, $pos)
	   =~ /^([^\x00-\x1f\x7f\(\)\{\s\"]+)/) 
    {
	my $key = $1;
	if ($key =~ /\[/) 
	{
	    my $index = index($str, ']') + 1;
	    my $s = substr($str, $pos, $index-$pos);
	    push @{$stack[-1]}, $s;
	    $pos = $index;
	} 
	else 
	{
	    if (!defined($stack[-1])) {
	       EMU::error 'PROBLEM PROBLEM: $stack[-1] is undef! This next call will fail!';
	       EMU::error "OUR DATA - key: ".ord($key)." ; STR: $str;";
	    }
	    push @{$stack[-1]}, $1;
	    $pos += length $key;
	}
    }
    else 
    {
	EMU::error ("parse_fields: eeek! bad parse at position $pos ($c) [$str]\n");
	  # Skip the char so we don't die..
	  $pos++;
    }
  }

  return ($stack[0]);
}

sub expand_to_hash
{
    my ($array_ref) = @_;

    my %parsed;

    my (@array) = @{$array_ref} if $array_ref;

    my ($done) = 0;
    my ($counter) = 0;

    while (! $done)
    {
	# Expand value if needed
	if (ref($array[$counter + 1] eq 'ARRAY'))
	{
	    $array[$counter + 1] = expand_to_hash($array[$counter + 1]);
	}
	
	if ($counter % 2 == 0)
	{
	    $parsed{$array[$counter]} = $array[$counter + 1];
	}
	
	$counter++;
	last if ($counter > $#array);
    }    

    return \%parsed;
}


sub search
{
    # Perform a search on the currently selected mailbox
    my ($imap) = shift;

    my ($criteria) = @_;
    my ($line, @lines);

    # Note: as currently written, this is for simple searches...
    # NOT the kind where you have two parameters to SEARCH and one needs to be quoted.

    $imap->cmd("UID SEARCH $criteria");

    my $response = $imap->get_response;
    EMU::debug("response $response");

    @lines =  map { "$_\n" } split(/\r?\n/,$response);

    $imap->interpret_response($lines[$#lines]);

    my (@uids);

    foreach $line (@lines)
    {
	 #* SEARCH 219 300 30303 449
	if ($line =~ s/^\*\sSEARCH\s//i)
	{
	    (@uids) = split(/\s/,$line);
	}
    }

    return \@uids;
}

sub list_since
{
    # Use disconnected mode methodology to get list of new uids

    my ($imap) = shift;
    my ($last_uid) = @_;

    $last_uid++;

  EMU::debug ("Searching for UID $last_uid and higher");

    return $imap->search("UID ".$last_uid.":*");
}

sub list_recent
{
    # Takes advantage of the IMAP \Recent flag, returning only the recent
    # UIDs

    my ($imap) = shift;

    return $imap->search("RECENT");
}

# Check to see if this object is connected and authenticated
sub isValid
{
   my $self = shift;
   
   return 0 if (!$self->{channel}->connected);
   
   # Fetch delimiter does a 'LIST "" ""' which is fast and only allowed in an authenticated state
   $self->fetch_delimiter;
   
   if ($self->interpret_response) {
      EMU::debug("returning true");
      return 1;
   } else {
      EMU::debug("returning false");
      return 0;
   }
}

sub folder_msginfo {
    # Perform a search on the currently selected mailbox
    my ($imap) = shift;
    my ($fold, $total_only, $size) = @_;
    my $total = undef;
    my $recent = undef;
    my $read = undef;
    my $answered = undef;
    my $new = undef;
    my (@lines, $line);

    $fold = safe($fold);

    # read-only select
    # $imap->cmd("EXAMINE \"$fold\"");
    $imap->cmd("EXAMINE " . $imap->massage($fold));
    my $response = $imap->get_response;

    @lines =  map { "$_\n" } split(/\r?\n/,$response);

    $imap->interpret_response($lines[$#lines]);

    foreach $line (@lines)
    {
	#* \d+ EXISTS
	if ($line =~ /^\*\s+(\d+)\sEXISTS\s/i)
	{
            $total = $1;
            last if ($total_only || defined($recent));
        }

        #* \d+ RECENT
        if ($line =~ /^\*\s+ (\d+)\sRECENT\s/i)
        {
            $recent = $1;
            last if (defined($total));
        }
    }

    $imap->{folder} = unsafe($fold);
    $imap->{read_only} = 1;

    return $total if ($total_only);
    return (0,0,0,0) if ($total == 0);

    # get values for read/answered
    $read = scalar(@{ $imap->search("SEEN") });
    $answered = scalar(@{ $imap->search("ANSWERED") });
    $new = scalar(@{ $imap->search("NEW") });
    my $unread = $total - $read;

    return ($total, $unread, $read, $answered, $size);
}

1;
