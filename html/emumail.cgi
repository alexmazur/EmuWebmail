#!/usr/bin/perl

package EMU;
require 5.005;

$EMU::Revision = q$Id:$;
$EMU::Date = q$Date: 2006/09/19 11:59:31 $;

$EMU::Language = "english";
$EMU::DB_Version = "4.00";

$EMU::Version = '8.1';
use subs qw(look move);

$| = 1;

use subs qw(debug error);

sub bool ($) { $_[0] ? 1 : 0 }
sub digit ($) { return $_[0] =~ /(\d+)/ ? $1 : 0; }
sub positive ($) { $_[0] < 0 ? 0 : $_[0] }

#
# GLOBALS

use vars qw($EMU_URL $SYSFILEDIR $TOP_IMAGE $SYSXTRADIR $EMU_DEBUG $exit_requested
    @smtp_host $smtp_port $umask $url $page_root $no_waitscreen 
    $NPH_Line $fcgi_counter %dictionary %checksum $waiting_printed $pop_port
    $html_data $html_boundary $db_opened $delay $site_emu_time $lang_emu_time
    %loaded $wrap_columns $trash_bin $trash_folder);

use vars qw($pop $query %connections);               # objects
use vars qw(%v $user_name $host $password $qs $passed $folder $date $this_host
	$homedir $popuser $pophost %poplist $db_package $initial_login
	$db_version $last_http_host $multi_interfaces $pop_connected %hostnames
        %checked_existence $firstlogin $mailloc %licensed %nouidl_list);

use vars qw($status $total_messages $tm $session_file %changed $extra_status);
use vars qw($numb $hash);
use vars qw($POWERED @HEADER_ORDER $INTERNAL_EMU $prefix );
use vars qw(@custom_headers @custom_headers_column @custom_headers_action );

use vars qw($protocol);         # 07/22/98: need this in order to create right object

use vars qw($voice_enabled);    # 11/22/99: $user && $site = $voice_enabled.

# Flags
use vars qw($header_printed);

# Static variables qw(those that don't change between FCGI loops)
use vars qw($FONT $FONT_FULL $FONT_BIG $FONT_BIG2 $FONT_IND $FONT_IND2);
use vars qw($FONT_ERROR $FONT_GRFX $FONT_BASE $FONT_GRFX2 $FONT_GRFX3);
use vars qw($FONT_SML $FONT_SML2 $FONT_BOD $FONT_IHELP $FONT_MONO $FONT_COLOR);
use vars qw($AD_VERT $AD_VERT_STR $AD_VERT_HEIGHT $AD_VERT_WIDTH $img_printed);
use vars qw($over_quota %ihelp $emu_type %dispatch %emu_cookies);

# 05/28/98: need this so that we can output cookies line after content-type
use vars qw($extra_head);
use vars qw(%userdb %folderdb %foldmap $inbox $tiehandle);

# HM 06/27/00
# This is better!
use vars qw/$mailbox %msg %c %iface_c %homedir_c %dcache/;

my %dcache;

#CHECKSUMS#
# We have the ability to have multiple iface signatures. Simply put them
# separated by a space...

#=====================================================================

$checksum{"address.html"} = "cd078c1473f3858048dfdbb41c035f52";
$checksum{"address_import_export.html"} = "38af3aa2c699b6d5363a6cc22254a35c";
$checksum{"address_popup.html"} = "b262028fce886526061581af5a707189";
$checksum{"admin_file_editor.html"} = "3be6813c1641c27dafcde2cc56863ed4";
$checksum{"attachment_popup.html"} = "e5c4be13da2d4ea4494ee4f711a033fe";
$checksum{"close_window.html"} = "15256e4ea79f17ca76cb779b23d0ab6d";
$checksum{"compose.html"} = "a5794a2d8d5eaa745f411bcad181128d";
$checksum{"contact_editor.html"} = "e8d434efefea9f137b054162e2c5d689";
$checksum{"directory.html"} = "aad2e93925f426a76c9164e0c8d9faa5";
$checksum{"errors.html"} = "f2e29d570fd566fe8849e585e2c4ae83";
$checksum{"filters.html"} = "c6f28ec203b0d35d0797c5c7527fd96a";
$checksum{"folder.html"} = "e5412f55776d043ac23e1f360869c087";
$checksum{"folder_subscriptions_popup.html"} = "18885ec728ff5ebfa366be33b83dbc31";
$checksum{"footer.html"} = "ed8db272b158c27e7e88371e55e69e69";
$checksum{"groups.html"} = "e417c5cc22ff55e791961a8a62bf5e82";
$checksum{"groups_editor.html"} = "30bc2aa2dccb3ea2b419e4674fb097e2";
$checksum{"header.html"} = "a902c27cdc1f1501fe05c55aad30da54";
$checksum{"iframe_update_message.html"} = "3edbda8e3a734a4b1de33e9c2d7abc0a";
$checksum{"login.html"} = "cbd75cea63c362c438498449b8e80680";
$checksum{"logout.html"} = "8ccce5a5bb6cb2f5c5495935087fe59a";
$checksum{"lookup.html"} = "6ef564ed77b326382f019ed7f5c0fee8";
$checksum{"mailboxes.html"} = "09ab54e1d10fd28745f0073af2f9f14e";
$checksum{"menu.html"} = "10830948419a3489e57eeec38f0e8ef1";
$checksum{"msgindex.html"} = "84380471d004ab1c83f5b30ef38aaf91";
$checksum{"msgview.html"} = "692a596f90b4d7fde5328ddc774406f4";
$checksum{"options.html"} = "f0db8c1abd1776c99f8ed66bba828443";
$checksum{"options_list.html"} = "1c71e1f32989713fc4dccfca2a9ef39d";
$checksum{"questionaire.html"} = "edb4ba24bad480675c15c300929b2377";
$checksum{"search.html"} = "36f47164c621432958cae50fd46262db";
$checksum{"spelling.html"} = "40c54dca26881e611909b02899cd4e38";
$checksum{"toolbar.html"} = "a0a6db49790fa2b91e0dc97f17a3e601";
$checksum{"waitwindow.html"} = "a84ef2a18090d06341148e66910a5af8";
$checksum{"wordview.html"} = "83a25276bcd169b95ac344cf2e698d2b";


$checksum{"License.pm"} = "a302e64349998a3f4867c0facdee9362";

#=====================================================================
#CHECKSUMS#

# constants, bitflags
sub FILTER_OFF  { 0x00 }        # 0000 0000  (0)
sub FILTER_TO   { 0x01 }        # 0000 0001  (1)
sub FILTER_FROM { 0x02 }        # 0000 0010  (2)
sub FILTER_SUBJ { 0x04 }        # 0000 0100  (4)
sub FILTER_HEAD { 0x07 }        # 0000 0111  (7)
sub FILTER_BODY { 0x08 }        # 0000 1000  (8)
sub FILTER_ANY  { 0x0F }        # 0000 1111  (15)
sub FILTER_DELETE { 0x10 }      # 0001 0000  (16)

sub FILTER_CONTAINS { 0x01 }
sub FILTER_DEVOID   { 0x00 }

sub STAT_NEW  { 0 }
sub STAT_READ { 1 }
sub STAT_ANS  { 2 }

sub VERSION_PROFESSIONAL { 0 }   # no restrictions

sub VERSION_ADVERT       { 1 }   # no expiry, no iface changes, ads

sub VERSION_DEMO         { 2 }   # no expiry, yes on iface changes, ads

# other version definitions... (mostly added for Intel)
sub VERSION_DEFAULT      { 3 }   # yes on iface changes, no ads, 
                                 # requires an expiry

sub VERSION_STANDARD     { -2 }  # no expiry, no iface changes, no ads

sub VERSION_ERROR        { -1 }  # indicates an error...


#    use vars QUIET;
    #Handle STDERR...

use CGI::Carp qw(carpout fatalsToBrowser);

# Modules We Use
# ==============
use strict;
use IO::ScalarArray;
use Fcntl;
use File::Copy;
use File::stat;
use Net::DNS;

use Time::Zone;
use MIME::Parser;
use MIME::Head;
use MIME::Body;
use MIME::Entity;
use MIME::QuotedPrint;

use Date::Parse;

use Data::Dumper;
local $Data::Dumper::Terse = 1;
local $Data::Dumper::Indent = 0;

use Mail::Address;
use Digest::MD5;
use Net::SMTP_auth;

# use ../data/lib as lib location
use FindBin qw($Bin);
use lib "$Bin/../data/lib";

use EMU::Config;
use EMU::POP3;
use EMU::IMAP;

use EMU::Locks;
my $ELocks;
use EMU::Time::Zones qw/English/;

sub read_ini
{
	local($/) = 1;

    open(INI, "init.emu") || FatalError("Bad","FATAL: Unable to open init.emu: $!\n");

    # grab the first valid entry
    <INI> =~ /page_root\s*=\s*(\S+)/m;
    close(INI);
    return($1);
}

# Load the init file, this will tell use where our page root
# is, which we use to load the rest of the files
$page_root = "$Bin/../data";
push (@INC, "$page_root/lib");

# now load our configurer
#    require EMU::Config;

sub map_emu_conf
{
	my ($file, $rh) = @_;
	my ($ob);

	$ob = new EMU::Config $file;
	return 0 if (!$ob);

	# read in the data
	return 0 if (!$ob->readConfig);

	%$rh = %{ $ob->getConfig }; # $rh = $ob->getConfig;

	return 1;
}

# Load the language file. 
# If we can't find it then we have to exit. VERY SERIOUS.
if (! map_emu_conf("$Bin/../data/lang.emu", \%msg))
{
	print "Fatal: Could not load $Bin/../data/lang.emu!";
    die;
}

# Load the main config file. Exit it we can't find it. VERY SERIOUS.
# MM: 11/28/98: Added concept of site config file, 
# and then interface config files
#   Precedence goes:  User Config File->Interface Config->Site Config
if (! map_emu_conf("$Bin/../data/site.emu", \%c))
{
	die "Fatal: Could not load $Bin/../data/site.emu!";
}

require "EMU/AddressbookDefs.pl";

# Now reassign stderr... typically reassign to the null device so
# we quiet the errors. Can optionally set the file in site.emu.
# Currently only configurable for unix.
#
# Note: This allows us to type:
#
# ./emumail.cgi test ''
#
# to get any error messages on stdout

my $quiet = 0;
if (!(bool($c{"Disable_QUIET"}))) {
	my $nuldev = ($^O =~ /^MSWin/i) ? "NUL" : "/dev/null";
    my $quietfile = $c{"QUIET_Fdev"} || $nuldev;
    
    # dont die if unable to open QUIET device... simply dont redirect!
    # RB: O_APPEND, not O_CREAT
    $quiet = 1 if (open QUIET, ">> $quietfile");
    
    carpout(\*QUIET) if ($quiet && $ARGV[0] ne "test");
}

use Sys::Hostname;
$this_host = hostname if ($c{"debug_hostname"});

if (!$c{"disable_fcgi_signals"}){
debug "Perl version is : $]";
	$SIG{'INT'}   = sub { &EMU::handle_signal("SIGINT"); };
	$SIG{'QUIT'}  = sub { &EMU::handle_signal("SIGQUIT"); };
	$SIG{'TERM'}  = sub { $exit_requested = 1 } if $] < 5.008; #08.14 Alex "fix for non standard exit"
	$SIG{'HUP'}   = sub { &EMU::handle_signal("SIGHUP"); };
	$SIG{'STOP'}  = sub { &EMU::handle_signal("SIGSTOP"); };
	$SIG{'ABRT'}  = sub { &EMU::handle_signal("SIGABRT"); };
	$SIG{'KILL'}  = sub { &EMU::handle_signal("SIGKILL"); };
	$SIG{'SEGV'}  = sub { &EMU::handle_signal("SIGSEGV"); };
	$SIG{'USR1'}  = sub { &EMU::handle_signal("SIGUSR1"); };
	$SIG{'PIPE'}  = sub { &EMU::handle_signal("SIGPIPE"); };
}

END
{
    $ELocks->locks_clean if $ELocks;
    unless ( $c{"use_modperl"} )
    {
		# Restore STDERR if needed
        close(STDERR);
	}
}

load:
{
	my $cgi_pkg;
	# Load up some modules now
    load_module("Benchmark") if ( $c{'emu_debug'} );
    load_module( ($c{'use_fastcgi'}) ? "CGI::Fast" : "CGI" );
    load_module("IO::Socket::SSL");
}

# init_variables(); # we never use modperl and variables are init'ed in run_emu
run_emu(); # unless ($c{'use_modperl'});

# 4/13/98 - Jah
# This run_emu function is here to allow the encrypted emumail.cgi
# to run under mod_perl without the need for recompiling the httpd
# or anything.  What the user needs to do is move emumail.cgi to
# EMU.pm and then create an emumail.cgi which is a wrapper that
# use's EMU.pm and then calls EMU->run_emu();
sub run_emu
{
    $EMU_DEBUG = bool($c{"emu_debug"});

	debug "starting up...";
    # Initialize - must be done inside here
    init_variables();
    reset_variables();

	my $lock_type = 'flock';
	$lock_type = 'file' if ( $c{'locks_on_nfs'} );
	debug "Lock type is $lock_type";
    $ELocks = EMU::Locks->new
    			(
    				type		=> $lock_type,
    				timeout		=> $c{"session_lock_timeout"} || 15,
    				waitingsub	=> sub {
						        $EMU::v{"wait_action"} = $EMU::msg{"WAIT_DBLock"};
						        EMU::print_progress_new(1);
    							},
    				initsub		=> sub {
								$EMU::v{"wait_interval"} = 3;
    							$EMU::v{"wait_count"} = 0;
    							},
    			);
    carp "can't load lock object: $!" unless $ELocks;


	if ($c{'use_fastcgi'})
	{
#       use autouse 'FCGI';
#       debug "FCGI VERSION: $FCGI::VERSION";
		$fcgi_counter = $c{'fcgi_counter'};

	    while ($query = new CGI::Fast)
	    {
			main();
			finish_waitscreen();
			reset_variables();

			debug "fcgi_counter: $fcgi_counter";
			if ($fcgi_counter ne undef) { $fcgi_counter--; }

#           FCGI::flush();
#           FCGI::finish();

            last unless ($fcgi_counter > 0 || $fcgi_counter eq undef || $exit_requested); #08.14 Alex "fix for non standard exit" 
	    }

		debug "Exiting...";
        # Check if special (custom) processing is necessary
        &EMU::Custom::quit() if ($EMU::Custom::call_on_quit == 1);
        $ELocks->locks_clean if $ELocks;
        exit(0);

	} else {
	    $query = new CGI;
	    main();
        finish_waitscreen();
	}

    # Check if special (custom) processing is necessary
    &EMU::Custom::quit() if ($EMU::Custom::call_on_quit == 1);
	$ELocks->locks_clean if $ELocks;
}

# one time initialization of EMUmail
sub init_variables()
{
    return if ($c{'__config_loaded'});

    #Don't load variables more than once
    $c{'__config_loaded'} = 1;

    $c{'__os_type'} = $^O =~ /^MSWin/ ? "NT" : "UNIX";
#    $c{'__version'} = $EMU::Version;

    # folder namelength has to be at least 1
    $c{'folder_namelen'} = $c{'folder_namelen'} < 1 ? 18 : $c{'folder_namelen'};
    
    $EMU_URL = $url = $c{'emu_url'};
    $SYSFILEDIR = $c{'sysfile_dir'};
    $SYSXTRADIR = $c{'sysfile_dir2'};
    $EMU_DEBUG  = bool($c{'emu_debug'});
#    $smtp_host  = $c{'smtp_host'};
    # smtp_host is a list so we can have fallback servers
    (@smtp_host) = split(/\s|\,/,$c{"smtp_host"});
    $smtp_port = $c{"smtp_port"} || "25";
    $pop_port = $c{"pop_port"} || "110";
    
    %loaded = undef;

    # process any custom header information
    if ($licensed{"custom_headers"}) {
        (@custom_headers)        = split(/\s|\,/,$c{"Customized_Headers"});
        (@custom_headers_column) = split(/\s|\,/,$c{"Customized_Headers_Column"});
        (@custom_headers_action) = split(/\|\|/,$c{"Customized_Headers_Action"});
        debug "custom_headers: @custom_headers";
    }

    # 08/20/98: the interface to use 
    $emu_type   = $c{'default_interface'} || "normal"; ## Default Iface changed to "normal" 11/28/98 MM

    $AD_VERT_HEIGHT    = 60;
    $AD_VERT_WIDTH     = 468;

    check_installation();

  DISTRIBUTION_CONFIG:
    {
	#  0 = PROF: Can change HTML no ads
	#  1 = ADVT: Can't change HTML, ads
	#  2 = DEMO: Can change HTML w/ads
	
    my $private;
	my ($AD_VERT,$private);
	#      = &EMU::License::check_key();
    #check_license_module($private);
	debug "advtype: $AD_VERT";
#        return if ($AD_VERT == -1);

	$INTERNAL_EMU = 0;
	$EMU::dist    = "RELEASE_EXTERNAL -- $AD_VERT";

	if ( ($EMU_URL =~ /^\s*https:\/\//) && ($AD_VERT))
	{
	    print_header($msg{'nohttps_title'});
	    print $msg{'nohttps_body'};
	    exit;
	}
    }
    
    # this is the header order for postponing messages
    @HEADER_ORDER = ("subject", "from", "sender", "selected_file", "replyto",
		     "organization","priority","attached","to","cc","bcc");

    $url = $c{'emu_url'};

    # Style definitions

    $POWERED = qq!$FONT_IND2<A HREF="http://EmuMail.com" target="_blank">[Powered by EMUmail &\#169;</A> <A HREF="http://EMUmail.com" target="_blank"> 1997-99 EMUmail, Inc.]</A></FONT>\n!; 

    $EMU::revision = $EMU::revision;            # be quiet perl!

    $umask    ||= 006;

    if (scalar(keys(%ihelp)) == 0)
    {
	%ihelp = (
		  "to"           => $msg{'MSG_Ihelp_To'},
		  "subject"      => $msg{'MSG_Ihelp_Subject'},
		  "from"         => $msg{'MSG_Ihelp_From'},
		  "replyto"      => $msg{'MSG_Ihelp_Replyto'},
		  "sender"       => $msg{'MSG_Ihelp_Sender'},
		  "organization" => $msg{'MSG_Ihelp_Organization'},
		  "cc"           => $msg{'MSG_Ihelp_Cc'},
		  "bcc"          => $msg{'MSG_Ihelp_Bcc'},
		  "priority"     => $msg{'MSG_Ihelp_Priority'},
		  "attach"       => $msg{'MSG_Ihelp_Attach'},
		  "EMUfiles"     => $msg{'MSG_Ihelp_Emufiles'},
		  );
    }

    # NT (and alike) specific configuration
    if ($c{'__os_type'} eq "NT")
    {
	binmode STDOUT;
	binmode STDIN;
    }
}


# 07/22/98: convert
# used in unison with the Config reader
sub convert
{
    my ($text, @arr) = @_;
    $text =~ s/%(\d+)/$arr[$1 - 1]/g;
    return $text;
}

# per loop initialization (for FCGI / mod_perl)
sub reset_variables
{
    umask($umask); 
    
    # reset all variables
    $pop             = undef;
    $firstlogin      = 0;
    $mailloc         = 0;
    $query           = undef;
    %changed         = ();
    %v               = ();
    %emu_cookies     = ();
    delete $v{"SESSION_OPEN"};
    delete $v{"SESSION_HOME"};
    $initial_login   = 0;
    %userdb          = undef;
    $tiehandle       = undef;
    $user_name       = undef;
    $popuser         = undef;
    $pophost         = undef;
    $db_version      = undef;
    %poplist         = ();
    $pop_connected   = 0;
    %checked_existence = ();
    $waiting_printed = 0;
    $db_opened       = 0;
    $html_boundary   = "Emumail-3.1";
    $html_data       = "";
    $host            = undef;
    $password        = undef;
    $qs              = undef;
    $passed          = undef;
    $folder          = undef;
    $date            = undef;
    $homedir         = undef;
    $multi_interfaces= undef;
    $status          = undef;
    $extra_status    = undef;
    $tm              = undef;
    $numb            = undef;
    $hash            = undef;
    $total_messages  = undef;
    $session_file    = undef;
    $img_printed     = undef;
    $over_quota      = undef;
    $extra_head      = undef;
    $TOP_IMAGE       = undef;
    $AD_VERT_STR     = undef;
    $NPH_Line = undef;
    $header_printed  = 0;
    $delay           = 0;

    @custom_headers = ();
    undef %connections;
    %nouidl_list = undef;
    %hostnames   = undef;

    $wrap_columns = $c{"default_wrap_columns"} || 74;

    $inbox = $c{'default_inbox_name'} || "INBOX";

    # disable the waitscreen if either the conf file says so or if the browser is an IE browser
    $no_waitscreen  = 1 if (bool($c{'disable_waitscreen'}));
#    debug "no_waitscreen: $no_waitscreen";

#    debug "JSCRIPTFLAG is $jscriptflag";

    $EMU::{'cleanupvars'}  = [];

    #Load site-wide Lang,site.emu if we've changed. 11/28/98 : MM
#    &load_conf("default") if ($c{"__CHANGED"});
#    &load_lang("default") if ($msg{"__CHANGED"});
}


sub get_top_image
{
    my ($ad_server,$AD_VERT_STR) = @_;

    # Let the "demo" version override... #3-1-00
    if ( ($AD_VERT == VERSION_DEMO()) && ($c{"adcode"}) )
    {
#        debug "setting top image... ".$c{"adcode"};
        $TOP_IMAGE = $c{"adcode"};
        return $c{'adcode'};
    }

    my (%emudb);

    # we had a weird error where an outsourcer had a $page_root/homes but
    # it was actually a file, not a dir! Guess need to take care of that
    unlink "$page_root/homes" if (-f "$page_root/homes");

    mkdir("$page_root/homes", 00700) if (!-e "$page_root/homes");

    dbmopen(%emudb, "$page_root/homes/emudb", 0666);
    my ($update_time) = $emudb{"update"} || (60*60*12);

    if ( (time - $emudb{"last_update"}) > $update_time ) # check for update every 12 hours
    {
	load_module("LWP::Simple");
	$emudb{"top_image"} = LWP::Simple::get ("http://ad.vert.net/adcode.cgi?".$c{"default_pop"});
    }

    $TOP_IMAGE = $emudb{"top_image"};
    $TOP_IMAGE =~ s/\#ad_server\#/$ad_server/g;
    $TOP_IMAGE =~ s/\#ad_vert_str\#/$AD_VERT_STR/g;

    $emudb{"last_update"} = time;

    dbmclose(%emudb);

    return $TOP_IMAGE;
}

# 11/28/98: MM Load Language Files -> %msg
sub load_lang
{
    my $type = shift;

    $type = $type || "default";
    
    debug "Lang: $type $emu_type";
    
    if ($type eq "default" && -e "$page_root/lang.emu")
    {
	undef %msg;
	return map_config("$page_root/lang.emu",\%msg);
	debug "Loaded $page_root/lang.emu";
    }
    elsif ($type eq "iface")
    {
	if (-e "$page_root/iface/$emu_type/lang.emu")
	{
	    $msg{"__CHANGED"} = 1;
	    return map_config("$page_root/iface/$emu_type/lang.emu",\%msg);
	}
    }
    elsif ($type eq "home")
    {
	if ($c{"allow_user_lang"})
	{
	    if (-e "$homedir/lang.emu")
	    {
		$msg{"__CHANGED"} = 1;
		return map_config("$homedir/lang.emu",\%msg);
	    }
	}
    }
    else
    {
	#Shouldn't get here...
	return map_config("$page_root/lang.emu",\%msg) if (-e "$page_root/lang.emu");
    }

    return 0;
}

# 11/28/98: MM Load Conf Files -> %c
sub load_conf
{
    my $type = shift;

    $type = $type || "default";

    debug "type is $type ; emu_type: $emu_type";

    if ($type eq "default")
    {
        # site.emu is the main config. Its presence forces deletion of all
        # current config variables!
        if (-e "$page_root/site.emu") {
            # Have to save __ vars... !  MM 990708
            map     
            {
	        delete $c{$_} if ($_ !~ /^__/);
            } keys (%c);
            map_config("$page_root/site.emu",\%c);
        }

        # Ok, to provide more flexible support to outsourcing, we've added two 
        # new "default" config files. That allows for us to not have a site.emu
        # at all in the $page_root and still give some flexibility in 
        # configuration. So now besides having "site.emu" as the site-wide
        # config file, we have also "virtual.conf" and a possible default
        # "conf.emu". The virtual.conf is intended to provide "private"
        # configuration for virtual webmail, where we have control over
        # those vars and the outsourcer doesn't (via file permissions).
        # The default conf.emu then has vars which can be configured
        # by the outsourcers. Both of these combined serve to provide a subset
        # of configuration for the outsourcer environment, without having
        # to reiterate the site.emu completely for all outsourcers. Note
        # that both of these simply override settings from site.emu, if
        # one exists, unlike site.emu which forces deletion of $c variables.
        if (-e "$page_root/virtual.conf")
        {
            debug "loading $page_root/virtual.conf";

            my %virtual_c;
	    map_config("$page_root/virtual.conf",\%virtual_c);

            # now map the iface conf.emu data into %c
            foreach my $hkey (keys %virtual_c) {
                $c{$hkey} = $virtual_c{$hkey};
            }
        }

        if (-e "$page_root/conf.emu")
        {
            debug "loading $page_root/conf.emu";

            my %conf_c;
	    map_config("$page_root/conf.emu",\%conf_c);

            # now map the iface conf.emu data into %c
            foreach my $hkey (keys %conf_c) {
                $c{$hkey} = $conf_c{$hkey};
            }
        }
    }
    elsif ($type eq "iface")
    {
	if (-e "$page_root/iface/$emu_type/conf.emu")
	{
            debug "loading $page_root/iface/$emu_type/conf.emu";
	    $c{"__CHANGED"} = 1;

            # before mapping new config variables, let's delete any existing 
            # configuration pertaining to %iface_c
            debug "deleting ".scalar(keys %iface_c)." from iface_c";
            foreach my $ikey (keys %iface_c) {
                delete($c{$ikey});
                delete($iface_c{$ikey});
            }

#	    return map_config("$page_root/iface/$emu_type/conf.emu",\%c);
	    map_config("$page_root/iface/$emu_type/conf.emu",\%iface_c);

            # now map the iface conf.emu data into %c
            foreach my $ikey (keys %iface_c) {
                $c{$ikey} = $iface_c{$ikey};
            }

            $inbox = $c{'default_inbox_name'} if ($c{'default_inbox_name'});
debug "custom state ".$c{"custom_state"};
	}
    }
    elsif ($type eq "home")
    {
        debug "allow_user_config ".$c{"allow_user_config"};
	if ($c{"allow_user_config"})
	{
	    if (-e "$homedir/conf.emu")
	    {
		$c{"__CHANGED"} = 1;
                debug "loading $homedir/conf.emu";

                debug "deleting ".scalar(keys %homedir_c)." from homedir_c";
                # before mapping new config variables, let's delete any 
                # existing configuration pertaining to %iface_c
                foreach my $hkey (keys %homedir_c) {
                    delete($c{$hkey});
                    delete($homedir_c{$hkey});
                }

		map_config("$homedir/conf.emu",\%homedir_c);

                # now map the iface conf.emu data into %c
                foreach my $hkey (keys %homedir_c) {
                    $c{$hkey} = $homedir_c{$hkey};
                }
	    }

	}
    }
    else
    {
	#Shouldn't get here...
	return map_config("$page_root/site.emu",\%c) if (-e "$page_root/site.emu");
    }

    return 0;
}


sub map_mailserver {
    my ($user, $host, $fold, $force) = @_;
    my $dont_change = 0;

    $fold = $folder if (!$fold);
#    debug "mapping $user, $host, folder $fold";
#    debug "userdb: ".$userdb{"folder:$fold:username"}.",".$userdb{"folder:$fold:hostname"};

    return ($user, $host) if ($user eq "" && $host eq "" || bool($c{"dont_map_mailserver"}));

    $v{"server_mapped"} = 1;

    return ($userdb{"folder:$fold:username"},
            $userdb{"folder:$fold:hostname"})
        if (!$force && 
            $userdb{"folder:$fold:username"} &&
            $userdb{"folder:$fold:hostname"});

    my ($u, $h) = split(/@/, $user) if ($user =~ /@/);

    if ($h && $c{'keepdomains'} ne 'ALL' && $c{'keepdomains'} !~ /\s+$h\s+/i) {
        $user = $u;
        $host = $h;
    }

    $host = $host || $c{'default_pop'};

    # Allow for double @'s
    if ($user =~ /.+@.+@.+/) {
        $user =~ s/^(.+@.+)@(.+)/$1:$2/; 
        ($user,$host) = split(/:/, $user);
    }

#    debug "host here is $host";
    # if host has multiple hosts, only pick up the first one...
    $host = (split(/@/, $host))[0] if ($host =~ /@.+@/);
    $host = lc($host);

#    debug "host is now $host";
    my $tmpmap;

    if ($c{"map2pop_ALL"}) {
        $tmpmap = "map2pop_ALL";
    }
    else {
        $tmpmap = "map2pop_$host";
    }
#    debug "tmpmap is $tmpmap";

    if ( $c{'add_domain_to_user'})
        {
	        my @hostnms = split /\s|\,/, $c{'add_domain_to_user'};
		map { $user = "$user\@".lc($_) if lc($_) eq $host} @hostnms;
		debug "HOSTNAMES: @hostnms HOST: $host USERNAME: $user";
				    
		$dont_change = 1;
	}

#    if ( $c{'add_domain_to_user'} ne "") {
#        $user = "$user\@$c{'add_domain_to_user'}";
#        $dont_change = 1;
#    }
    if ($c{$tmpmap} ne undef || $c{'keepdomains'} eq 'ALL' || $c{'keepdomains'} =~ /\s+$host\s+/i ) {
        $user = "$user\@$host" if (bool($c{"appendhost_$host"}) || 
                                   bool($c{"appendhost_ALL"}));
        $host = $c{$tmpmap} || $c{'default_pop'};
        $dont_change = 1;
    }

    # reassign $user_name based on mapping
    if (!$dont_change) {
        $user_name = "$user\@$host";
    }
    else {
        $user_name = $user;
    }

    debug "mapped ($_[0], $_[1]) to ($user, $host)";
    return ($user, $host);
}


sub check_conf_updates {
    # Check if any of the conf files have changed.

    my ($site_st, $lang_st);

    $site_st = stat("$page_root/site.emu");
    $lang_st = stat("$page_root/lang.emu");

    return 0 if (!$site_st || !$lang_st);

    if ($site_st->mtime > $site_emu_time) {
        debug "default site.emu has changed... let's reload";
        $site_emu_time = $site_st->mtime;
        return 1;
    }
    if ($lang_st->mtime > $lang_emu_time) {
        debug "default lang.emu has changed... let's reload";
        $lang_emu_time = $lang_st->mtime;
        return 1;
    }
}


sub main
{
    my $tmpstat;                # hack
    my $hostname;
    my ($user, $host);

    $delay = time;
    $v{"delay_max"} = $c{'waitscreen_timeout'} || 10;

    if ($query->param("passed") eq "checkstatus") {
        print "Content-type: text/html\n\nemumail.cgi::OK";
        return ;
    }

    if ($query->param("passed") eq "version") {
        version();
        return ;
    }

    my $http_host = lc $ENV{'HTTP_HOST'};
    $http_host = substr($http_host, 0, index($http_host, ':')) 
        if ($http_host =~ /:/);
    my $conf_changed = 0;

    debug "requested $http_host";
    debug "$http_host.init exists" if (-e "$http_host.init");
    debug "https requested? ".$query->param("https");

    # Check if need to reload conf... rules:
    # 1. If there's an init file for $http_host and the current $http_host
    #    is different than last host, we have a new config to load
    # 2. If there is no init file for $http_host and current $http_host
    #    is different, then we must go back to "default"
    # 3. Otherwise any other case we leave it alone.

#    if ( -e "$http_host.init" && ($http_host ne lc $last_http_host) ) {
    # let's always reload the page_root and init file. We got into config
    # trouble many times...
    if ( -e "$http_host.init" ) {
        # accessing a new domain and we have an init file for it... 
        # reassign $page_root. 

        open(INI, "$http_host.init") || debug "Can't open $http_host.init! : $! ";
        <INI> =~ /page_root\s*=\s*(\S+)/m;
        close(INI);
        $page_root = $1;
        $conf_changed = 1;
        debug "conf changed. loading $http_host.init";
    }
    elsif ($ENV{PAGE_ROOT} && -d $ENV{PAGE_ROOT}) {
        $page_root = $ENV{PAGE_ROOT};
        $conf_changed = 1;      
    } 
    elsif ($http_host ne lc $last_http_host) {
        # Ok... we don't have an init file for this http_host, which means
        # we should use default (init.emu), but our hosts don't match,
        # so reload init.emu
       
        open(INI, "init.emu");
        <INI> =~ /page_root\s*=\s*(\S+)/m;
        close(INI);       
        $page_root = $1;
        $conf_changed = 1;
        debug "conf changed. loading init.emu";
    }

    debug "Version Info: $EMU::Version $EMU::Revision $EMU::Date";
    if ($conf_changed || check_conf_updates()) {
#        <INI> =~ /page_root\s*=\s*(\S+)/m;
#        close(INI);
#        $page_root = $1;
#        $EMU_DEBUG = 1;
#        debug "reassigned page_root to $page_root";

        &load_conf("default");
        &load_lang("default");

        # we should really set (reset) this here because load_conf("iface")
        # uses $emu_type
        $emu_type = $query->param('type') || $v{'emu_type'};
        
        if (! grep( $emu_type eq $_, split(/[\s,]+/, $c{ifaces})) ) {
           $emu_type = $c{'default_interface'} || "normal";
        }

        &load_conf("iface");
        &load_lang("iface");

        $EMU_DEBUG = bool($c{'emu_debug'});

        if ($query->param("https") && $c{'https_url'}) {
            $EMU_URL = $url = $c{'https_url'};
        }
        else {
            $EMU_URL = $url = $c{'emu_url'};
        }

        debug "requested $http_host last was $last_http_host";

        my $private;
	    my ($AD_VERT,$private);
	    # = &EMU::License::check_key();
        #check_license_module($private);

        debug "version is $AD_VERT";
        if ($AD_VERT == -1) {
#            write_tmp("title", $status);
#            write_tmp("phrase", $status);
            load_page("errors.html");
            return;
        }
    }

     if ( $licensed{domains} ) {
       my @domains = map { s/\./\\./g; $_ } split(/\s+/, $licensed{domains});
       if (! grep ($ENV{SERVER_NAME} =~ /$_/i, @domains) ) {
          write_tmp("title", "Licensing Error");
          write_tmp("phrase", "Licensing Error: This Webmail installation may only be accessed via a domain matching '$licensed{domains}'. Contact Sales to remove this licensing restriction.");
          load_page("errors.html");
          return;
       }
     }
 
    if ((grep {/$page_root\/lib/} join(' ',@INC)) == -1) {
        push (@INC, "$page_root/lib") ;
        debug "$page_root/lib not found in INC path, so appended it";
    }

    debug "INC path is @INC";
    debug "Browser Info: ".$ENV{'HTTP_USER_AGENT'};

    $date = get_date();         # get the current date
#    debug "date is $date";

    $last_http_host = $http_host;

    #allow the url to change with the configuration.
    # mm: 09/12/99
    if ($query->param("https") && $c{'https_url'}) {
        $EMU_URL = $url = $c{'https_url'};
    }
    else {
        $EMU_URL = $url = $c{'emu_url'};
    }

    # also debug can change...
    $EMU_DEBUG = bool($c{'emu_debug'});

    if ($licensed{"fallback_smtp"}) {
        (@smtp_host) = split(/\s|\,/,$c{"smtp_host"});
    }
    else {
        (@smtp_host) = (split(/\s|\,/,$c{"smtp_host"}))[0];
    }

    debug "available smtp hosts: @smtp_host";
    $smtp_port = $c{"smtp_port"} || "25";
    $pop_port = $c{"pop_port"} || "110";
#    $smtp_host = $c{'smtp_host'};

    # process any custom header information
    if ($licensed{"custom_headers"}) {
        (@custom_headers)        = split(/\s|\,/,$c{"Customized_Headers"});
        (@custom_headers_column) = split(/\s|\,/,$c{"Customized_Headers_Column"});
        (@custom_headers_action) = split(/\|\|/,$c{"Customized_Headers_Action"});
#        debug "custom_headers: @custom_headers";
    }

    $inbox = $c{'default_inbox_name'} || "INBOX";
    $no_waitscreen  = 1 if (bool($c{'disable_waitscreen'}));

#    debug "http_host = $http_host, last_http_host=$last_http_host";

    # If nfs is being used, make sure we're properly setup
    my @nfs_presence = split(' ', $c{"verify_nfs_presence"});
    foreach my $pres (@nfs_presence) {
        if (!-e $pres) {
            debug "NFS presence for $pres failed!";
            my $errmsg = $msg{'ERR_Fail_NFS_Presence'} ||
"An NFS error in the system has been encountered, please contact the system administrator, %1 (%2)";

            $errmsg = convert($errmsg, $ENV{"SERVER_ADMIN"}, $ENV{"SERVER_ADDR"});
	    write_tmp("phrase", $errmsg, 1);
	    write_tmp("logintext", 1);

	    load_page("errors.html");
            return;
        }
    }

    # when a user comes to this script for the very first time, they will
    # be thrown to the login page. If they try to login but encounter some
    # error, they will be tossed back to the login page again. If everything
    # seems okay, and it's their "first" time then we set the username and
    # type cookies and then put the user in login_parse() which will handle
    # the rest.
    if (scalar($query->param())) # if there are any variables
    {
#       debug "BRANCH 1";

	if ($query->param('first'))
	{
	    my ($user, $host, $flag);
            debug "FIRST";
            write_tmp("first", 1);

            get_cookies();

	    $folder    = $inbox;
	    $user      = $query->param('user_name');
	    $host      = $query->param('hostname');

            if ($user =~ /\#/) {
                $user =~ s/^(.+)\#(.+)$/$1/;
                $flag = $2;
            }

#            debug "user $user flag $flag";

	    #Make Usernames uniform.  Case sensitivity error? 11/28/98: MM
	    $user = lc($user);
	    # RFC822 compatible
	    #$user =~ s/\s//g;
	    #$user =~ s/\"//g;
	    #$user =~ s/\'//g;
	    #$user =~ s/://g;
	    #$user =~ s/,//g;
	    $host = lc($host) || $c{"default_pop"};
	    $host =~ s/\s//g;
	    $host =~ s/\"//g;
	    $host =~ s/\'//g;
	    $host =~ s/,//g;
	    $host =~ s/://g;
	    $host =~ s/\.+$//g;

            unless ($c{"allow_nonstandard_usernames"}) {
                # remove leading .'s and any forward slashes from username
#                debug "not allowing use of nonstandard usernames.";
                $user =~ s/^[\.|\/]+//g;  # remove leading .'s and /'s
                $user =~ s/(\.\.\/)+|(\/\.\.)+//g; # remove any "../" sequence
            }

	    $user_name = "$user\@$host";

            ($user, $host) = map_mailserver($user, $host);
            $popuser = $user;
            $pophost = $host;

	    # 08/30/98: if the special `c' variable is passed along then we are to take it that
	    # the password has been code()ed, so we decode() it.
	    $password = $query->param('c') ? decode($query->param('password')) : $query->param('password');


            $homedir = getpath("$user\@$host") if ($user ne "" && $host ne "");
            
            # FIXME - This will break things for people how have case sensitive filesystems and multicased paths
            # getpath now handles this. It also lc's just the homedir, not the full path
#            $homedir = lc($homedir);  # make absolutely sure we're all lower

#	    debug "firstlogin with type=".$query->param('type');
	    debug "user=$user  host=$host  username=$user_name  homedir=$homedir popuser=$popuser";

	    #$emu_type = $query->param('type') || $v{'emu_type'} || $c{'default_interface'} || "normal";
	    $emu_type = $query->param('type') || $v{'emu_type'};
        
            if (! grep( $emu_type eq $_, split(/[\s,]+/, $c{ifaces})) ) {
               $emu_type = $c{'default_interface'} || "normal";
            }
                                   
	    # allow per use configuration files..
	    &load_lang("iface");
	    &load_conf("iface");
	    &load_lang("home");
	    &load_conf("home");

	    login_parse($user, $host, $flag);

	    $v{"emu_type"} = $emu_type;
	    $v{"time"} = time if ( isActivity4Session() );
        $v{"popuser"} = $popuser;
        $v{"pophost"} = $pophost;
        $v{"user_name"} = $user_name;
	    $v{"protocol"} =$protocol;
        $v{"password"} = code($password);

        unless ($userdb{"folder:$inbox:email"})
        {
        	$userdb{"folder:$inbox:email"} = $query->param("user_name")
            	if ($query->param("user_name") =~ /@/);
        }

	    close_db() if ($db_opened);
	    cleanup();      
	}
	else
	{
#	    debug "HTTP_COOKIE:".$ENV{"HTTP_COOKIE"};

	    $passed = $query->param('passed');
	    $passed =~ y!/!!;
#           $passed =~ s%/%%;   # funky IE workaround

	    if ($passed)
	    {
                # Parse cookies
                get_cookies();

                $user = lc($emu_cookies{"user"});
                $host = lc($emu_cookies{"host"});
                $qs = $emu_cookies{"qs"};

                ($user, $host) = map_mailserver($user, $host);
                $homedir = getpath("$user\@$host") if ($user ne "" && $host ne "");
                # getpath now handles this. It also lc's just the homedir, not the full path
                #$homedir = lc($homedir);  # make absolutely sure we're all lower

                open_session_file(1);

#		debug "Session is $qs";

		#$emu_type = $v{'emu_type'} || $emu_cookies{emu_type} || $c{'default_interface'};
		$emu_type = $v{'emu_type'} || $emu_cookies{emu_type};
        
                if (! grep( $emu_type eq $_, split(/[\s,]+/, $c{ifaces})) ) {
                   $emu_type = $c{'default_interface'} || "normal";
                }
                                   
#		debug "type= $emu_type";
	    
		$user_name = $v{"user_name"};
                $popuser   = $v{"popuser"};
                $pophost   = $v{"pophost"};
		$protocol  = $v{"protocol"}; # gotta use the same protocol to connect
		debug "homedir is $homedir popuser=$popuser username=$user_name ($v{user_name} $v{username}) protocol is $protocol !";

		# 08/30/98: if the special `c' variable is passed along then we are to take it that
		# the password has been code()ed, so we decode() it.
		$password = $query->param('c') ? decode($query->param('password')) : $query->param('password');

		$password = $password || decode($v{password});

#               debug "vpassword=$v{password}";

		# allow per use configuration files..
		&load_lang("iface");
		&load_conf("iface");
		&load_conf("home");
		&load_lang("home");

                if ($query->param('passed') ne "compose_parse") # Alex session escape fix
 		{       
                 	return &session_expired() if ($user eq "" || $host eq "" || !session_check());
 		}

                if ($query->param("passed") eq "restore_state") {
                    restore_state();
	            $passed = $query->param('passed');
	            $passed =~ y!/!!;
                }

		if ( !$query->param('folder') )
		{
		    $folder = $v{"folder"} || $v{"last_folder"};
		    $folder = $inbox unless $folder;
		}
		else
		{
		    $folder = $query->param('folder');
		}
				
		debug "passed=$passed  protocol=$protocol  variable=".$query->param('variable');
#		debug "query paramlist=", join(" ", $query->param());

		write_tmp("login_session", $qs eq "LOGIN", 1);
		
		open_db() unless $db_opened;
		$tmpstat = jump($passed);
		close_db() if $db_opened;

		cleanup($tmpstat);
	    }
	    else                # no passed subroutine 
	    {
		login();
		return;
	    }
	}
    }
    else
    {
	login();
	return;
    }
    
    debug "state: folder=".$query->param("folder")." passed=".$query->param("passed")." variable=".$query->param("variable")." quick.x=".$query->param("quick.x");
    debug "ALL THE WAY";
}

sub session_expired
{
    $status ||= $msg{'ERR_SessionExpired_S'};

    write_tmp("title", $msg{'ERR_SessionExpired_T'}, 1);
    write_tmp("phrase", $_[0].$msg{'ERR_SessionExpired_B'}, 1);
    write_tmp("logintext", 1);

    load_page("errors.html");
    close_db() if ($db_opened);
    return 0;
}

sub jump {
    my ($subroutine, @rest) = @_; 

    my %valid_subs = map {$_ => 1} qw/
    	msg options refresh logout go_index compose compose_parse multi select mailcheck 
    	send_readreceipt folders folders_parse edit_address_group address_groups address 
    	address_parse addto reply qreply forward delete_msg help options_parse detach index 
    	spelling_parse waiting version parse new_msg directory process_attachment 
    	process_options address_select mailboxes process_mailboxes collapse_menu toggle_menu
    	expand_menu import_addressbook export_addressbook process_filters update_subscriptions
    	questionaire questionaire_parse editor calevent_add/;

    debug "$subroutine, @rest";

    debug "homedir=$homedir popuser=$popuser folder = $folder";

#    return &$subroutine(@rest) if ($passed eq "version");
    if ($passed eq "version") {
        version();
        return;
    }

	# eh, let's reset this session counter of filtered spam here
	$v{"filteredspam"} = 0;

    # require in the file and then call its run() function
    if (session_check() or ($query->param('passed') eq "compose_parse")) #Alex session escape fix
    {
	$v{"time"} = time if ( isActivity4Session() );

      FORCE_CUSTOM_LOGIN_CHECK:
        {
            # we provide a mechanism to force a custom success_login check
            # if a previous one determined failure. This shuts a "back door"
            # However, this is only done if success_login explicitly calls for
            # setting of $v{"success_login_failed"} by returning a -1 value
            last if (!bool($c{"success_login_sub"}) || 
                     $v{"success_login_failed"} != 1);

            load_module("EMU::Custom");

            debug "Forcing Call to success_login($user_name)";
            my $success_login_status = &EMU::Custom::success_login($user_name);
            debug "status $success_login_status";

            if ($success_login_status == -1) {
                $v{"success_login_failed"} = 1;
#                login();
                return;
            }
            else {
                delete($v{"success_login_failed"});
            }
        }

         # Don't let the user do -anything- else if we're in the demo version and the user hasn't done the questionaire yet
         if (($AD_VERT == VERSION_ADVERT || $AD_VERT == VERSION_DEMO || $c{enable_questionaire}) && 
              $subroutine !~ /^questionaire/ && 
              !$userdb{"questionaire_complete"}) {
            debug "Forcing questionaire";
            $subroutine = 'questionaire';
            undef @rest;
         }

		if ( $valid_subs{$subroutine} )
		{
		    #MM 11/28/98 -- Gotta check the quota!
		    quota_check($subroutine =~ /logout|detach/);
	
		    no strict 'refs';
	
		    eval
		    {
				my ($sub) = $query->param("c_sub");
				if ($sub)
				{
				    load_module("EMU::Custom");
				    $sub = "EMU::Custom::".$sub;
				    &$sub;
				    debug "Ran $sub -XXX";
				}
		    };
			return &$subroutine(@rest);
		}
		else
		{
		    debug("subroutine jump error for $subroutine, valid subs are: " . join ' ', keys %valid_subs);
		    go_index();
		}
    }
    else
    {
        debug "huh? session expired!";
		$status ||= $msg{'ERR_SessionExpired_S'};

		write_tmp("title", $msg{'ERR_SessionExpired_T'}, 1);
		write_tmp("phrase", $msg{'ERR_SessionExpired_B'}, 1);
		write_tmp("logintext", 1);

		load_page("errors.html");
    }

    debug "END OF JUMP";
}

sub cleanup
{
#    undef %poplist;
    debug "cleaning up";

    $pop_connected = 0;

    # Close out all mail server connections
    &flush_connections();


#    goto end_of_line;
}

# verify that the directories we use are created and writeable.
# if they aren't, we print a nice error message and exit
sub check_installation
{
    my $msg;
    
  MAKE_DIRS:
    {
	-e $page_root || mkdir($page_root, 00700);
	-e "$page_root/homes" || mkdir("$page_root/homes", 00700);
	-e "$page_root/tmp" || mkdir("$page_root/tmp", 00700);
    }

  CHECK_DIRS:
    {
	if ( (! -e $page_root || ! -w $page_root) && (!-w "$page_root/homes" || !-w "$page_root/tmp") )
	{
	    $msg .= convert($msg{'ERR_CheckDirs_B'}, $page_root, $>);
	}
	
	if (! -e "$page_root/homes" || ! -w "$page_root/homes")
	{
	    $msg .= convert($msg{'ERR_CheckDirs_B'}, "$page_root/homes", $>);
	}
	
	if (! -e "$page_root/tmp" || ! -w "$page_root/tmp")
	{
	    $msg .= convert($msg{'ERR_CheckDirs_B'}, "$page_root/tmp", $>);
	}
    }

    if ($msg)
    {
	print_header();

	FatalError($msg{'ERR_CheckDirs_T'},$msg);

	# can't use the goto here because the exit point hasn't been defined yet
	exit;                   # won't work anyways
    }
}


sub reverse_html {
    # replace special characters with HTML codes

    my ($string) = @_;

    if ($licensed{"wap"} && $c{"is_wap"})
    {
        
	$string =~ s/<br\/>/\n/g;
	$string =~ s/\$\$/\$/ig;

        $string =~ s/\&quot;/"/ig;
        $string =~ s/\&apos;/'/ig;
        $string =~ s/\&gt;/>/ig;
        $string =~ s/\&lt;/</ig;
        $string =~ s/\&amp;/\&/ig;

      return $string;
   };

    $string =~ s/&#33;/\!/g;
    $string =~ s/&#34;/\"/g;
    $string =~ s/&#36;/\$/g;
    $string =~ s/&#39;/\'/g;
    $string =~ s/&#40;/\(/g;
    $string =~ s/&#41;/\)/g;
    $string =~ s/&#42;/\*/g;
    $string =~ s/&#47;/\//g;
    $string =~ s/&#61;/\=/g;
    $string =~ s/&#63;/\?/g;
    $string =~ s/&#64;/\@/g;
    $string =~ s/&#91;/\[/g;
    $string =~ s/&#92;/\\/g;
    $string =~ s/&#93;/\]/g;
    $string =~ s/&#123;/\{/g;
    $string =~ s/&#124;/\|/g;
    $string =~ s/&#125;/\}/g;
    $string =~ s/&#126;/\~/g;
    $string =~ s/&#43;&#43;/\+\+/g;
    $string =~ s/&#45;&#45;/\-\-/g;
    $string =~ s/&lt;/</g;
    $string =~ s/&#60;/</g;
    $string =~ s/&gt;/>/g;
    $string =~ s/&#62;/>/g;
    $string =~ s/&#43;/\+/g;
    $string =~ s/&#45;/\-/g;

    return $string;
}


# HM 10/26/00 - Better.
# Description: HTML Escapes specified characters in target string
# Example usage: &safe_html($mystr, '$&@'); 
# PARAM 0: Target String
# PARAM 1..X: Characters to escape. Defaults to !"$'()*\/=?@[\]{|}~+-<> if not provided.
sub safe_html
{
   my $str = shift;
   my $chars;
   
   if (@_) {
      $chars = join('', @_);
   } 
   elsif ($licensed{"wap"} && $c{"is_wap"}) {
      # Standard WAP set
      $chars = q/\&<>'"$/;

   } else {
      # Default to 'standard' set. This is the set of characters the old
      # &safe_html used.  We could probably use [:punct:], but I don't  
      # wanna go that far yet.
      $chars = q/!"$'()*\/=?@[\]{|}~+-<>/;
   }
    
   # We only replace certain things (in a certain way) in WAP mode
   if (!$licensed{"wap"} || !$c{"is_wap"})
   {

      $str =~ s/([\Q$chars\E])/'&#'.ord($1).';'/ge;

   } else {
      
      if ($chars =~ /\&/) {
         $str =~ s/\&/\&amp;/ig;
      }
      
      if ($chars =~ /</) {
         $str =~ s/</\&lt;/ig;
      }
      
      if ($chars =~ />/) {
         $str =~ s/>/\&gt;/ig;
      }
      
      if ($chars =~ /'/) {
         $str =~ s/'/\&apos;/ig;
      }
      
      if ($chars =~ /"/) {
         $str =~ s/"/\&quot;/ig;
      }
      
      if ($chars =~ /\$/) {
         $str =~ s/\$/\$\$/ig;
      }
   }

   return $str;
}

#  ******************************************************************* #
#
#   9/30/99 rcs.ngf.v.1 nph-emumail.cgi block.1 begin {

# get_useragent_props()                                # -- 8/10/99, NF
# 
# Since there's no standard syntax returned by browsers, this function
# tries to order the elements in the HTTP_USER_AGENT string, detecting
# MSIE posing as Mozilla. It returns a(n unordered) hash of :
# ( browser, major version, minor version, os, language ), where browser
# is the real one -- MSIE instead of "Mozilla (Compatible...)".
#
# The list of various browsers' HTTP_USER_AGENT lines tested was found at :
#  http://www.msb.edu/dept/msbtc/waehner/browser/

sub get_useragent_props
{
    my( $useragent_string, $working_useragent_string, $n, %useragent_props, 
	$browser, $lang, $version_no, $major_version, $minor_version,
	$first_parentheses, $rest_useragent_string, $system, $os );

    #print $query->header;

    $useragent_string = shift;
    #$useragent_string = "Mozilla/4.61 [en]C-compaq (Win98; I)"; # TEST -- troublemaker! -- 99/10/19 --ngf
    #$useragent_string = "Mozilla/4.5 [en]C-CCK-MCD compaq (Win98; U)"; # TEST --ngf
    #$useragent_string = "Mozilla/4.0 (compatible; MSIE 4.0; Windows 98; DigExt)";
    #$n = m/((\w|\s|\-|\_)+)\s*((\/)(((\d+)(\-|\.)?((\w)|\-|\.)+?)?\s*)+)\s*(\[(.*?)\])?([^(]*)?(\((.*?)\))?(.*)?/i;

    #$_ = $useragent_string;
    #setup stack
    $working_useragent_string = $useragent_string;
    debug "was: $working_useragent_string";   
    # get browser
    ($browser) = $working_useragent_string =~ /^((\w|\s|\-|\_)+)/i;

    #debug "BROWSER: $browser";

    #remove from stack
    $working_useragent_string =~ s/$browser\///i;

    #debug "was: $working_useragent_string";   

    # get version
    #($version_no) = $working_useragent_string =~ /((((\d+)(\-|\.)?((\w)|\-|\.)+?)?\s*)+)/i;
    #$_ = $working_useragent_string;

    $working_useragent_string =~ /(\S+)?(\s|\W|$)/i;
    $version_no = $1;
    #debug "version: $version_no";

    # remove
    $working_useragent_string =~ s/^.*?$version_no//o;
    #debug "was: $working_useragent_string";   
   
    #get lang
    ($lang) = $working_useragent_string =~ /\[(.*)\]/i;
    debug "LANG $lang";
    # REMOVE
    $working_useragent_string =~ s/^.*\[(.*)\]//g if $lang;
    #debug "was: $working_useragent_string";   
    
    ($first_parentheses) = $working_useragent_string =~ /(\((.*?)\))/i;
    debug "FIRST $first_parentheses";

#    $browser = $1;  $version_no = $6;  $major_version = $7;
#    $lang = $12;  $first_parentheses = $15;  $rest_useragent_string = $16;  

    #print "Content-type: text/html\n\n<br>\n"; # TEST
    #EMU::debug("1=$1, 2=$2, 3=$3, 4=$4, 5=$5, 6=$6, 7=$7, 8=$8, 9=$9, 10=$10, 11=$11, 12=$12, 13=$13, 14=$14, 15=$15, 16=$16, 17=$17, 18=$18 <br>\n");
    #EMU::debug("useragent_string = $useragent_string, n=$n, browser = $browser, version_no = $version_no, lang=$lang, first_parens=$first_parentheses, rest = $rest_useragent_string, major version = $major_version");  # TEST 

    # name of browser ?

    if( $browser =~ /Mozilla/i ) 
    {
	if( $first_parentheses =~ /MSIE/i )  # blow IE's cover!
	{
	    $browser = "msie";
	    $first_parentheses =~ m/MSIE\s*(\S+)?[;)\s]/i;
	    $version_no = $1;
	}	
    }
    elsif( $browser =~ /Lynx/i )
    {
	$_ = $browser;
	s/\///g; s/ //g;
	$browser = $_;
    }
    elsif( $browser =~ /IWENG|aolbrowser/i )
    {
	$browser = "aol";
    }


    # version no's ?
    #debug("version_no before getting major and minor : $version_no ");
    $version_no =~ m/(\d+)\.(.*)/i;  $major_version = $1;  $minor_version = $2;


    # which OS ?

    $_ = $first_parentheses;
    $n = m/(Linux|((win(\w+\s*\d+)?)\s*)|Solaris|SunOS|Irix|UX|FreeBSD|OSF|Mac|BeOS|OS\/2)/i;
    $os = $1 if $n;
    if( !$os ) { $os = "unknown"; }
    else 
    {
	if( $os =~ /win/i )
	{
	    $os = 'win';
	}
    }

    %useragent_props = ('browser'       => $browser,
			'major_version' => $major_version,
			'minor_version' => $minor_version,
			'os'            => $os,
			'language'      => $lang);


    EMU::debug "useragent = $useragent_string";
    EMU::debug "browser = $browser, lang = $lang, system = $first_parentheses, os = $os <br>";
    EMU::debug "major = $major_version, minor = $minor_version <Br>";

    #foreach (keys %useragent_props) { print "prop : $_ =  $useragent_props{$_} <Br>"; };

    return \%useragent_props;
}


# sub atoi ( $text_number, $radix )                   rcs.ngf.v.1  9/30/99 --ngf
#
#  this function returns the integer value of a number in a text string.

sub atoi
{
    my( $i, $integer, $digit );
    my( $text_number ) = shift(@_);
    my( $radix ) = shift(@_);

    for( $i = 0; $i < length( $text_number ); $i++ )
    {
	$digit = ord( substr($text_number, $i, 1) ) - 48; # Ascii to digit
	$integer += $radix**(length($text_number) - $i - 1) * $digit;
        #debug( "digit = $digit" );
    }

    &EMU::debug( "converted $text_number into integer $integer ");
    return $integer;
}


# find_approximate_template()
# 
# This function returns the closest custom template according to the
# user's browser environment, found by get_useragent_props().

sub find_approximate_template
{
    my( $basefile ) = shift;
    my( $testing, $found, $basename, $customfile, $actual_file, $full_filename, $ext, $this_prop, $rev_no,
	%useragent_props, @ordered_useragent_props, @files_to_try, $i, $j, $n, $index_where_found );

    if( !$basefile )
    {
	$customfile = "default.html";
    }
    else
    {
	($basename, $ext) = split /\./, $basefile;
	%useragent_props = %{ get_useragent_props( $ENV{'HTTP_USER_AGENT'} ) };

	$customfile = $basename;
	@ordered_useragent_props = ( 'browser', 'major_version', 'os', 'language' );

	# create list of browser/version/OS-specific filenames :

	foreach $this_prop (@ordered_useragent_props)
	{	
	    if( $this_prop =~ /major(\_)?version/i )
	    {
		$customfile .= "-?";
	    }
	    else
	    {
		$customfile .= "-" . $useragent_props{$this_prop};
	    }

	    $_ = $full_filename = lc( $customfile . "." . $ext );
	    s/ //g;  s/\///g;  s/\\//g;
	    $full_filename = $_;
	    
	    $files_to_try[$i++] = $full_filename;
	    debug "customfile added = $full_filename <br>";
	}
	

	# try the most browser/version/OS-specific filenames first :	

	$found = 0;
	for( $i = scalar(@ordered_useragent_props)-1; $i > -1  &&  $found == 0; $i-- )
	{
	    $actual_file = $customfile = $files_to_try[$i];
	    debug "trying custom file $customfile  .... ";

	    if( $actual_file =~ /\?/ )
	    {
		# add all previous major ver's of browser to list for backward compatibility :

		for( $j = EMU::atoi( $useragent_props{'major_version'}, 10 ); $j > 0 && $found == 0; $j-- )
		{
		    $actual_file = $customfile;
		    $_ = $actual_file;		    $n = s/\?/$j/e;		    $actual_file = $_;
		    #$actual_file = $actual_file =~ s/\?/$j/;

		    debug("actual_file = $actual_file");

		    if( -e "$page_root/iface/$c{'default_interface'}/$actual_file" )
		    {
			$found = 1;
			#$index_where_found = $i;

	                debug "found custom file $customfile<br>" ;
		    }
		    #else { debug "nope! <br>" ; }
		}

	    }
	    else
	    {
		if( -e "$page_root/iface/$c{'default_interface'}/$actual_file" )
		{
		    $found = 1;
		    #$index_where_found = $i;
		    
		    debug "found custom file $customfile<br>" ;
		}
	    }
	}
	    

	if( !$found )
	{
	    $customfile = $basefile;
	}
	else
	{
	    $customfile = $actual_file;
	}
	
    } # else $file is specified.


    return $customfile;
}


#  } end block.1 nph-emumail.cgi rcs.ngf.v.1 9/30/99
#
#  ******************************************************************* #



sub get_data_from_action {
    my ($hindex,$data) = @_;

    debug "headers data is $data";

    my $action = $custom_headers_action[$hindex];
    trim(\$action);

    debug "action is $action";

    if ($action =~ /^\s*headerdata\s*$/i) {
        $action = $data;
    }
    elsif ($action =~ /^\s*{\s*/ && $action =~ /\s*}$/) {
        debug "conditional... $action";
        # we have a conditional
        $action = eval($action);

        debug "action now $action";
    }

    return $action;
}


sub process_custom_headers {
    my ($h,$loophash,$i) = @_;
    my %h=%{$h} if $h;
    my %loophash=%{$loophash} if $loophash;

    my $hindex = 0;
    my $newcolindex = 0;

#    debug "custom headers are @custom_headers";
    # if we have any customized headers for processing, check them now
    foreach my $chead (@custom_headers) {
#        debug "checking for header $chead, index $hindex, data $h{$chead}";

        # We save Content-Type as :ct in folderdb, so if we don't have
        # a Content-Type in %h, check for :ct instead
        $chead = "ct" if ($chead =~ /content-type/i && !$h{$chead} && $h{ct});

        # this feature can either ask for matching a specific header, or
        # it can use DONTCARE to force creation of a new data column. Must also
        # check for "NEW" column which then must force get_data_from_action
        if ($h{$chead} || $chead eq "DONTCARE" || 
                $custom_headers_column[$hindex] =~ /new/i) {
            my $column = lc($custom_headers_column[$hindex]);
            my $data = get_data_from_action($hindex, $h{$chead});

            if ($column =~ /new/i) {
                # configuring a brand new column rather than replacing one
                $newcolindex++;
                $column = "newcolumn$newcolindex";
            }

            debug "setting $column$i to $data";
            $loophash->{"$column$i"} = $data if ($data);
        }

        $hindex++;
    }
}



# load_page
#
# This function will load and parse an HTML page for EMUtokens. If we
# are running under FCGI or mod_perl we will cache the document the
# first time it's read, then subsequent load_page()  calls for the same
# document will get the cached entry.
#
# The recognized EMUtokens are listed in the comment above do_emucode()
sub load_page
{
    my ($file, $bnocleanup, $force_type, $force_load) = @_;
    my ($ra_data,$md5,$checksum);
    my $do_checksum = 0;

    
    #  ******************************************************************* #
    #
    #   9/30/99 rcs.ngf.v.1 nph-emumail.cgi block.2 begin {


    if( lc( $c{'per_useragent_template'} ) )
    {
	$file = find_approximate_template( $file );

	EMU::debug( "custom page to load is $file " );
    }

    #  } end block.2 nph-emumail.cgi rcs.ngf.v.1 9/30/99
    #
    #  ******************************************************************* #


    &load_conf("iface");
    &load_lang("iface");

    # $parsed_output is the page after the EMU parsing, and before the Embperl parsing
    my ($parsed_output);

#    dumpstack() if ($c{'emu_debug'});

    no strict qw(vars refs);

    print_header();

    if ($query)
    {
	$emu_type = $force_type || $query->param('type') || $v{'emu_type'} || $emu_type;
    }
    else
    {
	$emu_type = $force_type || $v{'emu_type'} || $emu_type;
    }

    if (! grep( $emu_type eq $_, split(/[\s,]+/, $c{ifaces})) ) {
       $emu_type = $c{'default_interface'} || "normal";
    }
    
    debug "loading page with file $file. emu_type = $emu_type";
    write_tmp("load_page", $file);

    if ($INTERNAL_EMU)
    {
	$file =~ s/\.html$//;
	$ra_data = load_page_internal($file);
    }
    else
    {
	$ra_data = load_page_external($file);
    }

    if ($ra_data eq undef)
    {
	debug "Couldn't make an ra_data :(";
	# ERRROR
    }
    $parsed_output = join('', @{$ra_data});

  IS_CHECKSUMING_NEEDED:
    {
        # Here is our current licensing options:
        #
        # VERSION_ADVERT  => No license keys, no expiry, NO iface changes
        # VERSION_DEFAULT => auto expiration required, iface change OK, NO ads
        # VERSION_DEMO    => no default expiry, iface change OK, MUST have ads
        # VERSION_STANDARD=> no default expiry, NO iface changes, NO ads
        # VERSION_PROFESSIONAL => Do whatever you want... :-)
        # VERSION_ERROR   => If we've gotten an error dont bother checksuming

        # don't care about checksums if iface change is OK for this version
        last if ($AD_VERT == VERSION_PROFESSIONAL ||
                 $AD_VERT == VERSION_DEMO         ||
                 $AD_VERT == VERSION_DEFAULT      ||
                 $AD_VERT == VERSION_ERROR);

        # otherwise we want to checksum the template
        $do_checksum = 1;
    }

    # WHM (03/12/99) Added the Embedded Perl parsing. 
    # options => 512 removes HTML scan
    if ($c{"embedded_perl"})
    {
        debug "preparing to parse embperl";
	load_module("Embperl");
	load_module("EMU::Theme");
        # HM 06/28/00 - Lets set up some commonly used data for the interface
        my $params = {
                        DOCROOT => "$page_root/iface/$emu_type",
                        IMGURL  => $c{img_url},
                        HTMLURL => $c{html_url},
                        SKIN    => $userdb{'options.skin'} || $c{default_skin} || 'EMU_Original',
                        theme   => EMU::Theme->new,
                        folders => []
                     };

        if ($homedir) {
                my @folders = sort { lc($a) cmp lc($b) } grep {
                                      $_ ne $inbox &&
                                      $_ ne 'Search Results' &&
                                      !$EMU::userdb{"folder:$_:external"}
                                   } &EMU::get_subscribed_folders();
                debug "embperl folders are being set to: @folders";
                $params->{folders} = \@folders;
        }
        
        # JR(6/18/99): We need optDisableFormData = 256 here in order
        # to bypass the %fdat and @ffld creation, which were causing
        # the server to hang, waiting to gather CGI input.
        Embperl::Execute({ input     => \$parsed_output,
                           inputfile => $file,
                           output    => \$parsed_output,
                           options   => 2|16|256|512|16384,
                           mtime     => -M $file,
                           param     => [$params],
                           debug     => 0,
                           escmode   => 0 });
        debug "Done parsing embperl!";
    } 

#    debug "ra_data has ",join('',@{$ra_data});

  VERIFY_DEMO_ADS:
    {
        # before we continue, let's verify ads in case this is a DEMO version.
        # DEMO versions are forced to output ads unless 
        # $licensed{"override_ads"} is set
        last if ($force_load || $AD_VERT != VERSION_DEMO);

        if ( !$licensed{"override_ads"}    && 
                !$img_printed              &&
                $file ne "waitwindow.html" &&
                $parsed_output !~ /\({\s*top_image\(\)\s*}\)/i
                ) {
	   write_tmp('phrase', "Licensing Error: Your EMU license is for a DEMO version. Ads are required to be shown from your templates. Contact sales\@emumail.com for a valid license key.");
           return load_page('errors.html',  $bnocleanup, $force_type, 1);
        }
    }


    if ($c{"embedded_perl"})   
    {
        print $parsed_output;
    } 
    else
    {
        debug "Processing emucode.";
        my ($ah);                   # array handle
        $ah = new IO::ScalarArray [ split(/(\n)/,$parsed_output) ];
        if (!$ah)
        {
    	    FatalError("Bad bad bad", "Unable to create IO::ScalarArray object in load_page!<BR>($!)<BR>Please contact the administrator of this web service and inform them of this problem.");
    	    error("Unable to create IO::ScalarArrayObject in load_page: $!");
            return;
    	#die("Unable to create IO::ScalarArrayObject in load_page: $!");
        }

        while (defined($_ = $ah->getline))
        {
    	if (/\( \{ \s* (.*?) \s* \} \)/x)
    	{
    	    my ($code) = $1;
    #           debug "code=$code";
    	    if ($code =~ /^for \s+ (\S+) \s+ in \s+ \@(\S+)/x)
    	    {
    		my ($iterator, $array) = ($1, $2);
    		my (@looparr,%loophash);
    		my ($output);
    		
    #               debug "iterator=$iterator  array=$array";
    		
    		if ($array eq "messages")
    		{
                    my @data = get_msg_array();
                    @looparr  = @{ $data[0] };
                    %loophash = %{ $data[1] } if $data[1];

    		}
    		elsif ($array eq "folders")
    		{
    		    debug "using folders array";
    		    @looparr = get_folders();
    		}
                elsif ($array eq "suggestions")
                {
                    @looparr = split(':', get_var("suggestions"));
                }
                elsif ($array eq "imapdirs")
                {
                    debug "getting imap directories";
                    @looparr = &get_imap_dirs();
                    debug "folders: @looparr";
                }
    		elsif ($array eq "folders_encoded") #MM 04/25/99
    		{
    		    @looparr = get_folders();
    		    map { $loophash{$_} = private_str($_) } @looparr;
    		}
    		elsif ($array eq "folders3_encoded") #display hierarcical folders nicely.
                {
                    @looparr = get_folders_with_nodes();
                    my @all_folders = @looparr;

                    my ($folder,%all,%folders,@hierarchies,@folders);
    		    
    		    @folders = get_folders();
    		    
    		    map { $all{$_} = 1 } @looparr;
    		    map { $folders{$_} = 1 } @folders;
    		    
    		    foreach my $thekey (keys %all)
    		    {
    			push (@hierarchies, $thekey) if (! exists $folders{$thekey});
    		    }

                    map 
    		    {
    			$loophash{$_} = private_str($_) ;
    			my $end;
    			if (/\//)
    			{
    #			    /^([^\/]*)\/?(.*)$/; #just take end			    
    			    ($end) = /\/([^\/]*)$/; #just take end			    
    			}
    			else 
    			{
    			    $end = $_;
    			}

    			($loophash{"end_".$_}) = $end;
    		    } @looparr;
    		    
    		    #Reset Looparr
    		    @looparr = ();
    		    
    		    # Add "/" to the end of hierarchies.
    		    map 
    		    {
    			$loophash{"is_hierarchy$_"} = 1;
    			push (@looparr, $_);
    		    } @hierarchies;
    		    push (@looparr,@folders);
    		    
    		    #Set level of indentation
    		    map
    		    {
    			my $before = $_;
    			my $after = $_;

    			$after =~ s/\///g;
    			
    			$loophash{"levels$_"} = length($before) - length($after);
    		    } @looparr;

    		    @looparr = sort @looparr;
                }
    		elsif ($array eq "folders2")
    		{
    		    debug "using folders2 array";
    		    @looparr = get_folders_with_nodes();
    		}
                elsif ($array eq "directory")
                {
                  DO_THIS:
                    {
                       my @data = &get_directory();
                       @looparr = @{ $data[0] } if $data[0];
                       %loophash = %{ $data[1] } if $data[1];                    
                    }
                }
    		elsif ($array eq "filters")
    		{
    		    my (@filters, $total);
    		    
    		    $total = $userdb{"filters.total"} + 1;
    		    
#    		    debug "total = $total";
    		    @looparr = (1..$total);
    		    
    		    # NOTE: how about just letting the user dig into this data rather than reproducing it?
    		    for (@looparr)
    		    {
    			$loophash{"type$_"} = $userdb{"filters.type$_"};
    			$loophash{"action$_"} = $userdb{"filters.action$_"};
    			$loophash{"data$_"} = $userdb{"filters.data$_"};
    			$loophash{"modifier$_"} = $userdb{"filters.modifier$_"};
    			$loophash{"bRegex$_"} = $userdb{"filters.bRegex$_"};
    		    }
    		    
    		}
    		elsif ($array eq "addrs")
    		{
                    my @data = get_addrs_array();
                    @looparr  = @{ $data[0] } if $data[0];
                    %loophash = %{ $data[1] } if $data[1];

    		}
    		elsif ($array eq "headers")
    		{
                    my @data = get_header_array();
                    @looparr  = @{ $data[0] } if $data[0];
                    %loophash = %{ $data[1] } if $data[1];

    		}
    		else
    		{
    		    debug "NO ARRAY! ???";
    		    error("Invalid loop array specified: $array");
    		}
    		
    		my ($fordata);
    		my ($found) = 0;

    		while (($line = $ah->getline))
    		{
    		    do { $found = 1; last } if ($line =~ /\(\{\s*done\s*\}\)/);
    		    $fordata .= $line;
    		}
    		
    		if (!$found)
    		{
    		    error("EOF encountered before ({done}) for `for' loop!");
    		}
    		
    #                debug "fordata is $fordata";
     
    		for (@looparr)
    		{
#                    debug "loop: '$_'";
    		    my ($copy) = $fordata;
    		    $copy =~ s/\$$iterator/$_/g;
 		       $copy =~ s/\$$array\[(.*?)\]/&safe_html($loophash{$1},q{$})/eg;

                    # Handle '$var' expansion. 
                    # 10/02/00 - Allowing delayed code execution by calling code refs recevied from get_var
    		    $copy =~ s/
    		               \$([\w\.]+)
    		              /
    		               my $val = get_var($1);
    		               if (ref $val eq 'ARRAY' && ref $val->[0] eq 'CODE') {
    		                  my $f = shift @$val;
    		                  $val = &$f(@$val);
    		               }
    		               $val
    		              /gex; 

    		    $copy =~ s/\(\{\s*repeat\s*(.*)\s*\}\)\s*(.*?)\(\{\s*end_repeat\s*\}\)/$2 x $1/exsig;
    		    $copy =~ s/\( \{ (.*?) \} \)/do_emucode($1)/gxe; # ({ EMUCODE })

    		    $output .= $copy;
    		}

    #                debug "outputting $output";
    		
    		$_ = $output;
    	    }
    	    else
    	    {
    		s/\$([\w\.]+)/$_=get_var($1),chomp,$_/ge;               # $vars
    		s/\( \{ (.*?) \} \)/do_emucode($1)/gxe; # ({ EMUCODE })
    	    }
    	}
    	else
    	{
    	    s/\$([\w\.]+)/get_var($1)/ge;               # $vars
    	}
    	
    	next if ( ($EMU::{'private_doif'} ne undef) && ($EMU::{'private_doif'} == 0) );
    	
        print;
        }
    }

    unless ($bnocleanup)
    {
	for (@{$EMU::{'cleanupvars'}})
	{
	    $EMU::{$_} = undef;
#           delete(${"EMU::$_"});
	}
    }

    debug "done.";
    
    1;
} # load_page


#MM -- Add to addressbook functionality
sub add2addr
{
    my ($addr) = @_;
    my ($url) = make_url("address",$addr);
    my $disp = safe_html($addr, '<>');
    my $target = get_target(1);
    return "<a href=\"$url\" target=\"$target\" title=\"Click to add to your addressbook!\">$disp</a>";
}

sub load_page_internal
{
    my ($name) = @_;
    my ($ra_data);

    return undef if (!defined($dispatch{$emu_type}));

    my ($evalerr);
    $evalerr = eval { &{$dispatch{$emu_type}->{$name}} };
    if ($evalerr eq undef)
    {
	FatalError("Fatal EMU Error", "We have encountered a fatal EMU error while<br>locating the page `$emu_type/$name.html' ($!)");
    }
    else
    {
	$ra_data = [ map { "$_\n" } split(/\n/, $evalerr) ];
    }

    return($ra_data);
}

sub load_page_external
{
    my ($file) = @_;
    my ($ra_data);

    if ($c{'cache_emupages'} && ($c{'use_fastcgi'} || $c{'use_modperl'}))
    {
#	debug "USING CACHE";
	$ra_data = cache_has("$emu_type/$file") ? cache_read("$emu_type/$file") : cache_store("$emu_type/$file");
    }
    else
    {
	$ra_data = cache_store("$emu_type/$file", 1);
	if ($ra_data eq undef)
	{
	    FatalError("Bad News...","Error: Cannot locate template $emu_type/$file");
	}
    }

    return($ra_data);
}

sub cache_has
{
    my ($citem) = @_;

    exists($dcache{$citem});
}

sub cache_read
{
    my ($citem) = @_;
    $dcache{$citem};
}

sub cache_store
{
    my ($citem, $bnocache) = @_;
    my ($fh, $ra_data,$line);

#    debug "citem is $citem";

#    $fh = new IO::File "<$page_root/iface/$citem" or do { debug "CACHESTORE FAILED: $citem|$bnocache|page_root=$page_root|$!"; return undef };
#    $ra_data = [ $fh->getlines ];
#    $fh->close;

    open (IN, "$page_root/iface/$citem");
    #binmode IN;
    my (@lines);
    while (defined($line = <IN>))
    {
	push(@lines,$line);
    }
    close IN;

    $ra_data = [ @lines ];

#    debug "ra_data = ",join('',@{$ra_data});
    $dcache{$citem} = $ra_data unless($bnocache);
    return($ra_data);
}

# get_var
#
# retrieve a variable from the EMU symbol table if it is there, otherwise
# we eval() it and hope it's within current scope.
sub get_var
{
    my $name = shift;
    my $var;

    no strict 'vars';

    #MM 04/25/99 -- Allow encoding of vars
    my $orig = $name;
    if ($name =~ /(.*)_encode$/)
    {
        $name = $1;
    }

    if (defined($EMU::{"tmp_$name"}))
    {
	$var = $EMU::{"tmp_$name"};
#       debug "(TMP) VAR $name is '$var'";
    }
    elsif (defined($EMU::{"nooneenoo_$name"}))
    {
	$var = $EMU::{"nooneenoo_$name"};
#       debug "(NOONEE) VAR $name is '$var'";
    }
    elsif (defined($c{$name}))
    {
	$var = $c{$name};
    }
    elsif (defined($msg{$name})) #MM 12/5/98
    {
	$var = $msg{$name};
    }
    elsif (defined($userdb{"options.$name"}))
    {
	$var = $userdb{"options.$name"};
    }
    elsif ($query && defined($query->param($name)))
    {
	$var = $query->param($name);
    }
    elsif ($name eq "cache_bust")
    {
	# Added so we can have soemthing that will bust the cache for proxies
	# useful for ad serving...
	$var = time.$$;
    }
    elsif ($name !~ /\./ && $name !~ /:/)
    {   # scalars whose name have a '.' are impossible. Those annoying
        # "Bareword" errors we kept getting all over the place were
        # happening because we were evaling $name like "org.show" or any
        # other string with a '.' in the middle
	$var = eval("\$$name");
    }

    #04/25/99
    if ($orig ne $name)
    {
        $var = private_str($var);
    }
    
    return ($var);
}


# write a temp variable into the EMU symbol table so that
# it can be referenced by EMUcode.
sub write_tmp
{
    my ($var, $val, $nocrlf) = @_;

    add_cleanup("nooneenoo_$var");

    if ($nocrlf && !ref $val) {
        $val =~ s/\r?\n/ /g;
    }


#    debug "wrote tmpvar $var with value '$val'";

    return $EMU::{"nooneenoo_$var"} = $val;
}

sub get_max_messages
{
    # 07/24/01 - Consolidate max_messages setting to one sub
    #    Takes into account both the userdb setting as well as 
    #    the ability for each interface to have its own limit
    #    This allows WAP interfaces to have a limit of 9 msgs per index page
    #    While HTML interfaces have their own limits

    # Default to the user's perferences, or if not set, then the admin's preferences, or our own default
    my $max_messages = $userdb{"options.max_messages"} || $c{"max_messages"} || 15;

    # if the admin has defined a limit, make sure our value is within that limit
    if ($c{"max_messages_limit"} > 0)
    {
	$max_messages = $c{"max_messages_limit"} if ($max_messages > $c{"max_messages_limit"});
    }

    return $max_messages;
}

# do_emucode
#
#
sub do_emucode
{
    my $cmd = shift;
    my $varname;
    my $rest;

    my $uu = $user_name;  #set default user/pass
    my $pp = $password;

#    debug "pp=$pp";

    $multi_interfaces = bool($c{'multi_interfaces'});
    write_tmp("multi_interfaces", $multi_interfaces);

#    debug "cmd is $cmd";

    # endif
    #
    # set the end of an if's scope.
    if ($cmd =~ /^\s* endif \s* \(? .* \)?/x)
    {
#       debug "FOUND ENDIF";

	$EMU::{'private_doif'} = undef;

	return undef;
    }

    if ($cmd =~ /^\s* else \s* \(? .* \)?/x)
    {
	if ($EMU::{'private_doif'} eq undef)
	{
	    # hmm.. syntactical error
	    error "Error in EMUcode on line with $cmd at ", __LINE__;
	    next;
	}

#        debug "FOUND ELSE: ", (!$EMU::{'private_doif'} ? "DOING IT" : "NOT DOING IT");

	# well, to do the else we just need to reverse the if
	$EMU::{'private_doif'} = int(!$EMU::{'private_doif'});

	return undef;
    }

    # when private_doif is not undef and is 0 then we skip lines until
    # we come across an endif statement.
    next if ($EMU::{'private_doif'} ne undef && $EMU::{'private_doif'} == 0);

    # if (BOOL)
    #
    # an if statement, mark that we are inside and if and then continue
    # processing. If we are in and if and the if came through as TRUE
    # then we will do whatever we find until we reach an endif
    if ($cmd =~ /^\s* if \s* \( \s* (.*) \s* \)/x)
    {
#       my $status = !!$1;
	my ($unit, $status);

#        debug "cmd is $cmd";

	$unit = $1;

	$unit =~ s/@/\Q@/g;
#        debug "unit is $unit";

	if (index($unit, "==") != -1)
	{
	    # do a comparison
	    my ($lh, $rh);

	    ($lh, $rh) = split('==', $unit, 2);

	    trim(\$lh);
	    trim(\$rh);

	    #remove quotes.
	    $lh =~ s/^([\"\'])//;
	    $lh =~ s/$1$//;
	    $rh =~ s/^([\"\'])//;
	    $rh =~ s/$1$//;

#           debug "lh=$lh";
#           debug "rh=$rh";

#	    debug "string = return(qq{$lh} eq qq{$rh})";
	    $status = eval("return(qq{$lh} eq qq{$rh})");

#           debug "status=$status";
	}
	elsif (index($unit, "!=") != -1)
	{
	    # do a comparison
	    my ($lh, $rh);

	    ($lh, $rh) = split('!=', $unit, 2);

	    trim(\$lh);
	    trim(\$rh);

	    $lh =~ s/^([\"\'])//;
	    $lh =~ s/$1$//;
	    $rh =~ s/^([\"\'])//;
	    $rh =~ s/$1$//;

#           debug "lh=$lh";
#           debug "rh=$rh";

#           debug "string = return(qq{$lh} ne qq{$rh})";
	    $status = eval("return(qq{$lh} ne qq{$rh})");

#           debug "status=$status";
	}
	else
	{
	    $status = eval("qq{$unit}");
#            debug "status = $status unit=$unit";
	}

	add_cleanup('private_doif');

	if (defined($status) && $status ne "" && $status ne "0") # ne undef && $status != 0)
	{
	    # it was true! Mark that we are in an if.

#           debug "IF STATEMENT ($1) is TRUE";

	    $EMU::{'private_doif'} = 1;
	}
	else
	{
	    # false! set the inif status to 0

#           debug "IF STATEMENT ($1) is FALSE";

	    $EMU::{'private_doif'} = 0;
	}

	return undef;
    }

    if ($cmd =~ /^\s* checked \s* \( (.*) \)/x)
    {
#       my $status = !!$1;
	my ($unit, $status);

#        debug "cmd is $cmd";

	$unit = $1;

	if (index($unit, "==") != -1)
	{
	    # do a comparison
	    my ($lh, $rh);

	    ($lh, $rh) = split('==', $unit, 2);

	    trim(\$lh);
	    trim(\$rh);

	    $lh =~ s/^([\"\'])//;
	    $lh =~ s/$1$//;
	    $rh =~ s/^([\"\'])//;
	    $rh =~ s/$1$//;

#           debug "lh=$lh";
#           debug "rh=$rh";

#           debug "string = return(qq{$lh} eq qq{$rh})";
	    $status = eval("return(qq{$lh} eq qq{$rh})");

	}
	else
	{
	    $status = eval("$unit");
	}

	if (defined($status) && $status ne "" && $status ne "0") # ne undef && $status != 0)
	{
	    return "checked";
	}
	else
	{
	    return "";
	}
    }

    # (checked) if ($cc.show)
    if ($cmd =~ /^\s* \( \s* (.*) \s* \) \s* if \s* \( \s* (.*) \s* \)/x)
    {
	my ($unit, $status);
	my ($result) = $1;

	$unit = $2;
#        debug "cmd is $cmd";
#        debug "unit $unit, result $result";

	if (index($unit, "==") != -1)
	{
	    # do a comparison
	    my ($lh, $rh);

	    ($lh, $rh) = split('==', $unit, 2);

	    trim(\$lh);
	    trim(\$rh);

	    $lh =~ s/^([\"\'])//;
	    $lh =~ s/$1$//;
	    $rh =~ s/^([\"\'])//;
	    $rh =~ s/$1$//;

	    $status = eval("return(qq{$lh} eq qq{$rh})");
	}
	elsif (index($unit, "!=") != -1)
	{
	    # do a comparison
	    my ($lh, $rh);

	    ($lh, $rh) = split('!=', $unit, 2);

	    trim(\$lh);
	    trim(\$rh);

	    $lh =~ s/^([\"\'])//;
	    $lh =~ s/$1$//;
	    $rh =~ s/^([\"\'])//;
	    $rh =~ s/$1$//;

	    $status = eval("return(qq{$lh} ne qq{$rh})");
	}
	else
	{
	    $status = eval("$unit");
	}

	if (defined($status) && $status ne "" && $status ne "0") # ne undef && $status != 0)
	{
	    return $result;
	}
	else
	{
	    return "";
	}
    }

    # for i in @foo

    if ($cmd =~ /^\s* iface_select \s* \( .* \)/x)
    {
	return &get_iface_select_box();
    }

    if ($cmd =~ /^\s* mail_host_select_box \s* \( .* \)/x)
    {
	return &get_mail_host_select_box();
    }

    if ($cmd =~ /^\s* mail_host_input_box \s* \( .* \)/x)
    {
	return &get_mail_host_input_box();
    }

    if ($cmd =~ /^\s* top_image \s* \( .* \)/x)
    {
	show_ad();
	return undef;
    }

    if ($cmd =~ /^\s* load_page_data \s* \( .* \)/x)
    {
	return &load_page_data($1);
    }

#    if ($cmd =~ /^\s* private_data \(? .* \)?/x)
#    {
#        return form_header_private();
#    }

    if ($cmd =~ /^\s* help \( .* \)/x)
    {
	my $type = $prefix;
	my $url = ($type eq "nc" ? $c{'help_url'} . "_nc" : $c{'help_url'});
	my $img_url = $c{'img_url'};

	if ( $type eq "nc" )
	{
	    return qq{<A HREF="$url/index.html">[Help]</A>\n};
	}
	else
	{
	    return qq{<A HREF="$url/index.html"><IMG ALT="[Help]" SRC="$img_url/image/help.gif" BORDER=0></A>};
	}
    }

    if ($cmd =~ /^\s* linkpage \( (.*) \)/x)
    {
	my($match, @params, $url);

	@params = split(',', $1, 3);
	
	# 08/13/98: we can't have them calling the index() function since it's been put out of existance
	$params[0] = "go_index" if ($params[0] eq "index");

	$url = make_url($params[0]);
	
	return qq{<A HREF="$url" $params[2]>$params[1]</A>\n};
    }

    if ($cmd =~ /^\s* showindex \( (.*) \)/x)
    {
	my($match, @params, $url, %extra);

	@params = split(',', $1, 2);

	$extra{"sorttype"} = $params[0];

	$url = make_url("go_index",undef,%extra);
	
	return qq{<A HREF="$url">$params[1]</A>\n};
    }

    if ($cmd =~ /^\s* get_status \(? .* \)?/x)
    {
	return get_status(1);   # print publisher_name part
    }

    if ($cmd =~ /^\s* login_session \(? .* \)?/x)
    {
	return ($qs =~ /LOGIN/i);
    }

    if ($cmd =~ /^\s* print_full_headers \s* \(? .* \)?/x)
    {
	my $str = qq{<TABLE CELLSPACING=1 CELLPADDING=1 BORDER=1 BGCOLOR="WHITE" WIDTH=100%>\n};

	return $str.format_cells(get_var("full_headers"));
    }

    if ($cmd =~ /^\s* print_cells \s* \( .* \)/x)
    {
	return print_cells(get_var("full_headers"));
    }

    if ($cmd =~ /^\s* print_dictionaries \s* \(? .* \)?/x)
    {
	return print_dictionaries(get_var("default"));
    }


    if ($cmd =~ /^\s* print_basic_headers \s* \( \s* (.*) \s* \)/x)
    {
	my ($to, $cc, $from, $subj, $date, $tmp, $extra, $extra2, $img1, $str, $border);

	$to    = get_var("to");
	$cc    = get_var("cc");
	$subj  = get_var("subj");
	$date  = get_var("date");
	$from  = get_var("from");
	
	($extra, $img1, $border) = split(',', $1);

	$tmp = make_url("address", $from);
	$border ||= 0;
	
	$str .= qq{<TABLE CELLSPACING=1 CELLPADDING=1 BORDER=$border BGCOLOR="WHITE" WIDTH=100%>\n};
	$str .= qq{ <TR>\n};
	$str .= qq{  <TD>$FONT_IND <B>From:</B> </FONT></TD>\n};

	if ($img1)
	{
	    $str .= qq{  <TD><B><A HREF="$tmp">$FONT_IND $from </FONT></B></A></TD>\n};
	    $str .= qq{  <TD align=left bgcolor=#0066cc><A HREF="$tmp">$img1</A></TD>\n};
	}
	else
	{
	    $str .= qq{  <TD $extra><B><A HREF="$tmp">$FONT_IND $from </FONT></B></A></TD>\n};
	}

	$str .= qq{ </TR>\n};

	if ($to)
	{
	    $str .= "<TR><TD>$FONT_IND <B>To:</B> </FONT></TD><TD $extra>$FONT_IND <B>$to</B> </FONT></TD></TR>\n";
	}
	if ($cc)
	{
	    $str .= "<TR><TD>$FONT_IND <B>Cc:</B> </FONT></TD><TD $extra>$FONT_IND <B>$cc</B> </FONT></TD></TR>\n";
	}
	if ($date)
	{
	    $str .= "<TR><TD>$FONT_IND <B>Date:</B> </FONT></TD><TD $extra>$FONT_IND <B>$date</B> </FONT></TD></TR>\n";
	}
	if ($subj)
	{
	    $str .= "<TR><TD>$FONT_IND <B>Subject:</B> </FONT></TD><TD $extra>$FONT_IND <B>$subj</B> </FONT></TD></TR>\n";
	}

	return $str;
    }

    if ($cmd =~ /^\s* get_index \s* \( \s* (.*) \s* \)/x)
    {
	my ($total_messages, $indexlist, $total_pages, $next_page, %mailboxes);
	my ($max_messages);

	$max_messages = get_max_messages();

	if ($folder ne $inbox)
	{
	    $uu = $folderdb{"username"} || $uu;
	    # 08/13/98: was being set to $userdb{"folder...password"} || $pp
	    $pp = $folderdb{"password"} || $pp;
	}

	# pass the parameters along
	($total_messages, $indexlist) = make_msg_index($max_messages, $1);

	write_tmp("total_messages",($total_messages - 1) );
	
#	debug "total_messages=$total_messages  max_messages=$max_messages";

#	if ( ($total_messages > ($max_messages) ) && !($query->param('narrow')) )
	if ( $total_messages > $max_messages )
	{       
	    # Make the total pages an integer
	    $total_pages = ($total_messages/($max_messages));

	    if (int($total_pages) != $total_pages)  
	    {
		$total_pages = int(++$total_pages);
	    }
#            debug "folder_page $v{$folder.'_page'}";
            my $this_page;
            $v{$folder."_page"} = $total_pages if ($v{$folder."_page"} > $total_pages);
	    if ($v{$folder."_page"} >= 1)
	    {
		$next_page = ($v{$folder."_page"}+1)%($total_pages+1);
                $this_page = $v{$folder."_page"};
	    }
	    else
	    {
		$next_page = 2;
                $this_page = 1;
	    }
	    
	    $next_page ||= 1;
	    
#	    debug "total_pages=$total_pages";
#	    debug "next_page=$next_page";
#            debug "this_page $this_page";
	    write_tmp("moremsgs", 1); # so this if in the HTML falls through
	    write_tmp("next_page", $next_page, 1);
	    write_tmp("this_page", $this_page, 1);
	    write_tmp("prev_page", $this_page - 1, 1) if ($this_page > 1);
	    write_tmp("total_pages", $total_pages, 1);

	}
	else
	{
	    write_tmp("next_page", 0);
	    write_tmp("moremsgs", 0);
	    write_tmp("total_pages", 0);
            write_tmp("this_page", 1);
	    $v{$folder."_page"} = 1; # public var showing folder page
	} 

	write_tmp("nomessages", !($total_messages - 1));    

	return $indexlist;
    }

    if ($cmd =~ /^\s* attachments \s* \(? .* \)?/x)
    {
#	return get_var("here_atts") || $msg{'MSG_ATTFileNone'};
        return print_attachs();
    } 

    if ($cmd =~ /^\s* dump \s* \( \s* (.*) \s* \)/x)
    {
	my $file = basename($1);
	my $data;
	
	$file = "$page_root/$file";

	if (-e $file)
	{
	    local ($/);
	    open(IN, "<$file") || debug "EMUcode: dump $1 - $!";
	    # binmode  IN;
	    
	    $data = <IN>;       # swallowed
	    
	    close IN;

	    $data .= "\n<P>\n";
	}

	return $data;
    }

    if ($cmd =~ /^\s* print_filters \s* \(? .* \)?/x)
    {
	print_filters();
	return undef;
    }

    if ($cmd =~ /^\s* print_emufiles \s* \( \s* (.*) \s* \)/x)
    {
	print_emufiles(!!$1);
	return undef;
    }

    if ($cmd =~ /^\s* print_index_mailboxes \s* \(? .* \)?/x)
    {
	my (@folders, $f);

	@folders = grep (/^mailboxes\./, keys %userdb);
	@folders = grep (!/^mailboxes\.(?:p|r):/, @folders );
	
	# 07/24/98: this xx is so that the 2 characters chopped off don't mess with the folder's title
	push(@folders, "xx" . $msg{'MSG_MBoxNone'}) if (@folders < 1);

	foreach $f (@folders)
	{
	    $f = substr($f, 2, $c{'folder_namelen'} + 2);       # folder names are limited to 18 chars
	    if ($f eq $folder)
	    {
		print qq{<OPTION VALUE="$f" SELECTED>$f\n};
	    }
	    else
	    {
		print qq{<OPTION VALUE="$f">$f\n};
	    }
	}

	return undef;
    }

    if ($cmd =~ /^\s* print_index_folders \s* \(? .* \)?/x)
    {
	debug "PRINT_INDEX FOLDERS CALLED!!!!!!!!";
    }
    
    if ($cmd =~ /^\s* print_folders \s* \( \s* (.*) \s* \)/x)
    {
        debug "print folders";
	return print_folders(split(/,/, $1));
    }

    if ($cmd =~ /^\s* print_folders2 \s* \( \s* (.*) \s* \)/x)
    {
	return print_folders2($1);
    }

    if ($cmd =~ /^\s* print_ldap_hosts \s* \(? .* \)?/x)
    {
        return print_ldap_hosts();
    }

    if ($cmd =~ /^\s* print_nextpage_options \s* \(? .* \)?/x)
    {
	my($page, $total_pages, $next_page);

        if (get_var("load_page") eq "msgindex.html") {
            $total_pages = get_var("total_pages");
            $next_page = get_var("next_page");
            debug "next_page $next_page  total $total_pages";
        }
        else {
            # doing ldap_jump
            $total_pages = get_var("total_ldap_pages");
            $next_page = get_var("next_ldap_page");
            debug "next_page $next_page  total $total_pages (ldap)";
        }

	# 09/25/98 - RMK added for translation
	my $PAGE = $msg{'Next-Page-Title'} || "Page";
	my $OF = $msg{'Next-Page-OF'} || "of";
        my $selected;
	for ($page = 1; $page <= $total_pages; $page++)
	{
            if ($page == $next_page) {
                $selected = "SELECTED";
            }
            else {
                $selected = "";
            }
	    print qq{<OPTION VALUE="$page" $selected>$PAGE $page $OF $total_pages\n};
	}
	
	return undef;
    }

    if ($cmd =~ /^\s* print_emufiles_compose \s* \(? .* \)?/x)
    {
	print_emufiles_compose();
	return undef;
    }
    
    if ($cmd =~ /^\s* print_postponed \s* \(? .* \)?/x)
    {
	my (@files);

	debug "PRINTING POSTPONED MESSAGES";

	opendir DIR, "$homedir/files";
	@files = grep ( /^[0-9a-f]{32}$/, readdir DIR);
	closedir DIR;
	
	# map the filenames correctly
	map { $_ .= substr(":" . get_heldmsg_name($_, $userdb{"postponed.$_"}), 0, 30) } @files;
                                                         	
	foreach my $thefile (@files)
	{
            my ($fname, $fdate, $fsubj) = split(':', $thefile);
	    debug "file is $thefile, date is $fdate, subj is $fsubj";

	    if ($thefile =~ /^([0-9a-f]{32}):(.*)/i)
	    {
		print qq{   <OPTION VALUE="$1">$2\n};
		next;
	    }
	    print qq{   <OPTION VALUE="$fname">$fdate:$fsubj\n};
	}
	
	return undef;
    }

    if ($cmd =~ /^\s* print_message \s* \(? .* \)?/x)
    {
	return get_var("data") || $query->param('message');
    }

    if ($cmd =~ /^\s* print_priority \s* \(? .* \)?/x)
    {
        my ($parray, $phash) = get_priority_data();
        
        my @pri2 = keys %$phash;
        my @pri1 = values %$phash;

	my ($str, $pri);
	$pri = $query->param('priority') || "3 ($msg{'MSG_Priority_Normal'})";
	
        my $index=0;
	foreach my $thepri (@pri1) {
	    if ($pri eq $thepri)
	    {
		$str .= qq{<OPTION VALUE="$pri2[$index]" SELECTED>\u$thepri\n};
                $index++;
		next;
	    }
	    $str .= qq{<OPTION VALUE="$pri2[$index]">\u$thepri\n} if (/\(..+\)$/);
            $index++;
	}

	return $str;
    }

    if ($cmd =~ /^\s* ihelp \s* \( \s* (.*) \s* \)/x)
    {
	return get_ihelp(split(',', $1, 3));
    }

    if ($cmd =~ /^\s* print_addresses \s* \( .* \)/x)
    {
	print_addresses(split(',', $1)) || return $msg{'MSG_AddressBookEmpty'};
	return undef;
    }

    if ($cmd =~ /^\s* print_addrbook \s* \(? .* \)?/x)
    {
        return get_addrstr();
    }

    # var VARNAME = EMUCODE  --  Store the result of EMUCODE in a temp var named VARNAME
    #
    # allocate a variable: (var foo = eval(return "moooh"))
    if ($cmd =~ /^\s* var \s* (\w+) (.*)/x)
    {
	debug "FOUND A VAR STATEMENT: storing $1 with $2";
	$varname = $1;
	$rest    = $2;
	if ($rest =~ s/\s* = \s* (.*) \s*//x)
	{
	    add_cleanup("tmp_$varname"); # so we remember to clear it
	    $EMU::{"tmp_$varname"} = do_emucode($1);
	    debug "EMU::{tmp_$varname} = ", $EMU::{"tmp_$varname"};
	}
    }

    # value VARNAME  -- Retrieve the value of a stored EMUcode variable
    #
    # retrieve a value: (value varname)
    if ($cmd =~ /^\s* value \s* ([^ ]*) \s*/x)
    {
	debug "FOUND A VALUE STATEMENT: retrieving var EMU::{tmp_$1}=", $EMU::{"tmp_$1"};

	return $EMU::{"tmp_$1"} || undef;
    }

    # 10/02/98 - RMK added execute capability
    if ($cmd =~ /^\s* execute \s* \(\" (.*) \"\) \s*/x)
    {
	my $execute = $1;
	if (-x $execute) {
	    $cmd = `$execute`;
	    $cmd =~ s/content-type:\s*text\/html//i;
	}
	else {
	    $cmd = "";
	}
    }
    return $cmd;
}

sub load_page_data
{
    my ($fold) = @_;

    $fold = $fold || $folder || $inbox;

    my ($total_messages) = get_total_msgs($fold);
    my $max_messages = get_max_messages();

    my ($start,$finish);

#    if ($total_messages > $max_messages && !($query->param('narrow')))
    if ($total_messages > $max_messages)
    {
        my ($next_page, $total_pages);
#        debug "it is :".$v{$fold."_page"};

        $start = ( ($v{$fold."_page"} - 1) * $max_messages );
        $finish = $start + $max_messages;

#        debug "start=$start  finish=$finish  total=$total_messages";

        $finish = ($total_messages) if ($finish > ($total_messages));
        $finish--;

        $total_pages = ceil($total_messages / $max_messages);

#        debug "fold_page $v{$fold.'_page'}";
        $v{$folder."_page"} = $total_pages if ($v{$folder."_page"} > $total_pages);
        my $this_page;
        if ($v{$fold."_page"} >= 1)
        {
            # default to 1
            $next_page = (($v{"$fold\_page"} + 1) % ($total_pages + 1))  ||  1 ;
            $this_page = $v{$fold."_page"};
        }
        else
        {
            $next_page = 2;
            $this_page = 1;
        }

#        debug "total_pages=$total_pages  next_page=$next_page";
#        debug "this_page $this_page";

        write_tmp("moremsgs", 1);
        write_tmp("next_page", $next_page);
        write_tmp("this_page", $this_page);
        write_tmp("prev_page", $this_page - 1) if ($this_page > 1);
        write_tmp("total_pages", $total_pages);
#        $v{$fold."_page"} = ($next_page-1 || 1);
    }

    return undef;
}

#MM: 11/28/98 Multiple Interfaces from login
sub get_iface_select_box
{
    my ($html,$type,$iface);
    my (@ifaces) = split(/\s|,/,$c{"ifaces"});

    if (scalar(@ifaces) > 1)
    {
	$type = $query->param('type') || $emu_type || $emu_cookies{'emu_type'} || $c{"default_interface"};
	$html = qq {<select name="type">};

	foreach $iface (@ifaces)
	{
	    if ($iface ne $type)
	    {
		$html .= qq{<option>$iface\n};
	    }
	    else
	    {
		$html .= qq{<option selected>$iface\n};
	    }
	}
	$html .= "</select>";
    }
    elsif (scalar(@ifaces) == 1)
    {
	$type = pop(@ifaces);
	$html = qq{<input type="hidden" name="type" value="$type">};
    }
    else
    {
	$type = $c{"default_interface"};
	$html = qq{<input type="hidden" name="type" value="$type">};
    }

    return $html;
}

# add_cleanup
#
# add a variable for cleanup into the cleanupvars array
sub add_cleanup
{
    push @{$EMU::{'cleanupvars'}}, shift();
}

sub addrly { lc($a) cmp lc($b); }
sub alpha { lc($a) cmp lc($b); }


#__DATA__


sub get_mail_host_input_box
{
    my ($html,$hostname);

    # Do we want to put both a select box and an input box?
    return if ($c{"mail_hosts"} ne "");

    if ($c{"mail_host_input_box"})
    {
        my $box_size = $c{"mail_host_input_box_length"} || 30;
        my $style = $c{"mail_host_input_box_style"};
        $hostname = $query->param('hostname') || $emu_cookies{'host'};

        if ($emu_cookies{"noInfo"} || $hostname =~ /\@/) {
            $hostname = "";
        }

	$html = qq{ <input type="text" name="hostname" value="$hostname" size=$box_size style=$style>};
    }

    return $html;
}

sub get_mail_host_select_box
{
    # Print a select box of desired hmail_hosts that the user should chose from on login...
    my ($html,@hosts,$hostname);

    (@hosts) = split(/\s|\,/,$c{"mail_hosts"});
    if (scalar(@hosts))
    {
	# We have a list of hosts to make into a select box
	$hostname = $query->param('hostname') || $emu_cookies{'host'};
	$html = qq {<select name="hostname">};
	$html .= "<option value=\"\">".$msg{"MSG_SelectHost"}."\n";

	foreach my $host (@hosts)
	{
	    if (lc($host) ne lc($hostname))
	    {
		$html .= qq{<option>$host\n};
	    }
	    else
	    {
		$html .= qq{<option selected>$host\n};
	    }
	}
	$html .= "</select>";
	if ($c{"mail_host_input_box"})
	{
	    $html .= "<BR>";
	}
    }

    return $html;
}

sub dump_data
{
    my $d;

    no strict 'refs';

    open(OUT, ">$page_root/emudump");
    print OUT "====== EMU Symbol Table ======\n";
    $d = new Data::Dumper [map { ${"EMU::$_"} } keys %EMU::], [keys %EMU::];
    print OUT $d->Dump;

#    print OUT "\n\n====== main Symbol Table ======\n";
#    $d = new Data::Dumper [values %main::], [keys %main::];
#    print OUT $d->Dump;
    close OUT;

    return 1;
}

sub debug
{
    return unless $EMU_DEBUG;

    my ($line, $subname) = (caller(1))[2,3];
    my $now = localtime;
    my $data = join('', @_);
    my $ra = $ENV{"REMOTE_ADDR"};
    my $debug_root = $c{'debug_path'} || $page_root;
    
    if ( $c{'debug_users'} && $homedir )
    {
    	# we should do this only once!
    	for my $user ( split(/\s|,\s*/, $c{'debug_users'}) )
    	{
    		trim(\$user);
    		if (
    			$user !~ /@/ && $user eq $popuser # user without hostname, global
    		||
    			$user =~ /@/ && $user eq "$popuser\@$pophost" # user is email
    		)
    		{
    			$debug_root = $homedir;
    			last;
    		}
    	}
	}

    # default max size to 100 meg. 
    my $maxsize = $c{debug_max_size} || 100 * 1024 * 1024;

    $subname =~ s/^EMU:://;

    my $msg = $c{debug_format} || '[%l] %s: %m (%d: - %h PID %p)';

    $msg =~ s/%l/$line/g;
    $msg =~ s/%s/$subname/g;
    $msg =~ s/%m/$data/g;
    $msg =~ s/%d/$now/g;
    $msg =~ s/%h/$ra/g;
    $msg =~ s/%p/$$/g;
    $msg =~ s/\\n/\n/g;

    if ($c{"debug_hostname"} && $this_host) {
        # ensure we have no writing problems
        unlink "$debug_root/$this_host.emudebug" if (-s "$debug_root/$this_host.emudebug" > $maxsize);
        open OUT, ">>$debug_root/$this_host.emudebug";
        chmod(0755, "$debug_root/$this_host.emudebug");
    }
    else {
        # ensure we have no writing problems
        unlink "$debug_root/emudebug" if (-s "$debug_root/emudebug" > $maxsize);
        open OUT, ">>$debug_root/emudebug";
        chmod(0755, "$debug_root/emudebug");
    }

	
    # binmode  OUT;
    print OUT $msg,"\n";
    close OUT;
}

# Get our current time zone allow the user to specify this.
sub get_timezone
{   
    return $userdb{"options.timezone"} || $c{'timezone'} || 'GMT';
}

# sub get_date
#
# This function computes and returns a nice date string
#
sub get_date
{
    my ($date, $bypass_tz, $dont_translate, $be_abbr_gmt, $dont_process_month_n_wday) = @_;
    my ($tzname, $be_abbrtz);
    my @tztime = ();
    if (!$bypass_tz)
    {
    	# if this is not valid (in terms of Time::Zones) gmt we assume it to be GMT
    	my $gmt = get_timezone() || EMU::Time::Zones::tzabbr2key($c{timezone}) || 'GMT';
    	
    	my $gmt_lo = lc $gmt; 	
    	my $is_abbr_gmt = EMU::Time::Zones::isAbbreviatedUsually( $gmt_lo );

    	$be_abbrtz = $is_abbr_gmt && $be_abbr_gmt;
    	
   		@tztime = EMU::Time::Zones::tztime($gmt, $date || time); @tztime = gmtime($date || time) unless (scalar @tztime);
   		if ($be_abbrtz)
   		{
			$tzname = EMU::Time::Zones::tzabbr($gmt, $tztime[9]) || 'GMT';
   		} else
   		{
   			$tzname = EMU::Time::Zones::tzcode($gmt, $tztime[9]) || '+0000';
   		}
    	debug "TZ: $tzname";
    }
    else {
    	@tztime = gmtime($date || time);
        $tzname = ($be_abbrtz) ? 'GMT' : '+0000';
    }
	
    my ($ss, $mm, $hh, $day, $month, $year, $wday, $mday) = @tztime[0, 1, 2, 3, 4, 5, 6];
    $year  += 1900;
    
    my (@months,@days); #added ability to customize the names of days/months

	unless ( $dont_process_month_n_wday )
	{
    	@months = qw(Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec);
    	@months = split(/\s/,$msg{"Month_Names"}) if (!$dont_translate && $msg{"Month_Names"});
    	$month = $months[$month];
    }
    
    unless ( $dont_process_month_n_wday )
    {
	    @days = qw(Mon Tue Wed Thu Fri Sat Sun);
	    @days = split(/\s/,$msg{"Day_Names"}) if (!$dont_translate && $msg{"Day_Names"});
	    $wday  = @days[($wday-1)];
	}

	# debug tz_name($tzoff);

    # 24h/12h time modifier
    my $ampm = '';
    if (bool($c{'ampm_timeformat'}) && !$dont_translate)
    {
  		$hh += 0;
  		if ($hh > 12)
  		{
	  		$hh -= 12; $ampm = ' pm';
  		} elsif ($hh == 12)
  		{
  			$ampm = ' pm';
  		} elsif ($hh == 0)
  		{
  			$hh = 12; $ampm = ' am';
  		} else
  		{
  			$ampm = ' am';
  		}
    }
    
    # if we want an array we return (weekday, month, year) otherwise a formatted string with full date and time
    return wantarray() ? ($wday, $day, $month, $year, $hh, $mm, $ss, $ampm, $tzname)
	: sprintf("$wday, %02d $month $year $hh:%02d:%02d$ampm $tzname", $day, $mm, $ss);
}

sub error
{
    my ($line, $subname) = (caller(1))[2,3];
    my $error_root = $c{'debug_path'} || $page_root;

    debug(@_, " [$line,$subname]");

    $subname =~ s/^EMU:://;
    open(OUT, ">>$error_root/emuerror");
    print OUT "[", scalar(get_date()), " $user_name  $line] $subname: ",join('',@_),"\n";
    close OUT;

    # yumm yumm
#    dumpstack();
}


## FETCH ROUTINES ##

# the addressbook is stored in a has. the index is the person's nickname, and
# the value is their fullname:email
sub address
{
    my ($noparam) = @_;
    my ($from, $full, $addr, $nick, $nickname, $fullname, $address, $org, $phone, $desig);
    my (@addrs);

    $from = $query->param('variable') unless ($noparam);
    $from =~ s/^.*\.html$//;

    if ($from)
    {
	debug "has a from variable ($from), filling in part of the addressbook";

	$from = reverse_html($from);
#	$from =~ s/&lt;/</g;
#	$from =~ s/&gt;/>/g;
	
	($full,$addr) = addr_split($from);
	debug "full=$full  addr=$addr";

	$addr =~ s/[><]//g;
	$full =~ s/\"//g;
	
	$nick = substr($addr,0,index($addr,"@") || (split(/\s+/,$full,2))[0]);
        debug "nick $nick";
    }

    if ($query->param('email') && $query->param('nick') && $query->param('full')) {
        write_tmp("showentries", 1);
        $addr = $query->param('email');
        $nick = $query->param('nick');
        $full = $query->param('full');
        debug "filling in email=$addr, nick=$nick, full=$full";
    }

    unless ($query->param('save.x'))
    {
	$full = $full || $query->param('full');
    }

    @addrs = grep(/^addresses\./, keys %userdb);

    $full=$nick if ($full eq ''); #01.23.2003 Alex

    debug "nick is $nick, full is $full, addr is $addr";

    if ($from && $nick && $addr) {
        if (address_exists($nick)) {
	    set_status(convert($msg{'MSG_NicknameExists'}, $nick, $full, $addr));
        }
        else {
            $userdb{"addresses.$nick"} = "$addr:$full";
	    set_status(convert($msg{'MSG_AddressAdded'}, $nick, $addr));
        }
    }

    if ($nick || $full || $addr) {
        write_tmp("showentries", 1);
    }
    else {
        write_tmp("showentries", 0);
    }

    write_tmp("i", scalar(@addrs) || 0, 1);
    write_tmp("nick", $nick || "", 1);
    write_tmp("full", $full || "", 1);
    write_tmp("addr", $addr || "", 1);
    write_tmp("have_addresses", !!get_var("i")); # mooh
    write_tmp("status", $status, 1);

    if ($licensed{"custom_addrbook"}) {
        my @addrbk = keys %AddressbookDefs::addrbook_fields;
        foreach my $entry (@addrbk) {
            write_tmp($entry, $c{$entry});
        }
    }

    load_page("address.html");
}

sub print_addresses
{
    my ($allcells, $cell1, $cell2, $cell3) = @_;

    my(@addrs, $i);
    my ($nickname, $fullname, $address);

    @addrs = grep(/^addresses\./, keys %userdb);
    $i     = scalar(@addrs);            # get the new index
    
    # only print out current entries thingie if there are any current entries
    if (@addrs)
    {   
	@addrs = sort alpha @addrs;
	
	for ($i = 0; $i < @addrs; $i++)
	{
	    # split the data into its parts
	    $nickname = substr($addrs[$i], length("addresses."));

	    ($address, $fullname) = split(/:/, $userdb{$addrs[$i]});
	    
	    $nickname =~ s/[><\"]//g;
	    $fullname =~ s/[><\"]//g;
	    $address  =~ s/[><\n\r\"]//g;
	    
	    # generate each addressbook line
	    print qq{  <TR>\n};
	    print qq{   <TD $allcells align=center><INPUT TYPE="CHECKBOX" NAME="d$i"></TD>\n};
	    print qq{   <TD $allcells $cell1><INPUT NAME="n$i" VALUE="$nickname" SIZE=20></TD>\n};
	    print qq{   <TD $allcells $cell2><INPUT NAME="f$i" VALUE="$fullname" SIZE=20></TD>\n};
	    print qq{   <TD $allcells $cell3><INPUT NAME="e$i" VALUE="$address" SIZE=20></TD>\n};
	    print qq{  </TR>\n};
	}
    }
    else
    {
	return 0;
    }

#    dbmclose %userdb;
}


# address_parse
#
# parse the data passed from the address page
#
sub address_parse
{
    my ($orig, $nick, $full, $email, $designation, $org, $phone, $fax, $i);
    my $doing_ldap=0;

    if ($query->param('showentries') == 1) {
        write_tmp("showentries", 1); 
    }
    else {
        write_tmp("showentries", 0);
    }

    $nick  = $query->param('nick');
    $full  = $query->param('full');
    $email = $query->param('email');
    $email =~ s/://g;
    $nick  =~ s/://g;

    my $val = "$email:$full";

    my @addrbk = ();

    # Now let's process user-definable addressbook fields, if any
    if ($licensed{"custom_addrbook"}) {
        @addrbk = keys %AddressbookDefs::addrbook_fields;

        # differentiate between addrbook_1 and addrbook_01
        my $format = scalar(@addrbk) > 10 ? "addrbook_%02d" : "addrbook_%d";

        for (my $i=1; $i<=scalar(@addrbk); $i++) {
            my $entry = sprintf($format,$i);
            debug "$entry is ".$query->param($entry);
            $entry = $query->param($entry);
            $entry =~ s/://g;
            $val .= ":$entry";
        }
    }

    $orig = $query->param("orig");
    debug "val is $val orig is $orig";

    my $exists = address_exists($nick);

    if ($nick && (!$orig && $exists) ||
            ($orig && $orig ne $nick && $exists)) {
	set_status(convert($msg{'MSG_NicknameExists'}, $nick, $full, $email));
	return address();
    }
    elsif ($nick)
    {
	# add the new address
#	$nick = lc($nick);

	$userdb{"addresses.$nick"} = $val;
debug "setting nick $nick";
        # take care of removing older one if changing the nick
        if ($orig && $orig ne $nick) {
            delete $userdb{"addresses.$orig"};
        }
    }

    #04/25/99 - MM Allow updating of single addressbook entries
    my $update = $query->param("update") || 0;

    # perform edits on any of the current addresses
    # RMK 01/30/99 added processing of hidden original nicks
    for ($i = $update; defined($orig = $query->param("orig$i")); $i++)
    {
        debug "processing orig $i $orig";

	if ($query->param("d$i")) # "delete" it
	{
	    debug "Deleting entry $i: $orig";
	    
	    my $email=$userdb{"addresses.$orig"}; #01.27.2003 Alex
            $email=~ s/^(.*?):(.*?)$/$1/g;
	    my $nick=$2;
	    $nick=~ s/://gs;

	    my @groups=();
            @groups=grep(/^addressgroup\./, keys %userdb);
            foreach my $ind (@groups){
              $userdb{"$ind"}=~ s/((^|)'$nick'\|\|$email(:|$))//g;
	    }

	    delete $userdb{"addresses.$orig"};
	    next;
	}

	$email = $query->param("e$i");
	$email =~ s/://g;

	$full  = $query->param("f$i");

        $nick = $query->param("n$i");
	$nick  =~ s/[:\@]//g;

        $val = "$email:$full";

        for (my $j=1; $j<=scalar(@addrbk); $j++) {
            my $entry = "addrbook_$j$i";
            $entry = $query->param($entry);
            $entry =~ s/://g;
            $val .= ":$entry";
        }

        debug "val $val";
	# make the nickname default to the user's name
	$nick = substr($email,0,index($email,"@")) if (!$nick && index($email, "@"));
	$nick  = lc($nick);

	if ( (!$nick || !$email) || ($nick =~ /^\s*$/ || $email =~ /^\s*$/))
	{
	    debug "Missing a nickname or an email: nick=$nick  email=$email";
	    set_status($msg{'MSG_AddressMissing'});
	    next;
	}

	debug "Putting to addressbook: $nick = $val";

        # RMK 01/30/99 check for differing original/nick
        if ($orig ne $nick) {
            # if they're different then delete the previous entry
	    delete $userdb{"addresses.$orig"};
        }

        # now update the db
	$userdb{"addresses.$nick"} = $val;
    }

    set_status($msg{'MSG_AddressSaved'});

    return address(1);
}

# addr_split
#
# This function will split the given field into a list consisting of the Full Name,
# the E-mail Address and the Comment.  So if you gave the function this data:
#
#   "EMU Mail" <emu@emumail.com> (Ooga Booga)
#
# It would return a list consiting of: ("EMU Mail", "emu@emumail.com", "Ooga Booga")
#
sub addr_split
{
    my $ob;
    my $phrase="";
    my $address="";
    my $comment="";

#    load_module("Mail::Address");

    if (@_ > 1)
    {
        my @arr;
                                                                                        foreach my $theaddr (@_)
        {
            debug "parsing $theaddr";
            ($ob) = Mail::Address->parse($theaddr);
            if ($ob) {
                $address = $ob->address();
            }
            else {
                $address = "";
            }
            push @arr, $address;
        }

        return @arr;
    }                                                                               else
    {
        my ($field) = @_;

        debug "parsing $field";
        ($ob) = Mail::Address->parse($field);
        debug ("Unable to parse address $field") unless($ob);

        $phrase = $ob->phrase() if ($ob);
        $address = $ob->address() if ($ob);
        $comment = $ob->comment() if ($ob);

        return ($phrase, $address, $comment);
    }
}


sub del
{
 #Determine the username, password, protocol to delete a message
    my ($uid, $no_del_cache, $del_from, $dont_print) = @_;
    my @messages = @{$uid};
    my ($u,$p,$host);

    $uid = $messages[0];

    $v{"wait_interval"} = get_wait_interval($#messages+1) if ($#messages > 0);

    my ($fold) = $del_from || $folderdb{"$uid:folder"};
    my $index=-1;

    debug "F is $fold with U of $uid";

    if (!$mailloc) {
        ($u,$p,$host) = get_folder_credentials($fold);
        debug "U is $u and P is $p";
        debug "protocol is ".$userdb{"folder:$fold:protocol"};
    }

    $v{"wait_count"}++ if (print_progress_new() && $v{"wait_count"} == 0);

    #Delete it from the server
    if ($userdb{"folder:$fold:protocol"} =~ /imap/i || (!$userdb{"folder:$fold:external"} && ($c{"pure_imap"} || ($protocol =~ /imap/i))) )
    {
	del_msg_imap("$u\@$host",$p,$fold,\@messages,$dont_print);
    }
    elsif ($userdb{"folder:$fold:protocol"} =~ /pop/i && !$mailloc) {
        # If we're not syncing, flag this message as 'deleted' so it's not 
        # downloaded again.
        if ($userdb{"options.DontsynchronizePOP"}) {
            debug "Adding @messages to 'deleted' list";
            my @deleted = split(/:/, $folderdb{"deleted"});
            push(@deleted, @messages);
            $folderdb{"deleted"} = join(':', @deleted);
        } else {
            ($u, $host) = map_mailserver($u, $host, $fold);
            $index = del_msg_pop($u,$p,$host,\@messages,$fold,$dont_print);
        }
    }   

    # Cleanup local copy of message
    debug "don't delete local file? $no_del_cache";
    &del_local_msg(\@messages) unless ($no_del_cache);

    return $index;
}


sub store_messages {
    my ($msgs, $fold) = @_;
    my $dir = "folders";
    my $messages = join(':', @{$msgs});
    my %folddb;

    if ($fold =~ /:/) {
        $dir = "folders-ordered";
        $fold =~ s/://;
        # when doing folders-ordered delete an existing file
        unlink "$homedir/$dir/$fold" if (-e "$homedir/$dir/$fold");
    }
    debug "storing ". scalar(@{$msgs})." messages into $dir/$fold";

    if ($folder ne $fold) {
        if ( $ELocks->lock_create("$homedir/$dir/$fold", \%folddb, {mode => 'write', nb => 1}) )
        {
        	tie %folddb, $db_package, "$homedir/$dir/$fold", O_CREAT|O_RDWR, 0660;
        	$folddb{"messages"} = $messages;
#        	debug "set messages to $messages";
        	untie %folddb;
        	$ELocks->lock_remove(\%folddb);
        }
    }
    else {
        $folderdb{"messages"} = $messages;
#        debug "set messages to $messages";
    }
}


sub get_messages {
    my ($msgs, $fold) = @_;
    my $dir = "folders";
    my ($line);
    my ($lines) = 0;

    @{$msgs} = ();

    debug "getting messages for $fold";
    if ($fold =~ /:/) {
        $dir = "folders-ordered";
        $fold =~ s/://;
    }

    return 0 if (!-e "$homedir/$dir/$fold" || -s "$homedir/$dir/$fold" == 0);

    open (MSGS, "$homedir/$dir/$fold") || debug "Can't open $homedir/$dir/$fold!: $!";
    # binmode  MSGS;

    while ($line = scalar(<MSGS>)) {
        ${$msgs}[$lines++] = $line;
    }
    close MSGS;

    debug " total ". scalar(@{$msgs});
    return scalar(@{$msgs});
}


sub del_local_msg
{
 #Cleans up local databases, removing $uid
    my ($uid) = @_;
    my %delmsgs = ();
    my $key;
    my @msgs = @{$uid};

    foreach $uid (@msgs) {
        $delmsgs{$uid} = 1;
        del_from_local($uid, 1);
    }

    my @newmsgs;
    foreach my $themsg (split(/:/, $folderdb{"messages"})) {
        push(@newmsgs, $themsg) if (!exists($delmsgs{$themsg}));
    }

    $folderdb{"messages"} = join(':', @newmsgs);
#    debug "set messages to ".$folderdb{"messages"};
    
    return 1;
}


sub del_msg_imap
{
 #Delete a message from an IMAP server
    my ($u,$p,$foldorig,$uid,$dont_print) = @_;
    my ($fold_validity, $fold);
    my ($user, $host) = map_mailserver($u, "", $foldorig);
    my @msgs = @{$uid};

    debug "u: $u user: $user host: $host fold: $foldorig uid: $uid";


    my $success;
    if (ref $pop ne 'EMU::IMAP'   || 
            $pop->{user} ne $user || 
            ($pop->{"read_only"}) || 
            $pop->{host} ne $host) {
        ($success,$host,$user) = do_login_sequence("imap",$user,
                                                   $p,$host,
                                                   $foldorig,0);
        return undef if (!$success);
#        &do_imap_login($user,$p,$host,$foldorig) || return undef;
    }

    if ($userdb{"folder:$foldorig:external"}) {
       debug "$foldorig is external! Let \$foldorig be 'INBOX' ";
       $fold_validity = &get_folder_validity(get_fold_and_prefix($foldorig));
       debug "folder validity ($foldorig): $fold_validity ;";
      $fold = 'INBOX';
    } else {
       debug "'$foldorig' is NOT external!";
       $fold = get_fold_and_prefix($foldorig);
       $fold_validity = &get_folder_validity($fold);
       debug "Let \$fold be $fold ; folder validity: $fold_validity ;";
    }

    if ($pop->{folder} ne $fold) {
        $pop->select($fold);
    }

    my ($this_one);
    my $num_msgs = scalar(@msgs);
    $v{"wait_interval"} = get_wait_interval($num_msgs) if (!$v{"wait_interval"});
    debug "wait interval ".$v{"wait_interval"};

    foreach (@msgs) {

      WAITSCREEN:
        {
            last if ($#msgs <= 0);

            print_progress_new(0);
            if ($v{"wait_count"}++ % $v{"wait_interval"} == 0) {
                $v{"wait_action"} = convert($msg{"WAIT_Deleted"}, 
                                            $v{"wait_count"});
                debug "wait_count ".$v{"wait_count"};
            }
        }

        $this_one = $_;

        $this_one =~ s/^$fold_validity//; #get rid of validity junk

        $pop->delete_uid($this_one);
    }

}


sub search_digest {
    my ($digest, $nouidl, $force_uids) = @_;
    my ($ra_header, $total, $index1, $index2);
    my %uids = reverse %poplist unless ($nouidl);

    debug "looking for $digest";
    # This sub used when the digest doesnt match the index we thought
    # was correct
    if ($nouidl) {

        # No uidl is way too slow since we have to be matching up digests.
        # to improve, we'll save an in-memory hash the first time around
        if ($force_uids && !$nouidl_list{initialized}) {
            debug "re-process uids from server";

            # indicate we're initializing it
            $nouidl_list{initialized} = 1;

            # let's fill it in first time around
            $total = $index1 = ($pop->popstat)[0];

            for (; $index1 > 0; $index1--) {
                $ra_header = $pop->top($index1, 0);
                $ra_header = md5_lines($ra_header);
                $nouidl_list{$ra_header} = $index1;
            }

        }

        else {
            initialize_nouidl_list() if (!$nouidl_list{initialized});
        }

        if (!$nouidl_list{$digest}) {
            debug "not found!" 
        }
        else {
            # this is kinda crazy... but with nouidl lets make absolutely
            # sure we're getting at the correct message
            $ra_header = $pop->top($nouidl_list{$digest}, 0);
            $ra_header = md5_lines($ra_header);

            if ($ra_header ne $digest) {
                debug "MISMATCH in verifying digest! $ra_header, $digest";
                return undef;
            }
        }

        # with a list, simply return whether in list or not
        return $nouidl_list{$digest};
    }
    else {

#        $ra_header = $pop->uidl;
#        %uids = reverse %$ra_header;
#        debug "not in cache, downloading uid list. UID should be digest $digest";
        debug "decode = ".decode2($digest);
        if (exists($uids{decode2($digest)})) {
            debug "returning $uids{decode2($digest)}";
            return $uids{decode2($digest)};
        }
    }

    debug "returning 0";
    return 0;
}


sub del_msg_pop
{
 #Delete a message from a POP server
    my ($u,$p,$host,$uid,$fold,$dont_print) = @_;
    my ($index, $digest);
    my @msgs = @{$uid};
    my ($success,$user);

    debug "u: $u host: $host $pop";

  CHECK_FOR_CORRECT_POP_OBJECT:
    {
	my ($uu, $pp, $hh, $rest) = get_folder_credentials($fold);
	    
	if ( (ref $pop ne 'EMU::POP3') || ($uu ne $u) || ($hh ne $host) ) 
	{
            ($success,$host,$user) = do_login_sequence("pop3",$u,$p,$host,1);
            return if (!$success);
#	    &do_pop_login($u,$p,$host,1);
	}
    }

#    my %uids = %{$pop->uidl};

    my $nouidl = bool($folderdb{"nouidl"});

    my $num_msgs = scalar(@msgs);
    $v{"wait_interval"} = get_wait_interval($num_msgs) if (!$v{"wait_interval"});

    foreach my $msg (@msgs) {

        print_progress_new(0);
        if ($v{"wait_count"}++ % $v{"wait_interval"} == 0) {
            $v{"wait_action"} = convert($msg{"WAIT_Deleted"}, 
                                        $v{"wait_count"});
        }

        debug "search msg: $msg";
        $index = search_digest($msg, $nouidl);

        if ($index == 0 || $index eq undef) {
            debug "digest $msg doesnt match POP! Won't delete";
            next;
        }

        $pop->delete($index);

        debug "$msg (index $index) should be deleted. Msg subject: ".$folderdb{"$uid:subj"};
    }

    return $index;
}


# make an MD5 hash of an array of lines.
# $ra_head is a reference to an array
# $num is the number of lines to use
sub md5_lines
{
    my ($ra_head, $num) = @_;
    my $md5;
    my $H;

    my @head = @{$ra_head};

    if (!$num) { $num = scalar(@head) };

#    load_module("Digest::MD5");
#    $md5 = new Digest::MD5;
    # 07/16/98: Don't grab the Received line or lines that begin with spaces.
    # This was causing the can't delete message bug that occured with some pop servers.
    # The actual problem seems to lie in folded lines, so we grep out all folded parts...
    #
    # this isn't very elegant, but it works...
    if ($c{'md5_head_regex'})
    {
	@head = grep(/$c{'md5_head_regex'}/io, @head);
    }
    else
    {
	@head = grep(!/^(?:Status:|X-|Received:|\s+)/i, @head); 
    }

#    $md5->add(@head); #[0..$num]);
#    return $md5->hexdigest;
    return get_digest(\@head);
}

# sub get_index ($$$)
#
# print out an index of messages from the current folder
#
# This function takes the user's name and password as argument,
# and it will print out HTML that allows the user to sift through
# their messages.
#
# modified 07/23/98 ~ 6:00pm
sub get_index
{
 #New and improved Get_index
 # This one just looks at a folder (remote or local) and
 # returns a quick look at what the folder contains
 # it doesn't actually download anything but the headers.

    my ($u, $p, $force_check) = @_;

#    debug "u=$u  force_check=$force_check delay=$delay";
    $delay = time if ($delay == 0);

    # RMK 01/19/99 Check quota first. If over quota, don't check mbox
    quota_check(0);
#    debug "over_quota $over_quota";

    $v{"current_page"} = $v{$folder."_page"};
    my $allowed = $v{"quota_allowed"};
    my $used = $v{"quota_used"};
    $v{"quota_pct"} = ($used == 0) ? 0 : (($used / $allowed ) * 100.0) 
        if (! $v{"quota_pct"});

#    debug "quota info: allowed $v{'quota_allowed'} used $v{'quota_used'}";

    #Determine if we should check a remote mailbox for mail
#    unless (defined $force_check) #MM 10/18/98 (made more clear)
#    {
	$force_check = 
	    $query->param('refresh.x') +
		!$v{"cache"} +
		    $query->param('reload.x') +
			($query->param('variable') eq 'refresh') +
			    $c{"pure_imap"} + 
			        $v{"force_check"} +
                                    !$folderdb{"messages"};
#    }

    debug "###force_check = $force_check # $v{force_check} # $c{pure_map} # $v{cache}";

    $folder = $query->param('folder') if (!($folder));
#    debug "working with folder $folder";

    if ( ($msg{'V_SentmailFolderPretext'} && $folder =~ /^$msg{'V_SentmailFolderPretext'}/) ||
         ( lc($folder) eq lc($userdb{"options.sentfolder"}) ) ||
         ( lc($folder) eq lc($msg{'V_Outbox_Name'}))
       ) {
        write_tmp("is_sent_mail", 1);
    }
    else {
        write_tmp("is_sent_mail", 0);
    }
    
  RENEW_CONNECTION_FOR_POP:
    {
        last if (!$force_check || $userdb{"folder:$folder:protocol"} !~ /pop/i);

        if ($pop) {
#            $pop->quit();
            undef $pop;
            $pop_connected = 0;
        }
    }

    # knowing whether a folder is external is very important
    # down the line... so save it here
    $v{"external"} = $userdb{"folder:$folder:external"};

#    debug "protocol $protocol folder prot ".$userdb{"folder:$folder:protocol"};
  REFRESH_MSG_LIST_POP:
    {
        # RMK 01/19/99 don't check POP if over_quota
        last if (!$force_check || $over_quota) ;

        last if ($userdb{"folder:$folder:protocol"} &&
                 $userdb{"folder:$folder:protocol"} !~ /pop/i);

        last if ($c{"login_protocol"} !~ /pop/i);

        debug "USING POP! Folder is $folder";
        return (get_list_pop($userdb{"folder:$folder:username"},
                             decode($userdb{"folder:$folder:password"}),$folder));
    }

  REFRESH_MSG_LIST_IMAP:
    {
        # IMAP is handled differently, because it does UID slicing.
        # So even if we're overquota we really have to grab the list
        # otherwise we're left with stale data in $folderdb
        # Even do it if not forcing check... the slicing is too
        # sensitive... 

        last if (!$force_check || $over_quota) ;
        last if ($userdb{"folder:$folder:protocol"} &&
                 $userdb{"folder:$folder:protocol"} !~ /imap/i);

        last if ($c{"login_protocol"} !~ /imap/i);

        debug "USING IMAP! folder: $folder ;";

        # Get folder credentials...
        my ($user,$pass,$host,$junk);

        my $save_folder = $folder;

        ($user,$pass,$host,$folder) = get_folder_credentials($folder);

        # only split on "@" if there's more than one "@"
        if ($user =~ /.+@.+@.+/) {
            $user =~ s/^(.+@.+).+/$1/; 
        }

      GET_IMAP_MSGS:
        {
#            debug "will get messges for page ".$v{"current_page"};
            get_list_imap($host,$user,$pass,$folder) unless ($c{"lax_mailbox_sync"});
        }
    }

    $v{"cache"} =1;

    # We do another quota check because we've processed new messages
#    debug "check quota again";

    print_progress($msg{'WAIT_CheckQuota'});
    quota_check(0);

    # RMK 01/19/99 Output quota error on index if required
    if ($over_quota && $status eq "")
    {
	set_status(convert($msg{'ERR_QuotaExceeded_T'},
                           $v{"quota_allowed"},
                           $c{'help_url'}));
    }
    
    return(get_total_msgs($folder));
}

sub get_recent_uid
{
    my ($imap, $folder) = @_;
    my ($next_uid);

    eval 
    {
	$next_uid = $imap->status(get_fold_and_prefix($folder));
    };

#    debug "Server thinks next uid is $next_uid for fold $folder";

    return $next_uid;
}

sub get_recent_uid_db
{
    my ($fold) = @_;

    my $recent_uid = '';
    
    # dirty hack as usual
    my %stubforlock;
    my $tempfold = remove_fold_prefix($fold);
    $tempfold = process_fold_type($tempfold);
    if ( $ELocks->lock_search("$homedir/folders/$tempfold", 'path') )
    {
    	# folderdb
    	return $folderdb{'recent_uid'};
	}
	elsif ( $ELocks->lock_create("$homedir/folders/$tempfold", \%stubforlock, {mode => 'read', nb => 1}) )
	{
		tie my %tempfold, $db_package, "$homedir/folders/$tempfold", O_RDONLY, 0660;
		$recent_uid = $tempfold{'recent_uid'};
		untie %tempfold;
		$ELocks->lock_remove(\%stubforlock);
	}
    return $recent_uid;
}

sub save_recent_uid_db
{
    my ($fold, $uid) = @_;
    debug "Saving recent uid: $uid to $fold";

    # dirty hack as usual
    my %stubforlock;
    my $tempfold = remove_fold_prefix($fold);
    $tempfold = process_fold_type($tempfold);
    if ( $ELocks->lock_search("$homedir/folders/$tempfold", 'path') )
    {
    	# folderdb
    	debug "found $tempfold as folderdb.";
    	debug "folderdb msgs: $folderdb{messages}";
		$folderdb{'recent_uid'} = $uid;
	} 
	elsif ( $ELocks->lock_create("$homedir/folders/$tempfold", \%stubforlock, {mode => 'write', nb => 1}) )
	{
		tie my %tempfold, $db_package, "$homedir/folders/$tempfold", O_CREAT|O_RDWR, 0660;
		$tempfold{'recent_uid'} = $uid;
		untie %tempfold;
		$ELocks->lock_remove(\%stubforlock);
		return $uid;
	}
	
	return undef; # error
}

sub get_x_msgs
{
    my ($max_messages) = @_;
    my (@msgs, $str);

    # grab the messages from the current folder
    debug "Trying to sort with fold = $folder";
    my %args;
    $args{"sort"} = $query->param('sorttype');
    $args{"fold"} = $folder;
    get_sorted_msgs(\@msgs, \%args );

#        debug "@msgs";
    $total_messages = $#msgs + 1;
    if ($total_messages == 0)
    {
        $str .= $msg{'MSG_NoMessages'};
    }

#    debug "total_messages minus 1 = ".$#msgs;

    my ($start) = 0;
    my ($finish) = ($total_messages-1); #for now

    debug "folder $folder  page is $v{$folder.'_page'}";
    if (!$v{$folder."_page"})
    {
	$v{$folder."_page"} = 1;
    }

    # 08/7/98: gotta default the max_messages
    $max_messages = get_max_messages();

#    if ($total_messages > $max_messages && !($query->param('narrow')))
    if ($total_messages > $max_messages)
    {
	my ($next_page, $total_pages);
#	debug "folder $folder it is :".$v{$folder."_page"};

	$start = ( ($v{$folder."_page"} - 1) * $max_messages );
	$finish = $start + $max_messages;

	debug "start=$start  finish=$finish  total=$total_messages";

	$finish = ($total_messages) if ($finish > ($total_messages));
	$finish--;

	$total_pages = ceil($total_messages / $max_messages);
#        debug "folder_page $v{$folder.'_page'}";

        $v{$folder."_page"} = $total_pages if ($v{$folder."_page"} > $total_pages);
        my $this_page;
	if ($v{$folder."_page"} >= 1)
	{
	    # default to 1
	    $next_page = (($v{"$folder\_page"} + 1) % ($total_pages + 1))  ||  1 ;
            $this_page = $v{$folder.'_page'};
	}
	else
	{
	    $next_page = 2;
            $this_page = 1;
	}
	
#	debug "total_pages=$total_pages  next_page=$next_page";
#        debug "this_page $this_page";
	
	write_tmp("moremsgs", 1);
	write_tmp("next_page", $next_page);
	write_tmp("this_page", $this_page);
	write_tmp("prev_page", $this_page - 1) if ($this_page > 1);
	write_tmp("total_pages", $total_pages);
	$v{$folder."_page"} = ($next_page-1) || $total_pages;
    }

    return(@msgs[$start..$finish]);
}

sub make_msg_index
{
    my ($max_messages, $format) = @_;
    my (@msgs, $str);

    # 08/06/98: searching support
    if ($v{"narrow"} && $v{"narrow"} !~ /^\s*$/)
    {
	my (%msgs, @files, $file);
	opendir(DIR, "$homedir/messages");
	@files = readdir DIR;
	closedir(DIR);

	foreach $file (@files)
	{
            # look for unwanted chars in filename
#            $file =~ s/\//++/g;
#            my $f = code2($file);

	    open(IN, "$homedir/messages/$file");
	    while (<IN>)
	    {
		# NOTE: allow for more advanced searching later on
		$msgs{$file}++ if (/\Q$v{"narrow"}/i);
	    }
	}

	@msgs = keys %msgs;

	$total_messages = scalar(@msgs);
	if (!$total_messages)
	{
#           $str .= $msg{'MSG_NoMessages'};
	    $str = join '', $str, $msg{'MSG_NoMessages'};
	}

	delete $v{"narrow"};
    }
    else
    {
        # grab the messages from the current folder
        my %args;
#	    $args{"msgs"} = $userdb{"folder:$folder:msgs"};
        $args{"sort"} = $query->param('sorttype');
        $args{"fold"} = $folder;
        get_sorted_msgs( \@msgs, \%args );

	$total_messages = scalar(@msgs);

	if (!$total_messages)
	{
#           $str .= $msg{'MSG_NoMessages'};
	    $str = join '', $str, $msg{'MSG_NoMessages'};
	}
    }

    debug "total_messages = $total_messages";

    my ($start) = 0;
    my ($finish) = ($total_messages-1); #for now

    if (!$v{$folder."_page"} || $v{$folder."_page"} <= 0)
    {
	$v{$folder."_page"} = 1;
    }

    # 08/7/98: gotta default the max_messages
    $max_messages = get_max_messages();

    if ($total_messages > $max_messages)
    {
	debug "it is :".$v{$folder."_page"};
	$start = ( ($v{$folder."_page"} - 1) * $max_messages );
	$finish = $start + $max_messages;
	debug "start=$start  finish=$finish  total=$total_messages";
	$finish = ($total_messages) if ($finish > ($total_messages));
	$finish--;
    }
    
    # we've got messages
    if ($total_messages)
    {
	my $msg_num;

	foreach $msg_num (@msgs[$start..$finish])
	{
	    my $line = $format;

	    my $stat = $c{"Status" . $folderdb{"$msg_num:stat"}};
	    $line =~ s/\%status/$stat/;

	    my $from = $folderdb{"$msg_num:from"};

	    if ($c{'index_sender_mode'} > 0)
	    {
		my @addrpart = addr_split($from);
		# mode 1 is just the real name
		if ($c{'index_sender_mode'} == 1)
		{
		    $from = $addrpart[0];
		    if (!$from)
		    {
			# fall back on the email address
			$from = $addrpart[1];
		    }
		}
		# mode 2 is just the email
		elsif ($c{'index_sender_mode'} == 2)
		{
		    $from = $addrpart[1];
		}
	    }
	    
	    $from = substr($from, 0, $c{'index_sender_length'});
	    chomp($from);

	    $from = &safe_html($from,'<>');
	    $from =~ s/[\r\n]//g;

	    # 05/15/98: have to have something here.. when it's blank 
            # it's usually spaces, not null.
	    $from =~ /^\s*$/;
            $from = $msg{"MSG_NoFrom"} if (!$from);

	    my $tmp = make_url("msg", $msg_num);

	    $line =~ s(\%sender) (<A HREF="$tmp">$from</A>);

	    my ($date) = $folderdb{"$msg_num:date"};
	
	    $date =~ s/^(.*?)(\d+\s\w\w\w)(.*)/$2/;
	    $date =~ s/[\n\r]//g;
	
	    if (length($date) == 5)
	    {
		$date = join '', "0", $date;
	    }

	    $line =~ s/\%date/$date/;

	    my ($subj) = $folderdb{"$msg_num:subj"};

	    if (!($subj)) 
	    {
		$subj = $msg{'MSG_NoSubject'};
	    }
	    else
	    {
#               $subj .= " " x ($c{'index_subject_length'} + 1);

		$subj = substr($subj, 0, $c{'index_subject_length'});

                $subj = &safe_html($subj, '<>');
		$subj =~ s/[\r\n]//g;
	    }

	    $line =~ s/\%subject/$subj/;
	    $line =~ s/\%size/get_size($folderdb{"$msg_num:size"})/e;

	    my $color = "";            # mlah

	    my $the_pri = ""; #Set this as a default for NOW! CHANGE!
	    $the_pri = $folderdb{"$msg_num:pri"};

	    # Some pretty printing :)
	    if ($c{'PRIORITY_URGENT'} && $the_pri =~ /^urgent|^[12]/i)
	    {
		$color = "BGCOLOR=$c{'PRIORITY_URGENT'}";
	    }
	    elsif ($c{'PRIORITY_NURGENT'} && $the_pri =~ /non-urgent|^[45]/i)
	    {
		$color = "BGCOLOR=$c{'PRIORITY_NURGENT'}";
	    }
	    elsif ($c{'PRIORITY_NORMAL'})
	    {
		$color = "BGCOLOR=$c{'PRIORITY_NORMAL'}";
	    }

	    $line =~ s/\%color/$color/g;
	    $line =~ s/\%hash/$msg_num/g;

	    $str .= "<TR>$line\n";
	}
    }
    
    $str .= "</FONT></PRE></CENTER>";

    return (($total_messages+1),$str);
}

sub get_total_msgs
{
 #Return the total number of messages in a folder
    my ($fold) = @_;

    my @msgs = split(/:/, $folderdb{"messages"});
    return(scalar(@msgs));
}


sub get_folder_msginfo
{
    #Return a reference to an array containing all the messages in a folder
    my ($fullfold, $total_only) = @_;
    my ($unread, $read, $answered, $size);
    my ($folddb, %folddb, $fold);
    my $newtie = 0;
    my @msgs;

    my $prefix = get_outbox_prefix();
    $fold = $fullfold;

    $fold = remove_fold_prefix($fullfold) if ($prefix && $fold =~ /^$prefix/i);
    my $foldfile = process_fold_type($fold);

    # We should get current information...
    # 1. for imap folder or mailboxes, contact server and get status
    # 2. for local folders or inbox, simply use the folder file
    # 3. for pop mailboxes ???

    my $prot = get_folder_protocol($fold);

  IMAP_COUNT:
    {
        last if ($prot !~ /imap/i && !$c{pure_imap});

debug "here fold $fold, fullfold $fullfold";
        if (!ref $pop || !$pop->isValid) {
            my ($user,$p,$host) = &get_folder_credentials($fold);
            debug "IMAP, must login in order to set status...";
            &do_imap_login($user,$p,$host,$fold) || return (0,0,0,0);
        } 

        return $pop->folder_msginfo(get_fold_and_prefix($fold), $total_only, get_imap_folder_size($fold));
    }

  LOCAL_COUNT:
    {
        last if ($prot !~ /local/i);

    }

  POP_COUNT:
    {
        last if ($prot !~ /pop/i);

    }

    if (!-e "$homedir/folders/$foldfile" && $c{pure_imap} && !$userdb{"folder:$fold:external"}) {
	return (undef,undef,undef,undef,undef) unless $pop;

	$pop->select(get_fold_and_prefix($fullfold));
        my $count = $pop->{exists};
	my $size = 0;
	my $list_ref = $pop->list if $pop;
	my (@list_values) = values %{$list_ref} if $list_ref;
	foreach my $v (@list_values) {
	   $size += $v;
	}
        debug "Count of $fullfold: $count";
	return($count, $count, 0, 0, $size);
    }

    debug "\$fold: $fold ; \$folder: $folder ;";

    if ($fold eq $folder) {
       debug "Folder '$fold' is already opened as the folderdb!";
       %folddb = %folderdb;
       return if (!exists($folddb{messages}));
    } else {
	if ( $ELocks->lock_create("$homedir/folders/$foldfile", \%folddb, {mode => 'read', nb => 1}) )
	{
       		tie %folddb, $db_package, "$homedir/folders/$foldfile", O_RDONLY, 0660;
       		if (!exists($folddb{messages})) {
       			untie %folddb;
       			$ELocks->lock_remove(\%folddb);
          		return;
       		}
	}
    }

    @msgs = split(':', $folddb{"messages"});
    debug "messages in $fold: ".scalar(@msgs);
    my $themsg;
    foreach $themsg (@msgs)
    {
	$unread++ if ($folddb{"$themsg:stat"} == STAT_NEW || $folddb{"$themsg:stat"} eq "");
	$read++ if ($folddb{"$themsg:stat"} == STAT_READ);
	$answered++ if ($folddb{"$themsg:stat"} == STAT_ANS);
	$size += $folddb{"$themsg:size"};
    }
    
    debug "returning msginfo (",scalar(@msgs),",$unread,$read,$answered)";

    untie %folddb;
    $ELocks->lock_remove(\%folddb);

    return(scalar(@msgs)) if ($total_only);
    return(scalar(@msgs),$unread,$read,$answered, $size);
}

sub get_imap_folder_size
{
    my ($fold) = @_;

    my ($folddb, %folddb);
    my $foldfile = process_fold_type($fold);

    if ( $ELocks->lock_create("$homedir/folders/$foldfile", \%folddb, {mode => 'read', nb => 1}) )
	{
       		tie %folddb, $db_package, "$homedir/folders/$foldfile", O_RDONLY, 0660;
	}
    else
        {
	 return "N/A";
	}

    my @msgs = split(':', $folddb{"messages"});
    my $fold_size = 0;
    foreach (@msgs)
    {
       $fold_size += $folddb{"$_:size"};
    }

    untie %folddb;
    $ELocks->lock_remove(\%folddb);

    return $fold_size;
}

sub get_curr_folder_msginfo
{
    my ($unread, $read, $answered);
    my @msgs;

    @msgs = split(':', $folderdb{"messages"});
   debug "folderdb: ".$folderdb{"messages"};
    debug "messages: ".scalar(@msgs);
    my $themsg;
    foreach $themsg (@msgs)
    {
	$unread++ if ($folderdb{"$themsg:stat"} == STAT_NEW || $folderdb{"$themsg:stat"} eq "");
	$read++ if ($folderdb{"$themsg:stat"} == STAT_READ);
	$answered++ if ($folderdb{"$themsg:stat"} == STAT_ANS);
    }
    
    debug "returning msginfo (",scalar(@msgs),",$unread,$read,$answered)";

    return(scalar(@msgs),$unread||0,$read||0,$answered||0);
}


sub get_sorted_msgs
{
    my ($msgs, $hash_ref) = @_;
    my @msgs;
    my $nofreshness = 0;

    #return a sorted array of message uids
    my %hash =  %{$hash_ref} if $hash_ref;

    my ($fold) = $hash{"fold"};

    # Get sorttype either from parameter, or last saved, or default to select
    my $sorttype = $hash{"sort"} || $folderdb{"sortlast"} || $c{'default_sort'} || 'select';

    my $current_order = $folderdb{"sortorder.$sorttype"} || 0;
    my $order = $current_order;

    debug "current sort for $sorttype = $current_order";
    debug "args: sort =  $sorttype ($v{sortlast}), order= $order , fold=$fold";
#    debug "current msgs: @msgs";

    debug "sort requested? ".$query->param('sorttype');
    # Check for a sort request. If we have a $query->param('sorttype') then
    # we're requesting a sort reversal for that type. Simply negate the
    # current sorting for this type.
    if ($query->param('sorttype')) {
        $order = $current_order ? 0 : 1;
        $folderdb{"sortorder.$sorttype"} = $order;

        # also clear freshness to ensure re-sorting
        $folderdb{"freshness"} = 0;
    }

#        if ($folderdb{"sortlast"} eq $sorttype) {
#	    debug "reversing sortorder: ". !$order;
#	    $folderdb{"sortorder"} = !$order;
#	    $order = bool($folderdb{"sortorder"}); # gotta get it again
#        }
#        else {
#            debug "changing sorttype to ".$query->param('sorttype');
#            debug "default order to NORMAL";
#            $order = 0;
#            # also clear freshness to ensure re-sorting
#            $folderdb{"freshness"} = 0;
#        }
#    }

    # Get sorttype either from parameter, or last saved, or default to select
    $sorttype = $sorttype || $folderdb{"sortlast"} || $c{'default_sort'} || 'select';

    # update the last sorted type
    $folderdb{"sortlast"} = $sorttype;

    debug "sorting by $sorttype, $order";    

    # For default message sorting (sorttype is "select") don't do anything
    if ($sorttype ne "select" and $sorttype ne "default") {

        my $foldfile = $fold;
        $foldfile =~ s/\//./g;

        # special sort, get current set of messages
        my %folddb;
	if ( $ELocks->lock_create("$homedir/folders-ordered/$foldfile$sorttype", \%folddb, {mode => 'read', nb => 1}) )
	{
        	tie %folddb, $db_package, "$homedir/folders-ordered/$foldfile$sorttype", O_RDONLY, 0660;

        	if (-e "$homedir/folders-ordered/$foldfile$sorttype" and scalar(keys %folddb) > 0)
        	{
	            	# first make sure it exists and is a valid db file
	            	@msgs = split(/:/, $folddb{"messages"});
	
	            	# additional error checking here... if # messages don't match
	            	# then use original list...
	            	my $orig_msgs = $folderdb{"messages"} =~ tr/:/:/;
	            	debug "orig: $orig_msgs, ordered: ".$#msgs;
	            	if ($orig_msgs != $#msgs)
	            	{
		                debug "not using ordered folder data... bogus";
	        	        @msgs = split(/:/, $folderdb{"messages"});
	                	# force sorting
	                	$nofreshness = 1;
	            	}
        	}
        	else 
        	{
            		debug "$homedir/folders-ordered/$foldfile$sorttype no good, use original list";
            		@msgs = split(/:/, $folderdb{"messages"});
        	}
                
                untie %folddb;
                $ELocks->lock_remove(\%folddb);
        }
 
#        debug "current msgs: @msgs";
        # Check if we need to sort at all    

        my ($hash) = get_digest(join(':', @msgs));
        debug "found the freshness hash of $hash";
        debug "Current freshness: ".$folderdb{"freshness"};

debug "$nofreshness $sorttype $order $current_order ".$folderdb{"sorttype"};
        # RMK 01/19/99 don't get new messages if over_quota
        # RMK 01/21/99 check for change in order as well
        if (($nofreshness or $folderdb{"freshness"} ne $hash or
	        $current_order ne $order or 
                $sorttype ne $folderdb{"sorttype"}) and !$over_quota)
        {
	    debug "Sort needed, as msgs not fresh in cache. Using $sorttype";
debug "sorting ".scalar(@msgs)." messages";

            # Take care of IMAP. Since we use "quickview", we need to make
            # sure we have all header info prior to sorting
          GET_ALL_HEADERS_FROM_IMAP:
            {
                last if ($userdb{"folder:$folder:protocol"} !~ /imap/i);
                last if (scalar(grep { /:stat$/ } keys %folderdb) ==
                         scalar(split(/:/, $folderdb{"messages"})));

                debug "don't have full list of headers, need to process";
                my ($user,$p,$host) = &get_folder_credentials($folder);
   
                get_list_imap_full($host,$user,$p,$folder);
            }

	    if ($sorttype eq "subject")
	    {
	        @msgs = sort { lc($folderdb{"$a:subj"}) cmp lc($folderdb{"$b:subj"}) } @msgs;
	    }
	    elsif ($sorttype eq "sender")
	    {
	        @msgs = sort { lc($folderdb{"$a:from"}) cmp lc($folderdb{"$b:from"}) } @msgs;
	    }
	    elsif ($sorttype eq "size")
	    {
	        @msgs = sort { $folderdb{"$a:size"} <=> $folderdb{"$b:size"} } @msgs;
	    }
	    elsif ($sorttype eq "date")
	    {
#	        load_module("Date::Parse",0,'str2time');
                # "NORMAL" order is ordering in descending time
                my %datehash = map { $_ => str2time($folderdb{"$_:date"}) } @msgs;
                @msgs = sort { $datehash{$b} <=> $datehash{$a} } @msgs;                      
	    }
	    elsif ($sorttype eq "status")
	    {
	        @msgs = sort { $folderdb{"$a:stat"} <=> $folderdb{"$b:stat"} } @msgs;
	    }
            elsif (@custom_headers) {
                # allow for sorting on customized headers. 
                foreach my $chead (@custom_headers) {
                    if ($sorttype eq $chead) {
                        debug "sorting by customized header $chead";
                        @msgs = sort { lc($folderdb{"$a:$chead"}) cmp lc($folderdb{"$b:$chead"}) } @msgs;
                        last;
                    }
                }
            }
	    else
	    {
	        @msgs = reverse sort(@msgs);
	        $sorttype = "default";
	    }

	    # Store in cache
	    set_msgs_db(\@msgs, $fold,$sorttype);
        }
    }
    else
    {
		debug "using cache of sort...";
        @msgs = split(/:/, $folderdb{"messages"});
#       debug "messages are ".$folderdb{"messages"};
    }

    $folderdb{"sorttype"} = $sorttype;
#    $folderdb{"sortorder"} = $order;

    debug $order ? "REVERSE ORDER" : "NORMAL ORDER";

    # imap is the reverse of POP... so adjust order here accordingly
    $order = !$order if ($userdb{"folder:$fold:protocol"} =~ /imap/);

    @msgs = reverse @msgs if ($order);

    $folderdb{"freshness"} = get_digest(join(':', @msgs));

    # For the Search folder, we need to do additional processing.
    # That's because the search folder stays around and it may actually
    # contain messages that could have been deleted already, so double-check
    # for that.
    my $searchfold = $msg{"FOLD_Search_Results"} || "Search Results";
    if ($fold eq $searchfold) {
        my @tmpmsgs = ();
        foreach my $m (@msgs) {
            if (!-e "$homedir/messages/$m") {
                debug "$m has been deleted, removing from search folder";
            }
            else {
                push(@tmpmsgs, $m);
            }
        }
        @msgs = @tmpmsgs;
    }

    debug "msgs total ". scalar(@msgs);
#    debug "@msgs";

    write_tmp("sorttype", $sorttype);
    write_tmp("sortorder", $folderdb{"sortorder.$sorttype"});
debug "sorttype $sorttype, sortorder ".$folderdb{"sortorder.$sorttype"};

    @{$msgs} = @msgs;
}


sub make_imap_object
{
    my ($host,$user,$p,$fold, $force) = @_;

#    debug "Attempting to connect to $host as $user with $p";

    # Grr, this is an irritating necessity.
    $v{"mail_user"} = $user;
    $v{"mail_pass"} = $p;
    $v{"external"} = $userdb{"folder:$fold:external"} 
        if ($fold && !defined($v{"external"}));

    if (!$force && (my $c = find_connection('imap', $host, $user, $p))) {
       $pop = $c;
    } else {
       $pop = undef;
#       debug "host is '$host'";
       my $timeout = $c{"tcp_timeout"} || 10;

       my $port = 143;
              
       if ( $c{'imaps_mail_hosts'})
       {
		        my @hostnms = split /\s|\,/, $c{'imaps_mail_hosts'};
			map { $port = $c{'imaps_port'} || 993 if lc($_) eq $host} @hostnms;
			debug "IMAPS HOSTNAMES: @hostnms HOST: $host USERNAME: $user";
       }


       $pop = EMU::IMAP->new($host, Port=>$port, Timeout=>$timeout);

       if ($@) {
          debug "RECEIVED ERROR WHILE CONSTRUCTING EMU::IMAP: $@\n";
       }
#       debug "defined imap" if ($pop);

       if ($pop) {
          $pop->login($user,$p);
       }
       
       return if (!$pop || !$pop->isValid);

       $pop->{"prefix"} = $userdb{'options.prefix'} || $c{'default_imap_prefix'};
       if ($pop->{"prefix"})
       {
         my $delim = &get_imap_delimiter(1);
         $pop->{"prefix"} = $pop->{"prefix"}.$delim;
       }

       # Make this connection object available later
       &store_connection($pop, 'imap', $host, $user, $p);
    }

    $pophost = $host;
#    debug "pophost $pophost";
    return 1;
}

sub do_imap_login
{
    my ($user,$p,$host,$fold,$read_only) = @_;
    debug "Attempting to login with IMAP: user=$user,  host=$host,  folder=$fold";
    return undef unless ($user && $p && $host); #hopefully no zero names..

    if (my $c = find_connection('imap', $host, $user, $p))
    {
        debug "already have a valid connection...";
        if ($fold eq $c->{folder} && $c->{uidvalidity})
        {
            $pop = $c;
            return $c->{uidvalidity};
        }
    }

    debug "requested read only login - floop" if $read_only;

  	DROP_CONNECTION_IF_NECESSARY:
    {
        last unless $pop;

		if (ref($pop) ne 'EMU::IMAP')
		{
            debug "incorrect pop object...(got $pop)";
	    	undef $pop;
            $pop_connected = 0;
            last DROP_CONNECTION_IF_NECESSARY;
		}

        # if we're in read-only mode but want to be in read-write, simply
        # get out of the block (do nothing) and the folder will be selected
        # down below.

		if ( $pop->{"read_only"} && ! $read_only )
		{
            last DROP_CONNECTION_IF_NECESSARY;
		}

		unless ( ($pop->{"user"} eq $popuser) && 
                 ($pop->{"pass"} eq $p)       && 
                 ($pop->{"host"} eq $pophost) )
		{
	    # We're in a different mailbox...better login again:
	    	undef $pop;
            $pop_connected = 0;
	    	&make_imap_object($host,$user,$p) || return undef;
	    	return undef unless $pop;
		}
    }
    

  	MAKE_NEW_OBJECT:
    {
        last if ($pop);

		if (&make_imap_object($host,$user,$p,$fold))
		{
	    	debug "Successful Login" ;
		}
		else
		{
	    	debug "Unsuccessful Login: $user $p $host";
            undef $pop;
	    	return undef;
		}
    }
    
    debug "fold: $fold ; external: ", $userdb{"folder:$fold:external"}, " ; extra_fold: ", $userdb{"folder:$fold:extra_fold"};

    # Select a folder
    if (!$fold)
    {
        $fold = $c{'default_inbox_name'} || $inbox;
    }
    elsif ($userdb{"folder:$fold:external"} && $userdb{"folder:$fold:extra_fold"})
    {
        $fold = $userdb{"folder:$fold:extra_fold"};
    }
    elsif ($userdb{"folder:$fold:external"})
    {
      $fold = $c{'default_inbox_name'} || $inbox;
    }

	debug "FOLD: $fold";

    #MM 990520
#   $fold = get_imapfolder_from_emufolder($fold);

    $fold = get_fold_and_prefix($fold);

    # Unless we're already in the right folder, select it.
    debug "fold $fold and pop->folder ".$pop->{folder};

    unless ( ($pop->{folder} eq $fold) && ( $pop->{"read_only"} == $read_only ) )
    {
        # If we're already in the folder, we should really only change
        # between read-only and read-write if the request is to go
        # to read-write... because there are cases where we're 
        # already and someone like get_subscribed_imap requests
        # read-only, and all of a sudden we can't delete messages

	# Select the new folder
		my $success;

		SAME_FOLDER_GO_TO_READWRITE:
        {
            last if ($pop->{folder} ne $fold);

            # so... same folder but want to change to read-write
	    	$success = $pop->select($fold) unless $read_only;

            # if we request read-only, but are already selected,
            # then don't bother. Just skip and say it's successful.
            $success = 1 if ($read_only);
        }

      	DIFFERENT_FOLDER:
        {
            last if ($pop->{folder} eq $fold);

	    	$success = $pop->select($fold) unless $read_only;
	    	$success = $pop->examine($fold) if ($read_only);
        }

        debug "success $success read_only $read_only";
        debug "pop->folder now ".$pop->{folder};

        unless ( defined $success )
        {
            # Well, we tried...
	    	debug "Failed to log in :( -- second error $fold";
#           set_status(convert($msg{'ERR_FailedSelect'}, " $old_fold || $fold"));
	    	return undef;
		}
    }

    debug "Logged in and selected folder $fold";
    debug "fold $fold and pop->folder ".$pop->{folder};
    
    my $uid_validity;
    if ($fold eq $pop->{folder} && $pop->{uidvalidity}) {
        $uid_validity = $pop->{uidvalidity};
    }
    else {
        $uid_validity = $pop->uid_validity($fold);
    }

    debug "UID_Validity: $uid_validity";

    return $uid_validity;
}

#the folder isn't the prefix oh right.
sub get_imapfolder_from_emufolder
{
    my $fold = shift;
    my ($imapfold);

    return $fold if ($fold eq $inbox);

    my ($prefix) = &get_outbox_prefix();
    if ($prefix)
    {
	my $delim = &get_imap_delimiter(1);

	$imapfold = $folderdb{"imapfolder"} || "$prefix$delim$fold";
    }
    else
    {
	$imapfold = $fold;
    }
    debug "Found imapfolder $imapfold from input $fold";
    debug "imapfolder is ". $folderdb{"imapfolder"}. " prefix is $prefix fold is $fold";
    return $imapfold;
}

sub set_imapfolder
{
    my ($new_fold,$extra_fold) = @_;
    return $folderdb{"imapfolder"} = $extra_fold;
}

sub set_msg_status
{
    my ($message,$stat) = @_;
    return unless ($message);

    my $fold = $foldmap{$message};

    my $prefix = get_outbox_prefix();

    $fold = remove_fold_prefix($fold) if ($prefix && $fold =~ /^$prefix/i);

    $folderdb{"$message:stat"} = $stat;
    debug "setting status for $message to $stat";

   # A proper folder protocol check
    if ( ($userdb{"folder:$fold:protocol"} =~ /imap/i) || (!$userdb{"folder:$fold:external"} && $c{"pure_imap"}) && $stat != STAT_NEW ) {
        my ($user,$p,$host) = &get_folder_credentials($folder);
        if (!ref $pop || !$pop->isValid) {
            debug "IMAP, must login in order to set status...";
            &do_imap_login($user,$p,$host,$folder) or return;
        } 

        $pop->select($userdb{"msgs:$message:folder"}) if ($pop->{folder} ne $folder);
        $pop->set_flag($message, $stat);
        debug "setting flag for $message to $stat";
    }
}

sub set_msgs_db
{
    my ($msgs, $fold, $order) = @_;

    debug "Trying to set fold $fold and order $order";

    #Set in DB
    create_directory("$homedir/folders-ordered") 
            if (!-e "$homedir/folders-ordered");
    store_messages(\@{$msgs}, "$fold:$order");

    # update entire folder's freshness value
    my ($hash) = get_digest(join(':', @{$msgs}));

    debug "hash: $hash fold: $fold";

    $userdb{"folder:$fold:msgs:freshness"} = $hash;
}


sub update_folder_order_freshness
{
    my ($fold,$order) = @_;

    my ($freshness);
    
    $freshness = get_folder_freshness($fold);

    debug "Setting $freshness for $fold with $order";

    $userdb{"folder:$fold:msgs:$order:freshness"} = $freshness;

    return 1;
}

sub get_folder_order_freshness
{
    my ($fold,$order) = @_;
    debug "For $fold and $order";
    return $userdb{"folder:$fold:msgs:$order:freshness"};
}

sub get_folder_freshness
{
    my ($fold) = shift;

    debug "fold = $fold";

    my $freshness = $folderdb{"freshness"};
    $freshness = $freshness || get_digest($folderdb{"messages"});

    return $freshness;
}


sub get_list
{
    my ($fold) = @_;
    my ($proto);

    $delay = time if ($delay == 0);
    my ($user,$pass,$host) = get_folder_credentials($folder);
    ($user, $host) = split(/\@/,$user,2);           

    $proto = $userdb{"folder:$fold:protocol"};

    if ($proto =~ /pop/i)
    {
	return &get_list_pop($user,$pass,$fold);
    }
    else
    {
	return &get_list_imap($host,$user,$pass,$fold);
    }
}

sub fill_headers {
    # Fill in header info for digest
    my ($msg, $nouidl, $fold, $store, $deleted) = @_;
    my ($digest, $ra_header, %h);

    if ($nouidl) {
        $ra_header = $pop->top($msg,0);

        # create digest from header
        $digest = md5_lines($ra_header);
    }
    else {
        # Use hash, UIDLs already read in previously
        if (!exists($poplist{$msg})) {
            debug "Message $msg not found on pop server!";
            return 0;
        }
        $digest = code2($poplist{$msg});
    }
    
#    debug "digest for $msg is $digest";

    # make sure to set foldmap
    $foldmap{$msg} = $fold;

    my @msgs = split(/:/, $folderdb{"messages"});

    my $return0 = 0;

    debug "mailloc $mailloc, download_full_bodies ".$c{"download_full_bodies"};
  RETURN_IF_WE_HAVE_IT:
    {
        # Check if we previously processed message. 
        # as long as mailloc isnt set and neither is download_full_bodies
        # then we should simply return. For mailloc and download_full_bodies
        # we should really make sure message has been downloaded.

        last if ($mailloc || (bool($c{"download_full_bodies"}) &&
                              !$c{"$digest:downloaded"}));

        if (exists($folderdb{"$digest"}) && $folderdb{"$digest"} ne "" &&
                (grep (/^\Q$digest\E$/, @msgs) || $deleted->{$digest}) && -e "$homedir/messages/$digest" ) {
            return(0);
        }
        elsif (exists($folderdb{"$digest"}) && $folderdb{"$digest"} ne "" &&
                (grep (/^\Q$digest\E$/, @msgs || $deleted->{$digest})) && !-e "$homedir/messages/$digest") {
            # ok, we're continuing because everything indicates we have
            # the message... _however_, we don't have the file. Let's set
            # setup so we still return a 0, in that case we don't end up
            # with duplicate messages in our message list
            $return0 = 1;

            debug "will force a return of 0 so we don't duplicate messages";
        }
    }

    my $already_downloaded = 1 if ($folderdb{"$digest:downloaded"} == 1);

    my $force_download = bool($userdb{"options.DontsynchronizePOP"} && $userdb{"folder:$folder:protocol"} =~ /pop/i);

    debug "force download because of POP synchronization? $force_download";
    debug "$digest deleted? $deleted->{$digest}";
    if (!$deleted->{$digest} && ($mailloc || $c{"download_full_bodies"} || $force_download)) {
        my $success = 1;
        # let's download the file if not yet downloaded of if it is missing
        # from our directory
        my $download = bool($folderdb{"$digest:downloaded"} != 1 ||
                            (!-e "$homedir/messages/$digest") ||
                            (-s "$homedir/messages/$digest" == 0));
        if ($download) {
            debug "downloading $digest";
            download_msg($digest, $folder, 1);

            debug "size ".-s "$homedir/messages/$digest";

        }

        if ($mailloc) {
            debug "deleting $msg from pop";

            # safety measure... did message really get stored? If not dont delete
            $pop->delete($msg) if (-e "$homedir/messages/$digest");

            return 0 if (!$success || !-e "$homedir/messages/$digest" 
                    || -s "$homedir/messages/$digest" == 0);
        }
    }

    # if mailloc and message was previously downloaded, return 0
#    debug "mailloc $mailloc, already_downloaded $already_downloaded, folder ".$folderdb{"$digest:folder"}." size ".$folderdb{"$digest:size"};
    $return0 = bool( $return0 ||
                     ( $mailloc && $already_downloaded &&
                       $folderdb{"$digest:folder"} && 
                       $folderdb{"$digest:date"} &&
                       $folderdb{"$digest:from"} &&
                       $folderdb{"$digest:subj"} ) );
    return 0 if ($return0);

    debug "$digest exists but not in msg list" if (exists($folderdb{"$digest"}));

    # for uidl, haven't gotten header yet.
    $ra_header = $pop->top($msg,0) if (!$nouidl);

    # decompose header so we may fill in userdb
    my $rh_decomposed = decompose_header($ra_header, $digest);

    return 0 unless ($rh_decomposed);

    foreach my $thekey (keys %{$rh_decomposed})
    {
        trim(\$rh_decomposed->{$thekey}); # get rid of extra spaces and newlines
        $folderdb{"$digest:$thekey"} = $rh_decomposed->{$thekey} if (defined($rh_decomposed->{$thekey}));
    }

    # Set location of message, let vault know we have it.
    $folderdb{"$digest"} = "local"; 
    $folderdb{"$digest:folder"} = $fold; 

    # this can all be set blank
    $folderdb{"$digest:nouidl"}   = $nouidl;

    # set to zero unless set otherwise
    $folderdb{"$digest:downloaded"} = 0 unless ($folderdb{"$digest:downloaded"});

    # make sure to save correct pophost for folder
    $folderdb{"hostname"} = $pophost;

    # Set the size of the message
    $folderdb{"$digest:size"} = $pop->list($msg);

    debug "QQQ $digest is $fold";
    
    my $filtered = 0;

    # now add it to the folder
    add_to_folder($digest, $fold, $store);

	if ( has_spam_header($digest) )
	{
		debug "message $digest is SPAM. filtering it to hell";
		filter_spam_header($digest, $foldmap{$digest});
		return -1;
	}

  	DO_REALTIME_FILTER:
    {
        debug "folder $folder, do_realtime? ".$userdb{'options.do_realtime_filter'};
        # already filtered or we dont want realtime?
        last if ( $filtered || ! bool($c{"do_realtime_filter"}) && ! bool($userdb{'options.do_realtime_filter'}) );

        # local or imap folder? (imap we'll do in a special way elsewhere
        last if ($userdb{"folder:$folder:protocol"} eq "local" ||
                 $userdb{"folder:$folder:protocol"} =~ /imap/i);

        # Try to filter message right away if an INBOX...
        debug "applying realtime filter";
        $filtered = filter_message_local($digest);

        if ($filtered) {
            debug "message was filtered, returning -1";
            return -1;
        }
    }

    return $digest;
}


sub sync_to_pop {
    # Synchronize to POP (only for non-mailloc and upon login)
    my ($msgs, $fold, $nouidl) = @_;
    my %uids = reverse %poplist;
    my @msg;

    my $themsg;

#    debug "need to log into pop? ".(!$pop ? "1":"0");
    if (!$pop) {
         my $success;
         my ($user,$p,$host) = ($userdb{"folder:$fold:username"},
                                decode($userdb{"folder:$fold:password"}),
                                $userdb{"folder:$fold:hostname"});
         ($success,$host,$user) = do_login_sequence("pop3",$user,$p,$host,1);
         return undef if (!$success);
    }

    # for nouidls servers, if we're syncing, we need to clear out the hash
    %nouidl_list = () if ($nouidl);

    foreach $themsg (@{$msgs}) {
        next if $themsg eq "";
        # for each msg in msg list, check if it exists on POP server.
        # If not, delete from local store
        if ($nouidl) {
            my $good = search_digest($themsg, $nouidl, 1); # "1" forces uids
            push(@msg, $themsg) if ($good eq undef || $good == 0);
        }
        else {
#            debug "looking for $themsg in poplist";
            push(@msg, $themsg) if (!exists($uids{decode2($themsg)}));
        }
    }

    del_local_msg(\@msg) if (scalar(@msg) >= 1);

  ASSIGN_MSG_LIST:
    {

        if ($nouidl) {
            my %tmp_list = %nouidl_list;
            delete($tmp_list{initialized});

            @{$msgs} = sort { $tmp_list{$b} <=> $tmp_list{$a} } 
                           keys %tmp_list;
        }

        else {
            @{$msgs} = map { $_ = code2($poplist{$_}) } sort {$b <=> $a} 
                           keys %poplist;
        }

        $folderdb{"messages"} = join(':', @{$msgs});
    }
}


sub verify_msglist {
    # we use this as possible error recovery. We may have a folder
    # that lost its set of messages ("messages" is blank) but still
    # has message keys in it. If so, recover the msg list

    debug "folder $folder";
    my @keys = grep (/:date$/, keys %folderdb);
    my @foldkeys = keys %folderdb;
    my $current_msgs = $folderdb{"messages"} =~ tr/:/:/;

    if ( ($#keys >= 0 && $folderdb{"messages"} eq "") ||
            ($#keys != $current_msgs)) {
        debug "oops! our msg list is empty or out of synch!";
        my @keys2;

        # get digests by stripping out :date
        my $thekey;
        foreach $thekey (@keys) {
            $thekey =~ s/:date$//;
            push (@keys2, $thekey);
            debug "adding digest $thekey";
        }

        # order msgs chronologically
#        load_module("Date::Parse",0,'str2time');
        @keys2 = sort { str2time($folderdb{"$b:date"}) <=> str2time($folderdb{"$a:date"}) } @keys2;

        # now save into messages list
        $folderdb{"messages"} = join(':', @keys2);
#        debug "set messages now to ".$folderdb{"messages"};
    }
    @foldkeys = keys %folderdb;
#    debug "keys folderdb: @foldkeys";
}


sub initialize_nouidl_list {
    # fill in hash with current set of messages

    debug "initializing nouidl_list to set of messages";
    $nouidl_list{initialized} = 1;

    my @msgs = split(/:/, $folderdb{"messages"});
    my $index = $#msgs + 1;
    foreach my $digest (split(/:/, $folderdb{"messages"})) {
        $nouidl_list{$digest} = $index;
        $index -= 1;
    }
}


sub get_list_pop
{
    # Get the index of a POP folder
    my ($u,$p,$fold) = @_;
    my ($total, %h);
    my ($i, $digest, $ra_header);
    my ($rh_decomposed);
    my $nouidl=0;
    my $repeat=0;
    my $reversed=0;
    my %headers;
    my ($user, $host);
    my @newmsgs;
    my %msglist;
    my $filtered=0;

    if ($userdb{"folder:$fold:external"} == 1) {
        $host = $userdb{"folder:$fold:hostname"};
    }
    else {
        $host = $pophost;
    }

    $user = $u;

    ($user, $host) = map_mailserver($user, $host, $fold);

    my $delay_max = $c{'waitscreen_timeout'} || 10;

#    debug "firstlogin $firstlogin";
    # always force login here
#    if (!$firstlogin && $pop) {
#        $pop->quit() ;
#        undef $pop;
#        $pop_connected = 0;
#        debug "not firstlogin, reconnect to pop";
#    }

#    debug "need to log into pop? ".(!$pop ? "1":"0");
    if (!$pop) {
         my $success;
         ($success,$host,$user) = do_login_sequence("pop3",$user,$p,$host,1);
         return undef if (!$success || !ref $pop || !$pop->isValid);
    }

    # messages in inbox
    $total = ($pop->popstat)[0];

    # 04/30/99 MM: Removed my from below:
    $protocol = $protocol || "pop3";   # must default

    debug "total msgs: $total";

    # do a sanity check on the message list, possibly recover from error
#    verify_msglist();

    # original msg list
    my (@msgs) = split(/:/, $folderdb{"messages"});
    my $current_total = $#msgs + 1;
#    debug "current_msgs total: $current_total";

    $nouidl = $folderdb{"nouidl"};
    debug "NOUIDL $nouidl";

    my $num_msgs = $total;
    my $processed = 0;

    my $total_printed = 0;

    debug " mailloc: $mailloc";

    # this is done for mailloc accounts to make sure we dont have repeat
    # messages
    my $themsg;
    if ($mailloc) {
        foreach $themsg (@msgs) {
            $msglist{$themsg} = 1;
        }
    }

    $v{"wait_interval"} = get_wait_interval($num_msgs);

    $v{"wait_action"} = $msg{"WAIT_CheckHeaders"};
    print_progress_new(0,1);

    my $q_used = $v{"quota_used"};
    
    # If we're not syncing with the server, we need to make sure we don't
    # download any messages we've flagged as 'deleted'. To speed things up,
    # we build that list into a hash here.
    my %deleted = map { $_ => 1 } split(/:/, $folderdb{"deleted"});
    
    for (; $num_msgs >= 1; $num_msgs--) {

        print_progress_new(1);

        if ($v{"wait_count"} % $v{"wait_interval"} == 0) {
            $v{"wait_action"} = convert($msg{"WAIT_ProcessedMsgs"}, 
                                        $v{"wait_count"});
        }

        # fill_headers will return 0 if message already exists
        $digest = fill_headers($num_msgs, $nouidl, $fold, 0, \%deleted);
        debug "processing digest $digest";

      SAVE_NOUIDL_HASH:
        {
            last if (!$nouidl || $digest == -1);

            initialize_nouidl_list() if (!$nouidl_list{initialized});

            $nouidl_list{$digest} = $num_msgs if ($digest);
        }

        $processed++;
        
        if ($digest && $deleted{$digest}) {
            next;
        }

        if ($digest == -1) {
            debug "message was filtered, not adding" ;
            $filtered = 1;
        }

        # add if not already there, double-check against %msglist
        if ($digest && $digest != -1) {
            if (!$mailloc || !exists($msglist{$digest})) {
#                debug "adding digest $digest";
                push(@newmsgs, $digest);
                $repeat = 0;
            }

            if ($v{"quota_allowed"} > 0) {
                $q_used += -s "$homedir/messages/$digest";
                debug "quota used now $q_used";
            }
        }
        elsif (!$digest && !$mailloc) {
            # only do the repeat thing if not mailloc
            $repeat++;
        }
        last if ($repeat == 5);

        if ($v{"quota_allowed"} > 0 && $q_used > $v{"quota_allowed"}) {
	    set_status(convert($msg{'ERR_QuotaExceeded_T'},
                           $v{"quota_allowed"}));
            last;
        }
    }

#    debug "newmsgs @newmsgs";
    # default to @newmsgs if original @msgs blank
    if (!@msgs) {
        @msgs = @newmsgs;
        undef @newmsgs;
    }

    # if we've filtered anything out, then we *must* quit because POP
    # wont truly delete until the session quits...
    if ($filtered) {
        $pop->quit() if ($pop);
        $pop = undef;
#        $pop_connected = 0;
    }

    my $sync = 0;

  CHECK_IF_SYNC:
    {
        my $first = get_var("first");
#        debug "first is $first";
        last if (!$first);

        write_tmp("first", 0);
        
        # For non-syncing configurations, we DO need to keep up with our
        # 'deleted' list, so things don't get out of control. 'first' is a
        # good time to cull any stale digests listed in our 'deleted' list.
        if ($userdb{"options.DontsynchronizePOP"}) {
         
            debug "Cleaning up 'deleted' message list";
        
            # First, remove any 'deleted' messages that have been re-inserted
            # into the message list.
            foreach my $m (@msgs) { 
               delete $deleted{$m}; 
            }               
            
            # Next, check that all our 'deleted' messages still exist on the
            # server. Remove any that are not.
            foreach my $digest (keys %deleted) {
                 my $index = search_digest($digest, $nouidl);
                 if (!$index) {
                     debug "Removing: $digest";
                     delete $deleted{$digest};
                 } else {
                     debug "Deleted message '$digest' has index $index";
                 }  
            }                      
        }
            
        # for nouidl servers we have a decision to make. It's too slow
        # to keep processing all messages everytime, so we try not to
        # sync unless we *really* have to. "Really have to" means if
        # the number of messages at the server doesn't equal the number
        # of messages we think we should have.

        if ($nouidl) {
            $sync = 1 if (($#msgs+1) + ($#newmsgs+1) != $total);
        }

        else {
            # for uidl servers, since "first" is true, just set $sync to true
            $sync = 1;
        }
    }


  CHECK_POP_FRESHNESS:
    {
        last if ($sync || $nouidl);
        last if ($v{"quota_allowed"} > 0 && $q_used > $v{"quota_allowed"});

        my @pop_msgs = map { $_ = code2($poplist{$_}) } sort {$a <=> $b} keys %poplist;
        my $current_freshness = get_digest($folderdb{"messages"});
        my $pop_freshness = get_digest(join(':',@pop_msgs));

#        debug "freshness: $current_freshness, $pop_freshness";
        $sync = 1 unless ($current_freshness eq $pop_freshness);
    }

    debug "sync is $sync";

  ASSIGN_MSGS_LIST:
    {

        if (!$mailloc && !$userdb{"options.DontsynchronizePOP"}) {

            # sync if list isn't fresh
            if ($sync) {
                sync_to_pop(\@msgs, $fold, $nouidl);
#                debug "synchronized $fold with POP server";
            }

            elsif ($#newmsgs+1 > 0) {

                push (@newmsgs, @msgs);
                @msgs = @newmsgs;
            }
        }
        else {
             debug "mailloc";
             # Here... either mailloc or we dont want to synchronize with POP

             if (scalar(@msgs) == 0) {
                 @msgs = @newmsgs;
             }
             elsif (scalar(@newmsgs) != 0) {
                 push(@newmsgs, @msgs);
                 @msgs = @newmsgs;
             }
        }
    }
    
    # Update 'deleted' list
    $folderdb{"deleted"} = join(':', keys %deleted);

    # default order of '0' means reverse chronological order
#    my ($order) = $folderdb{"sortorder"} || 0;

    $total_messages = scalar(@msgs);
    $folderdb{"messages"} = join(':', @msgs);
#            debug "set messages to ".$folderdb{"messages"};

#    debug " $fold and $total_messages";

#    $pop->quit() if $pop;
    undef $pop;
    $pop_connected = 0;
    $v{"filtered to"} = 0;
    write_tmp("have_messages", 1);

    return ($total_messages + 1);
}


sub validate_hostname {
    my ($host,$noerror) = @_;
    load_module("Socket");

#    debug "validating $host";
    # do a gethostbyname... it will use the system's own resolving facility
    if (!gethostbyname($host)) {
        debug "failed lookup of host $host!";
        return 0 if ($noerror);

        my $error = convert($msg{'MSG_LoginError'}, "Invalid hostname $host");
        set_status($error);
        return 0;
    }

    debug "$host validated";
    return 1;
}


sub do_pop_login
{
    my ($user,$p,$host,$do_uidl) = @_;

    debug "doing pop login user=$user pophost=$host";
    return undef unless ($user && $p && $host); # hopefully no zero names..

    # See if we currently have a $pop and if so what type it is.
    if ($pop)
    {
		debug "Have a pop object...";
		if ( ref($pop) ne "EMU::POP3" )
		{
		    undef $pop;
            $pop_connected = 0;
		}
    }

    debug "POP here";

    if ( my $c = find_connection('pop3', $host, $user, $p) )
    {
       $pop = $c;
    } 
    else
    {
    	unless ( $pop )
    	{
			my $timeout = $c{"tcp_timeout"} || 10;

			debug "trying new POP connection to $host";
			$pop = new EMU::POP3 ($host,Port=>$pop_port,Timeout=>$timeout);
			# debug "defined pop" if ($pop);

			return undef if (!$pop);

			$pop_connected = 1;
			debug "created new pop object, host $host";
		}
		# debug "And here $host";

     	CHECK_POP_LOGIN:
		{
			my $apop_valid = 1;

			if (bool($c{"use_apop"}))
			{
				my $banner = (${*$pop}{'net_pop3_banner'} =~ /(<.*>)/)[0];
				debug "Banner for APOP is $banner";
   	    		if (!($banner))
   	    		{
   	        		debug "Configured for APOP but Not APOP capable!";
					$apop_valid = 0;
				}
				elsif (!($pop->apop($user,$p)))
				{
   	        		debug "APOP Failed. $user $p";
					# APOP Capable, but login failed
					$pop_connected = 0;
					my $timeout = $c{"tcp_timeout"} || 10;
					$pop = new EMU::POP3 ($host,Port=>$pop_port,Timeout=>$timeout);
					debug "apop $host";

					return undef if (!$pop); #whoa! Trouble!
					debug "apop $user $host $p";
					$apop_valid = 0;
					$pop_connected = 1;
				}
			}
			else
			{
				$apop_valid = 0;
			}

			if (!$apop_valid)
			{
				debug "attempting login...";
				$pop->user($user) if $pop;
				my $stuff = $pop->pass($p) if $pop;

				my $total = ($pop->popstat)[0];
				debug "total $total";
				debug "stuff is $stuff";
				if ($stuff eq undef) 
				{
					undef $pop;
					return 0; 
				}
			}
		}

		# Lets store our account info.
		${*$pop}{user} = $user;
		${*$pop}{password} = $p;
		${*$pop}{host} = $host;
	}
    
    debug "do_uidl $do_uidl";
    if ($do_uidl && $pop)
    {
		my $uids = $pop->uidl;
		if ($uids eq undef) {
			debug "can't do uidl!";
			$folderdb{"nouidl"} = 1;
		}
        else
        {
			undef %poplist;
			%poplist = %{$uids} if $uids;
			$folderdb{"nouidl"} = 0;
		}
    }

    store_connection($pop, 'pop3', $host, $user, $p);

    debug "logged into pop successfully";
    return 1;
}

sub get_list_imap_recent
{
    # This is similar to get_list_imap, except it only returns the UIDs who have 
    # uids greater than the last one we have found. Should be faster than getting everything.

    # Get a folder listing from an IMAP server
    my ($host, $u, $p, $fold) = @_;

#    debug "H: $host U: $u p: $p Fold: $fold";

    my ($user) = $u;

    unless ($host)
    {
	($user, $host) = split(/\@/, $u);
    }

    my $uid_validity = &do_imap_login($user,$p,$host,$fold,1) || return undef;

    &set_folder_validity($fold,$uid_validity);

    my $last_uid = get_last_uid($fold);

    my (@uids) = @{$pop->list_since($last_uid)};
    if (! $pop->{_errcode}) {
        # we have an error...
        set_status($pop->{errcode});
        return 0;
    }

    my $size = $#uids;
    $size++;

#    debug "size $size";

    my $tempfold;
    if ($folder eq $fold)
    {
        $tempfold = \%folderdb;
    } else
    {
        # open folder!
        my $tempfolder = process_fold_type($fold);
        if ( $ELocks->lock_create("$homedir/folders/$tempfolder", \$tempfold, {mode => 'write', nb => 1}) )
        {
            tie %$tempfold, $db_package, "$homedir/folders/$tempfolder", O_CREAT|O_RDWR, 0660;
        } else
        {
            debug "can't open folder $fold db for write, give up";
            return 0;
        }
    }

    # Update the folderdb
    my %msgs = map { $_ => 1 } split(':', $tempfold->{'messages'}), map { $uid_validity.$_ } @uids;
    $tempfold->{'messages'} = join (':', keys %msgs);
    
                                                                        
    my ($total_messages) = process_msg_list(\@uids,$uid_validity,"imap",$fold,$u,$p,0,$tempfold);

    if ($folder ne $fold)
    {
        # close this temp db, opened above in this func
        untie %$tempfold;
        $ELocks->lock_remove(\$tempfold);
    }
    debug "TOTAL MSGS: $total_messages";

    #Save Last Next UID
    save_recent_uid_db($fold,get_recent_uid($pop,$fold));
    
    return ($total_messages + 1);
}

sub get_last_uid
{
    # What's the greatest UID we have in our data cache?
	my ($fold) = @_;
	my ($msgs,$validity);
	
	if ($folder eq $fold)
	{
    	$msgs = $folderdb{'messages'};
    	$validity = $folderdb{'uidvalidity'};
    }
    else
    {
    	# open folder db to get last uid
    	my %tempfold; my $tempfold = process_fold_type($fold);
		if ( $ELocks->lock_create("$homedir/folders/$tempfold", \%tempfold, {mode => 'read', nb => 1}) )
		{
			tie %tempfold, $db_package, "$homedir/folders/$tempfold", O_RDONLY, 0660;
			$msgs = $tempfold{'messages'};
			$validity = $tempfold{'uidvalidity'};
			untie %tempfold;
			$ELocks->lock_remove(\%tempfold);
		}    	
    }
    
    if ($msgs =~ /:$validity(\d+):?$/) {
        return $1;
    } else {
        return;
    }
}

sub get_list_imap
{
    # Get a list of ID's for a folder.  If we can be
    # smart about it, and only get the differences from the
    # last time, that's a good thing.  Otherwise, we'll 
    # Get ALLLL the ID's

    my ($host, $u, $p, $fold) = @_;

    my $db_validity = get_folder_validity($fold);
    
    my $messagemap = '';
    if ($folder ne $fold)
    {
    	# open folder db to get messages
    	my %tempfold; my $tempfold = process_fold_type($fold);
		if ( $ELocks->lock_create("$homedir/folders/$tempfold", \%tempfold, {mode => 'read', nb => 1}) )
		{
			tie %tempfold, $db_package, "$homedir/folders/$tempfold", O_RDONLY, 0660;
			$messagemap = $tempfold{'messages'};
			untie %tempfold;
			$ELocks->lock_remove(\%tempfold);
		} else {
		    debug "FAILURE GETTING LOCK";
		}
    } else {
        $messagemap = $folderdb{"messages"};
    }
    
    my $db_exists = $messagemap =~ tr/:/:/;
    if ( index($messagemap, ':') )
    {
		# stored as: 1:2:3.  Special cases, when 0, and 1
		$db_exists++;
    }

    debug "Attempting to login...";
    my $server_validity = &do_imap_login($u, $p, $host, $fold, 1) || return undef;

    my $server_last_uid = (sort { $b <=> $a } @{$pop->list_uids})[0];
    my $db_last_uid = get_last_uid($fold);

    my ($server_exists) = $pop->{"exists"};

    my ($path);

    #debug "validity : d $db_validity s $server_validity ; exists: d $db_exists s $server_exists ; last: d $db_last_uid s $server_last_uid";

    # Decide which route to chose: full (2), recent only (1), or none (0)

    if ($db_validity ne $server_validity)
    {
		# If UID's don't match that means we need a full re-sync
		debug "chosing path: UID's don't match - $db_validity and $server_validity";
		$path = 2;
    }
    elsif ($server_exists < $db_exists)
    {
		# Possibly some messages got deleted?  We don't know which. better get them all
		debug "chosing path: Possibly some messages got deleted?";
		$path = 2;
    }
    elsif ($query->param("flush"))
    {
    	# force us to reload no matter what.
    	debug "chosing path: force to reload";
		$path = 2;
    }
    elsif ($db_last_uid < $server_last_uid)
    {
    	debug "chosing path: new messages only";
		# We have new messages only.  OK to do it quick.
		$path = 1;
    }
    elsif ($db_last_uid == $server_last_uid)
    {
    	debug "chosing path: no recent messaged, our db is good";
		# We have no recent messages, and our databases match
		$path = 0;
    }
    else
    {
    	debug "chosing path: other cases, full fetch";
		# Other cases?  If so, do a full fetch
		$path = 2;
    }

    debug "Chosing Path $path";

    if ($path == 2)
    {
		# Complete Listing
		return get_list_imap_full($host, $u, $p, $fold);
    }
    elsif ($path == 1)
    {
		# Recent (NEW) only listing
		return get_list_imap_recent($host, $u, $p, $fold);
    }
    else
    {
		# Reflexive listing
		my ($db_exists) = $folderdb{"messages"} =~ tr/:/:/;
		return $db_exists+1;
    }
}

sub get_list_imap_full
{
    # Get a folder listing from an IMAP server
    my ($host, $u, $p, $fold) = @_;
    
    my ($user) = $u;
	($user, $host) = split(/\@/, $u) unless ($host);

    debug "Attempting to login...";
    my $uid_validity = do_imap_login($user, $p, $host, $fold, 1) || return undef;
	set_folder_validity($fold,$uid_validity);
#   debug "UID VALIDITY: $uid_validity";

    my @uids = @{$pop->list_uids};
    unless ( $pop->{_errcode} )
    {
        # we have an error...
        set_status($pop->{errcode});
        return 0;
    }

    my $size = scalar @uids;
    debug "size of uid list is $size";

    my $tempfold;
    if ($folder eq $fold)
    {
        $tempfold = \%folderdb;
    } else
    {
        # open folder!
        my $tempfolder = process_fold_type($fold);
        if ( $ELocks->lock_create("$homedir/folders/$tempfolder", \$tempfold, {mode => 'write', nb => 1}) )
        {
            tie %$tempfold, $db_package, "$homedir/folders/$tempfolder", O_CREAT|O_RDWR, 0660;
        } else
        {
            debug "can't open folder $fold db for write, give up";
            return 0;
        }
    }

    # Update the folderdb
    $tempfold->{'messages'} = join (':', map { $uid_validity . $_ } @uids);

    my $total_messages = process_msg_list(\@uids, $uid_validity, "imap", $fold, $u, $p, 1, $tempfold); # 1 means process all messages in folder before search

    if ($folder ne $fold)
    {
        # close this temp db, opened above in this func
        untie %$tempfold;
        $ELocks->lock_remove(\$tempfold);
    }

    debug "TOTAL MSGS: $total_messages";

    #Save Last Next UID
    save_recent_uid_db($fold, get_recent_uid($pop, $fold));
    
    return ($total_messages + 1);
}


sub process_msg_list
{
    my ($uids, $uid_validity, $protocol, $fold, $u, $p, $process_all, $tf) = @_;
    my ($rh_decomposed);
    
    my $tempfold;
    if ($tf) {
        $tempfold = $tf;
    } else {
        if ($folder eq $fold)
        {
   	    $tempfold = \%folderdb;
   	}
   	else
   	{
            # open folder!
            my $tempfolder = process_fold_type($fold);
            if ( $ELocks->lock_create("$homedir/folders/$tempfolder", \$tempfold, {mode => 'write', nb => 1}) )
            {
                tie %$tempfold, $db_package, "$homedir/folders/$tempfolder", O_CREAT|O_RDWR, 0660;
            } else
            {
                debug "can't open folder $fold db for write, give up";
                return 0;
            }
        }
    }

    my ($key, $msgs, $been, $total_messages, @sorted);
    my ($delay_max, $interval, $msg_process_min, $msg_process_max);
    my ($header, %h);
    my $filtered = 0;

    my $num_messages = $pop->{"exists"};

    return undef unless $num_messages;

    my $dbfold = remove_fold_prefix($fold);

    my $uid_ix = 0;
    my $max_messages = get_max_messages();

    GET_DATA_FROM_SERVER:
    {
		# Execute the appropriate command to go out and get the msgs we want
		@sorted = sort {$a <=> $b} @$uids;

		my ($min,$max);

      	GET_SLICE_EXTREMITIES:
		{
	    	# If this is a sorted case, we have to do the whole list.
	    	my $sort_type = $query->param("sorttype");
	    	if ( $sort_type && $sort_type !~ /select|default/i || $process_all )
	    	{
				$msg_process_max = $#sorted;
				$msg_process_min = 0;

				debug "Doing a full extraction cibomatto";
	    	}
	    	else
	    	{
				# We can make it quick!  Just process our screen
				my $current_page = $v{"current_page"} || 1;
				$msg_process_max = ($#sorted + 1) - (($current_page - 1) * $max_messages) ;
				$msg_process_max = $#sorted if ($msg_process_max > $#sorted);
				$msg_process_min = ($#sorted + 1) - ($current_page * $max_messages) ;
				$msg_process_min = 0 if ($msg_process_min < 0); 
				debug "sorted is $#sorted current page is $current_page min is $msg_process_min, max is $msg_process_max, current id $uid_ix";
	    	}
	    
	    	$min = $sorted[$msg_process_min];
	    	$max = $sorted[$msg_process_max];

		    $min = 0 if $min < 0;
		    $max = 0 if $max < 0;

#		    debug "Doing a msg download with min $min to max $max cibo";
		}

		debug "Suggesting to get from $min to $max";

		# push spam header to custom headers and then shift it again
		# we need this dirty hack to make sure get_msg_quickview grabs this header
		# and then we can decide whether we should filter it
		push(@custom_headers, $c{'spam_determinative_header'}) if ($c{'spam_determinative_header'});
		# Get all the data we need from the IMAP server in one command.
		# Normal sorting this is OK, otherwise, weirdness.
		$msgs = $pop->get_msg_quickview($min,$max);
		pop(@custom_headers) if ($c{'spam_determinative_header'});
    }

	PROCESS_DATA:
    {
		# Now that we have our data, let's add it to the appropriate data store

		debug "zoo min to max: $msg_process_min .. $msg_process_max";

        my $wait_printed=0;
        $v{"wait_interval"} = get_wait_interval(scalar(@sorted[$msg_process_min..$msg_process_max]));

        $v{"wait_action"} = $msg{"WAIT_CheckHeaders"};
        print_progress_new(0,1);

		foreach my $uid (@sorted[$msg_process_min..$msg_process_max])
		{
	    	debug "ZUID: $uid";
	    	$total_messages++;

			PROGRESS_METER:
			{
				print_progress_new(1);
				$v{"wait_action"} = convert($msg{"WAIT_ProcessedMsgs"}, $v{"wait_count"})
					if ($v{"wait_count"} % $v{"wait_interval"} == 0)
            }

            debug "Ready to decide: $uid_validity.$uid $fold $foldmap{$uid_validity.$uid} $folderdb{$uid_validity.$uid} $folderdb{$uid_validity.$uid.':stat'} $folderdb{$uid_validity.$uid.':date'} $folderdb{$uid_validity.$uid.':downloaded'}";
            # if we've already processed the message, return... unless
            # we're supposed to download the message.
            next if (
                    # gotta download and already downloaded
                    (bool($c{"download_full_bodies"}) &&
                    $tempfold->{$uid_validity.$uid.":downloaded"}) ||

                    # or we already have sufficient info for the msg
	            	(
	            	$foldmap{$uid_validity.$uid} eq $fold &&
                    $tempfold->{$uid_validity.$uid} &&
                    defined($tempfold->{$uid_validity.$uid.":stat"}) &&
                    $tempfold->{$uid_validity.$uid.":date"} &&
                    -e "$homedir/messages/$uid_validity$uid")
                    );

            debug "downloaded ? ".$folderdb{$uid_validity.$uid.":downloaded"};
            debug "continuing with processing $uid_validity$uid";

			FOLDER_SETUP:
			{
				# make sure to set foldmap to the correct folder
				$foldmap{$uid_validity.$uid} = $dbfold;
	    	}

	  		FLAGS:
	    	{
				# First set message status (FLAGS)

				my $status;
				my $flag;
	    		$flag = join ('', @{$msgs->{$uid}->{"FLAGS"}})
	    			if ($msgs->{$uid}->{"FLAGS"});
#				debug "flags $flag";

				$status = STAT_READ if ($flag =~ /\\Seen/i);
				$status = STAT_ANS  if ($flag =~ /\\Answered/i);
				$status = $status || STAT_NEW;
		
				# Set in EMU's database
				$tempfold->{$uid_validity.$uid.":stat"} = $status;

				debug "status ".$uid_validity.$uid." ".$tempfold->{$uid_validity.$uid.":stat"};
	    	}


	  		SIZE:
	    	{
				# Set the size of the message
				$tempfold->{$uid_validity.$uid.":size"} = $msgs->{$uid}->{"RFC822.SIZE"};
#				debug "size ".$folderdb{$uid_validity.$uid.":size"};
	    	}

	  		HEADER:
	    	{
				$header = $msgs->{$uid}->{"HEADER"};
				$header =~ s/\)\n$/\n/;

				unless ($header)
				{
		    		debug "Unable to decompose $uid_validity$uid: (can't get header)\n";
		    		next;
				}
		
				# Decompose it into parts return in hash
				$rh_decomposed = decompose_header(\$header,$uid_validity.$uid);
				unless ($rh_decomposed)
				{
		    		debug "Unable to decompose $uid_validity$uid: (decompose failed)\n$header";
		    		next;
				}
		
				# make the key safe to enter into the database
				$uid = safe(':', $uid);
		
				ADD_HEADER_TO_DB:
				{
					last unless $rh_decomposed;
		    		# Add keys to userdb
		    
		    		while ( my ($keyname, $keyval) = each(%$rh_decomposed) )
		    		{
						trim(\$rh_decomposed->{$keyname}); # get rid of extra spaces and newlines
						$tempfold->{$uid_validity.$uid.":$keyname"} = $keyval;
#						debug $uid_validity.$uid.":$keyname = ".$folderdb{$uid_validity.$uid.":$keyname"};
		    		}
				}
			}

	  		EMU_DB_UPDATE:
	    	{
				# Set location of message, let vault know we have it.
				$tempfold->{"$uid_validity$uid"} = "remote_imap"; 
				$tempfold->{"$uid_validity$uid:folder"} = $dbfold; 
	    	}

	    	my $moved=0;
	    	my $message = "$uid_validity$uid";

	    	# Do we need to get the whole message now?
	    	download_msg($message, $fold, 1)
	    		if ($c{"download_full_bodies"} && !$c{"$message:downloaded"});
			$v{"filtered to"} = 0;
        	debug "moved ? $moved";
			if ( has_spam_header("$uid_validity$uid") )
			{
				debug "message $uid_validity$uid is SPAM. filtering it to hell";
				filter_spam_header("$uid_validity$uid", $foldmap{"$uid_validity$uid"});
			}   	
		}
	}

	my $substatus = '';
  	DO_REALTIME_FILTER:
    {
        debug "realtime filter? ".$userdb{'options.do_realtime_filter'};
        last if ( !$c{"do_realtime_filter"} && !$userdb{'options.do_realtime_filter'} ); 
        $substatus = filter_messages_imap("RECENT");
    }

    if ($v{"filtered to"} > 0) 
    {
#		debug "expunging, select folder $folder";
		$pop->select($folder) if ($pop && $pop->{folder} ne $folder);
        $v{"wait_action"} = convert($msg{"WAIT_FilteredNum"}, $v{"filtered to"});
        $pop->expunge();
        print_progress_new(0,1);
        set_status( convert($msg{'MSG_Filtered_Num'}, $v{"filtered to"}) . $substatus );
    }

    debug "total_messages $total_messages num4 $num_messages";

    if (!$tf) { 
	if ($folder ne $fold)
	{
		# close this temp db, opened above in this func
		untie %$tempfold;
		$ELocks->lock_remove(\$tempfold);
	}
    }

    return $num_messages;
}

sub get_msgs_in_hash
{
    my $msgs = shift;

    my %hash;

    map    {    debug "$_ !"; $hash{$_} = 1;    }  (split(':', $msgs));

    return \%hash;
}

sub filtered
{
    my ($uid) = @_;
    my $flag;
    
    # 08/24/98: make it safe
    $uid = safe(':', $uid);

    my $fold = remove_fold_prefix($folderdb{"$uid:folder"});
#    debug "fold $fold  folder $folder";
    $flag = ($fold ne remove_fold_prefix($folder)) ? 1 : 0;

    return $flag;
}


sub detect_cyrillic {
    my (@lines) = @_;
    my $convert_cyrillic = 0;
    my $convert_to = $c{"convert_cyrillic_to"} || "win";
    my @convert_from = split(' ',$c{"convert_cyrillic_from"});

    @convert_from = ("koi8","iso-8859-5") if (!scalar(@convert_from));
    my $srcenc;

    debug "converting from cyrillic";
    load_module("Lingua::DetectCharset");
    load_module("Convert::Cyrillic");
    $srcenc = Lingua::DetectCharset::Detect(@lines);
    debug "src encoding is $srcenc";

    foreach my $cyr_encoding (@convert_from) {
        if ($srcenc =~ /$cyr_encoding/i) {
            $convert_cyrillic = 1;
            last;
        }
    }

    # if we havent yet determined conversion is necessary, double check
    # for a Content-Type
    if (!$convert_cyrillic && scalar(my @tmp = (grep /^content-type/i, @lines)) > 0) {
        $convert_cyrillic = 1 if ($tmp[0] =~ /koi8-r/i);
        debug "detected koi8-r via Content-Type";
    }

    debug "convert_cyrillic=$convert_cyrillic, src=$srcenc, to=$convert_to";
    return($convert_cyrillic, $srcenc, $convert_to);
}


sub save_header {
    my ($header,$uid) = @_;

  CHANGE_DATA_TYPE:
    {
	# Make sure we have $header in an ARRAY REF
	my @h = ();
	
	if (ref ($header) eq "SCALAR")
	{
	    debug "Changing $uid, $$header to ARRAY";
	    (@h) = split(/\n/,$$header);
	    map { $_ .= "\n" } @h;
#	    map { debug ("look: $_") } @h;
	    $header = \@h;
	}
    }

    my @header = @$header if ref $header;
    my $srcenc = "";
    my $convert_to = "";
    my $convert_cyrillic = 0;

    ($convert_cyrillic, $srcenc, $convert_to) = detect_cyrillic(@header)
        if ($licensed{"convert_cyrillic"} && $c{"convert_cyrillic"});

#    debug "srcenc=$srcenc, convert_to=$convert_to";

    debug "saving header for $uid";
    open (HEAD, ">$homedir/messages/$uid");

    my $header_ok = 0;

    foreach my $line (@header)
    {
        next if (!$header_ok && ($line =~ /^\s/ || 
                $line =~ /^>/ || $line !~ /^[a-zA-Z]/ || $line !~ /:/) );

        if ($convert_cyrillic) { 
            $line = Convert::Cyrillic::cstocs($srcenc, $convert_to, $line)
        }

	print HEAD $line;
        $header_ok = 1;
    }

    close HEAD;
}


sub decompose_header
{
 # Takes a reference to an array of header lines
 # Returns a hash to be put into the userdb header
    my ($header, $uid) = @_;

	if (!-e "$homedir/messages/$uid")
	{
    	save_header($header, $uid);
    	debug "header saved";
    }

    my $h_ref = header_from_file($uid);

    return $h_ref || {};
}


sub header_from_file 
{
    my ($uid) = @_;

    my $fold = $foldmap{$uid};

    # if the foldmap entry is bogus, then let's assume folder is $folder
    # and set it accordingly.
    $fold = $foldmap{$uid} = $folder unless $fold;

    debug "$uid appears to be in folder '$fold'";

    my ($head);

  CHECK_DISK:
    {
	unless (-e "$homedir/messages/$uid")
	{
	    if (!download_msg($uid)) {
	        error "Couldn't download message $uid!";
                debug "Failed to download $uid!";
                set_status($msg{'ERR_MSGNotInServer'});
                return undef;
            }
	}
    }
         
    debug "getting header from file $uid";
    $head = MIME::Head->from_file("$homedir/messages/$uid");

    if ($head eq undef)
    {
	error "Couldn't create MIME::Head object for $homedir/messages/$uid: $!";
	debug "Couldn't create MIME::Head object for $homedir/messages/$uid: $!";
	set_status($msg{'ERR_MimeHeadParse'});

        ## HM 09/28/00 - Ack, this isn't good, causing an infinite loop and double page prints. Just return.
	#go_index();
	#cleanup();

	# 08/26/98: wasn't returning here!! gahh! 
	return undef;
    }

    # 08/27/98: decode it !
    $head->decode();

    my %h;

    $h{"replyto"} = $head->get('Reply-To'); $h{'replyto'} =~ s/\r?\n$//;
    $h{"subj"} = $head->get('Subject'); $h{'subj'} =~ s/\r?\n$//;
    $h{"from"} = $head->get('From') || $msg{"MSG_NoFrom"}; $h{'from'} =~ s/\r?\n$//;
    $h{'cc'}   = $head->get('Cc'); $h{'cc'} =~ s/\r?\n$//;
    $h{'bcc'}  = $head->get('Bcc'); $h{'cc'} =~ s/\r?\n$//;
    $h{'to'}   = $head->get('To'); $h{'to'} =~ s/\r?\n$//;
    $h{'date'} = $head->get('Date'); $h{'date'} =~ s/\r?\n$//;
    $h{'ct'}   = $head->get('Content-type'); $h{'ct'} =~ s/\r?\n$//;
    $h{'pri'}  = $head->get('Priority') || $head->get('X-Priority') || "normal"; $h{'pri'} =~ s/\r?\n$//;
    $h{'messageid'}  = $head->get('Message-ID'); $h{'messageid'} =~ s/\r?\n$//;
    $h{'mdn'}  = $head->get('Disposition-Notification-To'); $h{'mdn'} =~ s/\r?\n$//;
    $h{'size'} = -s "$homedir/messages/$uid" if (!($folderdb{$uid.":size"}));

    # Go thru list of customized headers, if any
    my $head_ix=0;
    foreach my $chead (@custom_headers) {
#        debug "checking for custom header $chead";
        $h{$chead} = $head->get($chead) if ($head->get($chead));
#        debug "h{$chead} = $h{$chead}";
    }

    # Message Status
    #
    # To determine a message's status we read in both the 'Status' and 
    # the 'X-Status' field.
    #
    # If the 'Status' field contains an "O" then the message is not new to 
    # this session (it may be unread but it isn't a brand-spanking new 
    # message). If the 'Status' line has an "R" then the message has been 
    # retrieved and EMUmail should register it as such (not new). If
    # the 'Status' line is either blank or set to 'U' then the message hasn't 
    # been read and is new.
    #
    # The 'X-Status' line can be set to the following:
    #  "A"  =>  Answered
    #  ""   =>  Read
    #  "N"  =>  New
    #  "D"  =>  Deleted (?)
    #
    # The 'Status' line always takes precedence over the 'X-Status'.  
    # We only use the 'X-Status' line to see if the message has been 
    # answered to yet.
    #
    # EMUmail has the following message statuses:
    #  STAT_READ  =>  The message has been read
    #  STAT_NEW   =>  The message has not been read
    #  STAT_ANS   =>  The message has been answered to
    #
  MSG_STATUS:
    {
	my ($status, $xstatus, $tmpstatus);
        $status = "";

#        debug "getting status from message header";
#        # HM 09/17/00 - Hrm, lets check the protocol for this message's folder instead
#        if ( $protocol !~ /imap/i ) 
         debug "folder $fold protocol ".$userdb{"folder:$fold:protocol"};
         if ( $userdb{"folder:$fold:protocol"} !~ /imap/i ) 
	 {

	    if ($tmpstatus = $head->get('Status'))
	    {
	        # check if the message has been read
	        if (index(uc($tmpstatus), "R") != -1)
	        {
		    $status = STAT_READ;
	        }
	    }

	    if ($xstatus = $head->get('X-Status'))
	    {
	        # if the xstatus says the message has been answered set the status thusly
	        # THUSLY?
	        $status = STAT_ANS if (index(uc($xstatus),"A") != -1);
	    }

	    $status = $status || STAT_NEW;

            debug "setting status to $status, protocol $protocol";
	    $h{'stat'} = $status;
        }
    }

    return \%h;
}


sub commas
{
    local($_) = @_;
    1 while s/(.*\d)(\d\d\d)/$1,$2/;
    $_;
}

sub get_size_mailboxes
{
    # This sub is an interface for getting the size of a user's mailbox
    #  Defined in the config file what to "count": { EMUmail files, Remote Server's, or Sum of both }
    # Note: at this time only counting EMUmail files is functional.
    my ($max) = @_;

    my ($used);

#    debug "getting usage for $homedir, max is $max";

my $processed=0;
    if ($c{"quota_type"} =~ /emumail/i)
    {
	load_module("File::Find",0,'find');

	# tally up the user's total usage
	my $subref = 
            sub { my $size = (-f $File::Find::name) ? -s $File::Find::name : 0;
                  $processed++;
                  $used += $size;
                  return $used if ($used > $max);
                };
	    
	find(\&$subref, "$homedir/messages", "$homedir/files");
    }

    debug "processed $processed files, total usage is $used";
    $used = $used || 0;

    return ($used);

}

sub quota_check
{
    my $flag = shift;

    my ($used,$uhost,$uname,$allowed, $stat);

    ($uname,$uhost) = (split('@', $user_name, 2));
#    debug "checking quota for $user_name... quota type is ".$c{"quota_type"};

    my $quota_type = $c{"quota_type"} || "emumail";
    if ($quota_type !~ /emumail/i) {
	load_module("EMU::Custom");

	debug "Evaling quota_check($uname)";
	eval
	{
	    $used = &EMU::Custom::quota_check($uname);
            debug "$used";
            if ($used =~ /:/) {
                ($stat, $v{"quota_allowed"}, $v{"quota_used"}, $v{"quota_pct"}) = split(/:/, $used);
                debug "allowed $v{'quota_allowed'} used $v{'quota_used'}";
            }
	};

        return;

    }

    if ($uname eq "" || $uname eq undef || $homedir eq "" || $homedir eq undef) {
        $over_quota = $v{"over_quota"} =0;
        return 0;
    }

    $v{"quota_allowed"} = &get_quota($uname,$uhost);
    $used = $v{"quota_used"} = $v{"quota_allowed"} >= 0 ? &get_size_mailboxes($v{"quota_allowed"}) : 0;

    debug "quota_allowed ".$v{"quota_allowed"}." used $used";

    my $q_allowed = ($v{"quota_allowed"} >= 1) ? ($v{"quota_allowed"}/1024.0) : $v{"quota_allowed"};
    $q_allowed =~ s/^(\d+)\.(\d)(\d)(.*)$/$1.$2$3 kB/;
    my $q_used = ($v{"quota_used"} >= 1) ? ($v{"quota_used"}/1024.0) : $v{"quota_used"};
    $q_used =~ s/^(\d+)\.(\d)(\d)(.*)$/$1.$2$3 kB/;
    write_tmp("allowed", $q_allowed);
    write_tmp("used", $q_used);

    if ( ($v{"quota_allowed"} > 0) && ($v{"quota_allowed"} < $used) && (!($flag)) )
    {
	### MM: Need to set $quota_msg, a local var, not $quota, a GLOBAL!!!
	### 07/27/98
	my $quota_msg = commas($v{"quota_allowed"});

	$over_quota = 1;

	return -1;
    }
    else
    {
	# 05/28/98: we aren't over quota if we get here
	$over_quota = $v{"over_quota"} = 0;
    }

    return $used;
}


sub get_quota
{
    my ($user,$host) = @_;

    $user = lc($user);
    $host = lc($host);

    my $allowed;

    #debug "user is $user host is $host";

debug "quota_source ".$c{"quota_source"}." userdb ".$userdb{"quota"};
    if ($c{"quota_source"} =~ /custom/i && !$userdb{"quota"}) {
        # a "custom" quota source means we're getting the quota allowed value
        # from a source other than site.emu. So we do it in Custom.pm and
        # assign the quota value to userdb.

        load_module("EMU::Custom");
	debug "Evaling get_quota($user\@$host)";
        my $q;
	eval
	{
	    $q = &EMU::Custom::get_quota("$user\@$host");
            debug "got quota of $q from Custom::get_quota";
        };

        if ($q eq undef) {
            delete($userdb{"quota"});
        }
        else {
            $userdb{"quota"} = $q;
        }
    }

    # Look first for user, then full popserver, then default, or NO quota (0)
    # Can't do with || because zero is valid.

    if ($c{"quota_source"} =~ /custom/i && defined($userdb{"quota"})) {
        $allowed = $userdb{"quota"};
    }
    elsif (defined($c{"quota_".$user."\@$host"}))
    {
	$allowed = $c{"quota_".$user."\@$host"};
    }
    elsif (defined( $c{"quota_\@$host"}))
    {
	$allowed =  $c{"quota_\@$host"};
    }
    elsif (defined( $c{"quota_default"}))
    {
	$allowed = $c{"quota_default"};
    }
    else
    {
	$allowed = 0;
    }

    return $allowed;
}


# filter message -- filters a single message
#
# go through the message list for the current folder, check each message to see
# if it meets any of the filters in place, and if so perform whatever action has
# been specified.
#
#  $digest  = the md5sum of the message to filter
#  $bRemove = flag. true means remove the message from its current folder when
#             filtered.
sub filter_message_local
{
    my ($digest) = @_;

    my ($ent, $i);
    my $bFilter = 0;            # will this message be filtered?
    my $filterto;               # what folder to filter this message to
    my $filtertype;             # type of the filter: message HAS or message DOESN'T have
    my $filter;                 # the actual filter that fits in the regex

    return if (!$userdb{"filters.total"});

    debug "entering filter_message; folder is $folder";

    return undef unless $digest;
    return 0  if ($trash_bin && ($folder eq $trash_folder));

    # let's allow for filtering only on mailboxes and the inbox
    # return 0 if (!$userdb{"folder:$folder:external"} && $folder ne $inbox);

    debug "filtering $digest";
    

  	MAIN_FILTER:
    for ($i = 1; $i <= $userdb{"filters.total"}; $i++)
    {
		do { debug "skipping filter $i -- is empty" and next } unless ($userdb{"filters.type$i"} != FILTER_OFF); # skip empty ones
		debug "Going through filter $i...";

		# set the name of the folder that we're filtering to
		$filterto = $userdb{"filters.action$i"};
		debug "filterto=$filterto";

		# the regex to filter by. if the user has specified that they 
        # want this to be a perl5 regex
		# then don't quote it, otherwise quote the meta characters.
		$filter = $userdb{"filters.bRegex$i"} ? $userdb{"filters.data$i"} : quotemeta($userdb{"filters.data$i"});

		debug "filter=$filter";

      	FILTER_BODY:
        {
	    	last if ($userdb{"filters.type$i"} != FILTER_BODY);
	    	debug "Filtering body...";
            # do we have the body to look at?
            if (!$folderdb{"$digest:downloaded"}) {
                if (!download_msg($digest)) { 
                    set_status($msg{'ERR_MSGNotInServer'});
                    return 0;
                }
            }

			# 03.01.2003 RB [start]
			# poor man body filtering...
	    	local $folder;
	    	my $message = $digest;
	    	my $rfc822attach = 0;
	    	if ($licensed{"rfc822_attach"} && $message =~ /(^.+)\%\%RFC822\%\%/) {
		        $message = $1;
		        $rfc822attach = 1;
	        	debug "This is an RFC822 attachment from message $message...";
	    	}
	
	    	my $parser = new MIME::Parser;
	    	$parser->ignore_errors(1);
	    	$parser->decode_headers(1); 
	    	$parser->extract_uuencode(1);
	    	$parser->output_dir("$homedir/tmp");
	    	$parser->output_prefix("tmp$$");
	    	$parser->extract_nested_messages(0);
	    	my $msgfile = ($rfc822attach) ? "$homedir/tmp/rfc822" : "$homedir/messages/$message";
	    	my $entity = $parser->parse_open($msgfile);
	    
	    	my @viewable_messages = ();
	    	if (process_parts($entity, \@viewable_messages, [], [], 0, 0, $rfc822attach ? 'rfc822' : $message))
	    	{
	    		for my $vmsg (@viewable_messages)
	    		{
	            	# Since body is multiline, we first see if the filter string
	            	# exists, then only later decide on whether it's FILTER_CONTAINS
	            	$bFilter = $vmsg =~ /$filter/i;
	
		            debug "filter is $filter  buffer is $vmsg";
	            
		            if ($bFilter && $userdb{"filters.modifier$i"} == FILTER_CONTAINS)
	    	        {
	        	    	last MAIN_FILTER;	
	        	    	# this is needed, but makes trouble
	            		# $parser->filer->purge; 
	            	}
	    		}
	        	debug "no match in body...";
	        
		        # if we get here, then there was no match... if we're NOT
		        # doing FILTER_CONTAINS then it "becomes" a match!
		        # this is needed, but makes trouble
				# $parser->filer->purge;
				if (!$bFilter && $userdb{"filters.modifier$i"} != FILTER_CONTAINS)
	        	{
	        		# must reset so the filter action actually happens
	                $bFilter = 1;
	                last MAIN_FILTER;
			 	}
	    	}
	    	next MAIN_FILTER;    
			# 03.01.2003 RB [end]
		}


      	FILTER_HEAD:
        {
	    	last if ($userdb{"filters.type$i"} != FILTER_HEAD);
		    debug "Filtering head...";

            # used the cached in headers for searching:
            # :to :from :replyto :pri :ct :date :subj :cc :bcc

            my $all_header = $folderdb{"$digest:to"}      ." ". 
                             $folderdb{"$digest:from"}    ." ". 
                             $folderdb{"$digest:cc"}      ." ". 
                             $folderdb{"$digest:bcc"}     ." ". 
                             $folderdb{"$digest:subj"}    ." ". 
                             $folderdb{"$digest:replyto"} ." ". 
                             $folderdb{"$digest:pri"}     ." ". 
                             $folderdb{"$digest:date"}    ." ". 
                             $folderdb{"$digest:ct"};

		    $bFilter = ($userdb{"filters.modifier$i"} == FILTER_CONTAINS)
			    ? ($all_header =~ /$filter/i)
		    	: ($all_header !~ /$filter/i);

	    	# we've found it, exit this loop!
	    	last MAIN_FILTER if ($bFilter);
            next MAIN_FILTER;
		}

		FILTER_HEADER_FIELD:
        {
	    	# set the field that we will be checking
	    	$filtertype = "to" if ($userdb{"filters.type$i"} & FILTER_TO);
	    	$filtertype = "from" if ($userdb{"filters.type$i"} & FILTER_FROM);
	    	$filtertype = "subj" if ($userdb{"filters.type$i"} & FILTER_SUBJ);
	
		    debug "Filtering field $filtertype... message $filtertype is ".$folderdb{"$digest:$filtertype"};

		    # move to the next filter
	    	next MAIN_FILTER unless $filtertype;

	    	# filter the field. Compare the filter string with the contents
            # of the specific header field for this message.

	    	$bFilter = ($userdb{"filters.modifier$i"} == FILTER_CONTAINS)
		    	? ($folderdb{"$digest:$filtertype"} =~ /$filter/i)
		    	: ($folderdb{"$digest:$filtertype"} !~ /$filter/i);

            # The filter "to" is really built as a recipient filter, so
            # we should really include "CC" in it...
            if ($filtertype eq "to" && !$bFilter) {
	        $bFilter = ($userdb{"filters.modifier$i"} == FILTER_CONTAINS)
		        ? ($folderdb{"$digest:cc"} =~ /$filter/i)
		        : ($folderdb{"$digest:cc"} !~ /$filter/i);
            }

	    	# we've found it, exit this loop!
	    	last MAIN_FILTER if ($bFilter);
		}
    }
    
    debug "Out of main filter loop...folder = $folder and filterto is $filterto";

    # if we are supposed to filter this message...

    # Somehow the folder prefix is getting added to $folder. Temporarily remove it.
    my $f = $folder;
    $f = remove_fold_prefix($f);

    if ($bFilter && ($f ne $filterto))
    {
        my $savefolder = $f;
        $query->param(-name=>'d', -value=>$digest);
        $folder = $filterto;
        $v{"last_folder"} = $savefolder;

		debug "lf: $savefolder";

        # check for action, is this a garbage (simply delete)?
        my $garbage = $msg{"GARBAGE_Filter_Name"} || "GARBAGE";
        my $action = $c{"GARBAGE_Filter_Action"} || "Folder";
		
		$v{"filtered pool"} = [] if ( !exists $v{"filtered pool"} || ref $v{"filtered pool"} ne 'ARRAY' );
		
        if ($filterto eq $garbage && $action =~ /delete/i)
        {
            # also check trash action
            if ( $trash_bin )
            {
                debug "moving to trash...";
               	push @{ $v{"filtered pool"} }, convert($msg{'MSG_Filtered_Trash'}, $folderdb{"$digest:subj"})
               		if ( $v{"filtered to"} <= $c{'verbosefiltering_threshhold'} );
                move_msg(1,1,1);
            }
            else
            {
                push @{ $v{"filtered pool"} }, convert($msg{'MSG_Filtered_Deleted'}, $folderdb{"$digest:subj"})
					if ( $v{"filtered to"} <= $c{'verbosefiltering_threshhold'} );
                debug "eliminating message $digest";
                remove_from_folder($digest,$savefolder,1,1);
            }
        }
        else
        {
	    	push @{ $v{"filtered pool"} }, convert($msg{'MSG_Filtered_Moved'}, $folderdb{"$digest:subj"}, $filterto)
               	if ( $v{"filtered to"} <= $c{'verbosefiltering_threshhold'} );
            move_msg(0,1,1);
	    	debug "Filtered to $filterto: $digest from $folder";
        }

		$changed{$filterto} = 1 if ($filterto ne $inbox);

		$v{"filtered to"}++;
		my $fm = $v{"filtered to"};

		my $substatus = (scalar @{ $v{"filtered pool"} }) ? "<br>\n" . join("<BR>\n", @{ $v{"filtered pool"} }) : '';
		$substatus .= "<br>\n" . $msg{'MSG_Filtered_TooMany'}
			if ( $v{"filtered to"} > $c{'verbosefiltering_threshhold'} );
		set_status( convert($msg{"MSG_Filtered_Num"}, $fm) . $substatus );
        $folder = $savefolder;
		return 1; # successfully filtered
    }

    debug "Message not filtered.";
    return 0; # we didn't filter this message
}


sub add_to_delimeted_scalar
{
    my ($scalar,$element) = @_;

#    $scalar = "$scalar\:$element";
    # we should really add it to the head of the list, that's how msgindex
    # displays it...
    $scalar = "$element:$scalar";
    $scalar =~ s/^://;

    return $scalar;
}

sub del_from_local
{
    my ($uid, $del_file, $fold) = @_;

    # Remove file from local cache
    unlink "$homedir/messages/$uid" if ($del_file); 

    $fold = $folder if (!$fold);
    debug "deleting $uid from folder $fold";

    # long list below, but much faster than doing a grep on file-based hash
    delete($folderdb{"$uid"});
    delete($folderdb{"$uid:replyto"});
    delete($folderdb{"$uid:subj"});
    delete($folderdb{"$uid:from"});
    delete($folderdb{"$uid:cc"});
    delete($folderdb{"$uid:bcc"});
    delete($folderdb{"$uid:to"});
    delete($folderdb{"$uid:date"});
    delete($folderdb{"$uid:pri"});
    delete($folderdb{"$uid:stat"});
    delete($folderdb{"$uid:folder"});
    delete($folderdb{"$uid:nouidl"});
    delete($folderdb{"$uid:downloaded"});
    delete($folderdb{"$uid:size"});
    delete($folderdb{"$uid:password"});
    delete($folderdb{"$uid:hostname"});
    delete($folderdb{"$uid:username"});
    delete($folderdb{"$uid:extra_fold"});
    delete($folderdb{"$uid:external"});
    delete($folderdb{"$uid:email"});
    delete($folderdb{"$uid:ct"});
    delete($folderdb{"$uid:mdn"});
    delete($folderdb{"$uid:mdn-sent"});
    delete($folderdb{"$uid:messageid"});


    foreach my $chead (@custom_headers) {
        $chead =~ s/\n//;
        $chead =~ s/\s//g;
        delete($folderdb{"$uid:$chead"});
    }

    delete($foldmap{$uid});
    return 1;
}

sub add_to_folder
{
    my ($uid, $fold_name, $store, $msg_status) = @_;
    my ($msg,$dup,@msgs,$proto,$remote_user,$remote_pass,$fold_type,$host);

    $fold_type = "local"; #Default folder type
    
    debug "Uid: $uid foldn: $fold_name";

    # 08/24/98: make the uid safe for the database

    $proto = get_folder_protocol($fold_name);
#    debug "Folder $fold_name has protocol $proto";

    $fold_name = remove_fold_prefix($fold_name) if ($proto =~ /imap/i);
    if (folder_exists($fold_name))
    {
#	debug "Folder exists.";

	if ( ($protocol =~ /imap/i && $proto ne "local") || ($proto =~ /imap/i) )
	{
	    $fold_type = "imap";
	    ($remote_user,$remote_pass,$host) = get_folder_credentials($fold_name);
	    my ($u,$d) = split(/\@/, $remote_user);
#	    ($remote_user,$junk) = split(/\@/,$remote_user);
	}
    }
    else #Create the folder
    {
	# A new Folder
	if ( (!($c{"remote_only"})) && ($protocol !~ /imap/) && (!($c{"pure_imap"})))
	{
	    debug "Creating local folder: $fold_name";
	    &create_folder($fold_name,'local');
	}
	else
	{
#	    debug "It's not local...must be imap or have remote only set...";
	    if ( ($protocol =~ /imap/) || ($c{"pure_imap"}) )
	    {
		($remote_user,$remote_pass,$host) = get_folder_credentials($inbox);
		my ($junk);

                if (!create_folder($fold_name,'imap',$remote_user,$host,$remote_pass)) {
                    $extra_status = convert($msg{'ERR_FailedAddToFolder'}, $fold_name);
                    debug "extra_status $extra_status";
                    return undef;
                }
		$fold_type = "imap";
	    }
	    else
	    {
		debug "Can't create folder with proto: $protocol";
		return undef; #Can't create Folder! setstatus?
	    }
	}
    }

    # save the (new) folder for the msg
    if ($fold_name ne $msg{"FOLD_Search_Results"} && $fold_name ne "Search Results") {
        $foldmap{$uid} = $fold_name;
        debug "set foldmap of $uid to $fold_name";
    } 

    if ($store) {
	debug "storing $uid in $fold_type u: $remote_user p: $remote_pass f: $fold_name";
	my $msg = "";
	&store_msg($fold_type,\$msg,$uid,$remote_user,$remote_pass,$fold_name,$host, $msg_status);
    }

    return 1;
}

sub store_msg
{
    # Attempt to abstract way of putting a message in a folder
    #  &store_msg('imap',\$the_msg,$uid,$remote_user,$remote_pass,$fold_name);
    #  Returns 1 on success
    
    my ($fold_type,$the_msg_ref,$uid,$remote_user,$remote_pass,$fold_name,$host,$msg_status) = @_;
    my ($the_msg,$dup,$new_uid);

    debug "storing $uid in $fold_name";

  SETUP_MSG:
    {
# 02.01.2003 RB [start] 
	# was: $the_msg = $$the_msg_ref; MEMORY LEAK
	
	# was unless ($the_msg)
	unless ($$the_msg_ref)
# 02.01.2003 RB [end] 
	{
	    if ($uid)
	    {
		$the_msg_ref = get_msg_scalar($uid);
		# Should do this with File Handles...!?
	    }
	}
    }   

  PROTOCOL_SPECIFIC_STORE:
    {
	if ($fold_type =~ /imap/i)
	{
            # if somehow the msg is empty, return. we dont want to append
            return 0 if (-s "$homedir/messages/$uid" == 0);

            ($remote_user, $host) = map_mailserver($remote_user, $host);

	    debug "Storing IMAP...";
	    &store_msg_imap($the_msg_ref,$remote_user,$remote_pass,$fold_name,$host,$msg_status) || return 0;
#	    debug "Stored f: $fold_name u: $remote_user uid: we don't know it w/imap";
	}
	else
	{
	    # NOOP for some reason?
	}
    }

  UPDATE_FOLDER_DB:
    {
	# Set folder of message This DOESN'T WORK WITH IMAP!
	add_msg_to_db($uid,$fold_name, $fold_type) if ($fold_type !~ /imap/i);
    }

    debug "Message Store Completed";

    return 1;
}

sub add_msg_to_db
{
    my ($uid,$fold,$fold_type) = @_;
    my ($line, $lines, @msgs);
    my (%folddb, $folddb, $foldfile);

    $fold = remove_fold_prefix($fold) if ($fold_type eq "imap");

#    debug "v-folder ".$v{"folder"}." fold $fold";
    if ($v{"folder"} ne $fold)
    {
        $foldfile = process_fold_type($fold);
#       debug "opening folder file $homedir/folders/$foldfile";

	if ( $ELocks->lock_create("$homedir/folders/$foldfile", \%folddb, {mode => 'write', nb => 1}) )
	{
        	tie %folddb, $db_package, "$homedir/folders/$foldfile", O_CREAT|O_RDWR, 0660;
        	$folddb = \%folddb;
        } else 
        {
        	$folddb = {};
        }
    }
    else {
        $folddb = \%folderdb;
    }

    my $msgs = $folddb->{"messages"};

    my $already_there = (bool(index($msgs, $uid) ne -1) ||
                        scalar(grep(/^$uid$/, keys %{$folddb}) > 0));
#    debug "already in folder? $already_there";

    # Set folder msg is in.
    $folddb->{"$uid:folder"} = $fold;
    $folddb->{"$uid"} = $fold_type;

    # Add to folder unless it's already there
#    unless (msg_in_folder($uid,$fold))
    if (!$already_there)
    {
        $msgs = add_to_delimeted_scalar($msgs,$uid);
    }

    $folddb->{"messages"} = $msgs;
#    debug "set messages to $msgs";
    $folddb->{"freshness"} = get_digest($msgs);

    if ($v{"folder"} ne $fold) {
        untie %folddb;
        $ELocks->lock_remove(\%folddb);
    }
}

sub get_digest
{
    my ($stuff) = shift;

    my (@headers);

    if (ref ($stuff) eq "ARRAY")
    {
	@headers = @{$stuff};
    }
    elsif (ref ($stuff) eq "SCALAR")
    {
	push(@headers,$$stuff);
    }
    elsif (!ref($stuff))
    {
	push(@headers,$stuff);
    }
    else
    {
	debug "ERROR: $stuff not a known type";
	return 0;
    }

#    load_module("Digest::MD5");
    my $md5 = new Digest::MD5;
    $md5->add(@headers);
    return $md5->hexdigest();
}

sub get_uidvalidity
{
    #IMAP specific function to return the folder's UID validity
    my ($fold) = @_;

    return undef unless $pop;

    my ($server_folder) = $pop->{"folder"};
    $server_folder = remove_fold_prefix($server_folder);

    my $validity;

    if ($server_folder eq $fold)
    {
	$validity = $pop->{uidvalidity};
    }
    else
    {
	$validity = $pop->uid_validity($fold);
    }

    return $validity;
}

sub store_msg_imap
{
    my ($the_msg_ref,$u,$p,$fold,$h,$msg_status) = @_;
    my ($host,$the_msg);
    my ($next_uid,$lf);

    $host = $h;
    
    unless ($host)
    {
	($u,$host) = split(/\@/,$u);  
    }

    debug "u: $u f: $fold h: $host";

	do_imap_login($u,$p,$host,$fold) || return undef;

    $fold = get_fold_and_prefix($fold);

    $lf = $pop->{folder};

    my $flag;

  	SET_MSG_FLAG:
    {
	if ($msg_status && $msg_status != STAT_NEW)
	{
	    if ($flag == EMU::STAT_ANS) 
	    {
		$flag = "\\Answered";
	    }
	    elsif ($flag == EMU::STAT_READ) 
	    {
		$flag = "\\Seen";
	    }
	}
    }

    $pop->append($fold, $$the_msg_ref, $flag);
    debug "setting msg status for $next_uid to $msg_status pop folder is ".$pop->{folder};
    debug "Appended OK";

    debug "lf $lf, pop->{folder} ".$pop->{folder};
    # go back and select original folder
    $pop->select($lf) if ($lf ne $pop->{folder});

    return 1;
}

sub get_msg_scalar
{
    #Get All of a message as a scalar.  Eats up memory.  Bad.
    my ($uid) = shift;

    my ($msg);

    my ($old) = $/;
    undef $/;

    open(IN, "$homedir/messages/$uid") || debug "Error opening message @_: $!\n";

    my $size = -s "$homedir/messages/$uid";

    while (<IN>) {
        $msg .= $_;
    }
    close IN;
    $/ = $old;

    return \$msg;
}

sub get_folder_credentials
{
    my ($fold_name) = @_;

    #Returns User and Pass for a folder
    my ($u,$p,$host);

    my $prefix = get_outbox_prefix();
    my $dbfold = $fold_name;

    $dbfold = remove_fold_prefix($fold_name) if ($prefix && $dbfold =~ /^$prefix/i);

debug "folder is $dbfold";
    # if pure_imap and this folder's credentials not yet set
    # use INBOX's credentials
    # if this is an imap folder, not external, we should use INBOX credentials.

#    if (($c{"pure_imap"} || $protocol =~ /imap/i) && 
#            !exists($userdb{"folder:$dbfold:password"})) {
    if (    $userdb{"folder:$dbfold:protocol"} =~ /imap/i &&
            !$userdb{"folder:$dbfold:external"}) {
        debug "getting info from ($inbox) instead";
        $u = $userdb{"folder:$inbox:username"};
debug "got username $u";
        $p = decode($userdb{"folder:$inbox:password"});
        $host = $userdb{"folder:$inbox:hostname"};
        debug "host is $host";
        $userdb{"folder:$dbfold:username"} = $u;
        $userdb{"folder:$dbfold:password"} = code($p);
        $userdb{"folder:$dbfold:hostname"} = $host;
    }
    else {
        $u = $userdb{"folder:$dbfold:username"};
        $p = decode($userdb{"folder:$dbfold:password"});
        $host = $userdb{"folder:$dbfold:hostname"};
    }

#    debug "Found $u and $p and $host for folder $dbfold";

    unless ($dbfold && $u && $p)
    {
	($u,$p,$host) = &get_outbox_credentials();
    }

#    debug "Host is now $host";

    $host = (split(/@/, $u, 2))[1] unless ($host);
    
#    debug "And host is now $host";

    $host = $host || $c{"default_outbox_host"};

#    debug "u is $u  pophost is $pophost  host is $host";

    ($u, $host) = map_mailserver($u, $host, $dbfold);

    if ($userdb{"folder:$dbfold:external"}) {
       # Ahhh not so simple... The classic iface allows for choosing of
       # a folder other than INBOX for imap mailboxes. So must take that
       # into account!
       $fold_name = $userdb{"folder:$dbfold:extra_fold"} ? 
           $userdb{"folder:$dbfold:extra_fold"} : $inbox;
       return ($u, $p, $host, $fold_name);
    } else {
       return ($u,$p,$host,$fold_name);
    }
#    return ($u,$p,$host,$fold_name);
}

sub get_imap_folder_path
{
    my ($fold) = shift;

    return $inbox unless ($fold);

    my ($imap_prefix) = $userdb{'options.prefix'} || $c{'default_imap_prefix'};

    if ( ($fold !~ /^$imap_prefix/) && ($fold ne $inbox) )
    {
	$fold = "$imap_prefix/$fold";
    }

    return $fold;
}

sub get_outbox_credentials
{
    #Returns User and Pass for outbox
    my ($u,$p,$host);

    $u = $userdb{"options.outbox.user"} || $user_name;
    $p = $userdb{"options.outbox.pass"} || $password;
    $host = $userdb{"options.outbox.host"} || $c{"default_outbox_host"} || undef;
    $host = (split(/@/, $u, 2))[1] unless ($host);

#    debug "u: $u p: $p host: $host";

    return ($u,$p,$host);
}

sub process_fold_type {
    # look at the fold type and insert a prefix if necessary
    my ($foldfile) = @_;

#    debug "folder $foldfile, folder:$foldfile:protocol ".$userdb{"folder:$foldfile:protocol"};

    my $searchfold = $msg{"FOLD_Search_Results"} || "Search Results";
    if ($foldfile eq $searchfold) {
        # search folder will always be local, ignore protocol
        return $foldfile;
    }

#    debug "protocol $protocol";

    return $foldfile if ($foldfile =~ /^inbox$/i || $foldfile eq $c{'default_inbox_name'});

    $foldfile =~ s/\//./g;

    if ($userdb{"folder:$foldfile:external"} == 1) {
        create_directory("$homedir/folders/.external")
            if (! -e "$homedir/folders/.external");
        return ".external/$foldfile";
    }

    if ((!exists($userdb{"folder:$foldfile:protocol"}) && 
            $protocol =~ /imap/i) || 
            $userdb{"folder:$foldfile:protocol"} =~ /imap/i) { 
        create_directory("$homedir/folders/.imap")
            if (! -e "$homedir/folders/.imap");
        return ".imap/" . EMU::IMAP::safe($foldfile);
    }

#    debug "found $foldfile";

    return $foldfile;
}


sub remove_fold_prefix {
    my ($fold) = @_;
    my $prefix = get_outbox_prefix();
    my $delim = &get_imap_delimiter(1);
    debug "delim $delim";

    $fold =~ s/^$prefix$delim// if ($prefix);
#    debug "fold is $fold";
    return $fold;
}

sub get_fold_and_prefix {
    my ($fold) = @_;
    my ($prefix) = &get_outbox_prefix();

    my $delim = get_imap_delimiter(1);

    $fold = "$prefix$delim$fold" 
        if ($prefix && $fold !~ /^$prefix$delim/ && $fold !~ /^inbox$/i);
#    debug "fold is $fold";
    return $fold;
}


sub get_outbox_prefix
{
    my ($fold) = @_;
    
    $fold ||= $inbox;

    # If we have an outbox stored in the mail/ folder, for example...
    # For external folders dont return the default prefix

    # This is only applicable on IMAP accounts, sooo... 
    return "" if (($userdb{"folder:$fold:external"} == 1 || $userdb{"options.dont_use_prefix"} == 1));

#    debug "trying to find a prefix";

    if (defined($userdb{'options.prefix'})) {
        return $userdb{"options.prefix"};
    } else {
        return $c{"default_imap_prefix"};
    }
}

sub msg_in_folder
{
    my ($uid,$fold_name) = @_;

    my (%otherfold,$ret);
    my $foldfile = process_fold_type($fold_name);
#    debug "folder $folder,$fold_name";

    # do we already have this folder open?
    return (bool(index($folderdb{"messages"}, $uid) ne -1))
        if ($ELocks->lock_search("$homedir/folders/$foldfile", 'path') && $folder eq $fold_name);

    if ( $ELocks->lock_create("$homedir/folders/$foldfile", \%otherfold, {mode => 'write', nb => 1}) )
    {
	    tie %otherfold, $db_package, "$homedir/folders/$foldfile", O_CREAT|O_RDWR, 0660;
	    debug "opened folder |$foldfile|";
	
	    $ret = bool (index ($otherfold{"messages"}, $uid) ne -1);
	    untie %otherfold;
	    $ELocks->lock_remove(\%otherfold);
    }

    return $ret;
}

sub remove_from_folder
{
    my ($uid,$fold,$delete_local,$del_cache) = @_;

    my (@msgs,$msg,$new);
    my $index=0;

    my $foldfile = process_fold_type($fold);

    #Folder Exists ?
    return 0 if (!-e "$homedir/folders/$foldfile");

    debug "removing $uid from folder $fold, curr folder is $folder";

    del_from_local($uid, 0, $fold);

    my @msg = ($uid);
    #Remove from folder if remote
    # 10/17/98 - MM
    if ( ($c{"pure_imap"}) || ($protocol =~ /imap/i))
    {
	del(\@msg,!$delete_local,$fold,1);
    }
    else
    {
	$index = del(\@msg,($del_cache) ? 0 : 1,$fold,1);
    }
     
    # remove $uid from folder
    @msgs = grep(!/^\Q$uid\E$/, split(/:/,$folderdb{"messages"}));
    
    $folderdb{"messages"} = join(':', @msgs);

    return 1;
}

sub msg_quickjump
{
    my ($mesg,$fold) = @_;
    my (@messages,$line,$counter,$it);
    my (%message,$the_subject,$the_date,$the_sender,$the_status, $the_pri);
    my ($this_message_numb,$this_message);
    my (@to_return);
    
    debug "mesg $mesg fold $fold";
    $counter = 0;
    
#    if (!$folderdb{"messages"})
#    {
#    	set_status($msg{'ERR_OpenFolder'});
#		return ();
#    }

    my %args;
    $args{"sort"} = $query->param('sorttype') || $folderdb{"sorttype"} || $c{'default_sort'} || 'select';
    $args{"fold"} = $fold;
    get_sorted_msgs( \@messages, \%args );

    $it = 0;
    for ($counter=0; $counter<=$#messages && $it == 0; $counter++) 
    {
        debug "looking for $mesg, found $messages[$counter]";
	$it = $counter if ($messages[$counter] eq $mesg);
        last if ($messages[$counter] eq $mesg);
    }

#    debug "it = $it.";

    $this_message_numb = ($it - 5);
    
    if ($this_message_numb <= 0 )
    {
	$this_message_numb = 0;
    }

#    debug "####this_message_numb = $this_message_numb\n";
    while ($this_message_numb <= ($it+5))
    {
	$this_message = safe(':', $messages[$this_message_numb]);
	
	last unless $this_message;
	
#	debug "this_message = $this_message";

        if ($folderdb{"$this_message:date"} eq "") 
	{
#            debug "info for $this_message missing";

            # we're assuming that the message belongs in the current folder
            # so let's just re-parse it
            
            my $h = header_from_file($this_message);
            
            if (!$h) {
               debug "Couldn't get header info for '$this_message'! Skipping.";
               $this_message_numb++;
               next;
            }
            
            $the_subject = $h->{"subj"};
            $the_date = $h->{"date"};
            $the_sender = $h->{"from"};
            $the_status = $h->{"status"};
            $the_pri = $h->{"pri"};
        }
        else {
	    $the_subject = $folderdb{"$this_message:subj"};
	    $the_date = $folderdb{"$this_message:date"};
	    $the_sender = $folderdb{"$this_message:from"};
	    $the_status = $folderdb{"$this_message:status"};
	    $the_pri = $folderdb{"$this_message:pri"};
        }

#	debug "the_subject = $the_subject.  the_date = $the_date.  the_sender = $the_sender the_status = $the_status";
	$the_subject =~ s/[\"<>\(\)\[\]\{\}\n\r]//g;
	$the_subject .= " " x 16;
	$the_sender =~ s/[\"<>\(\)\[\]\{\}\n\r]//g;
	$the_sender .= " " x 11;
	
	push(@to_return, substr($the_sender,0,10) . substr($the_subject,0,15) . $this_message);
	$this_message_numb++;
    }
    
    return (@to_return);
}

sub multi
{
    if ($query->param('reply.x'))
    {
	my ($reply_how, $reply_opt);

	$reply_how = lc($query->param('reply_how') || $query->param('reply.x'));
	debug "reply_how = '$reply_how'";
	# default to plain reply 
	$reply_how = "reply" if ($reply_how !~ /^q?reply(?:all)?$/);
	debug "reply_how = '$reply_how'";
	reply_msg($reply_how, $query->param('variable'));
    }
    elsif ($query->param('compose.x'))
    {
	compose();
    }
    elsif ($query->param('delete.x'))
    {
        $v{"wait_count"} = 0;

        if ( $trash_bin && ($folder ne $trash_folder)) {
            $query->param(-name=>'d', -value=>$query->param('variable'));
#            $query->param('d') = $query->param('variable');
            move_msg(1,0);
        }
        else {
	    delete_msg();
        }
    }
    elsif ($query->param('forward.x'))
    {
	forward();
    }
    elsif ($query->param('format.x'))
    {
	format_msg();
    }
    elsif ($query->param('vrmlize.x'))
    {
	vrmlize_msg();
    }
    elsif ($query->param('addto.x'))
    {
	addto();
debug "finished addto";
    }
    elsif ($query->param('display.x'))
    {
	my %opts = map { $_ => 1 } ($query->param('display'));

	if ($opts{'print'})
	{
	    format_msg();
	}
	elsif ($opts{'vrml'})
	{
	    vrmlize_msg();
	}
	else
	{
	for (qw[full_header basic_header show_html])
	{
	    # RMK 01/19/99 use full or basic headers
	    $userdb{"options.$_"} = $opts{$_} || 0;
	}

	# RMK 01/19/99 If both Full & Basic Headers are chosen, use Full
	if (($userdb{"options.full_header"} || bool($c{"view_display_full_headers"})) && $userdb{"options.basic_header"}) {
	    $userdb{"options.basic_header"} = 0;
	}

	msg_do($query->param('variable'));
	}
    }
    elsif ($query->param('options.x'))
    {
	my ($msg);

	$userdb{"options.full_header"}   = $query->param('full_header') || bool($c{"view_display_full_headers"}) || 0;
	$userdb{"options.basic_header"}   = $query->param('basic_header') || 0;
#	$userdb{"options.basic_header"}   = !$userdb{"options.full_header"};
	$userdb{"options.show_html"} = $query->param('show_html') || 0;

	$v{"returnto"} =~ /^msg=(.+)/;
	$query->param('variable', $1);

	msg();

	return;
    }
    elsif ($query->param('quick.x'))
    {
	# set the variable so that we know which file to reply to
	$query->param('variable', $query->param('variable2'));
	msg($query->param('variable2'));
    }
    elsif ($licensed{"worldlingo"} &&
            bool($c{"do_text_translation"}) && 
            $query->param('trans_pair') ne "none") {
        debug "asking for text translation ".$query->param('trans_pair');
        msg();
    }
    else
    {
	write_tmp("title", $msg{'ERR_Jump_T'});
	write_tmp("phrase", $msg{'ERR_Jump_B'});
	load_page("errors.html");
	return 0;
    }
}

sub search
{
	# wipe out old search folder
	debug "Entered search";
	my $searchfold = $msg{"FOLD_Search_Results"} || "Search Results";
	unlink "$homedir/folders/$searchfold" if -e "$homedir/folders/$searchfold";
	debug "Removed old search folder db";
	
	# getting data from user's input
    my $s_from   = $query->param('srch_criterion_from');
    my $s_to     = $query->param('srch_criterion_to');
    my $s_subj   = $query->param('srch_criterion_subj');
    my $s_body   = $query->param('srch_criterion_body');
    my $s_folder = $query->param('srch_folder_name');
    my $s_status = $query->param('srch_msg_status'); # ['read', 'new', 'answer']
    my $s_stdate = $query->param('srch_start_date'); # mm/dd/yyyy
    my $s_endate = $query->param('srch_end_date');   # mm/dd/yyyy
	debug "searching for from=$s_from, to=$s_to, subj=$s_subj, body=$s_body, folder=$s_folder, status=$s_status, start=$s_stdate, end=$s_endate";
    
    # preparing data
    my $isIMAP = $protocol =~ /imap/i; # get_folder_protocol($folder) =~ /imap/i; # it was shit as usual in this code
    debug "protocol is imap? $isIMAP";
    
    $s_stdate = str2time($s_stdate) if $s_stdate;
    $s_endate = str2time($s_endate) if $s_endate;
    debug "Converted dates: stdate = $s_stdate, endate = $s_endate" if ($s_stdate || $s_endate);
    
    $v{"wait_title"} = convert($msg{'WAIT_SearchFor'}, 'messages');
    my $delay_max = $c{'waitscreen_timeout'} || 10;
	my %temp_found_msgbase;

	if ($isIMAP && !$s_body)
	{
		# this is to make sure folder has message headers to search if IMAP
		my ($u, $p, $host) = get_folder_credentials($s_folder);
		debug "Getting folder credentials: user $u, pass $p, host $host";
		if ($u =~ /@/) { my ($uu, $h) = split(/\@/, $u); $u = $uu if (!exists($c{"appendhost_$h"})); }
	
		debug "Getting list of imap folder $s_folder";
		get_list_imap_full($host, $u, $p, $s_folder);
	}

	my @m_ids;
	my $fullfolder = process_fold_type($s_folder);
	# we don't need one more db access collision
	if ( $ELocks->lock_search( "$homedir/folders/$fullfolder" ) )
	{
		# such folder is already open. suppose it's folderdb
		@m_ids = map { [$_, $folderdb{"$_:downloaded"}] } split(':', $folderdb{'messages'});
	} else {
		# open folder
		my %folddb;
        if ( $ELocks->lock_create("$homedir/folders/$fullfolder", \%folddb, {mode => 'read', nb => 1}) )
        {
        	tie %folddb, $db_package, "$homedir/folders/$fullfolder", O_CREAT|O_RDONLY, 0660;
        	@m_ids = map { [$_, $folddb{"$_:downloaded"}] } split(':', $folddb{'messages'});
        	untie %folddb;
        	$ELocks->lock_remove(\%folddb);
        }
	}
	
	if ( $s_body )
	{
		# new thriller movie: "full body search case". starring imap or pop.
		debug "full body search: download message bodies if needed";
		for my $struct (@m_ids)
		{
			# struct: [0] = string msgid/digest, [1] = bool isDownloaded;
			unless ($struct->[1])
			{
				debug("downloading body of message " . $struct->[0] . " from $s_folder");
				download_msg($struct->[0], $s_folder);
			}
		}
	}
		
  	SEARCH_MSGS_CACHE:
	{
		debug "Searching in messages cache";
 
    	my $processed = 0;
    	$v{"wait_interval"} = get_wait_interval(scalar(@m_ids));
    
    	foreach my $struct (@m_ids)
    	{
    		my $msgid = $struct->[0];
        	print_progress_new(0);
			$v{"wait_action"} = convert($msg{"WAIT_ProcessedMsgs"}, $v{"wait_count"})
            	if ($v{"wait_count"}++ % $v{"wait_interval"} == 0);
		
			debug "Processing message $msgid";
			# decompose header so we may fill in header info
		    my $rh_decomposed = decompose_header('', $msgid);
	    	next unless $rh_decomposed;

	   		foreach my $key (keys %$rh_decomposed)
	    	{
				trim(\$rh_decomposed->{$key}); # get rid of extra spaces and newlines
			}
			
			CHECKMESSAGE:
			{
				next CHECKMESSAGE if ($s_folder ne $foldmap{$msgid} && $s_folder); 
				
				# Basic Headers
				next CHECKMESSAGE if ($s_from && $rh_decomposed->{from} !~ /\Q$s_from\E/i);
				next CHECKMESSAGE if ($s_to && $rh_decomposed->{to} !~ /\Q$s_to\E/i);
				next CHECKMESSAGE if ($s_subj && $rh_decomposed->{subj} !~ /\Q$s_subj\E/i);
				
				# Date range
				my $msgtime = str2time($rh_decomposed->{date});
				next CHECKMESSAGE if ($s_stdate && $msgtime < $s_stdate);
				next CHECKMESSAGE if ($s_endate && $msgtime > $s_endate);
				
				if ($s_body) # BODYSEARCH
				{
					my $parser = new MIME::Parser;
					$parser->ignore_errors(1);
					$parser->decode_headers(1); 
					$parser->extract_uuencode(1);
					$parser->output_dir("$homedir/tmp");
					$parser->output_prefix("tmp$$");
					$parser->extract_nested_messages(0);
					debug "parsing body of $homedir/messages/$msgid to perform full body search";
					my $entity = $parser->parse_open("$homedir/messages/$msgid");
					
					my @viewable_messages = ();
					my $found = 0;
					if ( process_parts($entity, \@viewable_messages, [], [], 0, 0, $msgid) )
					{
					        for my $vmsg (@viewable_messages)
						{
					    	        if ($vmsg =~ /\Q$s_body\E/i)
        					    	{
	        				    		$found = 1; 
	        				    		last;
		        			    	}
						}
					}
					
					next CHECKMESSAGE if (!$found);
				}

				# Since all matches have succeeded, store the message
				$temp_found_msgbase{$msgid} = $rh_decomposed;
				debug "Message $msgid meets our criteria";
				next CHECKMESSAGE;
	    	        }
	    	
			$processed++;
		}
	}

	my @msg_uids = keys %temp_found_msgbase; # our goal, a list of msgs
	$total_messages = scalar(@msg_uids) || 0;
	debug "Search results: found $total_messages message(s)";
	
	# Ok, now it's a salto mortale: I want to open message folder database for IMAP to 
	# get there the message status.
	my $bOpenedHelperDB = 0;
	my $helperdb;
	
	#if ($isIMAP) # this is valid for POP3 folder too
	#{
		debug "Trying to open helper db";
		if ( $ELocks->lock_search($s_folder) && $folder ne $s_folder )
		{
			# suppose the folder is open -- we'll be using folderdb
			# but it's VERY weak assumption
			$helperdb = \%folderdb;
			debug "Using already opened folderdb";
		}
		else
		{
			# hopefully folder is not open still
			my $preparedfolder = process_fold_type($s_folder);
		    if ( $ELocks->lock_create("$homedir/folders/$preparedfolder", \$helperdb, {mode => 'read', nb => 1}) )
		    {
				tie %$helperdb, $db_package, "$homedir/folders/$preparedfolder", O_RDONLY, 0660;
				$bOpenedHelperDB = 1;
				debug "Opened helper db";
			}
		}
	#}
	# end of salto mortale		
	
    # now that we've found the messages, stuff them into 
    # the search result folder. 
	my %tmpfold;
    if ( $ELocks->lock_create("$homedir/folders/$searchfold", \%tmpfold, {mode => 'write', nb => 1}) )
    {
		tie %tmpfold, $db_package, "$homedir/folders/$searchfold", O_CREAT|O_RDWR, 0660;
		$tmpfold{"messages"} = join(':', @msg_uids);
		# copy data to search db
		foreach my $uid (@msg_uids) 
		{
			foreach my $key ( keys %{ $temp_found_msgbase{$uid} } )
			{
				# debug "writing to search db: $key => " . $temp_found_msgbase{$uid}->{$key};
				$tmpfold{"$uid:$key"} = $temp_found_msgbase{$uid}->{$key};
			}
			$tmpfold{"$uid:folder"} = $s_folder;
			debug "helperdbstat: " . $helperdb->{"$uid:stat"} if $helperdb;
			$tmpfold{"$uid:stat"} = $helperdb->{"$uid:stat"} if $helperdb; # it's IMAP and we have db opened
			$tmpfold{$uid} = 0;
		}
	    
		untie %tmpfold;
		$ELocks->lock_remove(\%tmpfold);
	}
	
	# salto mortale continued
	if ($bOpenedHelperDB)
	{
		# close previously opened db
		untie %$helperdb;
		$ELocks->lock_remove(\$helperdb);
	}
	# second end of salto

	if ($total_messages <= 0)
	{
		# nothing found
    	set_status(convert($msg{'MSG_SearchNoResult'}, 'such messages'));
    } else
    {
    	# set_status(convert($msg{'MSG_Searched_S'}, 'messages'));
    }
    
	# force the search folder as local
	$userdb{"folder:$searchfold:protocol"} = "local";
	$folder = $msg{"FOLD_Search_Results"} || "Search Results";
	$v{$folder . "_page"} = 1; # we have to be on the first page!

    go_index();
}

#Move's a message from one folder to another.
sub do_move
{
    my ($msg,$lf,$fold) = @_;
    my %h;

    my $there = check_msg_location($msg,$lf);
    
    debug "there? $there";

    debug "folder $lf, protocol ".$userdb{"folder:$lf:protocol"};

  HANDLE_NONEXISTENT_IMAP:
    {
        last if ($there || $userdb{"folder:$lf:protocol"} !~ /imap/i);

        # if message isn't there and we want to move it, gotta download
        $there = 1 if (download_msg($msg,$lf,1));
    }


  FILL_IN_HEADER:
    {
        # if the current folder doesnt have the msginfo, fill in a hash
        last if ($folderdb{"$msg"} && defined($folderdb{"$msg:stat"}) &&
                 $folderdb{"$msg:date"} && $folderdb{"$msg:size"});

	my $h_ref = header_from_file($msg);
        last unless $h_ref;
        # we temporarily fill in the $folderdb hash for this message
        # because it will be copied and deleted below
        foreach my $thekey (keys %{$h_ref})
        {
            trim(\$h_ref->{$thekey}); # get rid of extra spaces and newlines
            $folderdb{"$msg:$thekey"} = $h_ref->{$thekey} if (defined($h_ref->{$thekey}));
        }

    }

  ADD_MSG_TO_FOLDER:
    {
        # Only refuse the move if we couldnt get it ($there=0) and the
        # message file no longer exists. Otherwise we could create a
        # deadlock condition where we try to move (or delete) a message
        # and refusing the move would prevent it from going away.
        return 0 if (!$there && ! -e "$homedir/messages/$msg");

        my $added = add_to_folder($msg, $fold, 1, $folderdb{"$msg:stat"});
            return 0 if (!$added || $added eq undef);

        debug "added $msg to $fold";

        my %folddb;
        my $foldfile = process_fold_type($fold);

	if ( $ELocks->lock_create("$homedir/folders/$foldfile", \%folddb, {mode => 'write', nb => 1}) )
	{
	        tie %folddb, $db_package, "$homedir/folders/$foldfile", O_CREAT|O_RDWR, 0660;
	        debug "opened folder |$foldfile|";
	
	        # long list below, but much faster than doing a grep on file-based hash
	        $folddb{"$msg"}            = $folderdb{"$msg"};
	        $folddb{"$msg:subj"}       = $folderdb{"$msg:subj"};
	        $folddb{"$msg:from"}       = $folderdb{"$msg:from"};
	        $folddb{"$msg:cc"}         = $folderdb{"$msg:cc"};
	        $folddb{"$msg:bcc"}        = $folderdb{"$msg:bcc"};
	        $folddb{"$msg:to"}         = $folderdb{"$msg:to"};
	        $folddb{"$msg:date"}       = $folderdb{"$msg:date"};
	        $folddb{"$msg:pri"}        = $folderdb{"$msg:pri"};
	        $folddb{"$msg:stat"}       = $folderdb{"$msg:stat"};
	        $folddb{"$msg:nouidl"}     = $folderdb{"$msg:nouidl"};
	        $folddb{"$msg:downloaded"} = $folderdb{"$msg:downloaded"};
	        $folddb{"$msg:size"}       = $folderdb{"$msg:size"};
	        $folddb{"$msg:ct"}         = $folderdb{"$msg:ct"};
	        $folddb{"$msg:replyto"}    = $folderdb{"$msg:replyto"};
	        $folddb{"$msg:mdn"}	   = $folderdb{"$msg:mdn"};
	        $folddb{"$msg:mdn-sent"}   = $folderdb{"$msg:mdn-sent"};
	        $folddb{"$msg:messageid"}  = $folderdb{"$msg:messageid"};

	        # reassign folder
	        $folddb{"$msg:folder"} = $fold;
	        untie %folddb;
	        $ELocks->lock_remove(\%folddb);
	}

        my $delete_local = ($protocol !~ /imap/i and
                 $userdb{"folder:$folder:protocol"} ne "local") ? 1 : 0;
        remove_from_folder($msg,$lf,$delete_local);

        # save to foldmap again, because the remove_from_folder deletes it
        $foldmap{$msg} = $fold;
    }

    return 1;
}


sub move_msg
{
    my ($trash, $noindex, $dont_quit) = @_;
    my ($msg,$lf,@garbage);

    debug "noindex? $noindex";
    if ($query->param('d') =~ /:/) {
        # actually a msg list
        @garbage = split(':', $query->param('d'));
    }
    else {
        @garbage = $query->param('d');
    }
#    debug "messages: @garbage";
    
    if (!@garbage)
    {
		set_status($msg{'ERR_NoMoveMessage'});
		go_index() if (!$noindex);
		return;
    }

    $folder = $trash_folder if ( $trash_bin && $trash);

    $lf = $v{"last_folder"};

    if ( ($folder eq $inbox) || ($userdb{"folder:$folder:protocol"} =~ /pop/i) ) #Can't move to POPs
    {
		set_status($msg{'ERR_NoMovetoInbox'});
		$folder = $lf;
		go_index() if (!$noindex);
		return;                 # in case
    }

    debug "===> lf is $lf, folder is $folder";

    unless ($lf && $folder)
    {
		# Error: didn't select a valid folder
		set_status($msg{'ERR_AddtoFolder'});

		$folder = $lf unless (!$lf);
		go_index() if (!$noindex);
		return;                 # in case	
    }

    my $local_folder = $folder;
    if ($lf ne $folder)
    {
        $v{"wait_title"} = convert($msg{"WAIT_MoveTitle"}, $#garbage+1, $folder);
        $v{"wait_interval"} = get_wait_interval(scalar(@garbage));

        my $imap_move = 0;
        my $total_moved = 0;

      	IMAP_MOVE:
        {
            debug "checking for block move: ($lf,$local_folder) ".$userdb{"folder:$lf:protocol"}.",".$userdb{"folder:$local_folder:protocol"}.",".$userdb{"folder:$lf:external"}.",".$userdb{"folder:$local_folder:external"};

            # we can do a block move if:
            # both folders are of type imap, and neither folder is
            # external... which means they reside on same server
            last if ($userdb{"folder:$lf:protocol"} !~ /imap/i ||
                     $userdb{"folder:$local_folder:protocol"} !~ /imap/i ||
                     $userdb{"folder:$lf:external"} ||
                     $userdb{"folder:$local_folder:external"});

            $imap_move = 1;

            # with IMAP we can do a block move as long as we're
            # moving between folders in the same account

            my ($success, $ph, $u) =
            do_login_sequence("imap",$userdb{"folder:$lf:username"},
                              decode($userdb{"folder:$lf:password"}),
                              $userdb{"folder:$lf:hostname"},$lf,0);

            if (!$success) {
                debug "failed login!!";
	    	    go_index() if (!$noindex);
		        return;                 # in case
            }
            my $validity = $pop->{uidvalidity};
            debug "validity: $validity";

            # remove validity from uids
            map { s/^$validity//; } @garbage;

            debug "garbage @garbage";
            my $f = get_fold_and_prefix($local_folder);
 
            # Before copying, grab the current number of messages
            # so that when we restore flags we can use an incrementing
            # counter of message numbers.
            if (!$pop->status($f))
            {
                # if this is the trash folder, then create it
                if ($folder eq $trash_folder)
                {
		    		my ($remote_user,$remote_pass,$host) = get_folder_credentials($inbox);

					if (!create_folder($f,'imap',$remote_user,$host,$remote_pass))
					{
                		$extra_status = convert($msg{'ERR_FailedAddToFolder'}, $f);
                    	debug "extra_status $extra_status";
	                	$folder = $lf unless (!$lf);
	                	go_index() if (!$noindex);
                    	return undef;
					}
					$pop->status($f);
                }
                else
                {
					set_status(convert($msg{'ERR_FolderSelected'},$local_folder));

					$folder = $lf unless (!$lf);
					go_index() if (!$noindex);
					return;                 # in case
				}
            }

            my $current_count = $pop->{num_msgs};
            debug "folder $f currently has $current_count messages";


            my $foldfile = process_fold_type($local_folder);

            my %folddb;
            
            # We need this so we can save the message headers and shit to the new folderdb!
            if (! $ELocks->lock_create("$homedir/folders/$foldfile", \%folddb, {mode => 'write', nb => 1}) )
            {
                debug "Cannot lock the new folder's ($local_folder, $foldfile) folderdb !";
	        	set_status("Lock Failure");
				write_tmp("folder",$folder,1);
				go_index() if (!$noindex);
                return;
            }
            
            my %flags;
            foreach my $msg (reverse @garbage)
            {
                $v{"wait_count"}++ 
                    if (print_progress_new(0) && $v{"wait_count"} == 0);

                # first grab flags for the messages so they can be
                # restored later.
                $flags{$msg} = $pop->get_flags($msg);
                debug "flags for $msg $flags{$msg}";
	    		if (!$over_quota || $folder eq $trash_folder)
     			{
                    my $id = $validity.$msg;
     			    debug "moving $msg ( $id )";
					# I think we have to check to see if $f exists!
                	$pop->copy($msg,$f);

                	my $imap_moved = $pop->interpret_response;
                	
                	if (!$imap_moved) {
                	   # Server failed to move our message(s) !
                	   
                	   my $msg = "Failure encountered while attempting to move message(s) to $local_folder.";
                	   
                	   if ($pop->{errcode}) {
                	      $msg .= "<br>\nServer says: $pop->{'errcode'}";
                       }
                	   
                	   set_status($msg);
                	   write_tmp("folder",$folder,1);
                	   go_index() if (!$noindex);
                	   return;
                	}
                	
                    # Now delete from the current folder
                    remove_from_folder($id,$lf,0);

                	$total_moved++;
				}
            	else
            	{
	        		set_status(convert($msg{'ERR_QuotaExceeded_Move'}, $local_folder));
					write_tmp("folder",$folder,1);
					go_index() if (!$noindex);
					return;
				}
            }

# TODO: this code was possibly causing problems. fix this or delete this one day, when you're in bad mood
#            # Now we go into the other folder and restore flags
#            $pop->select($f);
#
#            foreach my $msg (reverse @garbage)
#            {
#                $current_count++;
#                # do a store on message  #, not UID here...
#                $pop->cmd("STORE $current_count +FLAGS $flags{$msg}");
#                my $response = $pop->get_response();
#
#                del_from_local($msg, 0, $lf);
#
#                $v{"wait_action"} = convert($msg{"WAIT_MoveAction"}, 
#                                            $v{"wait_count"},
#                                            $local_folder)
#                    if (print_progress_new(0));
#
#                if ($v{"wait_count"}++ % $v{"wait_interval"} == 0)
#                {
#                    $v{"wait_action"} = convert($msg{"WAIT_MoveAction"}, 
#                                                $v{"wait_count"},
#                                                $local_folder);
#                }
#            }
#
#            # Should be done by now... go back to previous folder
#            $pop->select(get_fold_and_prefix($lf));

            $v{"wait_action"} = convert($msg{"WAIT_MoveAction"},
                                        $#garbage+1,
                                        $local_folder);

            $pop->expunge() unless ($dont_quit);
            print_progress_new(0,1);
        }

     	NON_IMAP_MOVE:
        {
            last if ($imap_move);

            # Here we have to resort to a very slow move, where we
            # have to download the messages if necessary, then add
            # them individually to the destination folder.

	    foreach $msg (@garbage)
	    {
	        debug "Moving message $msg to FOLDER $local_folder count ".$v{"wait_count"};

	        $total_moved += &do_move($msg,$lf,$local_folder);

                print_progress_new(0);
                if ($v{"wait_count"} % $v{"wait_interval"} == 0) {
                    $v{"wait_action"} = convert($msg{"WAIT_MoveAction"}, 
                                                $total_moved,
                                                $local_folder);
                }
	    }

            # Once we're done moving, if the original folder's type is
            # imap, then do an expunge, if it's pop, do a quit.
            $v{"wait_action"} = convert($msg{"WAIT_MoveAction"}, 
                                        $#garbage+1,
                                        $local_folder);

          QUIT_OR_EXPUNGE:
            {
                last if ($dont_quit);

                $pop->expunge() if ($userdb{"folder:$lf:protocol"} =~ /imap/i && $pop);
                $pop->quit() if ($userdb{"folder:$lf:protocol"} =~ /pop/i && $pop);
            }

            print_progress_new(0,1);
        }

      OUTPUT_STATUS:
        {
            last if (!$v{"wait_count"} && !$total_moved);

	    if (@garbage == 1)
	    {
	        set_status(convert($msg{'MSG_MoveMessage'}, $local_folder));
	    }
	    else
	    {
	        set_status(convert($msg{'MSG_MoveMessageMult'}, $total_moved, $local_folder));
	    }
        }

	$folder = $lf;
    }

    write_tmp("folder",$folder,1);

    go_index(1) if (!$noindex); #force check
} # move_msg()

# addto
#
# this function copies a message out of one folder into another. The message is
# removed from the original folder after being moved.
# Uses:
#   param(variable)     <-- message to move (hash)
#   param(add2folder)   <-- folder to move to. will be created if doesn't exist
sub addto
{
    my ($fold,$msg,$fold_proto);

    $fold = $query->param('add2folder'); # folder the message is being added to
    $fold =~ s/\"//g;
    if (!$fold)
    {
	set_status($msg{'ERR_AddtoFolder'}."0");
	go_index();
# Why call cleanup here?
#	cleanup();
	return;
    }

    if ( ($fold eq $inbox) || ($userdb{"folder:$fold:protocol"} =~ /pop/i) )
    {
	set_status($msg{'ERR_NoMovetoInbox'});
#	$folder = $lf;
	go_index();
	return;                 # in case
    }

    $msg  = $query->param('variable');   # the message itself

    debug "msg=$msg  fold=$fold  oldfold=$folder  lastfold=$v{last_folder}";

    $fold_proto = &get_folder_protocol($fold);
    if ( ($fold_proto eq "local") && ($c{"remote_only"}) )
    {
	set_status($msg{'ERR_AddtoFolder'}."1");
	go_index();
# Why call cleanup here?
#	cleanup();
	return;
    }
    debug "Add to fold is: $fold with $msg";
    
    if (!folder_exists($fold) && !create_folder($fold)) {
          go_index();
# Why call cleanup here?
#          cleanup();
          return;
    }

    my $orig_fold = $v{"last_folder"} = $folder;
    $folder = $fold;

    $query->param(-name=>'d', -value=>$msg);
    move_msg(0,1);

    $folder = $orig_fold;

    $v{"folder"} = $folder;
    go_index(1);
}

sub get_folder_protocol
{
    # Returns the protocol of a particular folder
    my ($fullfold) = shift;
    my ($proto);

    return undef unless $fullfold;
    
    my $prefix = get_outbox_prefix();
    my $fold = $fullfold;

    $fold = remove_fold_prefix($fullfold) if ($prefix && $fold =~ /^$prefix/i);
    
    return "imap" if ($c{"pure_imap"});

    # Should I default to $protocol???
    $proto = $userdb{"folder:$fold:protocol"};

    if (!$proto) {
        # not in userdb? check in folders directory
        debug "no protocol in userdb for folder $fold!";
        if (-e "$homedir/folders/$fold") {
            debug "found it as a local folder";
            $proto = $userdb{"folder:$fold:protocol"} = "local";
        }
        elsif (-e "$homedir/folders/.imap/$fold") {
            debug "found it as an imap folder";
            $proto = $userdb{"folder:$fold:protocol"} = "imap";
        }
        elsif (-e "$homedir/folders/.external/$fold") {
            debug "found it as an external folder";
            $userdb{"folder:$fold:external"} = 1;
        } else {
            # No files, no db entries...either this folder doesn't exist, 
            # or its IMAP, but only imap if not external and the inbox
            # is imap... otherwise this simply has to be a local folder.
            $proto = $userdb{"folder:$fold:protocol"} = 'imap'
                if ($userdb{"folder:$inbox:protocol"} =~ /imap/i); 
        }
    }

    # Default to our INBOX's protocol if none given. MM 20000923
# well we should only do that if the main inbox is imap (as above). It
# doesnt make sense. If we get to this point and still dont have a protocol
# then most likely this is a new folder...?? Unles... this is an
# external mailbox!
    $proto = $userdb{"folder:$inbox:protocol"} if (!$proto && $userdb{"folder:$fold:external"}); 

    $proto = "local" if (!$proto);

    debug "Protocol of $fold -> $proto";

    return $proto;
}

# delete_mass
#
# Description: delete selected messages
#
# Returns nothing
#
# Sets the status message to the number of messages deleted
sub delete_mass
{
    my($msg, @garbage);
    my ($first,$index);

    my $searchfold = $msg{"FOLD_Search_Results"} || "Search Results";
    if ($folder eq $searchfold) {
        set_status($msg{"ERR_DeleteSearchMsg"});
        go_index();
        return;
    }

    @garbage = $query->param('d');

    debug "There are ", scalar(@garbage), " messages selected for delete";
#    debug "param ".$query->param('d').", garbage @garbage";

    my $num_msgs = scalar(@garbage);

    $index = del(\@garbage,0,$folder);
    
#    debug "delete finished";
    # remove folder mapping
    my $themsg;
    foreach $themsg (@garbage) {
        delete($foldmap{$themsg});
#        debug "removed foldmap of $themsg";
    }

    if (@garbage == 1)
    {
	set_status($msg{'MSG_DelMessage'});
    }   
    else
    {
	set_status(convert($msg{'MSG_DelMessageMult'}, scalar(@garbage)));
    }

  POP_MUST_QUIT:
    {
        last if (!$pop || $userdb{"folder:$folder:protocol"} !~ /pop/i ||
                 ref $pop ne 'EMU::POP3');

        # Quit to make sure we really delete messages
        undef %poplist;
        $pop->quit();
        undef $pop;
        $pop_connected = 0;
    }

  IMAP_EXPUNGES:
    {
        last if (!$pop || $userdb{"folder:$folder:protocol"} !~ /imap/i ||
                 ref $pop ne 'EMU::IMAP');

        $v{"wait_action"} = convert($msg{"WAIT_Deleted"}, $#garbage+1); 
        $pop->expunge();
        print_progress_new(0,1);
    }

    go_index(1);
}


# Expand http:// -> a href=http://
sub urlify
{
    my ($text) = shift;
    my ($cid_hash)  = shift;
    my ($cid_array) = shift; 
    my ($line,$index) = 0;
    my (@folders, $f, $cid, $message, $part_number,@a);

    foreach $line (@{$text})
    {
#	debug "line: $line";
	$line =~ s {mailto:} {}g;
	$line =~ s {^[\n\r\t]} {<P>\n};
	$line =~ s {^\>(.*)} {&gt;$1<BR>};

	if ($line =~ /cid/i)
	{
	    if (!$message)
	    {
		$message = $query->param('variable');
		$message =~ s{/}{}g;
	    }

	    foreach $cid (@{$cid_array})
	    {
		$part_number++;
		$line =~ s {$cid} {&make_url("detach", "$message:$part_number")}e;
	    }
	}

	$text->[$index] = $line;

	$index++;
    }
    return $text;
}

sub get_target {
    my ($not_popup) = @_;# param provided for pages which normally are NOT popup
    my $target;

#debug "target frame ".$query->param("target_frame");
    if ($query->param("target_frame")) {
        $target = $query->param("target_frame");
    }
    elsif ($not_popup || $c{"disable_popup"}) {
        $target = "";
    }
    else {
        $target = "_blank";
    }

    return $target;
}


sub interpret 
{
    my ($text) = shift;

    my $SPECIALS = '()<>@,;:\\".[]\s';
    
    my $target = get_target();
    foreach ( @{$text} )
    {
	s {http://(([^\s\'\"\`\{\}\[\]\(\)\*\|\>\<])+)} {<A HREF="http://$1" target=$target>http://$1</A>}gi;
	s {https://(([^\s\'\"\`\{\}\[\]\(\)\*\|\>\<])+)} {<A HREF="https://$1" target=$target>https://$1</A>}gi;
	s {ftp://(([^\s\'\"\`\{\}\[\]\(\)\*\|\>\<])+)} {<A HREF="ftp://$1" target=$target>ftp://$1</A>}gi;
	s {([^\&\;\[\]\(\)\{\}\"\'\<\>\s\`,]+\@[^\[\]\{\}\*\&\^\(\)\"\'\<\>\s,\`]+)} {url_mailto($1)}ge;
    }
}

sub url_mailto
{
    my ($who) = @_;
    my ($mailurl);
    
#    $who =~ s/&lt;//g;
#    $who =~ s/&gt;//g;

    $mailurl = make_url("new_msg", undef, email => $who);

    my $target = get_target();
    return qq{<a href="$mailurl" target=$target>$who</a>};
}

sub msg
{
    my ($m) = @_;
    my ($message);
    my $rfc822 = 0;

    if (!$m)
    {
	$message = $query->param('variable');
#	$message =~ s{/}{}g;
    }
    else
    {
	$message = $m;
    }

    if (!$message)
    {
	go_index();
# Why call cleanup here?
#	cleanup();
	return;
    }

    debug "MESSAGE is $message";

    if ($licensed{"rfc822_attach"} && $message =~ /(^.+)\%\%RFC822\%\%/) {
        $message = $m = $1;
        $rfc822 = 1;
        debug "This is an RFC822 attachment from message $message...";
    }

    # Check to see if message has been downloaded yet...
    if (! &check_msg_location($message, $folder)) {
        #If we're here there's either an error or over quota.
        debug "ERROR: overquota maybe?";
        go_index();
# Why call cleanup here?
#        cleanup();
        return;
    }

    # Allow retrieval of part of the body of the message through "chunking"
    # if chunking is turned on, then we'll only return 1 chunk at a time of the
    # message.  This is useful for WAP devices where you can easily overload
    # the memory of the device with one long winded message...MM 07/13/00
    my $chunk = $query->param('ch') if ($licensed{"wap"} && $c{"chunk_messages"});

    # RMK 19990413 pass on a "1" to msg_do to indicate already checked msg
    waiting(\&msg_do, $m, 1, $rfc822, $chunk);      # display it

    $v{"clean_tmp"} = 1;
}

sub download_msg
{
    my ($message,$lf,$peek) = @_;
    my $index;
    my $downloaded=0;
    my $fold;
#    return 0 if ($over_quota);
    
    debug "downloading message $message";

#    debug "folder: ".$folderdb{"$message:folder"}.",$folder,lf $lf";


  	FIGURE_OUT_FOLDER:
    {
        # if we dont have a hashed value, try the foldmap, or
        # default to the global $folder
        if ($lf) {
           $fold = $lf;
        } 
        elsif (exists($folderdb{"$message:folder"}) && $folderdb{"$message:folder"}) {
           $fold = $folderdb{"$message:folder"};
        } 
        elsif ($foldmap{$message}) {
            $fold = $foldmap{$message};
        } else {
           $fold = $folder;
        }
    }

	# debug "fold is $fold";
    my ($u,$p,$host) = get_folder_credentials($fold);

	# debug "Host=$host u: $u p: $p mes=$message protocol $protocol ; folder: $fold ";
	# debug $folderdb{"$message"}." is teh m:m";

    if ($u eq "")
    {
        debug "Error! No username to download message";
        return 0;
    }

	my $fold_proto = get_folder_protocol($fold);
    debug "Folder protocol for folder '$fold': $fold_proto";
    if ($fold_proto =~ /imap/i)
    {
		debug "Imap MSG. Fold: $fold";
	    
		if ( get_msg_imap($u,$p,$host,$fold,$message,$peek) )
		{
	    	$folderdb{"$message"} = "local_imap";
	    	$downloaded = 1;
		}
    }
    else #pop 
    {
        ($u, $host) = map_mailserver($u, $host, $fold);
		# debug "FFF getting pop with $u and $host and $fold and $message";
		if ( $downloaded = get_msg_pop($u,$p,$host,$fold,$message) )
		{
	    	$folderdb{"$message"} = "local";
		} else {
            debug "Error... message not downloaded";
            return 0;
        }
    }

    # RMK 19990322 delete if mailloc indicates so
    if ($downloaded && $mailloc)
    {
		# debug "U is $u and P is $p";
        my @msg;

        push(@msg, $message);
        #Delete it from the server
        if ($fold_proto =~ /imap/i)
        {
            del_msg_imap("$u\@$host",$p,$fold,\@msg);
        }
        elsif ($fold_proto eq "pop3")
        {
            del_msg_pop($u,$p,$host,\@msg,$fold);
        }
    }

    $folderdb{"$message:downloaded"} = $downloaded;

    return 1;
}


sub check_spam
{
    my ($message, $folder) = shift;
    #Assumes message is already on disk...

    debug "Checking Message $message for SPAM";

    my ($junk,$host);

    # look for unwanted chars in filename
#    $message =~ s/\//++/g;
#    my $file = code2($message);

    # Get the hostname 
    my $from = '';
    if ($folderdb{"$message:date"})
    {
    	$from = $folderdb{"$message:replyto"} || $folderdb{"$message:from"};
    }
    else
    {
    	my $h_ref = header_from_file($message);
    	if ($h_ref)
    	{
    		$from = $h_ref->{'replyto'} || $h_ref->{'from'};
    	}
    }
    
    return undef unless $from;
    $from  = (addr_split($from))[1];
    ($junk, $host) = split(/\@/, $from, 2);
    
    load_module("EMU::RBL");
    my $rbl = new EMU::RBL($host);
    return undef unless $rbl;
    
    if ($rbl->is_blacklisted)
    {
	debug "Host is on blackhole list.\n";
	return 1;
    }

    debug "No Spam found";
    return 0; #Not SPAM (at least not on RBL list)
}

sub msg_in_db
{
    my ($message,$lf) = @_;

    my $location = $folderdb{"$message"};

    debug "location $location  protocol ". $userdb{"folder:$folder:protocol"}."  folder $folder  lf $lf";
    if ($location)
    {
        my $prot = ($lf ? $userdb{"folder:$lf:protocol"}
        				: $userdb{"folder:$folder:protocol"});
        $prot = "local" unless $prot;  # default to local if not set
        debug "prot $prot";

        # check certain criteria...
        # if :downloaded is true then it's been downloaded (but only valid
        # for current folder). If the protocol is local then it's local to
        # a local folder... lastly, check for mailloc because if the
        # message file exists and this is mailloc then we have it...
		if ( ($folderdb{"$message:downloaded"} == 1 ||
                $prot eq "local" || $mailloc) && 
                -e "$homedir/messages/$message")
		{
	    	debug "Message local";
	    	return 1;
		}
        elsif ($prot ne "local")
        {
            # only if not local. If local and message is missing, then 
            # we're in trouble... we lost the message
            debug "Message in db but not downloaded";
            return 2;
        }
        return 0;
    }
    else
    {
		debug "Can't find any reference to $message in db";

		return 0 if (! -e "$homedir/messages/$message");

        # otherwise, found message but it's not in current folder
        debug "message $message exists but not in current folder";
        return 3;
    }
}

sub check_msg_location
{
    my ($message,$lf) = @_;
    my $prot = $userdb{"folder:$folder:protocol"};
    my $res;

    $res = msg_in_db($message,$lf);

    if ($res == 1) { 
        debug "Complete message $message in db"; 
        return 1;
    }

    if ($res == 2)
    {
		debug "Complete message $message NOT in db";
		if ( !download_msg($message,$lf) ) 
		{
            set_status($msg{'ERR_MSGNotInServer'});
            return 0;
        }
        return 1;
    }

    if ($res == 3)
    {
		debug "Complete message $message NOT in db.  Have partial.";

		my $fold = $foldmap{$message};
		my $proto = get_folder_protocol($fold);

		return 1 if ($proto eq 'local');

		if(!$fold || !download_msg($message,$fold))
		{
            set_status($msg{'ERR_MSGNotInServer'});
            return 0;
        }
        return 1;
    }

    # $res is 0
    return 0;
}

sub get_folder_validity
{
    #IMAP specific function to get a folder's UID validity from db
    my ($fold) = shift;

    debug "\$fold is '$fold' ; \$folder is '$folder'";
    
    # this is dirty hack, but what can i do with this crap?!
    my %stubforlock;
    my $tempfold = remove_fold_prefix($fold);
    $tempfold = process_fold_type($tempfold);
    if ( $ELocks->lock_search("$homedir/folders/$tempfold", 'path') )
    {
    	# it's probably folderdb
    	return $folderdb{'uidvalidity'};
    } 
    elsif ( $ELocks->lock_create("$homedir/folders/$tempfold", \%stubforlock, {mode => 'read', nb => 1}) )
	{
		# open folder db to get uidvalidity
		tie my %tempfold, $db_package, "$homedir/folders/$tempfold", O_RDONLY, 0660;
		my $uidvalidity = $tempfold{'uidvalidity'};
		debug("uidvalidity: $uidvalidity");
		untie %tempfold;
		$ELocks->lock_remove(\%stubforlock);
		
		return $uidvalidity;
	}

	debug("can't get uidvalidity");	
	return ''; # we can't open db
}

sub set_folder_validity
{
    #IMAP specific function to get a folder's UID validity from db
    my ($fold, $uid_validity) = @_;
    debug "setting validity for $fold of $uid_validity";

    # this is dirty hack, but what can i do with this crap?!
    my %stubforlock;
    my $tempfold = remove_fold_prefix($fold);
    $tempfold = process_fold_type($tempfold);
    if ( $ELocks->lock_search("$homedir/folders/$tempfold", 'path') )
    {
    	# it's probably folderdb
    	return $folderdb{'uidvalidity'} = $uid_validity;
    } 
    elsif ( $ELocks->lock_create("$homedir/folders/$tempfold", \%stubforlock, {mode => 'write', nb => 1}) )
	{
		tie my %tempfold, $db_package, "$homedir/folders/$tempfold", O_CREAT|O_RDWR, 0660;
		$tempfold{'uidvalidity'} = $uid_validity;
		untie %tempfold;
		$ELocks->lock_remove(\%stubforlock);
		return $uid_validity;
	}
	return undef; # error
}

sub get_msg_imap
{
    # Actually retrieve and download a message
    my ($u,$p,$host,$foldorig,$uid,$peek) = @_;
    my ($junk,$uid_validity,$fold_validity, $fold);

    $delay=time if ($delay == 0);
    if ($u=~/@/) {
        my ($uu,$h) = split(/\@/,$u);
        $u = $uu if (!exists($c{"appendhost_$h"}));
    }

    my ($line,@lines,$get_this_one);

    debug "============ GETTING IMAP MESSAGE===============";
    debug "U: $u h: $host f: $fold";

    if ($userdb{"folder:$foldorig:external"}) {
        $fold = $inbox;
    } else {
       $fold = get_fold_and_prefix($foldorig);
    }

    debug "fold now $fold";

    if (!$pop) 
    {
        my $success;
        ($success,$host,$u) = do_login_sequence("imap",$u,
                                                $p,$host,
                                                $fold,1);
        return undef if (!$success);
    }

	debug "pop->folder is ".$pop->{folder};
    if ( ($pop->{folder} ne $fold) || ($pop->{"read_only"}) )
    {
		$pop->select($fold);
    }

    $uid_validity = $pop->{uidvalidity};

    $fold_validity = &get_folder_validity($foldorig);

    # because if the validity is wrong, that means that our
    # UID is no longer valid.

    if ($uid_validity ne $fold_validity)
    {
		debug "Uh oh!  Folders out of sync. uid_validity: $uid_validity ; fold_validity: $fold_validity";
		my ($user,$pass,$host) = get_folder_credentials($folder);
		($user, $host) = split(/\@/,$user,2) if (!$host);       
		get_list_imap($host,$user,$pass,$foldorig);

		$uid_validity = $pop->{uidvalidity};
        $fold_validity = &get_folder_validity($foldorig);
		debug "folder refreshed, now uid_validity: $uid_validity ; fold_validity: $fold_validity";
    }
    
    $get_this_one = $uid;

    $get_this_one =~ s/^$uid_validity//; #get rid of validity junk

    debug "Geting message $get_this_one";

    my $body_arref = $pop->get_with_uid($get_this_one);

    unless (scalar @$body_arref)    
    {
		debug "Didn't get anything!";
		get_list($fold);
		return 0;
    }

    debug "Got " . scalar(@$body_arref) . " lines!";

    my $success = store_msg_in_db($uid, $body_arref);
    $folderdb{"$uid:downloaded"} = 1 if ($success);
    debug "set downloaded to 1 for $uid";

    return $success;
}


sub get_msg_pop
{
 # Actually retrieve and download a message
    # possibly set the please wait screen???

    my ($u,$p,$host,$fold,$uid,$uidnum) = @_;
    my ($junk);

    my ($line, $subname) = (caller(2))[2,3];
    debug "Caller[2] = $line:$subname";

    debug "homedir=$homedir user is $u   host $host  uid $uid";

    if (ref $pop ne 'EMU::POP3' || !$pop->isValid)
    {
        my $success;
        ($success,$host,$u) = do_login_sequence("pop3",$u,$p,$host,1);
        return undef if (!$success);
	}

    my $total = ($pop->popstat)[0];
    debug "total $total";

    my $nouidl = $folderdb{"nouidl"};

    initialize_nouidl_list() if ($nouidl && !$nouidl_list{initialized});
    my $index = search_digest($uid, $nouidl);
    debug "message size is ".$folderdb{"$uid:size"};

    if ($index == 0) {
	set_status("Message not found in POP server!");
        debug "message $uid not found!";
        return 0;
    }

# 30.12.2002 RB. NOTE: get() uses large amount of memory, it's better to use Net::POP3::getfh()
    my $lines = $pop->get($index);
    debug "getting $uid. Index from map = $index";

    return store_msg_in_db($uid, $lines);
}


sub store_msg_in_db
{
    # Interface to message storage in db
    my ($uid, $lines) = @_;
    my $convert_cyrillic = 0;
    my $convert_to = "";
    my $srcenc = "";

    debug "Storing $uid";

    my $header_ok = 0;
    
    if (! open(WRITE_MSG, ">$homedir/messages/$uid")) {
        set_status("Error writing file $uid!!: $!");
        debug "Error writing file $homedir/messages/$uid!!: $!";
        return 0;
    }

    ($convert_cyrillic, $srcenc, $convert_to) = detect_cyrillic(@$lines)
        if ($licensed{"convert_cyrillic"} && $c{"convert_cyrillic"});

    debug "srcenc=$srcenc, convert_to=$convert_to";

    debug "writing ".scalar(@$lines)." to file";
    foreach my $line (@$lines)
    {
        next if (!$header_ok && (/^\s/ || /^>/) );
        $header_ok = 1;
        $line = Convert::Cyrillic::cstocs($srcenc, $convert_to, $line)
            if ($convert_cyrillic); 
	print WRITE_MSG $line;
    }
    close WRITE_MSG;

    if (!-e "$homedir/messages/$uid" || -s "$homedir/messages/$uid" == 0) {
        debug "Error writing to $homedir/messages/$uid!";
        return 0;
    }

    debug "message $homedir/messages/$uid stored, size ".-s "$homedir/messages/$uid";
    return 1;
}


# Return the first (text) part of a multipart
sub getFirstPart {
    debug "multipart";
    my @myparts = @_;
    my $firstpart = $myparts[0];
    my @tmp;

    # weird... firstpart isnt valid??? I wonder why...
    # but we did see an error like this, so gotta take care of it
    return @tmp if (!$firstpart);

    if ($firstpart->is_multipart) {
        my @subparts = $firstpart->parts();
        getFirstPart(@subparts);
    }
    elsif ($c{"inline_trans_sub_".$firstpart->mime_type()})
    {
        my $prologue = ${ do_inline_trans($firstpart) };
        return @{ $prologue };
    }
    elsif ($firstpart->mime_type =~ /^text\//i) {
        my @body;
        if (my $io = $firstpart->open("r")) {
            while (defined($_ = $io->getline)) { push(@body, $_) }
            $io->close;
        }
        return @body;
    }
    else { return @tmp; }
}

#05/04/99 -- MM Allow admin to customize translation subs for inlines
# The idea is to allow per mime type granularity of inlining
sub do_inline_trans
{
    my ($bodypart) = @_;

    my $prologue; #In this case the body

    debug "here";
    eval
    {
        no strict 'refs';
        load_module("EMU::Custom");
        my $ct = lc($bodypart->mime_type());
        my $sub = "EMU::Custom::".$c{"inline_trans_sub_".$ct};

        my $body = $bodypart->bodyhandle;

        $prologue .= &$sub($body->as_string);
    };

    debug "Did inline_trans_sub for ".$bodypart->mime_type();
    debug "Returning $prologue";

    return $prologue;
}


sub get_alternative2 {
    my ($part, $message_ref, $msg, $cids_ref) = @_;
    my $found_html = 0;
    my $found_alt = 0;
    my ($alt,$txt);

    foreach my $p ($part->parts) {
        debug "type ".$p->mime_type;

        get_alternative2($p, $message_ref, $msg, $cids_ref)
            if ($p->is_multipart);

        if ($p->mime_type =~ /text.html/i) {
            $found_html = 1;

            my $io = $p->bodyhandle()->open("r");
            write_tmp("inline_html", 1);

            my $html_part = get_html_part($p,$io,$msg,$cids_ref);
            write_tmp("inline_html_value", disable_style_mod($html_part));
            # ensure backwards compatibility with classic iface (which
            # only uses $the_message
            write_tmp("the_message", $html_part) if (!$c{"embedded_perl"});
        }
        elsif (!$found_html && $p->mime_type =~ /text.enriched/i) {
            $found_alt = 1;
            my $io = $p->bodyhandle()->open("r");
            $alt = get_html_part($p,$io,$msg,$cids_ref);
	    write_tmp("inline_html", 1);
	    write_tmp("inline_html_value", "<pre>".$alt."</pre>");
        }
        elsif (!$found_html && !$found_alt && $p->mime_type =~ /text.plain/i) {
            my $io = $p->bodyhandle()->open("r");
            $txt = get_html_part($p,$io,$msg,$cids_ref);
	    write_tmp("inline_html", 1);
	    write_tmp("inline_html_value", "<pre>".$txt."</pre>");
        }
    }

# take care of nonstandard case. Leave as "inline_html" but with <pre>
#05.15.03 Alex WTF "nonstandard case"? WE USE FOREACH IF PARTS MORE THAN ONE!!! (hehe:)
#     if (!$found_html) {
#         write_tmp("inline_html", 1);
#         if (!$found_alt) {
#             # as a last resort, write in the plain text
#             write_tmp("inline_html_value", "<pre>".$txt."</pre>");
# debug "using txt \n $txt";
#         }
#         else {
#             write_tmp("inline_html_value", "<pre>".$alt."</pre>");
# debug "using alt \n $alt";
#         }
#     }

}


sub get_alternative {
    my ($parts) = @_;
    my @parts = @{$parts};

    my $part = ($parts[0]->mime_type() =~ /text.plain/i) ? 1 : 0;
    
    $part-- if (!$parts[$part]);
    
    # Hmmmm this can get complicated. multipart/alternative doesn't
    # *always* have a simple text/plain + text/html. One message
    # that caused trouble had a text/plain and then a 
    # "multipart/related" as the second part, and the text/html
    # was a subpart within the multipart/related.
    # This means we have to look at the type of the alternative part
    
    if ($parts[$part]->mime_type() =~ /text.html/i) {
        # Ok, a simple text/html so just grab that
        debug "simple multipart/alternative, using part $part";
        return $parts[$part];
    }

    # Hmmm the alternative part is not text/html! :/
    if ($parts[$part]->is_multipart()) {
        debug "we have a multipart inside a multipart/alternative!";
        my @subparts = get_parts($parts[$part]);

        # I guess we just iterate to find an html
        foreach my $p (@subparts) {
            if ($p->mime_type() =~ /text.html/i) {
                return $p;
            }
        }

        debug "couldnt find an appropriate text/html for the alternative!";
        # bad...
	set_status($msg{'ERR_MimeHeadParse'});
    }

    return undef;
}


# 
# the msgdata hash stores the following data, separated by nulls:
#  subject, date, sender, status, priority
sub msg_do
{
    my ($m,$already_checked,$rfc822attach, $chunk) = @_;
    my ($full, $addr, $head, $tmphead, $to,$subj,$from,$date,$cc,$bcc,$parser);
    my ($show_html,$full_header,$basic_header, $view_list, $html);
    my ($the_subject,$the_date,$the_sender,$the_status);
    my (@folders, $entity, $parts, $part, $part_name, $disp_name, $orig_name);
    my ($was, $prologue, %prologues, $the_message, $got_it, $body_file);
    my ($line, $next_msgs, $msg_send, $msg_numb, $subj_counter);
    my ($messages, $the_size, $message, $reply, @emails, %email, $i, @email);
    my ($replyto, @parts, @the_message, @next_msgs, %messages, $autoload);
    my ($msg_subj, $the_pri, $image, @attachments);
    my (%cids, @cids, %cid_map, %used_cids, $ct, $pure);
    my ($vmsg_id, $vmsgID);  #  rcs.ngf.v.1 stmt.1  9/20/99  --ngf
    my ($mdn_email);
    my @files_to_delete;
    my $msgfile;
    my $not_text=0;
    my $inline_html=0;

    print_header();

    if (!$m)
    {
	$message = $query->param('variable');

	$message =~ s{/}{}g;
    }
    else
    {
	$message = $m;
    }
    
    if (!$message)
    {
	go_index();
# Why call cleanup here?
#	cleanup();
	return;
    }

    if ($rfc822attach) {
        $msgfile = "$homedir/tmp/rfc822";
    }
    else {
        $msgfile = "$homedir/messages/$message";
    }

    debug "msgfile is $msgfile";

    #10/19/98 -- Not always true! MM
    if ($folderdb{"$message:nouidl"} == 1)
    {
	$message = substr($message, 0, 32) ;    
    }

    $message = basename($message); # safety
    
    $v{"returnto"} = "msg=$message";
	
    if ($already_checked eq undef || $already_checked != 1)
    { 
	unless (&check_msg_location($message))
	{
		# here means error or over quota
		debug "ERRORERROR OR OVERQUOTA";
		go_index();
		# Why call cleanup here?
		# cleanup();
	        return;
	}
    }

    if (!-e $msgfile)
    {
        unless (&check_msg_location($message)) {
            debug "Can't find $message or not in userdb";
	    go_index();
# Why call cleanup here?
#	cleanup();
	    return;
        }
    }
    
    $head = MIME::Head->from_file($msgfile); # MEMORY LEAK

#    debug "$msgfile size ".-s $msgfile;
#    debug "MIME::Head version $MIME::Head::VERSION";
    if (!$head)
    {
	debug "Couldn't create MIME::Head object for $msgfile";
	set_status($msg{'ERR_MimeHeadParse'});
	go_index();
# Why call cleanup here?
#	cleanup();
	return;
    }

    # 08/21/98: gotta decode the header
    $head->decode();


    #  ******************************************************************* #
    #
    #   9/30/99 rcs.ngf.v.1 nph-emumail.cgi block.3 begin {


    $vmsg_id = $head->get('Voice-Id');
    chop($vmsg_id);

    if( $vmsg_id ) 
    { 
	write_tmp("vmsgID", $vmsg_id); 
	debug("vmsgID set to $vmsg_id");
    }  # 9/17/99 --ngf

    #  } end block.3 nph-emumail.cgi rcs.ngf.v.1 9/30/99
    #
    #  ******************************************************************* #
    
    # read receipt request handling
    
    # if read receipt was not sent and default behavior is: user decides
    if (!defined $folderdb{"$message:mdn-sent"} && !defined $c{'default_readreceiptaction'})
    {
    	$mdn_email = $head->get('Disposition-Notification-To');
    	chop $mdn_email;
    	debug "mdn_email: $mdn_email";
    	($mdn_email) = Mail::Address->parse($mdn_email);
    	if ($mdn_email)
    	{
    		$mdn_email = $mdn_email->address();
    		if ($mdn_email)
    		{
    			debug "read receipt requested by $mdn_email";
    			write_tmp('mdn_email', $mdn_email);
    		}
    	}
    }
    # if default behavior: always send -- send it silently
    elsif ($c{'default_readreceiptaction'})
    {
    	debug "sending read receipt silently";
    	send_readreceipt($message, $folder, 1); # last param - do not dislay something, just return
    }
    
    # end read receipt request handling

    my $reply_to;

    if (!$rfc822attach) {
        $subj = $folderdb{"$message:subj"} || $head->get('Subject');
        $replyto = $head->get('Reply-To') || $folderdb{"$message:replyto"};
        $reply_to = (bool($c{"from_is_reply_to"})) ? $replyto : "";
        $from = $reply_to || $folderdb{"$message:from"} || $head->get('From');
        $cc   = $folderdb{"$message:cc"} || $head->get('Cc');
        $bcc  = $folderdb{"$message:bcc"} || $head->get('Bcc');
        $to   = $folderdb{"$message:to"} || $head->get('To');
        $date = $folderdb{"$message:date"} || $head->get('Date');
        $ct   = $folderdb{"$message:ct"} || $head->get('Content-type');
    }
    else {
        $subj = $head->get('Subject');
        $replyto = $head->get('Reply-To');
        $reply_to = (bool($c{"from_is_reply_to"})) ? $replyto : "";
        $from = $reply_to || $head->get('From') || $msg{'MSG_NoFrom'};
        $cc   = $head->get('Cc');
        $to   = $head->get('To');
        $date = $head->get('Date');
        $ct   = $head->get('Content-type');
    }

    # we need to reformat date; was: Wed, 1 Jan 2003 10:10:10 +0200; now: Wed, 1 Jan 2003 10:10:10 EET
    $date = get_date(str2time($date));
    debug "ct=$ct  from=$from  subj=$subj  date=$date";

    if (!$from)
    {
	error "Error, couldn't find From field!";
	
	set_status($msg{'ERR_NoFromField'});
	go_index();
# Why call cleanup here?
#	cleanup();
	return;
    }
    
    debug "message is $msgfile, size is ".-s "$msgfile";

    # setup our parser object. we want files to output into the user's temp directory

    $parser = new MIME::Parser;
    $parser->ignore_errors(1);
    $parser->decode_headers(1); 
    $parser->extract_uuencode(1);
    $parser->output_dir("$homedir/tmp");
    $parser->extract_nested_messages(0);
    my $prefix = "tmp$$".time;
    $parser->output_prefix($prefix); #MM -- We were overwriting files with FCGI... 990521

    $reply = "";
    $reply .= "$cc" if ($cc);
    $reply =~ s/\n|\r|\t//g;

    @emails = $reply =~ /([a-zA-Z0-9\/\-\.\\_]+@\[?[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,3}|[0-9]{1,3}\]?)/g;
#    debug "emails is @emails";

    foreach (@emails)
    {
	$email{lc($emails[$i])} = $emails[$i];
	$i++;
    }
    
    my $thekey;
    foreach $thekey (keys(%email))
    {
	push (@email, $thekey) unless ( (/$user_name/i) || ($from =~ /$thekey/i) );
    }
    
    $replyto  = (addr_split($from))[1] || $from;

    $reply = join(",", @email);
    $reply =~ s/\r|\n//g;

    debug "ct=$ct  from=$from  subj=$subj  date=$date";

    $v{"reply_to"} = $replyto;
    $v{"reply_cc"} = $reply;
    $v{"reply_subj"} = $subj;
#    debug "reply_subj is $subj";
    $v{"reply_date"} = $date;
    
    my $orig_from = $from;
#    $subj = safe_html($subj);
#    $from = safe_html($from);

    chomp($from);

#    debug "The FROM field is $from";

    ($full, $addr) = addr_split($from);
    my ($suggested_fold, $addr2) = addr_split($orig_from);

    $suggested_fold = legalize(substr($suggested_fold, 0, $c{'folder_namelen'}));
    $suggested_fold ||= $addr2;
    $full ||= $addr;

    $suggested_fold =~ s/\"//g;
#    debug "suggested fold $suggested_fold";
#    debug "FULL is $full";
#    debug "ADDR is $addr";

    write_tmp("fullname", $suggested_fold);

    # read in some options
    $full_header   = $userdb{"options.full_header"} || bool($c{"view_display_full_headers"});
    $basic_header  = $userdb{"options.basic_header"};

    $show_html = $userdb{"options.show_html"} || bool($c{"view_display_HTML"});
    $autoload  = $userdb{"options.autoload"};
    $autoload = 1 if ($autoload eq undef);  # default if nothing is set.

#    debug "show_html=$show_html  full_header=$full_header  basic_header=$basic_header  autoload=$autoload";

    $subj = safe_html($subj);
    $from = safe_html($from);

    # escape the angle brackets
    $from = escape($from);
    $to   = escape($to);
    $cc   = escape($cc);
    $cc =~ s/\r|\n//g;
    $to =~ s/\r|\n//g;

    $entity = $parser->parse_open($msgfile);

    # 07/24/98: serious error if we can't read the message!
    if ($entity eq undef)
    {
        # Ok, weird, couldn't parse message. First let's see if we can
        # solve this problem by re-downloading the message. If not, then
        # just put up an error.
        debug "HUH? can't parse the message? let's re-download it";
        if (!download_msg($message)) {
            set_status($msg{'ERR_MSGNotInServer'});
            go_index();
	    return undef;
        }

        $entity = $parser->parse_open("$homedir/messages/$message");

        # Ok, we've re-read the message... see if it worked.
        if ($entity eq undef) {
	    debug "FATAL: Couldn't read message!!";
	    error("<Severe>: Couldn't parse message $message (".decode2($message).") for user $user_name: $! $homedir");
	    set_status($msg{'MSG_FailedParse'});
	    go_index();
	    return undef;
        }
        debug "re-download worked! :-)";
    }

    #@parts = $entity->parts();
    debug "entity has ".$entity->parts(). " parts";
    debug "multipart is ".$entity->is_multipart;
    my $multipart = $entity->is_multipart;
    @parts = get_parts($entity);
    debug "processing ".scalar(@parts)." parts";
    
    # HUH? Ran into this problem a couple of times. Somehow we had only
    # a partial header, no body and thought the message was downloaded.
    # Only saw this with multipart messages.
    if ($multipart && scalar(@parts) == 0) {
        download_msg($message);
        $entity = $parser->parse_open($msgfile);
        $multipart = $entity->is_multipart;
        @parts = get_parts($entity);
    }

#    debug "ttam: size of parts:".scalar(@parts);

    my $target = "";

    write_tmp("inline_html", 0);

    my @prologues;
# Julia changed 06.24.2005    
# Julia changed 06.07.2005    
#    if ($rfc822attach) {
#        $got_it = process_parts($entity,\@the_message,\@prologues,\@attachments,0,0,'rfc822');
#    } else {
#        $got_it = process_parts($entity,\@the_message,\@prologues,\@attachments,0,0,$message);
#    }

    my $used_cids = build_cids_hash($entity);
    debug "used_cids: " . Dumper($used_cids);
    
    if (scalar(@parts) == 0) {
    	if ($rfc822attach) {
    		$got_it = process_single_part($entity,\@the_message,\@prologues,\@attachments,0,0,'rfc822',$used_cids);
    	} else {
    		$got_it = process_single_part($entity,\@the_message,\@prologues,\@attachments,0,0,$message,$used_cids);
    	}
    } else {
    	if ($rfc822attach) {
        	$got_it = process_msg_parts(\@parts,\@the_message,\@prologues,\@attachments,0,0,'rfc822', $used_cids);
    	} else {
	        $got_it = process_msg_parts(\@parts,\@the_message,\@prologues,\@attachments,0,0,$message, $used_cids);
    	}
    }
# Julia changed end

    if (!($got_it))
    {
        debug "got_it is 0, reading file";
	open (FH, $body_file) || debug "$body_file error reading";

	# binmode  FH;

	@the_message = <FH>;
	close FH;
    }
    
    # only quoted-printable decode if the transfer encoding indicates the need
#    if ($entity->head->get('Content-Transfer-Encoding') =~ /quoted-printable/i)
#    {
#	decode_qp(\@the_message);
#    }

    if ($licensed{"worldlingo"} && bool($c{'do_text_translation'}) && 
            $c{'translation_url'} && $c{'translation_uname'} &&
            $c{'translation_pword'} && 
            ($query->param('trans_pair') && $query->param('trans_pair') ne "none")) {
        load_module("LWP::Simple");
        load_module("URI");

        debug "trans_pair is ".$query->param('trans_pair');
        my $tmp_txt = join('', @the_message);
#        debug "tmp_txt is $tmp_txt";
        my $uri = URI->new($c{'translation_url'});

        $uri->query_form( wl_text => $tmp_txt,
                  wl_lp   => $query->param('trans_pair'),
                  wl_uname => $c{'translation_uname'},
                  wl_pword => $c{'translation_pword'} );

        $tmp_txt = LWP::Simple::get($uri);
#        debug "after translation: $tmp_txt";

        @the_message = split(/\n/, $tmp_txt);
    }

    if ( $show_html )
    {
        debug "urlifying";
        @the_message = @{urlify(\@the_message,\%cids,\@cids)};
# HM - I think this is causing problems, not sure it's supposed to be here anyways.
#        interpret \@the_message;
    }

    if ($licensed{"wap"} && $c{"is_wap"} && !$not_text)
    {
        #Format for WAP devices
        foreach (@the_message)
        {
            $_ = safe_html($_);
            $_ =~ s/\r\n/<br\/>/g;
            $_ =~ s/\n/<br\/>/ig;
        }
    }

    unshift(@the_message, $image) if ($image);

    $the_message="";

    if (($parts[0]) && ($multipart)) {
        if ($parts[0]->mime_type() !~ /text/i) {
            # if the first part is not text then assign a blank message...
            write_tmp("the_message", "");
            debug "non-text first part... setting it to blank";
        }
        else {
            $the_message = join('', @the_message);
        }
    }
    else {
        $the_message = join('', @the_message);
    }

    # and NOW we do the chunking, passing in scalar and actually having it
    # return the already-chunked scalar.
    if ($licensed{"wap"} && $chunk && $c{"chunk_messages"}) {
        write_tmp("the_message", chunk_msg($the_message,$chunk));
    }
    elsif (!get_var("inline_html")) {
	if (($parts[0]) && ($parts[0]->mime_type() !~ /text\/plain/i)) {
	        # filter html images if the user desires it
	        if ($userdb{"options.no_html_images"}) {
                    $the_message =~ s/<img\s.*?>/<img src='$c{img_url}\/image_filtered.gif'>/igs;
	        } 
	        write_tmp("the_message", $the_message);
	}
	elsif ($ct =~ /text\/plain/i) { #Alex Hack for escalet
		write_tmp("the_message", proLinker($the_message));
	}
	elsif ($ct eq '') { #Alex Hack if Content-type don't specify
		write_tmp("the_message", proLinker($the_message));
	}
	else {
	        # filter html images if the user desires it
	        if ($userdb{"options.no_html_images"}) {
	            $the_message =~ s/<img\s.*?>/<img src='$c{img_url}\/image_filtered.gif'>/igs; 
	        } 
	        write_tmp("the_message", $the_message);
	}
    }

    @the_message = undef;       # clear from memory

    my $tmp;

    # do the quickjump for the stored session folder, or the current folder.
    @next_msgs = msg_quickjump($message, $v{last_folder} || $folder);
    $tmp = join('%%smoo1919', @next_msgs);

    $v{"folder"} = $folder; # current folder this quickjump is for
    $v{$message} = $tmp;

#    debug "next_msgs @next_msgs";
    foreach $msg_subj (@next_msgs)
    {
	($msg_send, $msg_subj, $msg_numb) = $msg_subj =~ /^(.{10})(.{15})(.*)/;

	$msg_subj = safe_html($msg_subj);

	if ($message =~ /\Q$msg_numb/)
	{
	    $view_list .= qq{<OPTION VALUE="$msg_numb" SELECTED>$msg_send: <I>$msg_subj</I>\n};
	} 
	else
	{
	    $view_list .= qq{<OPTION VALUE="$msg_numb">$msg_send: $msg_subj\n};
	}
	$subj_counter++;
    }
    
#    debug "VIEW LIST IS $view_list";

    debug "status: $message ".$folderdb{"$message:stat"};
    # if the message is new then mark it as being read now
    if ($folderdb{"$message:stat"} == STAT_NEW ||
            $folderdb{"$message:stat"} eq "")
    {
	&set_msg_status($message, STAT_READ);
    }

    debug "prologue has ".scalar(@prologues)." parts";
    $prologue = join("\n", @prologues);

    debug "we have ".scalar(@attachments)." attachments";
#    my $attachments = join(" ", map { $_{url} } @attachments);
    my $attachments;

    foreach my $a (@attachments) {
        $attachments .= qq{<A HREF="$a->{url}", $a->{target}>$a->{name}</A> };
    }
    debug "attachments $attachments";

    write_tmp("attachments", $attachments);
    write_tmp("attachments_array", \@attachments);
    write_tmp("cc", $cc);
    write_tmp("date", $date, 1);
    write_tmp("address_add", make_url("address", $from));
    write_tmp("folder_list", [\&fetch_folder_list, $suggested_fold]);
    write_tmp("from", $from, 1);
    write_tmp("full_headers", $head->original_text());
    write_tmp("header_obj", $head);
    write_tmp("headers", $basic_header);
    write_tmp("message", $message);
    write_tmp("no_interpret", !$show_html);
    write_tmp("prologue", $prologue);
    write_tmp("rdate", $the_date);
    write_tmp("show_html", $show_html);
    write_tmp("status", ($status =~ s/[\r\n]/ /));
    write_tmp("subj", $subj, 1);
    write_tmp("to", $to, 1);
    write_tmp("view_list", $view_list, 1);

    print_header();
    load_page("msgview.html");
    
    debug "finished loading msgview";
    $v{"last_folder"} = $folder;

    debug "deleting files @files_to_delete";
    unlink @files_to_delete if (scalar(@files_to_delete) > 0);
}


sub process_mime_type {
    my ($ix,$part) = @_;
    my (@cids,%cids);

    my $tmphead = $part->head();
    $tmphead->decode();

    my $part_name = $tmphead->recommended_filename();

    $cids[$ix] = $tmphead->get('Content-id');
    $cids[$ix] =~ s/\<|\>//g;
    if (!($cids[$ix]))
    {
        $cids[$ix] = $tmphead->get('Content-location');
    }
    $cids{$cids[$ix]} = $part->mime_type();

    my $content_type = $part->mime_type();

    handle_image_part($part)
        if ($part->mime_type =~ /gif|png|jpe?g/i);

    handle_text_part($ix,$part)
        if ($part->mime_type =~ /text.html/i || $part->mime_type =~ /text.plain/i);
    handle_rfc822_part($ix,$part)
        if ($part->mime_type =~ /message.rfc822/i);

    handle_misc_part($ix,$part,$part_name)
        if ($part_name && $part->mime_type !~ /message.rfc822/i);

}


sub viewable {
    my ($mime_type) = @_;

    $mime_type = lc($mime_type);
    
    my %viewable = map { $_ => 1} split(/\s+/, $c{viewable_mime_types});
    
    # check if this mime type is viewable
    return 1 if ($mime_type =~ /^text.plain/ || 
                 $mime_type =~ /^text.html/ ||
                 $mime_type =~ /^text.enriched/ ||
                 $mime_type =~ /^application.msword/ ||
                 $mime_type =~ /gif|png|jpe?g/ ||
                 $mime_type =~ /^message.rfc822/ ||
                 $viewable{$mime_type}
                );

    return 0;
}


sub process_parts {
    my ($part,$message_ref,$prologue_ref,$attach_ref,$multiparts,$ix,$msg,$used_cids) = @_;
    my $inline_html = 0;
    my $got_it = 0;
    my $target;
    my @parts;

    debug "here $ix, ".$part->mime_type;

    if ($ix == 0 && $part->is_multipart) {
        $used_cids = build_cids_hash($part);
    }

    if ($part->mime_type =~ /multipart.alternative/i) {
        debug "looking for alternative part";
        get_alternative2($part, $message_ref, $msg, $used_cids);
    }

    if ($part->parts > 0) {
        debug "multipart";
        foreach my $p ($part->parts) {
            $ix++;
            next if ($part->mime_type =~ /multipart.alternative/i);
            process_parts($p,$message_ref,$prologue_ref,$attach_ref,$multiparts+1,$ix,$msg,$used_cids);
        }
    }

    else {
        # process a single part

        debug "single part, ".$part->mime_type;
        my $is_attach = $ix > 1 ? 1 : 0;
        my $mime_type = lc($part->mime_type);

        my %viewable = map { $_ => 1} split(/\s+/, $c{viewable_mime_types});
    
        # first push in any message text (first part, if text/plain or text/html
        if ($ix <= 1 && viewable($mime_type) &&
                ($mime_type =~ /text.plain/ || 
                 $mime_type =~ /text.html/ ||
                 $mime_type =~ /text.enriched/ ||
                 $viewable{$mime_type} )
           ) {
            push (@$message_ref, get_part_text($part));
        }
        else {
            # next push in attachment if this is multipart (but don't push in
            # the first part of a multipart
            my $p_ix = $ix < 1 ? $ix : $ix - 1;
debug "push in attachment: part ". $part->head->get('Content-Type').", ix = " .$ix. ", multiparts = " . $multiparts;

            my $tmp = add_attach($part, $attach_ref, $ix - $multiparts, $msg);
            add_prologue($part, $prologue_ref, $p_ix, $tmp, $msg, $used_cids);
        }
    }

    return 1;

}


# Julia changed 06.24.2005   
# Julia added 06/07/2005
sub process_msg_parts {
    my ($parts,$message_ref,$prologue_ref,$attach_ref,$multiparts,$ix,$msg,$used_cids) = @_;
    my $inline_html = 0;
    my $got_it = 0;
    my $target;

	my $ix = 0;

	foreach my $part (@{$parts}) {
		process_single_part($part,$message_ref,$prologue_ref,$attach_ref,$multiparts,$ix,$msg,$used_cids);
    	$ix++;
	}
    return 1;
}

sub process_single_part {
	my ($part,$message_ref,$prologue_ref,$attach_ref,$multiparts,$ix,$msg,$used_cids) = @_;
	
        # process a single part
        debug "single part $ix, ".$part->mime_type;
		
        my $is_attach = $ix > 1 ? 1 : 0;
        
        my $mime_type = lc($part->mime_type);

        my %viewable = map { $_ => 1} split(/\s+/, $c{viewable_mime_types});
    
        # first push in any message text (first part, if text/plain or text/html
        if ($ix <= 1 && viewable($mime_type) &&
        ($ix < 1 && !$userdb{"options.autoload"}) &&
                ($mime_type =~ /text.plain/ || 
                 $mime_type =~ /text.html/ ||
                 $mime_type =~ /text.enriched/ ||
                 $viewable{$mime_type} )
           ) {
            push (@$message_ref, get_part_text($part));
        }
        else {
            # next push in attachment if this is multipart (but don't push in
            # the first part of a multipart
            my $p_ix = $ix < 1 ? $ix : $ix - 1;

debug "push in attachment: part ". $part->head->get('Content-Type').", ix = " .$ix;

            my $tmp = add_attach($part, $attach_ref, $ix, $msg);
            add_prologue($part, $prologue_ref, $p_ix, $tmp, $msg, $used_cids);
       }
       return 1;
}
# End of Julia added 06/07/2005
# End of Julia added 06/24/2005


# This is needed by the pre-4.5 interface. I moved it out of msg_do, but we cannot remove it entirely yet.
sub fetch_folder_list
{
    my ($suggested_fold) = @_;
    my $folder_list;

    # only put this here if the folder doesn't exist, otherwise we'll have doubles. We don't want doubles.
    my @folders = get_folders();

    if (!grep($_ eq $suggested_fold, @folders)) 
    {
	$folder_list = "<OPTION SELECTED>" . substr($suggested_fold, 0, $c{'folder_namelen'}); # folders are limited to 18 chars
    }

    debug "got here";
    foreach my $thefold (@folders)
    {
	debug "working folder $thefold ($folder)";
	$thefold = substr($thefold, 0, $c{'folder_namelen'});       # folders are cut at 18 characters
	next if ($thefold eq $folder); # what's the point of moving a message in a folder to the same folder ?

	if ($thefold eq $suggested_fold)
	{
	    $folder_list .= "<OPTION SELECTED>$thefold";
	    next;               
	}

	$folder_list .= "<OPTION>$thefold";
    }   
}

sub chunk_msg
{
    my ($message,$chunk) = @_;
    my ($string, $m);

    return $message unless $chunk;

    my ($chunk_size) = ($c{"chunk_size"} - 20) || 750;
             # chunk size is the size in bytes of each chunk.

    my ($ind) = ($chunk - 1) * $chunk_size;

    # Only do this if we've got something prior to find even
    if ($chunk > 1) {
        #get the beginning of cut off word at start of chunk
        my ($before) = substr($message, $ind-9, 10);
        $before =~ /\s(\S+)\S$/;
        $string .= $before;
    }
    
    #get the chunk we want 
    $m = substr($message, $ind, $chunk_size);

    #get the rest of a cut off word at end of chunk
    my $after = substr($message, ($chunk_size * $chunk) -1, 10);
    my ($wordend) = ($after =~ /^\S(\S+)\s/) ;

    $string .= $m . $wordend;

    #remove incomplete <br/> elements    
    $string =~ s/^br\/>|^r\/>|^\/>|^>|<br\/$|<br$|<b$|<$//ig;

    # Set next Chunk
    if ( (length($message)/$chunk_size) > $chunk)

    {
        write_tmp("next_chunk",($chunk+1));
    }

debug "message after: $string";

    return $string;
}
 


sub chunk_msg_second
{
    my ($msg_ref,$chunk) = @_;

    return $msg_ref unless $chunk;

    # Join and Scalarize array
    my (@msg) = @{ $msg_ref } if $msg_ref;
    my ($message) = join("\n",@msg);

    my ($chunk_size) = ($c{"chunk_size"} - 20) || 750; 
             # chunk size is the size in bytes of each chunk.


    my (@m);
    my $ind = ($chunk - 1) * $chunk_size;

    #make sure the chunk begins at a word boundary
    my $before = substr($message, $ind-9, 10);
    my ($wordbeg) = ($before =~ /\s(\S+)\S$/) ;
    if ($wordbeg) {push (@m, $wordbeg) };


    #get the chunk we want and arrayize it
    push (@m, substr($message, $ind, $chunk_size));


    #make sure the chunk includes all of the last word
    my $after = substr($message, ($chunk_size * $chunk) -1, 10);
    my ($wordend) = ($after =~ /^\S(\S+)\s/) ;
    if ($wordend) {push (@m, $wordend) };



    # Set next Chunk
    if ( (length($message)/$chunk_size) > $chunk)
    {
	write_tmp("next_chunk",($chunk+1));
    }

    return (\@m);
}

sub chunk_msg_first
{
    my ($msg_ref, $chunk) = @_;

    my (@long_msg) = @{ $msg_ref } if $msg_ref;
    my (@msg);
    foreach my $line (@long_msg)
    {
	my (@m) = split(/\n|\r/,$line);
	push (@msg,@m);
    }

#    my (@foo);
#    push(@foo, "size = ",scalar(@msg));
#    return \@foo;


    my ($chunk_size) = $c{"chunk_size"} || 500; # chunk size is the size in bytes of each chunk.

    my ($current_chunk) = 1;
    my ($current_size) = 0;
    my (@chunk,$chunk_complete,$extra);

    foreach my $line (@msg)
    {
	my ($line_size) = length($line);

	# Add onto our chunk
	if ( ($current_size + $line_size) < $chunk_size)
	{
	    push(@chunk,$line);
	    $current_size += $line_size;
	    $chunk_complete = 0;
	}

	else
	{
	    my ($difference) = abs($current_size - $chunk_size);

	    push(@chunk,substr($line,0,$difference)); # push last of chunk onto array
	    # @chunk should have our chunk.

	    $extra = substr($line,$difference);
	    $chunk_complete = 1;
	}

	if ($chunk_complete)
	{
	    if ($current_chunk == $chunk)
	    {
		last; #this is the chunk we want
	    }
	    else
	    {
		# Start over, but clear/increment counters
		$current_size = length($extra); #keep the size acurate
		$current_chunk++;
		@chunk = undef;
		push(@chunk,$extra); #Add the "extra" bit to the start of this chunk
	    }
	}
	return (\@chunk);
    }

    if (scalar(@chunk))
    {
	return \@chunk;
    }
    else
    {
	return \@msg;
    }
}


sub detach
{
    my ($message, $part, $getprologue) = @_;  # 09/24/98 - RMK
    my ($head, $tmphead, $parser, $line, $entity, @parts, $content_type, $filename, $io);
    my ($evalcheck, $force);

    if (!$message)
    {
	($message, $part, $content_type) = split(/:/, $query->param('variable'), 3);
    }

    $force = $query->param('force');

    $content_type = decode($content_type) if ($content_type);

    debug "Detaching part $part from message $message, ct=$content_type";

    my $msgfile;
    if ($message =~ /^rfc822/) {
        debug "opening rfc822 attachment";
        $msgfile = "$homedir/tmp/rfc822";
    }
    else {
        $msgfile = "$homedir/messages/$message";
    }

    if (!-e "$msgfile") {
        # hmmm why isnt it there? I guess we can attempt to find it in server
        if (!download_msg($message)) {
            set_status($msg{'ERR_MSGNotInServer'});
            go_index();
            return 0;
        }
    }

    $parser = new MIME::Parser;
    $parser->ignore_errors(1);
    $parser->decode_headers(1); 
    $parser->extract_uuencode(1);
    $parser->extract_nested_messages(0);
    $parser->output_dir("$homedir/tmp");
    $parser->output_prefix("det".time);

    $entity = $parser->parse_open($msgfile);

    @parts = get_parts($entity);

    # if there is more than just get the specific attachment the user specified
    if ($part > 0)
    {
	if (!$parts[$part])
	{
	    debug "no such part $part in message $message!";
	}

	$evalcheck = eval {
            $tmphead = $parts[$part]->head();
            $tmphead->decode();
	    $filename = $tmphead->recommended_filename;
            $filename =~ s/[\s|\/]/_/g;
	    $content_type = $content_type || $parts[$part]->mime_type() || find_mime_type($filename);
	    $io = $parts[$part]->bodyhandle()->open("r");
		debug "part is $part, Content-Type = " . $tmphead->get('Content-Type') . ", filename = ".$filename
	};
    }
    else
    {
        my $ent;
        if (@parts) {
          # If $parts is zero or undef, try the first part found
          $ent = $parts[0];
        } else {
          # If there aren't any parts, its likely the actual message is a file that we want.
          $ent = $entity;
        }

	$evalcheck = eval {
            $tmphead = $ent->head();
            $tmphead->decode();
	    $filename = $tmphead->recommended_filename();
            $filename =~ s/[\s|\/]/_/g;
	    $content_type = $content_type || $ent->mime_type() || find_mime_type($filename);
            debug "part name: $filename, type: ".$tmphead->mime_type();
	    $io = $ent->bodyhandle()->open("r"); 
            debug "ERROR opening attach!" if (!$io);
	};
        if ($@) {
           debug "eval error: $@";
           error "eval error: $@";
        }
    }

    $filename =~ s/\//./g;

    debug "content_type=$content_type  filename='$filename'";

    # 08/06/98: if the attachment doesn't have a name, use the content-type as the name
    if (!$filename)
    {
	$filename = $content_type;
	$filename =~ s/\//./g;
    }

#    debug "IO is $io and $evalcheck";

    if (!$io)
    {
	my($url);
	$url = make_url("go_index");

	write_tmp("title", $msg{'ERR_Detach_T'});
	write_tmp("phrase", convert($msg{'ERR_Detach_B'}, $url));
	load_page("errors.html");
    }
    else
    {
	debug "So far so good...";

        # map certain types to text/plain
        $content_type = "text/plain" if ($content_type =~ /message\//i);

	# NOTE:
	#  08/07/98: Got into some sort of endless loop when viewing a wordfile (ICQAPI.doc)
	if (!$getprologue && !$force && (lc($content_type) eq "application/msword") && !$c{'disable_msword'})
	{
	    debug "display Word file";

	    write_tmp("attachurl",make_url("detach","$message:$part", force => 1));
            my $wb = word_convert("$homedir/tmp/$filename");
            write_tmp("word_body", $wb);
	    &load_page("wordview.html");
	    return;
	}
	elsif (!$getprologue && $content_type ne "text/html")
	{
	    #this is the generic case...for some reason it's in the middle of this case...
	    debug "I'm here...$content_type filename=$filename";
	    print "Content-type: $content_type\n";
	    debug "Content-type: $content_type\n";
	    
	    my $disp = $c{attachment_disposition} || 'attachment';
	    
	    # 07/25/98: suggest the name of the file when the user tries to download it
	    print "Content-disposition: $disp; filename=$filename\n\n";
	    while ($_ = $io->getline()) {
                print;
            }
	}

	# 09/23/98 - RMK added specific inline for html attachments
	#Revamped by MM 01/11/99 (MHTML support!)
	elsif ($content_type =~ /text\/html/i)
	{
	    #This is the case when we have text/html and need to do CID rewriting for MHTML support
	    debug "detach text/html $content_type AND hello!!";
	    &print_content_headers($content_type);

	    print get_html_part($entity,$io,$message);
	}
	# 09/24/98 - RMK indicate no prologue
	elsif ($getprologue) 
	{
	    return 0;
	}
    }

    debug "END OF DETACH";
}

sub get_html_part
{
    my ($entity,$io,$message,$used_cids_ref) = @_;

    #This is used to get a nicely coded chunk of HTML.  
    # It translates CIDs into appropriate EMUmail calls
    #
    # Takes a MIME entity, MessageUID and an open File handle
    #
    # Returns a scalar

    my $final = undef;

    debug "here ".$entity->mime_type;
    my %cids;

    if (!$used_cids_ref) {
        my $cids = &build_cids_hash($entity);
        %cids = %{$cids} if $cids;
    }
    else {
        %cids = %$used_cids_ref;
    }

	my (@parts) = keys(%cids);
	my ($part);
	
	my $tmp = "";
        my $unfinished_body = 0;
        my $remove_base = 0;

debug "here 2";
        while (defined($tmp = $io->getline())) 
	{
debug "$tmp";
            if ( $tmp =~ /cid:([^\>\"\'\s]+)/i ) 
	    {
                my $cid = $1;
                debug "cid is ($cid) part is $cids{$cid}";

                my $url = make_url("detach", "$message:".$cids{$cid});
                debug "url $url";

                $tmp =~ s/cid:[^\>\"\'\s]+/$url/gi;
#                $used_cids_ref->{$cids{$cid}} = 1;
	    }

	    $tmp =~ s/\<\/*HTML\>//i;  #Remove <HTML> tags for Netscape rendering.
	    $tmp =~ s/HREF\s*=\s*\"FILE\:\/\/[^\"\>]*\"*//ig; # Security to make sure they can't mess with your files.
	    $tmp =~ s/\<\/BODY\>//ig;  #Remove close BODY tags
	    $tmp =~ s/\<\/HEAD\>//ig;  #Remove close HEAD tags
	    $tmp =~ s/\<HEAD.*?\>//ig;  #Remove HEAD tags

            # take care of unfinished removal of BASE tag
            if ($remove_base && $tmp =~ /\>/) {
                $tmp =~ s/^[^\>]*\>//;
                $remove_base = 0;
                debug "cut out remaining portion of BASE tag";
            }

            # remove any BASE references...
            if ($tmp =~ /\<BASE\s+([^\>]+)/i) {
                debug "removing BASE tag information, wont apply to us here";
                if ($tmp !~ /\<BASE\s+([^\>]+)\>/i) {
                    $remove_base = 1;
	            $tmp =~ s/\<BASE\s+([^\>]+)//i;
                }
                else {
	            $tmp =~ s/\<BASE\s+([^\>]+)\>//i;
                }
            }

            # take care of "unfinished body" by cutting out up to closing >
            if ($unfinished_body && $tmp =~ /\>/) {
                $tmp =~ s/^[^\>]*\>//;
                $unfinished_body = 0;
                debug "cut out remaining portion of BODY tag";
            }

	    # See if we have a BODY BACKGROUND that needs attention
	    if ($tmp =~ /\<BODY\s+([^\>]+)/i)
	    {
                if ($tmp !~ /\<BODY\s+([^\>]+)\>/i) {
                    $unfinished_body = 1;
	            $tmp =~ s/\<BODY\s+([^\>]+)//i;
                }
                else {
	            $tmp =~ s/\<BODY\s+([^\>]+)\>//i;
                }
debug "unfinished body? $unfinished_body";

		debug "velvety $1";
		my $body_parms = $1;
		my ($bg_color,$background);

		if ($body_parms =~ /BGCOLOR\s*=\s*\"?([^\s"]+)\"?/i )
		{
		    $bg_color = $1;
		    debug "found a background color: $bg_color";
		}

		if ($body_parms =~ /BACKGROUND\s*=\s*\"?([^\s"]+)\"?/i )
		{
		    $background = $1;
		    debug "found a background: $bg_color";
		}

		write_tmp("mhtml_bgcolor",$bg_color) if $bg_color;
		write_tmp("mhtml_background",$background) if $background;
	    }

	    $final .= $tmp;
	}

    return $final;
}

# Julia add 06/07/2005
#sub get_cid {
#    my ($part) = @_;
#
#    my $cid = $part->head()->get('Content-id');
#    $cid =~ s/\<|\>//g;
#    if (!($cid))
#    {
#	$cid = $part->head()->get('Content-location');
#    }
#
#    $cid =~ s/\r|\n//g;
#    return $cid;
#}

sub get_cid {
    my ($part) = @_;


	my $cid = $part->head()->get('Content-id');
    $cid =~ s/\<|\>//g;
    
    if (!($cid)) {
		$cid = $part->head()->get('Content-location');
    }

# some parts might not have nor Content-ID nor Content-location
    if (!($cid)) {
		$cid = $part->head()->get('Content-Type');
		my @tmp_cid = split(/;/, $cid);
		$tmp_cid[1] =~ /name="([A-z]+.[A-z]+)"/;
		$cid = $1;
	}
	
    $cid =~ s/\r|\n//g;
    return $cid;
}
# end of Julia add


sub build_cids_hash
{
    my ($entity) = shift;
    my (%cids,@parts,$part,@cids);

    @parts = get_parts($entity);
    debug "size of parts:".scalar(@parts);

    #what we're doing here is building a hash of content id's (cids)
    # to translate a part # into it later... 
    # there is definately a better way to 
    # do all this mime stuff... can't wait to rewrite

    if (@parts)
    {
	foreach $part (1 .. $#parts) # skip the first part because it's body msg
	{
	    debug "ttam: part hash: $part";
debug "mime type ".$parts[$part]->mime_type;
            my $cid = get_cid($parts[$part]);

	    $cids{$cid} = $part if ($cid);

	    debug "set $cid = ".$part;
	}
    }

    return \%cids;
}

sub print_content_headers
{
    my ($content_type,$filename) = @_;

    $content_type = $content_type || "text/html";

    if ($filename)
    {
	$filename =~ s/\"|\s/_/g;
	print "Content-disposition: attachment; filename=$filename\n";
    }

    unless ($c{"disable_cache_headers"})
    {
	my $cache;
	$cache = $c{"cache_headers"} || "Cache-Control: no-store, private";
	print "$cache\n";
    }

    debug "Content-type: $content_type";
    print "Content-type: $content_type\n\n";
}


sub get_parts 
{
    my ($ent,$total) = @_;
    my $part;
    my (@total);

    $total = 0 if (!($total));

    my @parts = $ent->parts;

debug "Found ".scalar(@parts)." parts";
    foreach $part (@parts)
    {
        debug "multipart ".$part->is_multipart." ".$part->mime_type();

debug "part is " . $part->head->get('Content-Type');
        
	if ($part->is_multipart() )
	{
            # Ahhh we need to be able to process cases where the first
            # part of a multipart happens to be a multipar/alternative.
            # In that case, favor an html alternative
            if ($part->mime_type =~ /multipart.alternative/i) {
                my @tmp_parts = $part->parts;
                my $tmp_part = get_alternative(\@tmp_parts);
                push(@total, $tmp_part) if ($tmp_part);
            }
            else {
                push (@total, get_parts($part,\@total) );
            }
	}
	else
	{
	    push (@total, $part);
	}
    }

    debug "ttam: total parts: ".scalar(@total);

    return (@total);
}

sub get_allparts
{
   my ($entity) = @_;
   
   if ($entity->is_multipart && (my @parts = $entity->parts)) {
      return map { get_allparts($_) } @parts;
   } else {
      return $entity;
   }
}

sub find_mime_type
{
    my ($extn, $default) = @_;

    if ($extn =~ /^[0-9a-f]{32}$/i) 
    {
	return "text/plain";
    }

    return "text/plain" if ($extn =~ /text.plain$/i);
    return "text/html" if ($extn =~ /text.html$/i);

    $extn =~ s/.*(\..*)/$1/;    # get the extension

  SWITCH:
    {
	$extn =~ s {\.html?$} {text/html}i              && last; # .htm or .html
	$extn =~ s {\.txt$}   {text/plain}i             && last;
	$extn =~ s {\.gif$}   {image/gif}i              && last;
	$extn =~ s {\.png$}   {image/png}i              && last;
	$extn =~ s {\.bmp$}   {image/x-MS-bmp}i         && last;
	$extn =~ s {\.jpe?g$} {image/jpeg}i             && last; # .jpg or .jpeg
	$extn =~ s {\.pdf$}   {application/pdf}i        && last;
	$extn =~ s {\.tex$}   {application/x-tex}i      && last;
	$extn =~ s {\.zip$}   {application/zip}i        && last;
	$extn =~ s {\.tar$}   {application/x-tar}i      && last;
	$extn =~ s {\.gz$}   {application/x-gzip}i      && last;
	$extn =~ s {\.tgz$}   {application/x-tar}i      && last;
	$extn =~ s {\.mpe?g$} {video/mpeg}i             && last;
	$extn =~ s {\.mp3$}   {audio/mpeg}i             && last;
	$extn =~ s {\.avi$}   {video/avi}i              && last;
	$extn =~ s {\.mov$}   {video/quicktime}i        && last;
	$extn =~ s {\.wav$}   {audio/x-wav}i            && last;
	$extn =~ s {\.au$}    {audio/basic}i            && last;
	$extn =~ s {\.ps$}    {application/postscript}i && last;
	$extn =~ s {\.eps$}   {application/postscript}i && last;
	$extn =~ s {\.doc$}   {application/msword}i     && last;
	$extn =~ s {\.rtf$}   {application/rtf}i        && last;
	$extn =~ s {\.msg$}   {message/rfc822}i         && last;
	$extn =~ s {\.xl.$}   {application/vnd.ms-excel}i        && last;
	$extn =~ s {\.pp.$}   {application/vnd.ms-powerpoint}i   && last;
	$extn =~ s {\.pntg?$} {image/x-macpaint}i         && last;
	$extn =~ s {\.xml$}   {application/xml}i          && last;
	$extn =~ s {\.dcr$}   {application/x-director}i   && last;
	$extn =~ s {\.hqx$}   {application/mac-binhex40}i && last;
	$extn =~ s {\.swf$}   {application/x-shockwave-flash}i     && last;
	$extn =~ s {\.tiff?$}   {image/tiff}i           && last;
	$extn =~ s {\.vcf$}   {text/x-vcard}i           && last;
	$extn =~ s {\.sit$}   {application/x-stuffit}i  && last;
	# default
	$extn = $default || "application/octet-stream";
    }

    return $extn;
}

sub go_index
{
    my ($force_check) = @_;
    my ($foldertype,$foldfile);
    my ($reload);
    my ($total, $uu, $pp);

    $delay=time if ($delay == 0);
#    debug "checkpointing delay";

    debug "folder=$folder last folder=".$v{"last_folder"};
#   debug "current page is ".$v{$folder."_page"};

    untie %folderdb;
	$ELocks->lock_remove(\%folderdb); # it was done if ($v{"last_folder"}) but i don't understand the reason
	debug "removed lock from folderdb";

    $foldfile = process_fold_type($folder);
    debug "trying to reopen folder db";
    if ( $ELocks->lock_create("$homedir/folders/$foldfile", \%folderdb, {mode => 'write', nb => 1}) )
    {
		tie %folderdb, $db_package, "$homedir/folders/$foldfile", O_CREAT|O_RDWR, 0660;
		debug "opened folder |$foldfile|";
    }
    else
    {
    	debug "can't lock folder $foldfile. $!";
    }
    
    if ( (($protocol =~ /imap/i) || ($c{"pure_imap"})) && !$userdb{"folder:$folder:external"})
    {
	($uu, $pp) = ($userdb{"folder:$inbox:username"}, decode($userdb{"folder:$inbox:password"}));
    } else {
	($uu, $pp) = ($userdb{"folder:$folder:username"}, decode($userdb{"folder:$folder:password"}));
    }
#	debug "uu=$uu  ; ", $userdb{"folder:$folder:external"}, " ; ", $userdb{"folder:$folder:username"}, " ; ";
    write_tmp("folder", $folder);
    $v{"folder"} = $folder;

    $v{"wait_title"} = $msg{"WAIT_CheckHeaders"} if(!$v{"wait_title"});

    get_index($uu, $pp, $force_check);
    
    my ($total_msgs, $unread_msgs, $read_msgs, $answered_msgs) = get_curr_folder_msginfo();

    debug "TOTAL=$total_msgs";


    $reload = $userdb{"options.checkmail"} || 300;

    
    if ($folder eq $inbox) {
       my $new_mail;
       if (exists($v{total_msgs})) {
          $new_mail = $total_msgs - $v{total_msgs};
          $new_mail = 0 if $new_mail < 0;
       } 
       $v{total_msgs} = $total_msgs;
       write_tmp('new_mail', $new_mail);
    }

    # 07/24/98: allow the admin to configure what is prepended to outbound mail folder names 
#    $foldertype = ($folder =~ /^\Q$msg{'V_SentmailFolderPretext'}/ ? $msg{'V_IndexTop_To'} : $msg{'V_IndexTop_From'});

#    write_tmp("foldertype", $foldertype, 1);
    write_tmp("total_msgs",$total_msgs);
    write_tmp("unread_msgs", $unread_msgs);
    write_tmp("read_msgs", $read_msgs);
    write_tmp("answered_msgs", $answered_msgs);
    
    my $q_allowed = ($v{"quota_allowed"} >= 1) ? ($v{"quota_allowed"}/1024.0) : $v{"quota_allowed"};
    $q_allowed =~ s/^(\d+)\.(\d)(\d)(.*)$/$1.$2$3 kB/;
    my $q_used = ($v{"quota_used"} >= 1) ? ($v{"quota_used"}/1024.0) : $v{"quota_used"};
    $q_used =~ s/^(\d+)\.(\d)(\d)(.*)$/$1.$2$3 kB/;
    write_tmp("allowed", $q_allowed);
    write_tmp("used", $q_used);

    write_tmp("quota_pct", $v{"quota_pct"});

    write_tmp("myfolder", $folder || $inbox, 1);
    write_tmp("reload", $reload, 1);
    write_tmp("tmp", make_url("go_index", "refresh"), 1);
    write_tmp("status", $status, 1);
    $v{"force_check"} = $force_check;

    my $sorttype = $folderdb{"sorttype"};

    if ($query->param('first'))
    {
	my ($page);
	if ($page=$c{'post_login_page'})
	{
	    waiting(\&load_page, $page, undef, $query->param('type') || $v{'emu_type'} || $c{'default_interface'});
	}
	else
	{
	    waiting(\&load_page, "msgindex.html");
	}
    }
    else
    {
	waiting(\&load_page, "msgindex.html");  
    }

    # write two public variables
    $v{"returnto"} = "go_index";
    $v{"last_folder"} = ($folder || $inbox);

}


sub print_progress {
    my ($text) = @_;

#    debug "no_waitscreen=$no_waitscreen waiting_printed=$waiting_printed";
    return if ($no_waitscreen || bool($c{"disable_waitscreen"}) || !$waiting_printed);

#    debug "$text";
    print "<script language=JavaScript>\n";
    print "waitscr.document.writeln('".$text."')";
    print "\n</script>\n";

}


sub finish_waitscreen {
    return if (!$waiting_printed);

    print <<END;
<script language=JavaScript>
waitscr.close()
</script>
END

}


sub display_waitscreen {
    return 1 if ($waiting_printed);
    return 0 if ($no_waitscreen || bool($c{"disable_waitscreen"}));

    $| = 1;

    STDOUT->autoflush(1);
#    debug "doing waitscreen... time is ".time.", delay is $delay";

    print_header() if (!$header_printed);

    print <<END;
<head>
<script language=JavaScript>
waitscr = window.open("", "waitscreen", "scrollbars=1,width=250,height=325");
END

    my $ra_data = load_page_external("waitwindow.html");

    my $html_page;
    my $thedata;
    foreach $thedata (@{$ra_data}) {
        $thedata =~ s/\n//;
        $html_page .= qq{$thedata};
    }

    $html_page .= $v{"wait_title"} if ($v{"wait_title"});

    print "waitscr.document.writeln('".$html_page."')";
    print "</script>";

    $waiting_printed = 1;
#    debug "$waiting_printed";
    return 1;
}


sub get_wait_interval {
    my ($num_msgs) = @_;

#    debug "total: $num_msgs";
    return ($num_msgs > 1000) ? int($num_msgs/30) : ($num_msgs > 500) ? int($num_msgs/25) : ($num_msgs > 100) ? int($num_msgs/20) : ($num_msgs > 50) ? int($num_msgs/10) : 5;
}


sub select
{
    debug "folder is $folder last folder is ".$v{"last_folder"};

    #for multiple selections
    if ($query->param('reload.x'))
    {
	go_index();
    }
    elsif ($query->param('changem.x'))
    {
	my ($mbox);
	
	$mbox = $query->param('mailbox');

	if (defined $userdb{"mailboxes.u:$mbox"})
	{
	    # note: save main protocol?
	    $v{'bRemoteBox'} = $mbox;

	    debug "Set remote mailbox for $mbox with folder $folder\n";

	    $folder     = $mbox;
	    
	    $v{"folder"} = $folder;
	}
	else
	{
	    set_status($msg{'ERR_MBoxNoExist'});
	}

	go_index();
    }
    # RB 1/26/2004
    # returning old apply filters code by customer's request
    elsif ( $query->param('filter.x') )
    {
	debug "going to apply filters";
	my ($filtercount, $status);

	# initialize the counter prior to starting
	$v{"filtered to"} = 0;

	$v{"wait_title"} = $msg{"WAIT_FilterMsgs"};

	FILTER_LOCAL_OR_POP:
	{
		debug "filtering folder $folder, protocol ".$userdb{"folder:$folder:protocol"};
		last if( $userdb{"folder:$folder:protocol"} =~ /imap/i );

		my @msgs = split( /:/, $folderdb{"messages"} );
		debug "we have " . scalar @msgs . " msgs before filtering";
		$v{"wait_interval"} = get_wait_interval( scalar(@msgs) );

		my $processed = 0;
		my $themsg;
		
		foreach $themsg ( @msgs )
		{
			debug "filtering $themsg";
			# remove the message from the folder if filtered
			$filtercount += filter_message_local( $themsg, 1 );
			print_progress_new(0);

			if ($v{"wait_count"}++ % $v{"wait_interval"} == 0)
			{
				$v{"wait_action"} = convert( $msg{"WAIT_ProcessedMsgs"}, $v{"wait_count"} );
				$v{"wait_action"} .= convert( $msg{"WAIT_FilteredNum"}, $filtercount );
			}
			$processed++;
		}

		$v{"filtered to"} = $filtercount;
	}

	FILTER_IMAP:
	{
		last if( $userdb{"folder:$folder:protocol"} !~ /imap/i );

		my( $u, $p, $host ) = get_folder_credentials( $folder );
		do_login_sequence( "imap", $u, $p, $host, $folder, 0)
			if (!$pop || ref $pop ne 'EMU::IMAP' || 
			$pop->{user} ne $u || $pop->{host} ne $host);

		# $pop->select($folder) if ($pop && $pop->{folder} ne $folder);
		# We only filter from inboxes
		
		$pop->select( $inbox );
		$status = filter_messages_imap() if( $pop );
		debug "finished filtering, folder is $folder";
	}

	if( $protocol =~ /imap/i ) # && $v{"filtered to"} > 0
	{
		debug "expunging, select folder $folder";
		$v{"wait_action"} = convert( $msg{"WAIT_FilteredNum"}, $v{"filtered to"} );
		$pop->expunge();
		print_progress_new( 0, 1 );
		my $message = convert( $msg{'MSG_Filtered_Num'}, $v{"filtered to"} );
		$message .= $status if $v{"filtered to"} > 0;
		set_status( $message );
	}
	$v{"filtered to"} = 0;
	go_index(1);
	
    }
    elsif ($query->param('refresh.x'))
    {
	# if we are in a remote mailbox and they are hitting check for
	# new mail then we need to set them into the remote mailbox's inbox
	# and refresh. If they aren't in a remote mailbox then we set
	# ourselves into the main INBOX and refresh.

	debug "Folder has been set to $folder";
	$v{"folder"} = $folder;

	go_index();
    }
    elsif ($query->param('compose.x'))
    {
	compose();
    }
    elsif ($query->param('move.x'))
    {
        $folder = $query->param('folder');
	move_msg(0,0);
    }
    elsif ($query->param('index_jump.x'))
    {
	index_jump();
    }
    # 02/12/99 RMK Added export funciont for selected messages
    elsif ($query->param('export.x'))
    {
        my (@messages) = $query->param('d');

        if (scalar(@messages) <= 0) {
	    set_status($msg{'ERR_NoMoveMessage'});
	    go_index();
	    return;
        }
#        debug "messages to export: @messages";
        export_messages("selected_msgs", @messages);
    }
    elsif ($query->param('delete.x'))
    {
        $v{"wait_count"} = 0;
        my @garbage = $query->param('d');

        $v{"wait_title"} = convert($msg{"WAIT_DeleteMsgs"}, scalar(@garbage));

        if ( $trash_bin && ($folder ne $trash_folder)) {
            move_msg(1,0);
        }
        else {
	    delete_mass();          # delete a group of messages
        }
    }
    elsif ($query->param('options.x'))
    {
	options();
    }
    elsif ($query->param('newfold.x'))
    {
	folders();
    }
    elsif ($query->param('empty.x'))
    {
        my $f = $folder;
        empty_folder($f);
        set_status(convert($msg{'ERR_FolderEmpty'}, $f));
        go_index();
    }
    elsif ($query->param('mark.x'))
    {
	my @moved = $query->param('d');
	mark_read_unread(@moved);	
    }
    else
    {
	search();
    }
}


sub index_jump
{
    debug "folder $folder POSITION2: ".$query->param('position2');
    #select a page to view
    $v{$folder . "_page"} = $query->param('position') || $query->param('position2');
    debug "folder: $folder, page: ".$v{$folder."_page"};

    # force a check when jumping? Since IMAP does UID slicing, we need to
    # force a check... but POP doesnt.
    my $force_check = $userdb{"folder:$folder:protocol"} =~ /imap/i ? 1 : 0;

    go_index($force_check);
}

sub reply_msg
{
    my ($reply_type, $message) = @_;
    my ($msgto, $msgcc, $msgsubj);
    my (@cc,@to);
    my $h_ref;

    # 08/24/98: make the uid safe for the database
    $message = safe(':', $message);

    debug "parms are @_";

    my $searchfold = $msg{"FOLD_Search_Results"} || "Search Results";
    if ($folder eq $searchfold || $folderdb{"$message:date"} eq "")
    {
	$h_ref = header_from_file($message) || {};
    }
    else
    {
        $h_ref->{"replyto"} = $folderdb{"$message:replyto"};
        $h_ref->{"from"}    = $folderdb{"$message:from"};
        $h_ref->{"to"}      = $folderdb{"$message:to"};
        $h_ref->{"cc"}      = $folderdb{"$message:cc"};
        $h_ref->{"bcc"}     = $folderdb{"$message:bcc"};
        $h_ref->{"subj"}    = $folderdb{"$message:subj"};
        $h_ref->{"date"}    = $folderdb{"$message:date"};
    }

    my $to = $h_ref->{"replyto"} || $h_ref->{"from"};
    $msgto = (addr_split($to))[1]; # just get the email address part

    # add in the cc's if they're replying to everyone
    if (-1 != index($reply_type,"all"))
    {
	my $msg_fold = $folderdb{"$message:folder"};
	# don't let the email address of the message's current folder be put in the reply list...
        # RMK 19990506 do a few other filters as well
        debug "parsing to ".$h_ref->{"to"};
        @to = Mail::Address->parse($h_ref->{"to"});
        @to = map ( $_->address() , @to);
        debug "to list is @to";

	#MM 10/18/98 -- Fixed condition under REPLY_ALL where @to returned full addr instead of e-mail only
        debug "parsing cc ".$h_ref->{"cc"};
        @cc = Mail::Address->parse($h_ref->{"cc"});
        @cc = map ( $_->address() , @cc);
        debug "cc list is @cc ";

        # weed out any repetitive addresses
	@to = grep(!/^$folderdb{"username"}$/, @to) if ($folderdb{"username"});
	@to = grep(!/^$userdb{"options.email"}/, @to);
	@to = grep(!/^$msgto/, @to);
        @cc = grep(!/^$userdb{"options.email"}/, @cc);
	@cc = grep(!/^$msgto/, @cc);

        # make the cc list a combination of to & cc
        push(@cc, @to) if ($#to >= 0);

	$msgcc = join(", ", @cc);
        debug "full cc list is $msgcc";

        if (!$userdb{"options.cc.show"} && scalar(@cc) > 0) {
            debug "cc.show not selected but setting it temporarily";
            write_tmp("cc.show", 1);
        }
    }

    $msgsubj = $h_ref->{"subj"};
    $msgsubj =~ s/^\Q$msg{'MSG_Reply'}\E\s?//i;
    $msgsubj = convert($msg{'MSG_ReplySubject'}, $msgsubj);

    debug "replytype=$reply_type  msgto=$msgto  msgcc=$msgcc  msgsubj=$msgsubj";

    $v{"rmsg"} = "$message";

    # if doing quoted reply
    if (index($reply_type, "qreply") != -1)
    {
	debug "Quoted Replying";

	my (@message);
	@message = parse_message("$homedir/messages/$message");
        debug "qreply wrapping message";
	#@message = text_wrap("> ", @message); Alex 25.02.2003

	my @from = addr_split($h_ref->{"from"});

	my ($unknown) = $msg{"MSG_UnknownSender"} || "Someone";

	# we can't pass plain date here, it must be parsed with our cool get_date() func
	# also we should pass 1 as fourth parameter (be_abbr_gmt, if needed ofc)
	unshift(@message, convert($msg{'MSG_QReplyTop'}, scalar get_date(str2time( $h_ref->{"date"} ), 0, 0, 1), $from[0] || $from[1] || $msg{"MSG_UnknownSender"}) . "\n\n");
#       unshift(@message, "\n\n");
        push(@message, "$msg{'MSG_ForwardFormat_End'}");#alex 25.02.2003
	$v{"sigappended"} = 0;

	compose($msgto, $msgcc, $msgsubj, 1, @message);
    }
    else
    {
	debug "Normal Replying";
	compose($msgto, $msgcc, $msgsubj);
    }

    if (!$userdb{"options.cc.show"} && scalar(@cc) > 0) {
        undef $EMU::{"nooneenoo_cc.show"};
    }
}

sub new_msg
{
    my ($address);

    $address = $query->param('email');
    $address =~ s/mailto\://gi;
    debug "selma $address and ".$query->param('email');
    &compose($address);
}

sub reply2
{
    my ($to, $re, $message);

    print_header();

    $to = $query->param('reply_to') || $v{"reply_to"};

    $to =~ s/mailto://gi;

    $re = $v{"reply_subj"};
    $re =~ s/^Re:\s*//i;
    
    $message = $query->param('variable');
    $v{"rmsg"} = "$message:1";
    $v{"sigappended"} = 0;

    debug "to=$to, re=$re, message=$message";

    
    compose($to, $v{"reply_cc"}, convert($msg{'MSG_ReplySubject'},$re));
}


sub add_prologue {
    my ($part, $prologue_ref, $ix, $tmp, $msg, $used_cids) = @_;
    my $autoload  = $userdb{"options.autoload"};
    $autoload = 1 if ($autoload eq undef);  # default if nothing is set.
    my $mime_type = $part->mime_type;

    return if (!$autoload);
    
    if ($mime_type =~ /^image/i) {
        push(@$prologue_ref, qq{&nbsp;<A HREF="$tmp"><IMG SRC="$tmp" BORDER=0></A>&nbsp\n});

debug "image ".$tmp;

    }

    else {
        push(@$prologue_ref, handle_mime_type($part,$msg, $used_cids));
    }
}


sub handle_mime_type {
    my ($part,$msg, $used_cids) = @_;
    my $mime_type = $part->mime_type;

    if ($mime_type =~ /text.html/i) {
        my $io = $part->bodyhandle()->open("r");
        my $html_part = get_html_part($part,$io,$msg, $used_cids);
        return $html_part;
    }

    if ($mime_type =~ /text.plain/i) {
        return get_part_text($part);
    }

    if ($mime_type =~ /message.rfc822/i) {
        return get_part_text($part);
    }

    if ( $mime_type =~ /text.calendar/i ) { # FIXME $licensed{"emucal"} && 
        return handle_text_calendar($part);
    }

}


sub handle_text_calendar {
    my ($part) = @_;

	return '' unless ( $c{'cal_url'} ); # if no calendar installed, ignore this attachment
	
    my $cal_event_str = join("", get_part_text($part));
	debug "event: $cal_event_str";

    # get top-level component
    debug "Going to parse ICal attach";
    load_module('Net::ICal::Component', 1);
	my $cal = eval { Net::ICal::Component->new_from_ical( $cal_event_str ) };
	if ( !$cal || $@ ) { debug "Can't create calendar object!"; return ''; }
	my $cal_event;
	my $ev = 0;

    debug "have " . scalar( @{ $cal->events }) . " events";	
	for my $e ( @{ $cal->events } )
	{
		$cal_event = '';
    	# get subcomponents (only VEVENTS)

        my %props;

		$props{'DESCRIPTION'} = ($e->description && ref($e->description) eq 'HASH') ? $e->description->{content} : "Not specified";
		$props{'SUMMARY'} = $e->summary || "Not specified";
		$props{'DTSTART'} = get_date( $e->dtstart->epoch ) || "Not specified";
		$props{'DTEND'} = get_date( $e->dtend->epoch ) || "Not specified";
		$props{'LOCATION'} = ($e->location && ref($e->location) eq 'HASH') ? $e->location->{content} : "Not specified";
		$props{'CATEGORIES'} = $e->categories || "Not specified";
        
		my @date_st = get_date( $e->dtstart->epoch, undef, undef, undef, 1 ); # don't translate
		my @date_fi = get_date( $e->dtend->epoch, undef, undef, undef, 1 );   # to human readable fmt
		
        $props{"DTSTART:year"}   = $date_st[3];
        $props{"DTSTART:month"}  = $date_st[2] + 1;
        $props{"DTSTART:day"}    = $date_st[1];
        $props{"DTSTART:hour"}   = $date_st[4];
        $props{"DTSTART:minute"} = $date_st[5];

        $props{"DTEND:year"}     = $date_fi[3];
        $props{"DTEND:month"}    = $date_fi[2] + 1;
        $props{"DTEND:day"}      = $date_fi[1];
        $props{"DTEND:hour"}     = $date_fi[4];
        $props{"DTEND:minute"}   = $date_fi[5];

        $cal_event = qq{
====================== Calendar Event Information ======================
Description: $props{DESCRIPTION}
Title:       $props{SUMMARY}
Category:    $props{CATEGORIES}
Where:       $props{LOCATION}
When:        $props{DTSTART}
Ends:        $props{DTEND}
========================================================================
};
		$cal_event .= insert_event_form(++$ev, %props) if ($c{"cal_url"});
		$cal_event = "\n\n----- No calendar EVENT specified in this attachment<br>" if (!$cal_event);
	}

    return $cal_event;
}


sub insert_event_form {
    my ($ix, %props) = @_;

    my $uri = $ENV{REQUEST_URI};
    $uri =~ s/\?.+$//;
    $uri =~ s/^\///;

    my $form_txt = qq{<center><form name="calevent$ix" method=post action="$EMU::EMU_URL" target="addcalevent_popup">};
    $form_txt .= qq{<input type=hidden name=passed value="calevent_add">};
    $form_txt .= qq{<input type=hidden name=start_year value="$props{'DTSTART:year'}">};
    $form_txt .= qq{<input type=hidden name=start_month value="$props{'DTSTART:month'}">};
    $form_txt .= qq{<input type=hidden name=start_day value="$props{'DTSTART:day'}">};
    $form_txt .= qq{<input type=hidden name=start_hour value="$props{'DTSTART:hour'}">};
    $form_txt .= qq{<input type=hidden name=start_minute value="$props{'DTSTART:minute'}">};
    $form_txt .= qq{<input type=hidden name=finish_year value="$props{'DTEND:year'}">};
    $form_txt .= qq{<input type=hidden name=finish_month value="$props{'DTEND:month'}">};
    $form_txt .= qq{<input type=hidden name=finish_day value="$props{'DTEND:day'}">};
    $form_txt .= qq{<input type=hidden name=finish_hour value="$props{'DTEND:hour'}">};
    $form_txt .= qq{<input type=hidden name=finish_minute value="$props{'DTEND:minute'}">};
    $form_txt .= qq{<input type=hidden name=title value="$props{SUMMARY}">};
    $form_txt .= qq{<input type=hidden name=description value="$props{DESCRIPTION}">};
    $form_txt .= qq{<input type=hidden name=location value="$props{LOCATION}">};
    $form_txt .= qq{<input type=hidden name=category value="$props{CATEGORIES}">};
    $form_txt .= qq{<input type=submit value="Insert this event into my calendar" onclick="popup = window.open('', 'addcalevent_popup', 'width=400,height=200,status=1,toolbars=0,scrolling=0,resizable=1');"></form></center>};

    return $form_txt;
}


sub add_attach {
    my ($part, $attach_ref, $ix, $msg) = @_;
    my $tmp;
    my $mime_type = $part->mime_type;
    my $disp_name;

    if ($mime_type =~ /message.rfc822/i) {
        $tmp = make_url("msg", "$msg\%\%RFC822\%\%");
        $disp_name = $msg{'MSG_RFC822_TITLE'} || "Attached Message";
    }
    else {
        $tmp = make_url("detach", "$msg:$ix:" . code($mime_type));
        $disp_name = $part->head()->recommended_filename || $mime_type;
    }

    my $target = "target=".get_target();
    $target = "" if (!viewable($mime_type));
#    debug "adding attachment $disp_name ($mime_type) target is $target";
    debug "url is $tmp, name $disp_name";
    push(@$attach_ref, { url => $tmp, name => $disp_name, content_type=>$mime_type, target => $target });

    return $tmp;
}


sub get_part_text {
    my ($part) = @_;
    my @message;

    if ($part->parts > 0) {
        foreach my $p ($part->parts) {
            push (@message, get_part_text($p));
        }
    }
    elsif ($part->mime_type =~ /message.rfc822/i) {
debug "processing rfc822";
        my $parser = new MIME::Parser;
        $parser->ignore_errors(1);
        $parser->decode_headers(1);
        $parser->extract_uuencode(1);
        $parser->extract_nested_messages(0);

        $parser->output_dir("$homedir/tmp");
        my $pre = "tmp$$".time;
        $parser->output_prefix($pre);

        my $bh = $part->bodyhandle();
        return if (!$bh);

        my $io = $bh->open("r");
        return if (!$io);

        open (RFC822, ">$homedir/tmp/rfc822");
        my $msg = "";
        while (my $line = $io->getline()) {
            $msg .= $line;
            print RFC822 $line;
        }
        $io->close;

        close RFC822;

        my $ent = $parser->parse_data($msg);
        my $attach_name = $msg{'MSG_RFC822_TITLE'} || "Attached Message";
        my $from = $msg{"MSG_HeaderFrom"}." ".$ent->head->get('From');
        my $subj = $msg{"MSG_HeaderSubject"}." ".$ent->head->get('Subject');
        my $date = $msg{"MSG_HeaderDate"}." ".$ent->head->get('Date');
        my $text = qq{\n\n\n#################### ($attach_name) ####################<br>----- $from<br>----- $subj<br>----- $date<br>};
        push (@message, "$text");
        push (@message, get_part_text($ent));
    }
    else {
        my $qp = $part->head->get('Content-Transfer-Encoding');
        my $bh = $part->bodyhandle();
        return if (!$bh);

        my $io = $bh->open("r");
        return if (!$io);

        # if it's not viewable in text, dont do anything
        return  if ($part->mime_type !~ /^text/i);

        my @msg;
        push (@msg, "</PRE>") if ($part->mime_type =~ /text.html/i);

        my $size = 0;
        while (my $line = $io->getline()) {
            push(@msg, $line);
        }
        $io->close;
        decode_qp(\@msg) if ($qp =~ /quoted-printable/i);
        @msg = text_wrap("", @msg);

debug "type is ".$part->mime_type;
        if ($part->mime_type =~ /text.html/i) {
            push (@msg, "<PRE>");
            push (@message, @msg);
        }
        elsif ($part->mime_type =~ /text.plain/i) {
	    format_pure(\@msg);

            #if (!$c{"is_wap"} && $c{"view_display_HTML"}) {
            #   interpret(\@msg);
            #}

            my $msg = join("",@msg);
            push (@message, $msg);
#            foreach my $themsg (@msg) { push (@$message, escape($themsg)); }
        }
        else {
            my $msg = join("", @msg);
            push(@message, $msg);
        }
    }

    return @message;
}


#
# Format for printer
#
sub format_msg
{
    my ($filename, $ent, @message, %options);
  
    $filename = $query->param('variable');

    if (!$filename)
    {
	set_status($msg{'ERR_FormatNoMessage'});
	return;
    }

    print_header("EMUmail");

    # look for unwanted chars in filename
#    my $file = code2($filename);

    debug "printing $filename ";

    # Parse the input stream and get a mime:entity (hopefully)
#    open IN, "$homedir/messages/$filename";

    my $parser = new MIME::Parser;
    $parser->ignore_errors(1);
    $parser->decode_headers(1);
    $parser->extract_uuencode(1);
    $parser->extract_nested_messages(0);

    $parser->output_dir("$homedir/tmp");
    my $pre = "tmp$$".time;
    $parser->output_prefix($pre);

    $ent = $parser->parse_open("$homedir/messages/$filename");
#    eval { $ent = $parser->parse(\*IN); };
#    close IN;

    if (!$ent) {
        my $err = ($@ || $parser->last_error);
        debug "Failed to parse $filename! : $err";
        return;
    }

#    my @parts = get_parts($ent);

    my $header;
    if ($userdb{"options.full_header"}) {
        $header = $ent->header_as_string . "\n";
    }
    else {
        $header = $msg{"MSG_HeaderDate"} || "Date:";
        $header .= " ".get_date(str2time($folderdb{"$filename:date"}))."\n";
        $header .= $msg{"MSG_HeaderFrom"} || "From:";
        $header .= " ".$folderdb{"$filename:from"}."\n";
        $header .= $msg{"MSG_HeaderTo"} || "To:";
        $header .= " ".$folderdb{"$filename:to"}."\n";
        $header .= $msg{"MSG_HeaderCc"} || "Cc:" 
            if ($userdb{"options.cc.show"} && $folderdb{"$filename:cc"});
        $header .= " ".$folderdb{"$filename:cc"}."\n"
            if ($userdb{"options.cc.show"} && $folderdb{"$filename:cc"});
        $header .= $msg{"MSG_HeaderSubject"} || "Subject:";
        $header .= " ".$folderdb{"$filename:subj"}."\n";
        my $attachments = get_var("attachments_array");
        if ($attachments) {
            $header .= $msg{"MSG_HeaderAttachments"} || "Attachments:"
                if ($userdb{"options.attach.show"} && 
                    scalar(@{$attachments}) >= 1);
            $header .= " @{$attachments}\n"
                if ($userdb{"options.attach.show"} && 
                    scalar(@{$attachments}) >= 1);
        }
        $header .= "\n\n";
    }

    my %useragent_props = %{ get_useragent_props( $ENV{'HTTP_USER_AGENT'} ) };

    if ($useragent_props{browser} =~ /Mozilla/i) {
        print "<BODY BGCOLOR=white onload=\"print()\"><PRE>";
    }
    else {
        print "<BODY BGCOLOR=white><PRE>";
    }

#    debug "header is $header";

    print escape($header);
#    push(@message, $header);

#Alex we have not to show attachments here 
#START

	my @viewable_messages = () ;
	if (process_parts($ent, \@viewable_messages, [], [], 0, 0, 0))
	{
	    for my $vmsg (@viewable_messages)
	    {
		push(@message, $vmsg); 
	    }
													    
	}

#END

#    push(@message, get_part_text($ent));
#    my $qp = $ent->head->get('Content-Transfer-Encoding');

#    if ($#parts < 0) {
#        my $io = $ent->bodyhandle()->open("r");
#        while (my $line = $io->getline()) {
#            push(@message, $line);
#        }
#        $io->close;
#	decode_qp(\@message) if ($qp =~ /quoted-printable/i);
#
##        @message = wrap("", "", @message);
#        @message = text_wrap("", @message);
#        foreach my $themsg (@message) { print escape($themsg); }
#        print "\n\n";
#    }
#    else {
#        my $partix = 0;
#        foreach my $part (@parts) {
#            $partix++;
#            @message = ();
#            my $io = $part->bodyhandle()->open("r");
#            my $qp = $part->head->get('Content-Transfer-Encoding');
#
#            # special processing for embedded messages
#            if ($part->mime_type =~ /message.rfc822/i) {
#            }
#
#debug "part $partix encoding is $qp";
#            while (my $line = $io->getline()) {
#                push(@message, $line);
#            }
#            $io->close;
#	    decode_qp(\@message) if ($qp =~ /quoted-printable/i);
#
##            @message = wrap("", "", @message);
#            @message = text_wrap("", @message);
#            print "========================= Message Part $partix: ".$part->mime_type()." =========================\n";
#            foreach my $themsg (@message) { print escape($themsg); }
#            print "\n\n";
#        }
#    }

#    @message = wrap("", "", @message);

#    write_tmp("the_message", join('\n', @message));

#    my $themsg;
#    foreach $themsg (@message) { print escape($themsg); }

    print "@message\n\n</PRE>";
}


# vrmlize for VRML browser
sub vrmlize_msg
{
    my ($filename, @message, $v, $y, $ent);
  
    load_module("VRML");

    $filename = $query->param('variable');

    if (!$filename)
    {
	set_status($msg{'ERR_VrmlNoMessage'});
	return;
    }

#    open IN, "$homedir/messages/$filename";

    my $parser = new MIME::Parser;
    $parser->ignore_errors(1);
    $parser->decode_headers(1);
    $parser->extract_uuencode(1);
    $parser->extract_nested_messages(0);
    $parser->output_dir("$homedir/tmp");
    my $pre = "tmp$$".time;
    $parser->output_prefix($pre);

    $ent = $parser->parse_open("$homedir/messages/$filename");
#    eval { $ent = $parser->parse(\*IN); };
#    close IN;

    @message = split(/\n/, $ent->stringify);

    # VRML messages come out backwards

    @message = reverse @message;
    
    # only quoted-printable decode if the transfer encoding indicates the need
    if ($ent->head->get('Content-Transfer-Encoding') =~ /quoted-printable/i)
    {
	decode_qp(\@message);
    }

    print "Content-type: model/vrml\n";
    print "Content-disposition: attachment; filename=email.vrml\n\n";

    $y = 0;
    foreach (@message)
    {
	chomp;
	
	s/\t/    /g;

	# 07/27/98: output vrml 2 format
	$v = VRML->new(2);
	
	$v->at("t=0 $y 0");
	$v->text($_, 'lightblue', '1 SERIF BOLD');
	$v->back();
	$v->print();
	
	$y++;
    }
    
    $v->PerspectiveCamera("0 $y 24");
    $v->print();
}

sub forward
{
    my ($date, $to, $re, @message, $line, $tmphead);
    my ($sender, $mydate, $subject, $priority);
    my (%messages, $entity, $parser, @files);
    my $h_ref;
    my $message = $query->param('variable');
    
    debug "Forwarding from message '$message'";

    $v{"forwarding"} =$message;
    
    if ( !$v{"reply_to"} && !$query->param('reply_to') )
    {
	set_status($msg{'ERR_ForwardNoReturnEmail'});
# Why call cleanup here?
#	cleanup();
	go_index();
	return;
    }

    if (!$query->param('reply_to'))
    {
	$to = $v{"reply_to"};
    }
    else
    {
	$to = $query->param('reply_to');
    }

    $re = $folderdb{"$message:subj"} || $v{"reply_subj"};
    debug "reply_subj $re";

    my $forward_letters = $msg{'MSG_ForwardLetters'} || "Fw: "; #MM 990521 allow config of these letters

    $re = "$forward_letters$re" unless (($re =~ /$forward_letters/i) || (!($re)) );

    $parser = new MIME::Parser;
    $parser->ignore_errors(1);
    $parser->decode_headers(1); 
    $parser->extract_uuencode(1);
    $parser->extract_nested_messages(0);
    $parser->output_dir("$homedir/tmp");
    $parser->output_prefix('fwd'.time);

    $entity = $parser->parse_open("$homedir/messages/$message");

    my @parts = get_allparts($entity);
    
    debug "Parts found: ".scalar(@parts);

    # If the first part is plain text, use it for the default message body
    if (lc($parts[0]->mime_type) eq 'text/plain') { #alex 21.02 WTF?
       @message = shift(@parts)->bodyhandle->as_lines;
    }else{
       @message = parse_message("$homedir/messages/$message");
       #@message = text_wrap("> ", @message); #Alex 25.02.2003
    }

    # Iterate through our attachments to determine all filenames.
    foreach my $p (@parts) {
       my $filename = $p->head->recommended_filename;
       my $tmpname = $p->bodyhandle->path;
       
       if (!$filename) {
          # Come up with something pretty enough for the user to read
          $tmpname =~ /(\.\w+)$/;
          $filename = $p->mime_type.$1;
       }
        
       # Remove unwanted characters
       $filename =~ s{[\s/]}{_}g;  
       
       my $count = 0;
       while (-e $filename) {
          my $c = $count+1;  
          if ($count) {
             $filename =~ s/-$count(\.\w+)$/-$c$1/;
          } else {
             $filename =~ s/(\.\w+)$/-$c$2/;
              }
           $count = $c;
       }

       # Relocate the file
       debug "Moving '$tmpname' to '$homedir/tmp/$filename'";
       move($tmpname, "$homedir/tmp/$filename");

        push(@files, $filename);
    }

    if (@files) {
       $query->param(-name => 'attached', "-values" => join(' ', @files));
       debug "Files attached: @files";
       $userdb{"options.attach.show"} = 1;
    }

    my $searchfold = $msg{"FOLD_Search_Results"} || "Search Results";
    if ($folder eq $searchfold || $folderdb{"$message:date"} eq "")
    {
	$h_ref = header_from_file($message) || {};
    }
    else
    {
        $h_ref->{"replyto"} = $folderdb{"$message:replyto"};
        $h_ref->{"from"}    = $folderdb{"$message:from"};
        $h_ref->{"to"}      = $folderdb{"$message:to"};
        $h_ref->{"cc"}      = $folderdb{"$message:cc"};
        $h_ref->{"bcc"}     = $folderdb{"$message:bcc"};
        $h_ref->{"subj"}    = $folderdb{"$message:subj"};
        $h_ref->{"date"}    = $folderdb{"$message:date"};
    }

    # get header info
    $subject = $h_ref->{"subj"};
    $mydate  = $h_ref->{"date"};
    $sender  = $h_ref->{"from"};

    chomp($subject);
    chomp($mydate);
    chomp($sender);

    debug "subject $subject  sender $sender";

#    @message = wrap("", "", @message);
    @message = text_wrap("", @message);

    if ($entity->head->get('Content-Transfer-Encoding') =~ /quoted-printable/i)
    {
	decode_qp(\@message);
    }

    # add header info
    unshift(@message, convert($msg{'MSG_ForwardFormat'}, $sender, scalar get_date( str2time($mydate), 0, 0, 1), $subject));
    unshift(@message, "\n\n");
    push(@message, "$msg{'MSG_ForwardFormat_End'}");
    push(@message, "\n\n".get_signature());
    splice(@message, 0, 1); #alex 26.02 (this line is removal of empty lines at the top of the message)

    $v{"sigappended"} = 1;

    compose("", "", $re, 1, @message);
}

# sub compose
#
# put up a page for the user to compose their email message in
#
sub compose
{
    my ($to, $cc, $subj, $dosig, @data) = @_;
    my (@addresses, $sig, $junk, $address, $nickname, $tmp, $rowspan);
    my ($organization, $email, $replyto, $sender, $bcc, @files);
    my ($key, $val, $dsn, $mdn, $save_outbox);

    print_header();

#    debug "bjork called as compose $to, $cc, $subj, ".join("",@data);

    $dsn              = $userdb{"options.dsn"} ? "CHECKED" : "";
    $mdn              = $userdb{"options.mdn"} ? "CHECKED" : "";
    $save_outbox      = ($userdb{"options.save_outbox"} eq "" || ($userdb{"options.save_outbox"} ne "" && $userdb{"options.save_outbox"} != 0) || !(bool($c{"compose_dont_save_outgoing"}))) ? "" : "CHECKED";
    $organization     = $query->param('organization') || $userdb{"options.organization"};
    $email            = $query->param('from')         || $userdb{"options.email"} || $user_name;
#    debug "from is $email";

    # checkmarks
    my $attach_checked   = ($userdb{"options.attach.show"} || $c{"compose_display_attach"}) ? "SELECTED" : ""; # file attachment
    my $manager_checked  = $userdb{"options.manager.show"}  ? "SELECTED" : ""; # file manager
    my $cc_checked       = ($userdb{"options.cc.show"} || $c{"compose_display_CC"}) ? "SELECTED" : "";
    my $bcc_checked      = $userdb{"options.bcc.show"}      ? "SELECTED" : ""; 
    my $from_checked     = $userdb{"options.from.show"}     ? "SELECTED" : ""; 
    my $replyto_checked  = ($userdb{"options.replyto.show"} || $c{"compose_display_replyto"}) ? "SELECTED" : ""; 
    my $priority_checked = ($userdb{"options.priority.show"} || $c{"compose_display_priority"}) ? "SELECTED" : ""; # message priority
    my $sender_checked   = $userdb{"options.sender.show"}   ? "SELECTED" : ""; # sender field
    my $ihelp_checked    = $userdb{"options.ihelp.show"}    ? "SELECTED" : ""; # inline help

    $rowspan          = $ihelp_checked ? "ROWSPAN=2" : ""; # for the inline help

    $replyto          = $query->param('replyto') || $email || "";
    $sender           = $query->param('sender')  || $replyto || "";
    $to               = $to || $query->param('to') || "";
    $cc               = $cc || $query->param('cc') || "";
    $bcc              = $bcc || $query->param('bcc') || "";
    $subj             = $subj || $query->param('subject') ||"";

#    debug "replyto $replyto sender $sender to $to cc $cc bcc $bcc subj $subj";

    if (!@data)
    {
	@data = $query->param('message'); 
    }

    
    # only append the signature if v{sigappended} is equal to 0
    if ($v{'sigappended'} == 0  ||  !@data)
    {
	$sig = get_signature();
	push(@data, "\n\n\n$sig") if $sig;

	$v{"sigappended"} = 1;
    }
    
    if ( $to && ($query->param('passed') !~ /^q?reply/) )
    {
	$to =~ s#/$##;              #remove trailing / from url weirdness\
        my $theto;
	foreach $theto (split(",", $to))
	{
	    $tmp .= (addr_split($theto))[1] . ", "; # just the email address please
	}
	$tmp =~ s/,\s*$//;
	$to  = $tmp;
    } 
    #We shold check what user want to attach. We don't allow to attach ../../etc/passwd!
    my $safe_attach = $query->param('attached');
    $safe_attach =~ s/(\.{2}?\/)+?//g;
 
#    debug "attachments ".$query->param('attached');
    write_tmp("dsn", $dsn, 1);
    write_tmp("mdn", $mdn, 1);
#    debug "save_outbox $save_outbox dont_save_outgoing ".$c{"compose_dont_save_outgoing"};
    write_tmp("save_outbox", $save_outbox, 1);
    write_tmp("ds", $save_outbox, 1);  # "ds" only for 3.0 backwards compatibility
    write_tmp("cc_checked", $cc_checked, 1);
    write_tmp("bcc_checked", $bcc_checked, 1);
    write_tmp("from_checked", $from_checked, 1);
    write_tmp("replyto_checked", $replyto_checked, 1);
    write_tmp("sender_checked", $sender_checked, 1);
    write_tmp("priority_checked", $priority_checked, 1);
    write_tmp("attach_checked", $attach_checked, 1);
    write_tmp("manager_checked", $manager_checked, 1);
    write_tmp("ihelp_checked", $ihelp_checked, 1);
    write_tmp("postponed_count", count_postponed_msgs(), 1); #04/25/99 MM
#    write_tmp("here_atts", basename($query->param('attached')) || "");
    write_tmp("here_atts", $safe_attach || "");

#    debug "attachments are ", get_var("here_atts");
	
    my $data = join("", @data); #Alex WYSIWYG .

	# rb, 7/7/2003
	# if we have richeditor and it's html
	# so replace \n to <br> in data[0], data[-2]
	# they are reply/fwd top and bottom respectively
	# see compose.html for the weird regexp, guessing if it's html
	if ( $userdb{'options.richeditor'} && $data =~ /<\s*(a|b|i|td|br|hr|font|html|img)/ )
	{
		$data[0] =~ s/\015?\012/<br>/g;
		$data[-2] =~ s/\015?\012/<br>/g if $data[-2];
		# re-join modified data
		$data = join("", @data);
	}

#     if (($userdb{"options.richeditor"} == 1) && ($ENV{HTTP_USER_AGENT} =~ /MSIE/i)){
# 
#         $data=~ s/(?:\r?\n){2,}/<br><br>/gos;
#         $data=~ s/\r?\n/<br>/gos;
# 
#     }else{
# 
#         $data =~ s/<br>/\r\n/igs;
#         $data =~ s/<br><br>/\r\n/gs;
#         $data =~ s/<.*?>//gos; Alex 20.02.2003
#     }

#    write_tmp("data", join("", @data));


    write_tmp("data", $data);
    write_tmp("to", $to || "", 1);
    write_tmp("cc", $cc || "", 1);
    write_tmp("subj", safe_html($subj), 1);
    write_tmp("dosig", $dosig);
    write_tmp("sig", $sig);
    write_tmp("sigwap", safe_html($sig)) if ($licensed{"wap"});

    write_tmp("email", safe_html($email), 1);
    write_tmp("organization", $organization || "", 1);
    write_tmp("sender", $sender, 1);
    write_tmp("bcc", $bcc, 1);
    write_tmp("replyto", $replyto, 1);
    write_tmp("rowspan", $rowspan, 1);
    write_tmp("msg_continued", $query->param('msg_continued') || "");
    write_tmp("status", $status, 1);

    if ($query->param('msg_continued') && $query->param('sender')) {
        write_tmp("from", $query->param('sender'));
    }
    else {
        write_tmp("from", $userdb{"options.email"});
    }

    load_page("compose.html");
}

## MM: 04/25/99 -- count the number of postponed messages
sub count_postponed_msgs
{
    my ($size);
    my (@files);

    opendir DIR, "$homedir/files";
    @files = grep ( /^[0-9a-f]{32}$/, readdir DIR);
    closedir DIR;

    $size = scalar(@files);

    return $size;
}


sub load_module
{
# This subroutine will require modules on an as needed
# basis.  EMUerrors on failure unless called with
# an optional second argument.
#
# Returns 1 on success.

    my ($module,$no_die,@list) = @_;
    my ($result);

    # Hrm, can't do much without a module
    return if (!$module);
    return 1 if ($loaded{$module});
    
    $result = eval("use $module qw(@list); 1");

    if ($result != 1 && !$no_die)
    {
		EMUerror("Module error: $module", "Required module $module not found.<P>Contact your EMUmail administrator. ($@)");
		exit;
    }

   	$loaded{$module} = 1 if ( $result );
   	return $result;
}

sub do_lookup
{
    #Use some dictionary server to lookup words
    # parts lifted from the ORA book "Web client Programming"
    # by Clinton Wong, ISBN: 1-54592-214-X
    # 
    my ($word) = @_;

    my ($ua,$lookup_url,$result);

  LOOKUP:
    {
	#Load in the needed modules...
	&load_module("HTML::Parse") || last;
	&load_module("LWP::UserAgent") || last;

	my ($dictionary) = $c{'dictionary'};
	write_tmp("default",$dictionary);

	print_header("Remote Dictionary Lookup");  

	#Legalize the word (remove spaces, etc.)
	$word =~ s/\s//go;
	( set_status($msg{'ERR_DictNoWord'}) && last ) if (!($word));
	
	#Setup User Agent
	$ua = new LWP::UserAgent;
	$ua->agent("Mozilla/3.01 (Macintosh; I; PPC)"); #well, not really.

	#Setup URL
	$lookup_url = "$dictionary$word";
        debug "lookup url: $lookup_url";

	my $request  = new HTTP::Request('GET', $lookup_url);
	my $response = $ua->request($request);

        debug "url requested";

	if ($response->is_error)
	{
            debug "we got an error";
	    set_status($msg{'ERR_DictConnect'});
	    last;
	}
	elsif ($response->is_success)
	{
            debug "lookup successful";
            my $resp = $response->content;
#            debug "content $resp";
#	    my $html = HTML::Parse::parse_html($resp)->format;
            my $html = $resp;

#            debug "parsed. html is $html";

            write_tmp("suggestions", get_var("suggestions"));

	    #Filter out extra nonsense
	    $html =~ s/^\s$//gsoi;
	    $html =~ s/\[FORM NOT SHOWN\]//gsoi;
	    $html =~ s/\[TABLE NOT SHOWN\]//gsoi;
	    $html =~ s/This page was generated by a customized vers?ion of htgrep(.*)//gsoi;
	    $html =~ s/Don\'t make me hand over my privacy keys!//gsoi;
	    $html =~ s/Additional Hypertext Webster Gateway Lookup//gsoi;
	    $html =~ s/Other dictionaries on the Web include the ARTFL project\'s dictionary,//gsoi;
	    $html =~ s/and Merriam-Webster\'s dictionary.//gsoi;
	    $html =~ s/---//gsoi;
	    $html =~ s/You may wish to try an alternative spelling \(change what you had in//gsoi;
	    $html =~ s/the box below\)\, or use an approximate match \(click on the \`\`Approx\'\'//gsoi;
	    $html =~ s/button\) instead//gsoi;
	    $html =~ s/\[IMAGE\]//gsoi;
	    $html .= convert($msg{'MSG_DictSource'},substr($dictionary,0,50));

	    write_tmp("def",$html);
	    write_tmp("lookat",$word);
	}

    }

    load_page("lookup.html");
}

sub get_msg_file
{
    my ($digest) = @_;

    my ($line,$msg);

    return undef unless $digest;

    debug "ttam: reading $digest";
    open(IN, "$homedir/files/$digest");
    # binmode  IN;
    
    my @lines;
	    
    while ( defined($line = <IN>) )
    {
	$msg .= $line;
    }
    
    close IN;
    
#    $msg =~ s/\r?\n/\xfe/;

    return ($msg);
}

## MM 11/27/98 -- Interface to add a digest
sub put_msg_file
{
    my ($digest,$the_message) = @_;

    return undef unless $digest;

    debug "TTAM: writing $digest";

    open(OUT, ">$homedir/files/$digest") || return 0;
    # binmode  OUT;
    print OUT $the_message;
    close OUT;
    
    return 1;
}

## MM -- Added 11/27/98
sub spelling_substitute_word
{
    my ($start,$end,$word,$digest) = @_;

    my ($the_message) = get_msg_file($digest);

    # No clue what all this +1 -1 business is about...figure it out!
    my $delta = $end-$start+1;

    $start = 0 if ($start == 1);
    $delta = $delta + 1 if ($start == 0);

    debug "TTAM: delta: $delta s: $start w: $word";

    substr($the_message,$start,$delta) = $word;

    return put_msg_file($digest,$the_message);
}

## MM: New 11/27/98
sub tokenize
{
    my ($the_message) = @_;
    my (@starts,@ends,@words,$pos,$word,$buffer,$start,$end);

    return unless ($the_message);

    foreach $pos (0..length($the_message))
    {
	my $char = substr($the_message,$pos,1); #load character

	# Test type of CHAR
	if ($char =~ /[A-Za-z0-9_\'-]/)
	{
	    # We're within a word (possibly a number)

	    #Set word buffer with this char
	    $buffer .= $char;

	    #Update word position info
	    unless ($start)
	    {
		$start = $pos; #Set start position for word
	    }
	    $end = $pos; #Set current END for word
	  
	    next;
	}
	else 
	{
	    #Out of word
	    if ($buffer =~ /[A-Za-z]/) #Test for numerics,ignore them
	    {
		push(@words,$buffer);
		push(@starts,$start);
		push(@ends,$end);
	    }

	    #Clear
	    $end = $start = $buffer = undef;
	    next;
	}
    }
   
    return (\@words,\@starts,\@ends);
}


sub spelling_check_word
{
    my ($word) = @_;

    my $emu_type = $v{'type'} || $v{'emu_type'} || $emu_type || $c{'default_interface'};

    if (-e "$page_root/words/$emu_type.txt")
    {
				open (WORDS, "$page_root/words/$emu_type.txt") || return undef;
				debug "TTAM: opened dictionary $emu_type";
    }
    else
    {
				debug "Trying words.txt";
				open (WORDS, "$page_root/words/words.txt") || return undef; #Better error?
				debug "opened standard dictionary";
    }

    my @skip_words = ();
    # also look at list of words to skip, if one exists
    if (-s "$homedir/tmp/spelling-skip.txt" > 0) {
        open (SKIP, "$homedir/tmp/spelling-skip.txt");
        @skip_words = <SKIP>;
        close SKIP;
        debug "skip words: @skip_words ".scalar(@skip_words);
    }
		
		#push (@skip_words, 'br', 'a', 'b', 'style', 'p');
		
    my ($position,$tmp_word);

    $position = look(*WORDS, $word, 1, 1);
    debug "TTAM: position: $position";
    $tmp_word = <WORDS>;
    chomp($tmp_word);

    #remove nonword characters for comparison
    $tmp_word =~ s/\W//go;

    debug "TTAM: tmp_word is $tmp_word";
    debug "TTAM: size of tmp: ".length($tmp_word);

    if ( $word !~ /^[\.\,\!\"\'\>\<\:\)\(\]\[]*$tmp_word[\?\;\.\,\!\"\'\>\<\:\)\(\]\[]*$/i  &&
            !grep(/^$word\s*/i, @skip_words))
    {
	#We didn't match!
	my $bad_word = $word;
	debug "TTAM: badword is $bad_word";
	if ( ($bad_word =~ /^[\d\W]+$/) || ($bad_word =~ /(?:\@)|(?:http\:\/\/)/i) || ($bad_word =~ /(?:\'t)|(?:\'s)|(?:\'ve)|(?:n\'t)|(?:\'d)|(?:\'ll)|(?:\'m)|\'$/i) ) 
	{
	    close WORDS;
	    return undef; #It's really OK...?
	}
	else #Get suggestions
	{
	    my $pos = tell WORDS;
            my $num_suggestions = $c{"spelling_suggestions"} || 30;

	    seek WORDS, ($pos-($num_suggestions*2)), 0; #rewind some...
	    my $junk = <WORDS>;

	    my (@suggestions,$w,$c);

	    while (defined($w = <WORDS>))
	    {
		if ($word =~ /^[A-Z]/)
		{
		    $w = ucfirst($w); #If uppercase original, upper suggestion.
		}
		
		push(@suggestions,$w); #Get suggestions
		debug "TTAM: $w -- suggestion";
		$c++;
		last if ($c >= $num_suggestions);
	    }
	    
	    close WORDS;
	    return (\@suggestions);
	}
    }
    else
    {
	#It's a good word
	close WORDS;
	return undef;
    }
}
    
sub spelling_find_error
{
    my ($word_num,$the_message) = @_;
    my ($start,$end,$bad_word,$word_num_new,$suggestions,$word);

    load_module("Search::Dict",0,'look');
    $bad_word = "";
    $word_num = $word_num || 0;
    $word_num_new = $word_num;

    my ($w,$s,$e) = tokenize($the_message);

    my (@words,@starts,@ends,$count);
    @words = @{$w} if $w;
    @starts = @{$s} if $s;
    @ends = @{$e} if $e;

    $count = $word_num-1;#-1??? why do I need this!@?

  FIND_MISPELLING:
    {
	foreach $word (@words[$word_num..$#words])
	{
	    debug "TTAM: $word is being examined. $count $word_num_new $suggestions";

	    $word_num_new++;
	    ($suggestions) = spelling_check_word($word);
	    debug "TTAM: suggestions: $suggestions";
	    if ($suggestions)
	    {
		debug "TTAM: $word was not found!";
		#If here, we have a "bad" word
		$bad_word = $word;
		$count++;
		last FIND_MISPELLING; #Is mispelling spelled correctly?
	    }

	    $count++; #Next for @starts, @ends (positioning arrays)
	}
    }

    $start = $starts[$count] || 0;
    $end = $ends[$count] || 0;

    return ($start,$end,$bad_word,$word_num_new,$suggestions);
}


sub save_spelling_skip {
    # take the current word and save it in a "skip" file so we dont put up
    # that word again next time we see it
    open (SKIP, "$homedir/tmp/spelling-skip.txt");
    my @skip_words = <SKIP>;
    close SKIP;

    my $skip_word = $query->param("unknown_word");
    if (!grep (/^$skip_word\s*/i, @skip_words)) {
        push (@skip_words, $skip_word);
        debug "skip_words: @skip_words ".scalar(@skip_words);
        open (SKIP, ">$homedir/tmp/spelling-skip.txt");
        print SKIP join("\n", sort @skip_words);
        close SKIP;
    }
}


## MM -- Modified 11/27/98  (whole sub)
sub spelling_parse
{
    my ($the_message,$digest,$start_pos,$end_pos,$start_pos_new,$end_pos_new,$word_num,$bad_word);
    my ($word_num_new,$suggestions,@sug);

  GET_MSG_DIGEST:
    {
	$digest = get_var("digest");
	$digest = $query->param('selected_msg') if (!($digest));
	debug "ttam: digest is $digest";
	write_tmp("digest",$digest);
    }

  LOAD_POSITION_INFO:
    {
	$start_pos = $query->param('start_pos') || 0;
	$end_pos   = $query->param('end_pos') || 0;
	$word_num  = $query->param('word_num') || 0;
    }

  WHERE_NOW:
    {
	if ($query->param('continue.x'))
	{
		  #die "HERE";
	    compose_parse();
	    return;
	}
	elsif ($query->param('replace.x'))
	{
	    
	    debug "TTAM: s $start_pos e $end_pos d $digest r ".$query->param('replacement');
	    spelling_substitute_word($start_pos,$end_pos,$query->param('replacement'),$digest);
	}
	elsif ($query->param('skip.x'))
	{
            debug "bad_word skipped: ".$query->param('unknown_word');
            save_spelling_skip() if ($query->param('unknown_word'));
	    $word_num++; #Move on to next word.
	}
	elsif ($query->param('lookup.x'))
	{
            debug "do lookup";
	    waiting(\&do_lookup,$query->param('replacement'));
	    return;
	}
        else {
            # first time into spelling check. We can clear out the skip list
#            unlink "$homedir/tmp/spelling-skip.txt";
#            debug "deleting skip list to start a new one";
# decided not to do that... keep the file for an entire session. File will
# be deleted upon next login.
        }
    }

  GET_THE_MSG:
    {
	$the_message = &get_msg_file($digest);
    }


  LOOK_FOR_ERRORS:
    {
	($start_pos_new,$end_pos_new,$bad_word,$word_num_new,$suggestions) = spelling_find_error($word_num,$the_message);

	debug "TTAM: MADE IT $suggestions";
	debug "TTAM: MIH $word_num_new : $bad_word : $end_pos_new : $start_pos_new !";

#       if (scalar(@{$suggestions}))
	if ($bad_word)
	{
	    debug "TTAM: MADE IT";

	    @sug = @{$suggestions};
	    debug "TTAM: Sugg size: $#sug";
            write_tmp("suggestions", join(':', @sug));
	}
	else
	{
	    debug "No more errors";
	    # No more errors
	    $status = $msg{'MSG_DictNoMoreErrors'};
	    compose_parse(2); #Says we're continuing.
	    return;
	}

    }

  PREPARE_THE_MESSAGE:
    {
	#This is what the user sees...
#	my ($sp) = $start_pos_new - 140;
	my $sp = $start_pos_new - 20;
#	my $sp = index($the_message,'\s',$start_pos_new - 140);
	$sp = 0 if ($sp < 0);

        my $orig_length = length($the_message);
	$the_message = substr($the_message,$sp,400);
        my $changed = ($orig_length != length($the_message)) ? 1:0;

        # display starting at a white space
        $the_message =~ s/^\S*\s//;
debug $the_message;
        # end display at a word boundary
#        $the_message =~ s/(.*[\W\D]+)\S*$/$1/;
        $the_message =~ s/\s\S+$// if ($changed);

        my @tmp_message;
        push(@tmp_message, $the_message);
        @tmp_message = text_wrap("",@tmp_message);
        $the_message = join("", @tmp_message);
debug "here";
debug $the_message;

        $the_message = safe_html($the_message, '<>');
	$the_message =~ s/([\s\W\d])$bad_word([\s\W\d])/$1\<font color=red\>\<strong\>$bad_word\<\/strong\>\<\/font\>$2/g;
    }

    write_tmp("bad_word",$bad_word);
    write_tmp("start_pos",$start_pos_new);
    write_tmp("end_pos",$end_pos_new);
    write_tmp("word_num",$word_num_new);
#    write_tmp("the_message", join('\n', @the_message));


    write_tmp("the_message",$the_message);
    
    debug "ttam: in spelling_parse";

    load_page("spelling.html");
}

# This subroutine gives a nice waiting screen while EMUmail is "thinking"...
# Make sure no other Content-types have been called.
sub waiting
{
    my ($function,@args) = @_;
    my ($count, $data);
    my $boundary;
#    debug "waiting on $function with args: @args";

    &$function(@args) if $function;
    finish_waitscreen();
}

sub print_dictionaries
{
    my ($selected) = @_;
    my (@keys, $key, @values, $html);  

    $html = '<select name="dicturl">';

    foreach $key (sort keys %dictionary)
    {
	$html .= '<option value="'.$dictionary{$key}.'">'.$key unless ($selected eq $dictionary{$key});
	$html .= '<option SELECTED value="'.$dictionary{$key}.'">'.$key if ($selected eq $dictionary{$key});
    }

    $html .= "</select>";

    return ($html);
}

sub compose_parse
{
    my $flag = shift;
    my %outbox;
    my $force_check = 0;
    
    my ($msg,$errors,$from,$file);
    my ($the_message, $the_subject,$the_date,$the_sender,$the_status,$the_pri);
    my ($person,$to_who,$addr_parse,$result,@rcpts, $i, $sender);
    my ($cc,$to,%messages,$organization, $real_name, $email);
    my (@message, $fullfile, $priority, $bcc, @atts, $ent, $tmp, @tmpatts);
    my ($ent_head);  # 9/20/99 rcs.ngf.v.1 stmt.2 --ngf

#    load_module("File::Copy",0,'move');

    @atts = ();

  	SET_FLAGS:
    {
        #DSN: on or undef DS: NO or undef
		my $dsn = $query->param("returnreceipt");
		$userdb{"options.dsn"} = $dsn;
		my $mdn = $query->param("readreceipt");
		$userdb{"options.mdn"} = $mdn;


        my $outbox = $query->param('outbox');

        if (defined $outbox && !$outbox)
        {
            $userdb{"options.save_outbox"} = 0;
		} else {
	    	$userdb{"options.save_outbox"} = 1;
		}

        debug "outbox: $outbox ; save_outbox: ", $userdb{"options.save_outbox"};
    }

  	GET_ADDRESSES:
    {
	# Get usernames from addressbook
	$email = $query->param('from') || "";
	debug "passed in: ".$query->param('to').",".$query->param('to_s').",".$query->param('cc').",".$query->param('cc_s');
	$to  = get_address_string($query->param('to'), $query->param('to_s'));
	$to  =~ s/,\s*$//;

	$cc  = get_address_string($query->param('cc'), $query->param('cc_s'));
	$cc  =~ s/,\s*$//;

	$bcc = get_address_string($query->param('bcc'), $query->param('bcc_s'));
	$bcc =~ s/,\s*$//;

#	debug "to is $to\n\ncc is $cc\n\nbcc is $bcc\n\n";

	$query->param('to', $to);
	$query->param('cc', $cc);
	$query->param('bcc', $bcc);
	$query->param('message', $query->param('message')); # gotta make sure it sticks
    }

#    debug "delete_attach is ". $query->param('delete_attach');
#    debug "which_att is ".$query->param('which_att');
    if ($query->param('delete_attach') && $query->param('attached')
            && $query->param('which_att')
            && $query->param('which_att') ne $msg{"MSG_ATTFileNone"}
            && $query->param('which_att') ne $msg{"MSG_ATTSelDel"} ) {

        # Deleting selected attachment
#       my $attached = split(' ',$query->param('attached'));
        my $attached = $query->param('attached');
        my $delete = $query->param('which_att');
        my @attlist;

#       debug "deleting attachment $delete";
        if (!$attached) {
            @attlist = ($query->param('attached'));
        }
        else {
            @attlist = split(' ', $query->param('attached'));
        }

#       debug "original att list: ". join(' ',@attlist);
        @attlist = grep {!/^$delete$/} @attlist;
#       debug " new att list: ". join(' ',@attlist);
        $attached = join(' ', @attlist);
        $query->param('attached', $attached);
#		debug "attached $attached";
        compose();
        return;
    }
    
    if ($query->param('richeditor.x')) #WYSIWYG Alex 10.02.2003
    {
        if ($query->param('message_ct') eq "text/html"){
            $userdb{"options.richeditor"} = 1;
        }else{
            $userdb{"options.richeditor"} = 0;
        }
           compose();
           return;

    }

#    debug "attached ".$query->param('attach.x');
#    debug "tmpupload ". $query->param('tmpupload');
    # grab whatever is in the tmpupload (attach) field and put it into the tmp directory
    if ($query->param('attach.x') || $query->param('tmpupload'))
    {
	my($attached, $tmpfile);                # files currently "attached" to the message

        my $error;
        ($fullfile, $file, $error) = &attach_file();

	if ($query->param('attach.x'))
	{
	    compose();
	    return;
	}

        if ($error || $query->param('attach.x'))
        {
           compose();
           return;
        }

    }
    
  CHANGE_PROPERTIES:
    {
	# called with properties.x, write the set properties to options and reload compose page

	if ($query->param('properties.x'))
	{
#	    print_header();

	    my %opts = map { $_ => 1 } ($query->param('options'));

	    for (qw[attach cc bcc from replyto sender priority org ihelp manager])
	    {
#		debug "Setting $_ to $opts{$_}";

		$userdb{"options.$_.show"} = $opts{$_};
	    }

	    compose();
	    return;                     # just in case it falls through
	}
    }
    
   

  FILESPACE_CONTROLS:
    {
	my $filename;

      UPLOAD:
	if ($query->param('upload.x'))
	{
	    debug "UPLOADING";
	    upload_emufile(($query->param('uploaded_file'))[0], "$homedir/files", "compose");

	    return;
	}

      VIEW:
	if ($query->param('view.x'))
	{
	    debug "VIEWING";

	    view_emufile(($query->param('selected_file'))[0] || "", "compose");

	    return;
	}

    }

  POSTPONE_MESSAGE:
    {
	# Postponing a message
	# ====================
	#
	# Everything needs to be saved, all data currently set. Then the stuff
	# needs to get written into a dbm file with a hash as 32 character md5
	# checksum as the key. The checksum will be derived from all the data.
	#
	# When we are listing the files, we'll check if the filename is 32
	# characters long, if it's purely hexadecimal ([0-9a-fA-F]) and if it's
	# a valid key into the dbm file. If all this is true we'll read in the
	# data for this key from the database and get the Date and Subject for
	# the message. This text will be prepended with the date it was sent,
	# so a postponed message will look something like "01/19/79: Hey fool"
	# when interpreted, but in actuality the file will be something like:
	#
	#   d772ab9b1567c7898bd86d7fc5ba9682
	#
	# Hmm. The file will contain body data, and the index in the dbm will
	# contain the headers.

	# If spelling or postpone save draft. If flag is set, don't go in...
	if ( ( ($query->param('postpone.x')) || ($query->param('spelling.x')) ) && (!$flag) )
	{    
	    debug "ttam: POSTPONING";

	    my($md5, $digest, @headers, %heldmsgs);

	    # okay, they want to postpone a message. Save all the header 
            # information to our postpone db, and then write a file with the 
            # header stuff md5'd. This file will contain the body of the 
            # message that they've typed.

	    # time and SUBJECT must be the first two!
	    for ($i = 0; $i <= $#HEADER_ORDER; $i++)
	    {
		if ($HEADER_ORDER[$i] eq "to")
		{
		    $headers[$i] = $to;
		    next;
		}
		elsif ($HEADER_ORDER[$i] eq "bcc")
		{
		    $headers[$i] = $bcc;
		    next;
		}
		elsif ($HEADER_ORDER[$i] eq "cc")
		{
		    $headers[$i] = $cc;
		    next;
		}
		elsif ($HEADER_ORDER[$i] eq "from")
		{
		    $headers[$i] = $email;
		    next;
		}
		elsif ($HEADER_ORDER[$i] eq "attached") # move temporary attachments to permanent directory
		{
		    my $attached =  $query->param('attached');
		    $attached =~ s/ ,/ /;
		    
                    my $theattach;
		    foreach $theattach (split(' ', $attached))
		    {
			move("$homedir/tmp/$theattach", "$homedir/files/$theattach");
		    }
		}

		$headers[$i] = join("%%flurp813", $query->param($HEADER_ORDER[$i]));
#		debug "headers[$i] is $headers[$i]";
	    }

#	    load_module("Digest::MD5");
	    $md5 = new Digest::MD5;
#           debug "(POSTPONE) MD5 digest created from this data:\n@headers\n";
	    $md5->add(@headers);
	    $digest = $md5->hexdigest();

	    unshift(@headers, time); # time goes first

	    open(OUT, ">$homedir/files/$digest");
	    # binmode  OUT;
	    print OUT $query->param('message');
	    close OUT;

	    write_tmp("digest",$digest);

	    $userdb{"postponed.$digest"} = join("\0", @headers);

	    set_status($msg{'MSG_Postpone_S'}) if ($query->param('postpone.x'));

	    go_index() if ($query->param('postpone.x'));
	    spelling_parse() if ($query->param('spelling.x'));
	    return;
	}
    } # POSTPONE_MSG
    
  CONTINUE_MSG:
    {
	if ( ($query->param('continue.x')) || ($flag > 0) )
	{
	    my ($filename, @headers, %heldmsgs);

	    debug "CONTINUING";

	    $filename = $query->param('selected_msg') || get_var("digest");

	    if (!$filename)
	    {
		set_status($msg{'MSG_ContNoneSelected'});
		compose();
		return;
	    }

	    if ($filename !~ /^[0-9a-f]{32}$/i) # not really a postponed message
	    {
		set_status(convert($msg{'MSG_ContNoSuchMessage'}, $filename));
		compose();
		return;
	    }

	    $filename = basename(legalize($filename)); # may as well be safe

	    # everything's looking good. Now we just read in the message body 
            # from $filename and the headers from $heldmsgs{$filename}. Set 
            # the appropriate fields in the
	    # query object and then it should all be fine.

	    if (!$userdb{"postponed.$filename"}) # hmm, not a valid index...
	    {
		set_status($msg{'MSG_ContNoPostponed'});
		compose();
		return;
	    }

	    @headers = split("\0", $userdb{"postponed.$filename"});

	    $date = shift @headers;
#            debug "date is $date";
	    for ($i = 0; $i <= $#HEADER_ORDER; $i++)
	    {
		if ($headers[$i] =~ /%%flurp813/)
		{
		    my @tmp = split("%%flurp813", $headers[$i]);
		    
		    $query->param(-name => $HEADER_ORDER[$i], "values" => [ @tmp ]);
		    next;
		}
		
		if ($HEADER_ORDER[$i] eq "attached")
		{
		    my ($attached, @err, @arr);
			
		    $attached = $headers[$i];

		    debug "CONTINUING WITH ATTACHED FILES $attached";

		    # When a user continues a postponed message we have to check if the
		    # file exist in the user's emu file directory. If it doesn't exist
		    # then we remove the file from the attachments line and give the user
		    # an error message. If it does exist then we move it to the user's
		    # emufiles directory and continue on.

		    for (split(' ', $attached)) 
		    {
			if (!-e "$homedir/files/$_")
			{
			    push @err, $_;
			    next;
			}

			push @arr, $_; # an attachment we use

			copy("$homedir/files/$_", "$homedir/tmp/$_");
		    }

		    if (@err)
		    {
			set_status(convert($msg{'ERR_ContAttachFailed'}, join(', ', @err)));
		    }

		    $query->param($HEADER_ORDER[$i], join(' ', @arr));
		}

		$query->param($HEADER_ORDER[$i], $headers[$i]); # set the fields
	    }
	     
	    READ:
	    {
		local($/) = undef; # so we can read the file in one swoop
		my $msg;
		
		open(INMSG, "<$homedir/files/$filename");
		# binmode  INMSG;
		$msg = <INMSG>;
		close(INMSG);

		$query->param(-name => "message", -value => $msg);
	    }


	    set_status(convert($msg{'MSG_Continue_S'}, scalar(get_date($date))))
                if ($flag != 2);

	    $query->param('msg_continued', $filename); # so we know to delete it when sent

	    compose();
	    return;
	}
    }

  DELETE_MSG:
    {
	if ($query->param('delete.x'))
	{
	    my ($filename, $msg);
	    my (@headers, %heldmsgs);

	    debug "DELETING MESSAGE";

	    $filename = $query->param('selected_msg');
	    
	    if ($filename !~ /^[0-9a-f]{32}$/i) # not really a postponed message
	    {
		set_status(convert($msg{'ERR_DelePostNoSuchMessage'}, $filename));
		compose();
		return;
	    }

	    $filename = basename(legalize($filename)); # may as well be safe

	    if (!$userdb{"postponed.$filename"}) # hmm, not a valid index...
	    {
		set_status($msg{'ERR_DeleMissingMessage'});
		compose();
		return;
	    }
	    
	    delete $userdb{"postponed.$filename"};

	    unlink "$homedir/files/$filename";

	    set_status($msg{'MSG_DelePost_S'});

	    compose();
	    return;
	}

    }
 
    #MM 05/04/99 -- allow multi content types.  Only format when none/text/plain
    my $message_ct = $query->param("message_ct") || "text/plain";

#    debug "message_ct $message_ct";

    if (!($c{"no_wrap_messages"}))
    {
					@message = split(/\n/,$query->param('message'));
					
					if ($message_ct =~ /^text\/plain/i)
					{
					    format_it(\@message);
					}

					$the_message = join('',@message);
						
    }
    else
    {
        $the_message = $query->param('message');
    }
    
    $the_message =~ s/\r//g if ($c{'delete_new_line'});

    $real_name    = reverse_html($userdb{"options.real_name"});
    $email        = $email || $query->param('from')        || $userdb{"options.email"} || $user_name;
    $organization = $query->param('organization') || $userdb{"options.organization"};
    $priority     = $query->param('priority');
    $sender       = $query->param('sender');

    # Hmm, trying to send without TO ? (smart) <-giggle
    if (!$to)
    {
				set_status($msg{'ERR_MissingToAddress'});
				compose();              # try again
				return;
    }

# 	Already implemented (by Groups feature)
	# Nicknames feature -> replace nicknames from addressbook with emails
	# Get addressbook from userdb.
	
	# nick => email
#	my %addrbook_users = map { $_, (split(':',$userdb{"addresses.$_"}))[0] } grep { s/^addresses\.// } keys %userdb;
#	debug "nicknames. have such users: ", keys %addrbook_users;
#	for my $para (qw/to cc bcc/)
#	{
#		my @reps = split(/\s*,\s*/, $query->param($para));
#		debug "nicknames: have such recipients in $para: @reps";
#		for my $rep (@reps)
#		{
#			for my $user (keys %addrbook_users)
#			{
#				if ( $user =~ /^\Q$rep\E$/i )
#				{
#					$rep = $addrbook_users{$user};
#					debug "nicknames: replaced nick $user with $addrbook_users{$user} in $para";
#				}
#			}
#		}
#		$query->param( $para, join(', ', @reps) );
#	}
	# end of nickname feature

    $addr_parse = Mail::Address->new($real_name, $email);
    $from = $addr_parse->format();

    my $subj = $query->param('subject') || $msg{'MSG_NoSubject'};

    # get current date. For composing, we DO NOT want to apply any
    # any translations, because we end up not following standards
    $date = get_date(0,0,1);
#    debug "date is $date";
    my %paramhash = (-From           => $from,
		     "-Reply-To"     => $query->param('replyto') || $from,
		     -To             => $to,
		     -Date           => $date,
		     -Subject        => $subj,
		     "-X-Mailer"     => get_xmailer_string() || undef,
		     "-X-Browser"    => "$ENV{'HTTP_USER_AGENT'}",
		     "-X-Browser-IP"     => $ENV{"REMOTE_ADDR"},
		     "-X-webmail-user"     => $user_name,
		     "-X-HTTP_HOST"     => $ENV{'HTTP_HOST'},
		     "-MIME-Version" => "1.0",
		     );

#    $paramhash{"-X-advert"} = $c{"xadvert"} if $c{"xadvert"};
    $paramhash{"-Cc"}     = $cc if ($cc);

#We no need add Bcc to header.
#    $paramhash{"-Bcc"}     = $bcc if ($bcc);
    $paramhash{"-Sender"} = $sender if ($sender && $sender ne $from);
    $paramhash{"-Organization"} = $organization if ($organization);
    $paramhash{"-Priority"} = $priority if ($priority);
    $paramhash{"-X-Priority"} = $priority if ($priority);

    if ( $AD_VERT == VERSION_ADVERT )
    {
       load_module("LWP::Simple");
       if (!(defined ($tmp = LWP::Simple::get ("http://ad.vert.net/tagline.cgi?".$c{"default_pop"}))))
       { 
         $tmp = "This message powered by EMUmail.  http://EMUmail.com\n" ;
       }

       $tmp = "\n\n$tmp\n";
   }
    else # Professional
    {
       $tmp = $userdb{tagline} || $msg{'MSG_Tagline'} || "";
    }

#    load_module("MIME::Entity");
    $ent = new MIME::Entity;

    # How will we be setting up the MIME object?
    #
    # There are four different ways that someone can attach a file:
    #
    # \1  The user selects a file from their system with the Browse button and then they
    #     send off their message. This will attach the single file that they've selected
    #     when the message is sent.
    #
    # \2  The user selects a file from their system like in the first method, then they
    #     click on Attach More and select another file until they repeat this until
    #     they've attached everything they want. Each time they hit Attach More it uploads
    #     the file and saves it in their temporary directory. When the message is sent,
    #     each of the files is attached to the document and it is put out on its way.
    #
    # \3  The user does everything as in method two except they also leave the browse button
    #     filled in for the last attachment. When this happens, the file from the browse
    #     should be moved to the temporary directory like the others, and then it should
    #     be attached along with everything else.
    #
    # \4  The user can select multiple files from their filespace and these would be attached
    #     to the document. This method should intermingle freely with the above mentioned ones.
    #



    if ($query->param('selected_file') || $query->param('attached')
	|| $query->param('upload') || $query->param('tmpupload')
        || scalar( grep { $_ =~ /^attachment_/i } $query->param() ) > 0 )     #  rcs.ngf.v.1 stmt.3 8/30/99 --ngf
    {
	my %options;


        # ********************************************************* #
        # 
        #   9/30/99 rcs.ngf.v.1 nph-emumail.cgi block.4 begin {


        my $text; # The text before the tagline 

      ADD_TEXT_BEFORE_TAGLINE: 
        {
           if ($c{"add_body_handler"})
           {
               my ($sub) = $c{"add_body_handler"};

               if ($sub)
               {
                   my( $evalstr );
                   load_module("EMU::Custom");
                   $sub = "EMU::Custom::".$sub;

                   $evalstr = "\$text = &$sub(\"" . $query->param('attachment_00_Filename') ."\", \\\%c);";
                   $result = eval( $evalstr );

                   debug("Ran $sub : error ? : result = $result,  text = $text, \$\@ = $@ ");

               }
           }
           else
           {
                $text = $query->param("add_to_body");
           }

            #Add something before the tagline
            $tmp = $text . $tmp;

            #print "tmp = $tmp <br>"; # TEST
        }      

        #  } end block.4 nph-emumail.cgi rcs.ngf.v.1 9/30/99 --ngf 
        # 
        # ************************************************************************* #


	# multipart message
	$paramhash{"Type"} = "multipart/mixed";

        debug "upload";
	$ent = $ent->build(%paramhash); 
	
	%paramhash = ( Type     => $message_ct,
		       Encoding => $userdb{'options.encoding'} || $c{'default_encoding'},
		       Data     => $the_message."\n"
		     );

        my %sighash;


        #  ******************************************************************* #
        #
        #   9/30/99 rcs.ngf.v.1 nph-emumail.cgi block.5 begin {


        if( $text )  # i.e. if Messagebay message exists  #  rcs.ngf.v.1  9/20/99 --ngf
        {
            # we add this variable to the header so the browser (emumail!) can detect the message ID :

            $ent_head = $ent->head;
            $ent_head->add( 'Voice-Id', $query->param('attachment_00_Filename'));  # 9/20/99 --ngf
        }


        #  } end block.5 nph-emumail.cgi rcs.ngf.v.1 9/30/99
        #
        #  ******************************************************************* #


        if ($message_ct eq 'text/plain')
        {
          $paramhash{"Data"} .= "\n$tmp\n";
        }
        elsif ($message_ct eq 'text/html')
        {
          $paramhash{"Data"} .= "<br>$tmp<br>";
        }
        elsif ($tmp)
        {
        # Add this as an attachment incase the Content type isn't text/plain
          %sighash = ( Type     => "text/plain",
                       Encoding => $userdb{'options.encoding'} || $c{'default_encoding'},
                       Data     => "\n$tmp\n"
                     );

        }

#          debug "attaching 1";
          $ent->attach(%paramhash);
          $ent->attach(%sighash) if (keys %sighash);

	##
	## Now let's start attaching some files
	##
	
	# read the files from the filespace selection box
	if ($query->param('selected_file'))
	{
	    my @files = $query->param('selected_file');
            debug "selected file @files";

            my $thefile;
	    foreach $thefile (@files)
	    {
		if (/^(sys[01]):(.*)/)
		{

		    $thefile = ($1 eq "sys0" ? "$SYSFILEDIR/$2" : "$SYSXTRADIR/$2");
		    next;
		}

		$thefile = "$homedir/files/$thefile";
	    }

	    push @atts, @files;
	}

	my $tmp_attached;

	# read the files which are just temporarily uploaded
	$tmp_attached = $query->param('attached');
        # get rid of leading white space
        trim(\$tmp_attached);
	if ( $tmp_attached )
	{
	    my ($mlah, @err);
#            debug "tmp_attached $tmp_attached";

	    # if we are continuing a message then all attachments should
	    # now be in the files directory. However, we want to keep
	    # track that they're actually "temporary" files and should
	    # be deleted when the user sends this message
	    $mlah = $query->param('continued_msg') ? "files" : "tmp";

	    # 07/25/98: take out the characters that we added (the space). this fixes the attachment w/space in
	    # name problem.
	    $tmp_attached =~ s/\,\s/,/g;
#debug "tmp_attached $tmp_attached";
	    @tmpatts = map { $_ = "$homedir/$mlah/$_" } split(' ', $tmp_attached);

            my $theattach;
	    foreach $theattach (@tmpatts)
	    {
                next if $theattach eq "";
		if (!-e $theattach)
		{
                    debug "Can't find file $theattach";
		    push (@err, $theattach);
		}
	    }

	    if (@err)
	    {
		set_status(convert($msg{'ERR_FailedAttachSendAgain'}, join(', ', map basename($theattach), @err)));

		foreach (@err)
		{
		    @tmpatts = grep !/^$theattach$/, @tmpatts;
		}
		
		$query->param('attached', join(' ', @tmpatts));

		compose();
		return;
	    }

	    push @atts, @tmpatts;
	}

#        debug "atts @atts";
	# If there is a file in the FILE UPLOAD field in the FILE MANAGER then
	# the file should be uploaded, saved and attached. If the file is in
	# the ATTACH field then it should be uploaded and attached but not saved.
	if ($query->param('upload'))
	{
	    $fullfile = $query->param('upload');
	    $file     = legalize(basename($fullfile));
	    
	    open(FILEOUT, ">$homedir/files/$file");
	    binmode(FILEOUT);
	    
	    my $fh = $query->upload('upload');
	    
	    while (<$fh>) {
	       print FILEOUT $_;
	    }
	    
	    close(FILEOUT);

	    # add the file to the list
	    push @atts, "$homedir/files/$file";
	}

#	debug "ATTS ARE @atts";

      VERIFY_ATTACHMENTS:
	{
	    my @at = @tmpatts;
	    for (@atts)
	    {
		# if the temporary attachment of a message can't be found then we will
		# send the message anyways, because if we don't then they will never
		# be able to send the message since you can't remove temporary attaches
		# from the message
		if (!-e $_)
		{
		    if ($_ =~ m{/tmp/})
		    {
			@at = grep !/^$_$/, @at;
			set_status($status . convert($msg{'ERR_FailedAttach'}, basename($_)));
			next;
		    }
  
		    set_status($status . convert($msg{'ERR_FailedAttach'}, basename($_)));
		    return;
		}
	    }
	}


      #  ******************************************************************* #
      #
      #   9/30/99 rcs.ngf.v.1 nph-emumail.cgi block.6 begin {


      ADD_ATTACHMENTS :              # 8/19/99 --ngf
        {
            my( @keys, @compose_atts, %atts_paramhash, %tmp_hash, 
                $this_att_param, $this_att_file, $this_att_num,
                $this_att_prop, $this_att_value, $this_mime_type, 
                $att_hash_ref, $my_handler, $tmpfile, $my_ent, $eval_string );

            # print $query->header;

            # ######################################################################### 
            #  Add user's set of attachments :     # this section unchanged 

	    foreach my $a (@atts)
	    {
	        next if !$a;        # flurp

                # remove trailing index
                my $a_name = $a;
                $a_name =~ s/_\d+$//;

                my $ctype = find_mime_type($a_name);
                debug "attaching $a_name type $ctype"; 

                my $enc = ($ctype =~ /message.rfc822/i) ? "" : "base64";

	        $ent->attach(Type     => $ctype,
	    		     Encoding => $enc,
			     Path     => $a,
			     Filename => basename($a_name));
            }

            # ######################################################################### ++
            #  make hash of attachment properties specified in compose.html
            #  e.g. :
            #       (attachment_$n          = ($fullfilename))+
            #       (attachment_$n_Type     = text/html)* || 'application/octet-stream'
            #       (attachment_$n_Encoding = base64)*
            #       (attachment_$n_X-(.*)   = (.*) \n)+

            if( !($c{'site_voice_enabled'} && !$userdb{'options.user_voice_enabled'}) ) 
            { 
                @compose_atts = grep { $_ =~ /attachment_(\d+)/ && $_ !~ /attachment_00/i } $query->param();
            }
            else 
            {
                @compose_atts = grep { $_ =~ /attachment_(\d+)/ } $query->param();
            }

            foreach $this_att_param (@compose_atts)
            {
                $_ = $this_att_param;   m/(attachment_(\d+)_(.*))/i;
                $this_att_num = $2;   $this_att_prop = $3;
                $this_att_value = $query->param($this_att_param);

                debug "this_att_param = $this_att_param, this_att_value = $this_att_value<br>\n";

                if( $this_att_value )
                {
                    $atts_paramhash{$this_att_num}{$this_att_prop} = $query->param($this_att_param);
                }
            }

            # **********   add compose.html attachments via handler or self :  *********# 

            # select only filled in attachment_nn_(.*) fields :
            @compose_atts = grep { $query->param("attachment_$_\_Filename") =~ /\w/ } (keys %atts_paramhash);

            # debug "compose_atts = @compose_atts<br>\n";
            # debug "attvmsg = " . $query->param('attvmsg') . "<br>\n";

            foreach $this_att_num (@compose_atts)
            {
#                debug "this_att_num = $this_att_num <br>"; 

                # Copy attachment from the cached multi-part message to a real file :

                $atts_paramhash{$this_att_num}{'Path'} = "$homedir/tmp/" . basename($atts_paramhash{$this_att_num}{'Filename'});

                open(FILEOUT, ">$atts_paramhash{$this_att_num}{Path}");
                binmode(FILEOUT);

                my $fh = $query->upload($atts_paramhash{$this_att_num}{'Filename'});

                while (<$fh>) {
                   print FILEOUT $_;
                }

                close(FILEOUT);

                # Call user's default handler for this attachment :

                $_ = $this_mime_type = $atts_paramhash{$this_att_num}{'Type'} 
                        || find_mime_type($atts_paramhash{$this_att_num}{'Filename'});
                m/(.*)?\/(.*)/i;   $this_mime_type = $2 if $2;

#                debug "mime_type(attachment_$this_att_num) = $this_mime_type <Br>\n";

                if( $my_handler = $c{"compose_handler_".$this_mime_type} )
                {
#                    debug "my_handler for attachment_$this_att_num exists!<br>";

                    %tmp_hash = %{ $atts_paramhash{$this_att_num} };

                    load_module("EMU::Custom");
                    $eval_string = "\&$my_handler(\$ent, \\\%tmp_hash, \\\%c);";
                    $my_ent = eval( $eval_string );

                    if (!$my_ent)
                    { 
#                        debug "ADD_ATTACHMENTS: eval returned nothing.<br>"; # DEBUG

                        if( find_mime_type($atts_paramhash{$this_att_num}{'Filename'}) )
                        {
                            $ent->attach(%{$atts_paramhash{$this_att_num}});

#                            debug "added attachment of $_ type : number of MIME parts now = " . $ent->parts . "<br>\n";
                        }
                        else 
                        {
                            debug "attachment type unknown; part not added.";
                        }

                    }  # elsif problem attaching using custom handler. 
                }
                else
                {
                    debug "my_handler for attachment_$this_att_num DNE!<br>";

                    $ent->attach(%{$atts_paramhash{$this_att_num}});

#                    debug "number of MIME parts is now " . $ent->parts . "<br>\n";

                }  # elsif no custom handler.


            }  # foreach compose.html attachment


            if( !$this_att_num ) { debug("no compose.html attachments!"); }

        }   # ********    end of ADD_ATTACHMENTS   # 8/19/99 --ngf     ******** #

        #  } end block.6 nph-emumail.cgi rcs.ngf.v.1 9/30/99
        #
        #  ******************************************************************* #


    }
    else                        # otherwise it's a single plain text
    {
#        debug "building plain text message";
#        $paramhash{"Type"} = "multipart/mixed";
#        $ent = $ent->build(%paramhash);

        # Sorry--every message is multipart
#        $paramhash{"Type"} = $message_ct; #05/04/99 MM

        if ( (!($c{"signature_as_attach"})) && ($message_ct eq 'text/plain') )
        {
#            debug "signature appended (not attached), text/plain";
            $paramhash{"Type"} = "text/plain";
            $paramhash{"Data"} .= "$the_message\n$tmp\n";
            $ent = $ent->build(%paramhash);
#            debug "1";
        }
        else
        { 
#            debug "signature is attachment";

            $paramhash{"Type"} = "multipart/mixed";
            $ent = $ent->build(%paramhash);
            
            $paramhash{"Type"} = "$message_ct"; 

            if ($message_ct eq 'text/html') {
               $paramhash{"Data"} = "$the_message<br>\n$tmp<br>\n";
            } else {
               $paramhash{"Data"} = $the_message."\n";
               
               #05/04/99 MM -- Allow Sig as attachment
               my %sighash;
               $sighash{"Type"} = "text/plain";
               $sighash{"Data"} =  "\n$tmp\n";

               $ent->attach(%sighash);
            }
            
            $ent->attach(%paramhash);

        }

    }
    
    delete $v{"forwarding"};
    
    if ($to !~ /,$/)
    {
	$to .= ",";
    }
    
#    load_module("Net::SMTP");

    my $smtp;
    foreach my $host (@smtp_host) {
    	#debug "User: $user_name $host $password";
        $smtp = Net::SMTP_auth->new($host, Port=>$smtp_port);
        $smtp->auth('CRAM-MD5', $user_name, $password) if defined $c{smtp_auth};
        debug "$host is no good, going on to next!" if (!$smtp);
        next if (!$smtp);
        last;
    }

    if (!$smtp)
    {
	set_status($msg{'ERR_SmtpServConnect_S'});
	EMUerror($msg{'ERR_SmtpServConnect_T'}, $msg{'ERR_SmtpServConnect_B'});
        return;
    }

    if ($userdb{"options.dsn"})
    {
        my $type = $c{"dsn_type"} || "full";
        $smtp->mail($email, { Return => $type}) || $errors++;
    }
    else {
        $smtp->mail($email);
    }
    
    if ($userdb{"options.mdn"})
    {
	my $ent_head = $ent->head;
	$ent_head->add( 'Message-ID', int(rand(9999999999)).".".int(rand(9999999999))."@".(split '@', $from)[1]);
	$ent_head->add( 'Disposition-Notification-To', $from );
    }

    $to_who = "$to,$cc,$bcc";
#    debug "to_who=$to_who";

    $to_who =~ s/(,\s*){2,}/,/g;
    $to_who =~ s/,\s*$//;
#    debug "to_who=$to_who";
    @rcpts = split(/,/, $to_who);

    if ($c{max_recipients} && scalar(@rcpts) > $c{max_recipients}) {
       set_status( convert($msg{'ERR_TooManyRecipients'}, $c{max_recipients}) );
       compose();
       return;
    }
     
#    debug "rcpts is @rcpts";

  SMTP_TO:
    {
	my (@addrs, $i);

	foreach $person (@rcpts)
	{
#	    debug "SENDING TO '$person'";
	    
            if ($userdb{"options.dsn"})
            {
               eval 
               {
                   my $when = $c{"dsn_when"} || "success";
                   my (@when) = ($when);
   	           $result = $smtp->to($person, {Notify => \@when});
               };
            }
            else
            {
	        $result = $smtp->to($person);
#                debug "result: $result";
            }

	    if (!$result) 
	    {
	        debug "SERVER CODE: ", $smtp->code, "; MESSAGE:", $smtp->message;
		$addrs[$i++] = $person;
		$errors++;
	    }
	}

#	debug "ADDRS ARE @addrs";

	set_status($status . convert($msg{'ERR_EmailAddrInvalidMult_S'}, join (', ', @addrs))) if (@addrs > 1);
	set_status($status . convert($msg{'ERR_EmailAddrInvalid_S'}, $addrs[0])) if (@addrs == 1);
    }

  ERROR_HANDLING:
    {
	if ($errors)
	{
            debug "found errors ($errors)";
	    set_status($status . $msg{'ERR_FailedMessageSend_S'});
	    compose($to, $cc, $subj, 0, $query->param('message'));
	    return;
	}
    }

    # NOTE:
    #  header() is a method from Mail::Header
    # 
    # We print out the header and then print out the data.

    my ($md5, $digest);

    $digest = get_digest(time^$$);
   
    # Create and save outgoing message
    open (MSG, ">$homedir/messages/$digest") || $errors++;
    # binmode  MSG;

#    debug "printing out message $digest";

    $ent->print(\*MSG);
    close MSG;

#    debug "finished printing $digest";

    # Now we send the message to the smtp server. However, send it one
    # line at a time because sending the whole thing at once forces
    # too much memory allocation
    open (MSG, "<$homedir/messages/$digest") || $errors++;
    # binmode  MSG;

    $smtp->data();
    while (<MSG>) {
        $smtp->datasend( $_ );
    }
    close MSG;
    $smtp->dataend();

    $smtp->quit();

#    debug "smtp message sent";

    my $delete_msg = 0;
    my $fold = get_outbox_name();
    my $proto = $userdb{"folder:$fold:protocol"} || $c{"outbox_protocol"} || $userdb{"folder:$inbox:protocol"};
    my $added_status;

  SAVE_TO_OUTBOX:
    {
        # dont save if we're not configured to save
        if ($c{"disable_outbox"}) {
             $delete_msg = 1;
             last SAVE_TO_OUTBOX;
        }

        # if remote only and the outbox is local (not imap) then dont save
        if ($c{"remote_only"}) {
            if ($proto !~ /imap/i) {
                $delete_msg = 1;
                last SAVE_TO_OUTBOX;
            }
        }

        # dont save if per-user config says not to
        if (defined($userdb{"options.save_outbox"}) && 
                !$userdb{"options.save_outbox"}) {
             $delete_msg = 1;
             last SAVE_TO_OUTBOX;
        }

        # don't save if over quota or over a configured limit
        if ($over_quota || ($c{"outbox_msg_size_limit"} &&
                (-s "$homedir/messages/$digest") > $c{"outbox_msg_size_limit"})) {
            $delete_msg = 1;

            if ($over_quota) {
                $added_status = convert($msg{MSG_SentMessageNotSaved},
                                    $fold, $msg{MSG_SentMessageNotSavedQuota});
            }
            else {
                $added_status = convert($msg{MSG_SentMessageNotSaved},
                                    $fold, $msg{MSG_SentMessageNotSavedLarge});
            }
            last SAVE_TO_OUTBOX;
        }

        # ok, i guess we can save it...

        $outbox{"$digest:to"} = $to_who;
        $outbox{"$digest:from"} = $from;
        $outbox{"$digest:date"} = $date;
        $outbox{"$digest:subj"} = $subj;
        $outbox{"$digest:size"} = -s "$homedir/messages/$digest";
        $outbox{"$digest:uid"} = $digest;

        my $added = add_to_outbox($digest, \%outbox);

        $force_check = 1 if ($added == 2);

        $added_status = convert($msg{MSG_SentMessageSaved}, $fold) if ($added);
    }

    if ($delete_msg) {
        debug "not saving to outbox!";
        del_from_local($digest, 1);
    }

    # 08/6/98: if we have rmsg set here then this message was a reply and 
    # we need to update the status of the message stored on disk to reflect 
    # that we've now answered it.
    if ($v{"rmsg"})
    {
	my ($msg) = $v{"rmsg"};
#        $userdb{"msgs:$msg:stat"} = STAT_ANS;
	set_msg_status($msg,STAT_ANS);
        delete $v{"rmsg"};
#        debug "status now ".$folderdb{"$msg:stat"};
    }
    
    $to_who =~ s/(.*)\n/$1/g;
    
  CLEANUP:
    unlink @tmpatts;            # delete the temporary uploads

    # the user continued a postponed message, delete the postponed message from
    # storage and from the heldmsgs hash
    if ($query->param('msg_continued'))
    {
	my ($filename, $attached, $index, @attached);

	# 07/22/98: umm, was using == on a string comparison before.... /Jah
	$index++ while ($HEADER_ORDER[$index] ne "attached"); # get the index

	$filename = basename(legalize($query->param('msg_continued')));
	
	$attached = (split("\0", $userdb{"postponed.$filename"}))[$index];
	$attached =~ s/,//g;

#	@attached = split(' ', $attached);
	@attached = split(' ', $tmp);
	foreach (@attached)
	{
	    unlink "$homedir/files/$_";
	}
 
	delete $messages{"postponed.$filename"};

	debug "deleting file $filename";
	unlink "$homedir/files/$filename";
    }

#    debug "save_outbox: $save_outbox ",$userdb{"options.save_outbox"};
    $status = "$msg{'MSG_SentMessage'} $added_status";
    $v{"clean_tmp"} = 1;

    return &session_expired("$msg{'MSG_SentMessage'} $added_status <BR>") 
    	   if (!session_check()); #Alex session escape fix

    set_status($status);
    go_index($force_check);
}

sub get_outbox_name
{
    # What's the name of our outbox?
    my ($month, $year) = (get_date())[2,3];
    my $fold;

    # allow admin to provide a system-wide outbox name which bypasses
    # the formatting below
    if ($msg{'V_Outbox_Name'}) {
        $fold = $msg{'V_Outbox_Name'};
    }
    else {
        # 07/24/98: let the admin configure this (or the user 09/28/00)
        $fold = $userdb{"options.sentfolder"} || convert($msg{'V_SentmailFolderFormat'}, $msg{'V_SentmailFolderPretext'}, $month, $year);
    }

    return $fold;
}

sub add_to_outbox
{
    my ($digest, $hash) = @_;

    my ($fold, %folddb);
    my $foldfile;
    my $samefold = 0;

    $fold = get_outbox_name();
    my $proto = $userdb{"folder:$fold:protocol"} || $c{"outbox_protocol"} || $userdb{"folder:$inbox:protocol"};

    # if we dont yet have an outbox, save in the protocol so it is properly
    # created down the line.
    $userdb{"folder:$fold:protocol"} = $proto
        if (!defined($userdb{"folder:$fold:protocol"}));

    my $prefix;
    my $delim = &get_imap_delimiter(1) if ($protocol =~ /imap/i);

    $samefold = 1 if ($folder eq $fold);

 	SET_OUTBOX_FOLDER:
    {
        $prefix = get_outbox_prefix() if ($protocol =~ /imap/i);
		if ($prefix)
		{
	    	debug "Outbox prefix: $prefix";
	    	$fold = "$prefix$delim$fold"; #BAD... / isn't necessarily the delimeter...
		}
    }

    my $added = add_to_folder($digest, $fold, 1);

    debug "added to $fold? $added";

    # we need to force check on go_index if we're in the same folder
    $added += 1 if ($samefold);

    return $added if ($proto =~ /imap/i);

    debug "folder $folder, fold $fold";
    undef %folddb;

    if ($folder ne $fold)
    {
        $fold =~ s/^$prefix$delim// if ($prefix);
        $foldfile = process_fold_type($fold);
		if ( $ELocks->lock_create("$homedir/folders/$foldfile", \%folddb, {mode => 'write', nb => 1}) )
		{
        	tie %folddb, $db_package, "$homedir/folders/$foldfile", O_CREAT|O_RDWR, 0660;
        	debug "opened folder |$foldfile|";
        }
    }

    my @k = keys %$hash if $hash;

    foreach (@k)
    {
        $folddb{$_} = $$hash{$_} if (%folddb ne undef);
        $folderdb{$_} = $$hash{$_} if (%folddb eq undef);
    }

    if ($folder ne $fold && %folddb ne undef)
    {
        untie %folddb;
        $ELocks->lock_remove(\%folddb);
    }

    return $added;
}

sub format_it 
{
    my $message = shift;

    foreach (@{ $message })
    {
	s/\r\n/\n/;             # transpose \r\n's to \n's
    }

    debug "wrapping message";
#    @{$message} = wrap("", "", @{$message});
    @{$message} = text_wrap("", @{$message});
}

sub format_cells
{
    my (@ftemp, $line, $field, $data);

    @ftemp = split(/[\n\r]/, join("", @_)); 

    foreach $line (@ftemp)
    {
        $line = &safe_html($line, '<>'); #escape HTML

	debug "LINE is $line";

	if (($field, $data) = ($line =~ /^([\w-]+):(.*)/))
	{
	    $data =~ /^\s*$/;
            $data = "<BR>" if (!$data);
	    $line =  qq{<TD bgcolor=white><B>$FONT_IND $field: </FONT></B></TD>\n};
	    $line .= qq{<TD bgcolor=white><B>$FONT_IND $data </FONT></B></TD>\n</TR>\n<TR>\n};
	}
	else
	{
	    $line = qq{<TD bgcolor=white><BR></TD>\n<TD bgcolor=white>$FONT_IND <B>$line</B></FONT></TD>\n</TR>\n<TR>\n};
	}
    }

    return (join('', @ftemp));
}

sub print_cells
{
    my ($data, $it, $iterator) = @_;
    my (@ftemp, $line, $field);

    @ftemp = split(/[\n\r]/, join("", @_)); 

    foreach $line (@ftemp)
    {
        $line = &safe_html($line, '<>'); #escape HTML

	debug "LINE is $line";

	if (($field, $data) = ($line =~ /^([\w-]+):(.*)/))
	{
	    $data =~ /^\s*$/;
            $data = "<BR>" if (!$data);
	    $line =  qq{<TD bgcolor=white><B>$FONT_IND $field: </FONT></B></TD>\n};
	    $line .= qq{<TD bgcolor=white><B>$FONT_IND $data </FONT></B></TD>\n</TR>\n<TR>\n};
	}
	else
	{
	    $line = qq{<TD bgcolor=white><BR></TD>\n<TD bgcolor=white>$FONT_IND <B>$line</B></FONT></TD>\n</TR>\n<TR>\n};
	}
    }

    return (join('', @ftemp));
}

# sub format_pure
#
# called with a full email message as arugment when the interpret HTML option is OFF
sub format_pure
{
    my $message = shift;

    return $message if ($licensed{"wap"} && $c{"is_wap"});

    foreach ( @{ $message } )
    {
        s/\r\n/\n/;             # better this way..
        $_ = &safe_html($_, '<>');
    }
}

sub redirect
{
    my ($redir) = shift;
    trim(\$redir);      
    # make sure to clean up
    close_db() if ($db_opened);
    print_header();
    print qq{<META HTTP-EQUIV="Refresh" CONTENT="0; URL=$redir">};
}

sub logout
{
    my @files;
   
    if ($c{"success_logout_sub"})
    {
	load_module("EMU::Custom");

	debug "Calling success_logout($user_name)";
        &EMU::Custom::success_logout($user_name);
debug "extra_head: $extra_head";
    }

    # 08/28/98: allow the logout page to be overriden
    if (!$c{'redirect_logout'} && !$c{'perlsub_redirect_logout'})
    {
	load_page("logout.html");
        debug "loaded logout page";
    }

    debug "now continuing to do other stuff in the background";

    # cleanup tmp files (except session file)
    wildrm("$homedir/tmp", '^session\.', 1);

    # cancel out time
    $v{"time"} = 0;

    # remove cached passwords
    foreach my $e ( grep (/^folder:/, keys %userdb) ) {
        my (undef, $name, $key) = split(':', $e);
        
        if ($key eq 'password' && !$userdb{"folder:$name:external"}) {
           delete($userdb{$e});
        }
    }

    # delete all of the user's file if account persistance is turned off
    if ($c{'disable_account_persistence'})
    {
        untie %userdb;
        untie %folderdb;
	deltree($homedir);
    }

    # Delete messages/tmp files if the EMUtype is remote_only
    elsif ($c{'remote_only'})
    {
	deltree("$homedir/messages");
	deltree("$homedir/tmp");
	deltree("$homedir/folders", '.external');
#	deltree("$homedir/folders/.external");
	deltree("$homedir/folders/.imap");
	deltree("$homedir/folders-ordered");
    
#        foreach my $k (grep(/^folder:/, keys %userdb)) {
#           $k =~ /folder:(.+?):.*/;
#           my $f = $1;
#           if (!$userdb{"folder:$f:external"}) {
#                delete $userdb{$k};
#           }
#        }   

    }
    else
    {
	# Cleanup old msgs
	&flush_msg_cache() unless (bool($c{"dont_flush_on_logout"}));
    }

    # we werent closing on logout??? Added it 2000/09/30 RMK
    &close_db() if ($db_opened);

    &rescue_dbs() unless ($c{no_db_refresh});

    if ($c{'redirect_logout'} || $c{'perlsub_redirect_logout'}) {
	my ($redir);
	
	if ($c{'perlsub_redirect_logout'})
	{
	    my ($sub) = $c{'perlsub_redirect_logout'};
	    $sub =~ s/^\s*{// && $sub =~ s/\s*}\s*$//;
	    my ($subref) = eval("sub { $sub }");
	    $redir = &$subref($query);
	    debug "From using perlsub_redirect, going to $redir";
	}

	$redir = $redir || $c{'redirect_logout'};
        redirect($redir);
    }

}


sub create_foldmap
{
    return unless ($homedir);

    # go through each folder and create a map of message -> folder

    my ($uid, $tmpuid, $msgfile, @badheaders);
    my $head = undef;
    my %folders = ();
    my $fold;
    my @folders = get_folders();
    debug "valid folders are @folders";

    # save messages from folders
    my %foldmsgs;
    my %tmpfold;
    my @msgs;
    my $foldfile;

    if ( $ELocks->lock_create("$homedir/foldmap", \%foldmap, {mode => 'write', nb => 1}) )
    {
    	tie %foldmap, $db_package, "$homedir/foldmap", O_CREAT|O_RDWR, 0660;
    }

    debug "current folder is $folder";
    debug "$folder messages: ".$folderdb{"messages"};
    foreach $fold (@folders) {
        if (!/^$folder$/i) {
            my $searchfold = $msg{"FOLD_Search_Results"} || "Search Results";
            next if ($fold eq $searchfold);

            $foldfile = process_fold_type($fold);

            # make sure the folder we're processing isnt already opened
            if ($fold eq $folder && $ELocks->lock_search("$homedir/folders/$foldfile", 'path'))
            {
                untie %folderdb;
                $ELocks->lock_remove(\%folderdb);
            }

            debug "opening folder $foldfile";
            if ( $ELocks->lock_create("$homedir/folders/$foldfile", \%tmpfold, {mode => 'read', nb => 1}) )
            {
	            tie %tmpfold, $db_package, "$homedir/folders/$foldfile", O_RDONLY, 0660;
	            @msgs = split(':', $tmpfold{"messages"});
	            untie %tmpfold;
	            $ELocks->lock_remove(\%tmpfold);
	    }
        }
        else {
            @msgs = split(':', $folderdb{"messages"});
        }

        foreach my $themsg (@msgs) {
            debug "mapping message $themsg to folder $fold";
            $foldmap{$themsg} = $fold;
        }
    }

}

# Check for missing message files. 
# If the files cannot be retrieved from the server,
# remove the messages from the folderdb.
sub check_msg_cache
{
	return if !$homedir;
    
	my @folders = get_folders();
	debug "Folders: @folders";
    
	untie %folderdb;
    
	foreach my $f (@folders)
	{
		debug "Processing folder $f";
		my $file = process_fold_type($f);
      
      		my %tmpdb;
      		if ( $ELocks->lock_create("$homedir/folders/$file", \%tmpdb, {mode => 'read', nb => 1}) )
      		{
			tie %tmpdb, $db_package, "$homedir/folders/$file", O_RDONLY, 0660;

			my @msgs = split(':', $tmpdb{"messages"});
			my %bad;
			foreach my $msg (@msgs)
			{
	 			if (!-f "$homedir/messages/$msg" && !download_msg($msg) )
	 			{
	    				debug "Discovered bad messageid '$msg'.";
	    				$bad{$msg} = 1;
	 			}
			}
	
			foreach (keys %tmpdb)
			{
	 			my ($id) = split(':', $_);
	 			if ($bad{$id})
	 			{
	    				debug "Removing '$_' from folder '$f'";
	    				delete($tmpdb{$_});
	 			}
			}
	 
			untie %tmpdb;
			$ELocks->lock_remove(\%tmpdb);
      		}
   	}      
}      

sub flush_msg_cache
{
    return unless ($homedir);

    # check contents of messages directory against userdb
    # if a message is not in userdb then delete it

    my ($uid, $tmpuid, $msgfile, @badheaders);
    my $head = undef;
    my %folders = ();

    my @folders = get_folders();
    debug "valid folders are @folders";

    # save messages from folders
    my %foldmsgs;
    my %tmpfold;
    my @msgs;
#    debug "current folder is $folder";
#    debug "$folder messages: ".$folderdb{"messages"};

    # So we don't screw up in trying to do a tie, let's untie the current 
    # %folderdb.
    untie %folderdb;
    $ELocks->lock_remove(\%folderdb);

    foreach (@folders) {
#        debug "opening folder $_";
        my $foldfile = process_fold_type($_);
#        debug "foldfile is $foldfile";

#        db_timeout("$homedir/folders/$foldfile",0,1)
#            if (-e "$homedir/folders/$foldfile.lok");
	if ( $ELocks->lock_create("$homedir/folders/$foldfile", \%tmpfold, {mode => 'read', nb => 1}) )
	{
        	tie %tmpfold, $db_package, "$homedir/folders/$foldfile", O_RDONLY, 0660;
        	@msgs = split(':', $tmpfold{"messages"});
        	untie %tmpfold;
        	$ELocks->lock_remove(\%tmpfold);
        }

        foreach my $msg (@msgs) {
            $foldmsgs{$msg} = 1;
        }
    }

    # Get File List
    opendir DIRHAND, "$homedir/messages";
    foreach (readdir(DIRHAND)) {
        s/\n//;
        next if (/^\./);
        if ($foldmsgs{$_} != 1) {
            debug "message $_ not found in folders, deleting";
            unlink "$homedir/messages/$_";
        }
    }
    closedir DIRHAND;

    # Reconnect folderdb
    my $foldfile = $v{"folder"} || $inbox; 
    my $currfold = $foldfile;
    
    $foldfile = process_fold_type($foldfile);
    
    my $searchfold = $msg{"FOLD_Search_Results"} || "Search Results";
               
    # open folder. Be careful to check for valid tie. Don't open if doing Search
    if ($foldfile ne $searchfold) {
      open_folder_db($foldfile, 0);
    } 
       
    return 1;
}


sub del_msg_from_cache
{
    my $msg = shift;

    return unless $msg;
    return if ($msg =~ /^\./);

    del_from_local($msg, 1);

    debug "GOT RID OF EXTRA $msg";
    return 1;
}

sub save_state {
    # save current state into session file

#    return if ($query->param("passed") eq "restore_state");

    my @state = grep { /^state_/ } keys %v;
    foreach my $s (@state) {
        delete($v{$s});
    }

    if (!$query->param("passed") || $query->param("passed") eq "login_parse" ||
            $query->param("passed") eq "toggle_menu") {
        $v{"state_passed"} = "go_index";
    }
    else {
        $v{"state_passed"} = $query->param("passed");
    }
    $v{"state_variable"} = $query->param("variable");

    $v{"state_load_frameset"} = $query->param("load_frameset");

    my @x = grep { /\.x$/ } $query->param;

    foreach my $x (@x) {
debug "saving state_$x to ".$query->param($x);
        $v{"state_$x"} = $query->param($x);
    }
}


sub restore_state {
    my (@params,$params);

    $query->param(-name=>'folder', -value=>$v{"folder"}) if ($v{"folder"});
    $query->param(-name=>'passed', -value=>$v{"state_passed"}) if ($v{"state_passed"});
    $query->param(-name=>'variable', -value=>$v{"state_variable"}) if ($v{"state_variable"});

    $query->param(-name=>'load_frameset', -value=>$v{"load_frameset"}) if ($v{"load_frameset"});

    if ($v{"state_passed"} eq "multi") {
        $query->param(-name=>'reply_how', -value=>$v{"state_reply_how"}) if ($v{"state_reply_how"});
        $query->param(-name=>'display', -value=>$v{"state_display"}) if ($v{"state_display"});
        $query->param(-name=>'reply.x', -value=>$v{"state_reply.x"}) if ($v{"state_reply.x"});
        $query->param(-name=>'compose.x', -value=>$v{"state_compose.x"}) if ($v{"state_compose.x"});
        $query->param(-name=>'forward.x', -value=>$v{"state_forward.x"}) if ($v{"state_forward.x"});
        $query->param(-name=>'format.x', -value=>$v{"state_format.x"}) if ($v{"state_format.x"});
        $query->param(-name=>'display.x', -value=>$v{"state_display.x"}) if ($v{"state_display.x"});
        $query->param(-name=>'quick.x', -value=>$v{"state_quick.x"}) if ($v{"state_quick.x"});
    }

    if ($c{"custom_state"}) {
debug "restoring custom state";
        load_module("EMU::Custom");
        EMU::Custom::custom_state(\$query);
    }

debug "frameset? ".$query->param("load_frameset");
}


sub close_db
{
    delete $v{"SESSION_OPEN"};
    delete $v{"current_page"};
    delete $v{"mail_user"};
    delete $v{"mail_pass"};
    delete $v{"external"};
    delete $v{"wait_title"};
    delete $v{"wait_action"};
    delete $v{"wait_interval"};
    delete $v{"wait_count"};
    delete $v{"delay_max"};
    delete $v{"server_mapped"};
    delete $v{"new_user"};

    save_state();

    write_tmp("inline_html",0); 
    write_tmp("inline_html_value","");

    if (exists($v{"clean_tmp"})) {
        wildrm("$homedir/tmp", '^session\.|^rfc822|^SESSION|\.doc$|\.DOC$', 1);
        delete($v{"clean_tmp"});
    }

    # write out session vars
    debug "writing out session vars to $qs";
 	if ($qs && open (SESS, "> $homedir/tmp/$qs"))
 	{
     	while (my ($key, $val) = each %v)
     	{
 	        print SESS "$key = $val\n";
     	}
     	close SESS;
    }


    # unlock current folder
    my $foldfile = process_fold_type($folder);
#   debug "removing folder ($folder) lock  $homedir/folders/$foldfile.lok";
    my $foldlock = $ELocks->lock_search("$homedir/folders/$foldfile", 'path');
    debug "unlocking folder $foldfile via lock $foldlock";
    $ELocks->lock_remove($foldlock);
    
    write_tmp("have_messages", 0);
    untie %userdb;
    $ELocks->lock_remove(\%userdb);
    undef %userdb;
#   debug "closed userdb";

    untie %folderdb;
    $ELocks->lock_remove(\%folderdb);
#   debug "closed folderdb";

    untie %foldmap;
    $ELocks->lock_remove(\%foldmap);
#   debug "closed foldmap";

    if ($pop && $pop_connected) {
#        undef %poplist;
#        debug "quitting pop";
#        $pop->quit();
        undef $pop;
        $pop_connected = 0;
    }

#    debug "session protocol is ".$v{"protocol"};
    %v = () if (!bool($c{"disable_account_persistence"}) and
                !bool($c{"remote_only"}));

    $ELocks->lock_remove('LOCK');
    $ELocks->lock_remove('SESSIONLOCK');

    # grrr gave up trying to find exactly where sometimes we leave a lok
    # file around... so on close_db just clean those up
    load_module("File::Find",0,'find');
    my $subref = 
        sub { 
        	return if (! -f $File::Find::name ||  $File::Find::name !~ /\.loc?k$/);
              	unlink $File::Find::name if ($File::Find::name =~ /\.loc?k$/);
            };

    find(\&$subref, "$homedir/folders");

    $db_opened = 0;
    debug "DBS closed";
}



sub process_conversions {
    my ($no_db_version, $have_userdb) = @_;
    my @keys;

    # perform necessary conversions based on db_version

    debug "no_db_version: $no_db_version";
    my $converted_db = 0;
    my %tmpdb;
    my @files;
    my @folders_list = ();
    my $msgdata_file;

    debug "have_userdb $have_userdb";
    # is this a 2.7 conversion??
    if ($c{"convert2x_file_type"} ne "" && $no_db_version) {
        debug "checking for 2.x files...";

        load_module($c{"convert2x_file_type"});

        # take a look at the directory and check for signs of 2.x files
        opendir DIR, "$homedir";
        @files = grep ( !/^\./, readdir DIR);
        closedir DIR;
        my $do_folders=0;
        foreach (@files) {
            if (/^addrbook/) {
                debug "Found 2.x addressbook file, converting";
                convert2x_addrbook($_);
            }
            elsif (/^options/) {
                debug "Found 2.x options file, converting";
                convert2x_options($_);
            }
            elsif (/^filters/) {
                debug "Found 2.x filters file, converting";
                convert2x_filters($_);
            }
            elsif (/^msgdata/) {
                $do_folders = 1;
                $msgdata_file = $_;
            }
        }

        # do folders last
        if ($do_folders) {
            debug "Found 2.x msgdata, converting folders";
            convert2x_folders($msgdata_file);
        }

        $converted_db = 1;
    }

    # not a 2.7 conversion... check for 3.x
    # Let's try to convert db if
    # 1. no db_version established   OR
    # 2. we have a db_version but for some reason userdb seems unreadable
    elsif ( ($no_db_version && !exists($userdb{"db_version"}))  ||
            ($no_db_version == 0 && (!$tiehandle || $tiehandle eq undef)) ) {
        # this is legacy, don't even have a version... or it's not
        # legacy and have a different db type.

        debug "using the wrong db type" if (!$tiehandle || $tiehandle eq undef);

        debug "lets continue...";
        # convert db type?
        # Here we don't have an established db version yet, convert
        # db if an original_dbm type is indicated
        if ($have_userdb && 
                $c{"original_dbm"} && 
                $c{"original_dbm"} ne $db_package) {

            untie %userdb;

            my $userdbfile = $c{"orig_userdb"} || "userdb";
            debug "original userdb: ". -s "$homedir/$userdbfile";
            debug "converting userdb from original ".$c{"original_dbm"};
            debug "Error making userdb backup copy: $!"
                if (! copy("$homedir/$userdbfile", "$homedir/userdb.bak"));
            debug "userdb.bak: ". -s "$homedir/userdb.bak";

            tie %userdb, $db_package, "$homedir/newuserdb", O_CREAT|O_RDWR, 0660;
            debug "opened newuserdb";

            %tmpdb = ();
            # open userdb with original_dbm
            load_module($c{"original_dbm"});
            my $tieh = undef;
            $tieh = tie %tmpdb, $c{"original_dbm"}, "$homedir/$userdbfile", O_RDONLY, 0660;

            if (!$tieh || $tieh eq undef) {
                # something is wrong here!
                debug "unable to open original userdb with type ".$c{"original_dbm"};
                return;
            }

            debug "here 2; keys tmpdb ".scalar(keys %tmpdb);
            @folders_list = split('%%smoo1919', $tmpdb{"variable:folders"});
            debug "folders @folders_list";
            foreach (keys %tmpdb) {
               my ($k, $v) = ($_,$tmpdb{$_});
#               debug "Copying $k=>$v from tmpdb to userdb";
               $userdb{$k} = $v;
            }

            untie %tmpdb;
            untie %userdb;

            # move newuserdb to userdb
            move("$homedir/newuserdb", "$homedir/userdb");

            # re-establish tie to userdb
            tie %userdb, $db_package, "$homedir/userdb", O_CREAT|O_RDWR, 0660;
            debug "opened userdb";
            debug "keys in userdb: ".scalar(keys %userdb);

            $converted_db = 1;
        }

        # at a minimum convert to new folder style
        if ( scalar(@folders_list) >= 1 ) {
            convert_newfolders(@folders_list);
            $converted_db = 1;
        }

        # if we havent yet cleaned out msgs: from the db, do so now
        @keys = grep (/^msgs:/, (keys %userdb));
        foreach (@keys) {
            delete($userdb{$_});
        }

        $db_version = $EMU::DB_Version;
    }

    else {
        # ok we have a db_version... process according to the old version
        if ($db_version eq "3.5" || $userdb{"db_version"} eq "3.5") {
            debug "converting from 3.5...";
            create_foldmap();
            $db_version = $EMU::DB_Version;
            $converted_db = 1;
        }
        else {
            # any labelling > 3.5 and <= 4.0 ignored (no conversion) but
            # still update the DB_VERSION file
            update_db_version() if ($db_version ne $EMU::DB_Version);

            # do we need to do some cleanup maybe?
            if ($db_version eq $EMU::DB_Version && 
                    scalar(grep (/^msgs:/, (keys %userdb)) > 0) ) {

                debug "we have msgs keys, clean up. userdb size is ". -s "$homedir/userdb";
                tie %tmpdb, $db_package, "$homedir/newuserdb", O_CREAT|O_RDWR, 0660;
                %tmpdb = ();

                while (my($k,$v) = each %userdb) {
                    $tmpdb{$k} = $v if ($k !~ /^msgs:/);
                }

                untie %tmpdb;
                untie %userdb;
                undef %userdb;

                # move newuserdb to userdb
                move("$homedir/newuserdb", "$homedir/userdb");

                debug "userdb size is now ". -s "$homedir/userdb";
                # re-establish tie to userdb
                tie %userdb, $db_package, "$homedir/userdb", O_CREAT|O_RDWR, 0660;
                debug "opened userdb";
                debug "keys in userdb: ".scalar(keys %userdb);
            }
        }

    }

    # ok, we've done away with per-user mailloc configurations. This causes
    # too many problems. So if this user has options.mailloc set, we should
    # really copy his INBOX to a local folder "OLD_INBOX" so he doesnt risk
    # losing old mails
    if ($userdb{"options.mailloc"} && !$c{"convert2x_file_type"}) {
        move ("$homedir/folders/$inbox", "$homedir/folders/OLD_INBOX");
        $userdb{"folder:OLD_INBOX:protocol"} = "local";
        $userdb{"options.mailloc"} = 0;
    }

    debug "converted_db? $converted_db";

    if ($converted_db) {
        update_db_version();

        # also apply "new" default options
        set_default_compose();
        set_default_addresses();
        set_default_filters();
    }

    return $converted_db;
}


sub update_db_version {
    debug "updating DB_VERSION";
    open(DBV, ">$homedir/DB_VERSION");
    print DBV "$EMU::DB_Version\n";
    close DBV;
}


sub db_timeout {
    # wait for a while if there's a lock on the db file
    debug "hello. i'm deprecated method. please remove me."; return 0;
    
    my ($file,$nosuffix,$nowait) = @_;

    my $timeout = $c{"session_lock_timeout"} || 15;
    $file .= ".lok" unless ($nosuffix);

    $v{"wait_interval"} = 3;
    $v{"wait_count"} = 0;

    while (-e "$file" && $timeout > 0) {
        $v{"wait_action"} = $msg{"WAIT_DBLock"};
        debug "found a db lockfile ($file)! let's wait up to $timeout seconds";
        sleep 1;
        $timeout--;
        print_progress_new(1) unless ($nowait);
    }
}


sub open_folder_db {
	my ($foldfile,$restore_db) = @_;
	
	$db_package = $c{'dbm_isa'} || "GDBM_File";
	
	# create lock on folder
	my $foldhandle;
	my $foldexists = (-e "$homedir/folders/$foldfile");
	if ( $ELocks->lock_create("$homedir/folders/$foldfile", \%folderdb, {mode => 'write', nb => 1}) )
	{
		restore_db($db_package, "$homedir/folders/$foldfile") if ($restore_db);
		$foldhandle = tie %folderdb, $db_package, "$homedir/folders/$foldfile", O_CREAT|O_RDWR, 0660;
		debug "folder $homedir/folders/$foldfile is succ. opened.";
	}
	else
	{
		debug "ERR: failed to open folder $homedir/folders/$foldfile!";
	}
	#debug "$foldfile has ".scalar(split(':',$folderdb{"messages"}))." messages";
	
	if ($foldexists && $c{"original_dbm"} && $c{"original_dbm"} ne $db_package && !$foldhandle)
	{
		# oops! tie failed even though folder exists?
		debug "oh oh! can't open folder file $foldfile... let's try and convert folder";
		untie %folderdb;
		$ELocks->lock_remove(\%folderdb);
	
		copy("$homedir/folders/$foldfile", "$homedir/folders/$foldfile.bak");
		load_module($c{"original_dbm"});
		
		my %tmpdb;
		if ( $ELocks->lock_create("$homedir/folders/$foldfile", \%tmpdb, {mode => 'read', nb => 1}) )
		{
			my $tieh = tie %tmpdb, $c{"original_dbm"}, "$homedir/folders/$foldfile", O_RDONLY, 0660;
	
			# check if this tie worked...
			if ($tieh)
			{
	    			# ok, good. we're able to tie... now convert
				# debug "tie with $c{'original_dbm'} worked!";
				if ( $ELocks->lock_create("$homedir/folders/$foldfile.tmp", \%folderdb, {mode => 'write', nb => 1}) )
				{
	    				$foldhandle = tie %folderdb, $db_package, "$homedir/folders/$foldfile.tmp", O_CREAT|O_RDWR, 0660;
	    				while (my($k,$v) = each %tmpdb)
	    				{
		        			$folderdb{$k} = $v;
	    				}
	    			}
			
	    			untie %tmpdb;
	    			$ELocks->lock_remove(\%tmpdb);
	    			untie %folderdb;
	
	    			# now rename .tmp file and re-attach with $db_package
	    			copy("$homedir/folders/$foldfile.tmp", "$homedir/folders/$foldfile");
	    			$ELocks->lock_remove(\%folderdb);
	    			unlink "$homedir/folders/$foldfile.tmp";
	    			if ( $ELocks->lock_create("$homedir/folders/$foldfile", \%folderdb, {mode => 'write', nb => 1}) )
	    			{
	    				tie %folderdb, $db_package, "$homedir/folders/$foldfile", O_CREAT|O_RDWR, 0660;
	    			}
			}
			else
			{
	    			debug "ERROR: cannot process folder file $homedir/folders/$foldfile";
	    			# might as well delete the folder file, keep the backup, 
	    			# and create a new one
	    			unlink "$homedir/folders/$foldfile";
	    			$ELocks->lock_remove(\%folderdb);
	    			if ( $ELocks->lock_create("$homedir/folders/$foldfile", \%folderdb, {mode => 'write', nb => 1}) )
	    			{
	    				tie %folderdb, $db_package, "$homedir/folders/$foldfile", O_CREAT|O_RDWR, 0660;
	    			}
			}
		}
	}
	#    debug "opened folder |$homedir/folders/$foldfile|";
	#    debug "messages in $foldfile ". scalar(split(':', $folderdb{"messages"}));
}


sub restore_db {
	my ($db_package, $fname) = @_;
	my (%db,%tmpdb);
	
	debug "restoring db file $fname";
	if (	$ELocks->lock_create($fname, \%db, {mode => 'read', nb => 1}) &&
		$ELocks->lock_create("$fname.tmp", \%tmpdb, {mode => 'write', nb => 1}) )
	{
		tie %db, $db_package, $fname, O_CREAT|O_RDONLY, 0660;
		tie %tmpdb, $db_package, "$fname.tmp", O_CREAT|O_RDWR, 0660;
	
		foreach my $k (keys %db)
		{
			$tmpdb{$k} = $db{$k};
		}
	
		untie %db;
		untie %tmpdb;
		move("$fname.tmp", $fname);
		$ELocks->lock_remove(\%db);
		$ELocks->lock_remove(\%tmpdb);
	}
}


sub open_db
{
    my ($restore_db) = @_;

    my $converted_db = 0;

    # allow the user to override the DBM type (possibly adding their own which does neat special things)

    $db_package = $c{'dbm_isa'} || "GDBM_File";
    my ($flags);
    my $no_db_version = 0;

    debug "using $db_package";

    load_module($db_package);

#    debug "homedir=$homedir ";

    # check to see if we need to establish the homedir tree
    my $new_user = bool(! -e $homedir);
    my $setdefaults = create_dirtree();
    $new_user = 1 if (!$new_user && $setdefaults > 0 && !$c{"convert2x_file_type"});

    # before we do anything... check for lock file so we don't step on
    # any previous session
    # RB: this lock fails sometime \:
    return 0 unless $ELocks->lock_create("$homedir/LOCK", 'LOCK', {mode => 'write', nb => 1}, 1);

    debug "new_user ? $new_user";

    my $orig_db_version="";
    if (-e "$homedir/DB_VERSION") {
        open(DBV, "<$homedir/DB_VERSION");
        $db_version = <DBV>;
        $orig_db_version = $db_version;
        chomp($db_version);
        close DBV;
    }
    else {
        update_db_version();
        $no_db_version = 1;
    }

#    debug "db_version: $db_version";
    debug "EMU DB_Version: $EMU::DB_Version";

    my $userdbfile = $c{"orig_userdb"} || "userdb";
    debug "userdbfile $userdbfile";
    my $have_userdb = bool(-e "$homedir/$userdbfile");

    restore_db($db_package, "$homedir/$userdbfile") if ($restore_db);

    if ( $ELocks->lock_create("$homedir/$userdbfile", \%userdb, {mode => 'write', nb => 1}) )
    {
    	$tiehandle = tie %userdb, $db_package, "$homedir/$userdbfile", O_CREAT|O_RDWR, 0660;
    }
    else
    {
    	debug "can't lock userdb $homedir/$userdbfile: file is busy or error";
    }

    open_session_file() unless (exists($v{"SESSION_OPEN"}));

    my $prot = $userdb{"options.protocol"} || $v{"protocol"} || $protocol;
    $userdb{"options.protocol"} = $prot if ($prot && !$userdb{"options.protocol"});
#    debug "protocol ".$userdb{"options.protocol"};

    # only convert if there are files to convert
    $converted_db = process_conversions($no_db_version, $have_userdb)
        if (!$new_user && ($setdefaults == 0 || $no_db_version || 
                $orig_db_version ne $EMU::DB_Version));

    $userdb{"db_version"} = $db_version;

    # do we need to maybe recreate foldmap?
    my $nofoldmap = (-e "$homedir/foldmap") ? 0 : 1;

    if ($nofoldmap && !bool($c{"disable_account_persistence"})) {
        create_foldmap();
    }
    else {
    	if ( $ELocks->lock_create("$homedir/foldmap", \%foldmap, {mode => 'write', nb => 1}) )
    	{
        	tie %foldmap, $db_package, "$homedir/foldmap", O_CREAT|O_RDWR, 0660;
        }
        else
        {
        	debug "can't lock foldmap. $!";
        }
    }

    my $foldfile = $v{"folder"} || $inbox;
    my $currfold = $foldfile;
    $foldfile = process_fold_type($foldfile);

    my $searchfold = $msg{"FOLD_Search_Results"} || "Search Results";

    # open folder. Be careful to check for valid tie. Don't open if doing Search
    if ($foldfile ne $searchfold) {
    	debug "open folder $foldfile";
        open_folder_db($foldfile,$restore_db);
    }

    # HM 12/04/00 - Disable  per-user mailloc functionality.
    if ($c{force_mail_local} && $currfold eq $inbox && $protocol =~ /pop/i) {
       $mailloc = 1;
    } else {
       $mailloc = 0;
    }

    debug "mailloc is $mailloc. $currfold, ".bool($userdb{"options.mailloc"}).",".bool($c{"force_mail_local"});


    debug "setdefaults=$setdefaults converted_db=$converted_db";
    &set_default_options() if ($new_user || ($setdefaults && !$converted_db)); 

#    debug "BOOGA: $setdefaults, $converted_db";
    $db_opened = 1;

    if (bool($c{"implement_trash_folder"}) || $userdb{"options.use_trash_folder"}) {
        $trash_bin = 1;
        $trash_folder = $msg{"TRASH_Fold_Name"} || "TRASH";
    }
    else {
        $trash_bin = 0;
        $trash_folder = "";
    }

    $v{"new_user"} = 1 if ($new_user);
    return $no_db_version;
}

sub delete_in_db
{
    my ($table) = shift;

    debug "Attempting to del $table";
    
    $table =~ s/\[/\./;
    debug "$table";
    return map { delete $userdb{$_}; } (grep (/^$table/, (keys(%userdb))) );        
}


sub get_cookies {
    my $cookies = $ENV{"HTTP_COOKIE"};
    my @cookie_sets = split(/;/, $cookies);
    my ($user1, $host1, $noInfo, $timetag1, $timetag2, $name, $cookie, $type);

#    debug "HTTP_COOKIE:".$ENV{"HTTP_COOKIE"};

    %emu_cookies = ();
    foreach (@cookie_sets) {
        if (/emu_cookies=/) {
            $cookie = (split(/=/, $_))[1];
            ($user1, $host1, $qs, $noInfo, $timetag2, $type) = split(/\|\|/, $cookie);
            if ($timetag1 eq "" || $timetag2 > $timetag1) {
                $emu_cookies{"user"} = $user1;
                $emu_cookies{"host"} = $host1;
                $emu_cookies{"qs"} = $qs;
                $emu_cookies{"noInfo"} = $noInfo;
                $emu_cookies{"emu_type"} = $type;
                $timetag1 = $timetag2;
            }
        }
#        $emu_cookies{"qs"} = (split(/=/, $_))[1] 
#            if (/emu_session=/ && (!exists($emu_cookies{"qs"}) || 
#                                    $timetag2 > $timetag1));
    }

#    debug "cookies: user=$emu_cookies{'user'}  host=$emu_cookies{'host'} qs=$emu_cookies{'qs'} emu_type=$emu_cookies{'emu_type'}";
}


# login
#
# 07/27/98:
#  Combined the three login functions login(), login_menu() and
#  login_normal() into one. 
#
# /Jah
sub login
{
    my ($user, $host);

    get_cookies();

    # 08/28/98: allow the login page to be overriden
    if ($c{'redirect_login'} || $c{'perlsub_redirect_login'})
    {
	my ($redir);
	
	if ($c{'perlsub_redirect_login'})
	{
	    my ($sub) = $c{'perlsub_redirect_login'};
	    $sub =~ s/^\s*{// && $sub =~ s/\s*}\s*$//;
	    my ($subref) = eval("sub { $sub }");
	    $redir = &$subref($query);
#	    debug "From using perlsub_redirect, going to $redir";
	}

	$redir ||= $c{'redirect_login'};
	trim(\$redir);      
	print "Location: $redir\n\n";
	debug "redirecton is now going to $redir";
        return;
    }

    undef $emu_type;

    if ($c{detect_interface}) {
       foreach my $a ( grep(/^accept_/, keys %c) ) {
          my $v = $c{$a};
          $a =~ s/^accept_//;
           
          if ($ENV{HTTP_ACCEPT} =~ /\Q$v\E/) {
             $emu_type = $a;
             last;
          }
       }
    }

    $emu_type ||= $query->param('type') || $v{'emu_type'} || $emu_cookies{'emu_type'};

    if (! grep( $emu_type eq $_, split(/[\s,]+/, $c{ifaces})) ) {
       $emu_type = $c{'default_interface'} || "normal";
    }

    debug "EMU type: $emu_type";

    # check interface's existence.
    if (! -d "$page_root/iface/$emu_type") { $emu_type = $c{'default_interface'} }

    # If load appropriate lang and conf files.
    if ($emu_type ne $c{'default_interface'})
    {
	&load_lang("iface");
	&load_conf("iface");
    }

    $user = $query->param('user_name') || $emu_cookies{'user'};
    $host = $query->param('hostname') || $emu_cookies{'host'};

#    debug "param user_name ".$query->param('user_name');
#    debug "param hostname ".$query->param('hostname');
#    debug "1: user=$user  host=$host";

#    debug "noInfo is: ".$emu_cookies{"noInfo"};
#    debug "write_tmp: user $user";
    if ($emu_cookies{"noInfo"} == 1 || $user =~ /@/ || $host =~ /@/) {
        debug "user requested to not save user_name and hostname or garbage data";
        # make sure to blank out user_name and hostname
        write_tmp("user_name", "");
        write_tmp("hostname", "");
        write_tmp("emu_type", "");
    }
    else {
        write_tmp("user_name", $user);
        write_tmp("hostname", $host);
        write_tmp("emu_type", $emu_type);
    }

    if ($emu_cookies{"noInfo"} == 1) {
        write_tmp("noInfo", "CHECKED");
    }
    else {
        write_tmp("noInfo", "");
    }

    ($user, $host) = map_mailserver($user, $host);

    $user_name = "$user\@$host";
    debug "user_name $user_name";
    $user_name = "" if ($user_name eq "@");

    load_page("login.html");
}


sub checkpoint_pop {
    # This simply tries to solicit a response from the server... if any
    # meaningful response is received then at least the connection was
    # properly established.

    if (ref($pop) eq "EMU::POP3") {
        $pop->command('NOOP');
        my $resp = $pop->getline();
        debug "pop response: $resp";
        return ($resp =~ /ok/i || $resp =~ /err/i) ? 1 : undef;
    }

    $pop->cmd(" NOOP ");
    my $response = $pop->get_response();
    return $pop->interpret_response;
}



sub do_login_sequence {
    my ($proto,$user,$password,$host,@params) = @_;
    my ($success);

    $v{"mail_user"} = $user;
    $v{"mail_pass"} = $password;

    # If any alternates are configured, try those first
    my @mail_hosts = ($host);

    push (@mail_hosts, $pophost) if ($pophost && $pophost ne $host);
    push (@mail_hosts, split(' ', $c{"alternate_mail_hosts"}));

    # try protocol-specific hosts if we still don't have a connection
    push(@mail_hosts, "pop.$host")
        if (!$c{"dont_guess_mail_hosts"} && $proto =~ /pop/i);
    push(@mail_hosts, "imap.$host")
        if (!$c{"dont_guess_mail_hosts"} && $proto =~ /imap/i);
    push(@mail_hosts, "mail.$host") if (!$c{"dont_guess_mail_hosts"});

    my $valid_host = "";
    debug "will try these hosts: @mail_hosts";
    foreach $valid_host (@mail_hosts) {
        debug "attempting login sequence: $proto,$user,$valid_host";
        if ( $proto =~ /pop3/i ) {
            $success = do_pop_login($user,$password,$valid_host,$params[0]);

            if ($success) {
                $user = ${*$pop}{user};
                $pophost = ${*$pop}{host};
            }
        }
        else {
            # undef $pop so we can make a new object
            my $fold = $params[0] if $params[0];
            my $read_only = bool($params[1]);
            $success = (do_imap_login($user,$password,
                                      $valid_host,$fold,
                                      $read_only) eq undef) ? 0 : 1;
            debug "imap success $success host $valid_host";
        }

        if ($success) {
            debug "login validated, $user and $valid_host";
            $pophost = $valid_host;
            return (1,$pophost,$user);
        }

    }

    return (0,$pophost,$user) if ($c{"dont_guess_mail_hosts"});

    # Failed all normal attempts... let's try MX hosts then??

    $valid_host = try_mx_hosts($proto, $host);

    return (1,$valid_host,$user) if ($valid_host);

    return (0,$pophost,$user);
}


sub login_parse
{
    my ($user, $host, $flag) = @_;
    my ($error, $used, $p, $rebuild_home, @files) = ();
    my $flush_msgs = 0;
    my $purge = 0;
    my $do_uidl = 0;
    my $check_cache;

    my $force_pop3 = 0;
    my $force_imap = 0;
    my $restore_db = 0;
    my $no_db_version;
    my $validpop = "";
    my $success=0;
    my $save_user;

    $emu_type = $query->param('type') || $v{'emu_type'};

    if (! grep( $emu_type eq $_, split(/[\s,]+/, $c{ifaces})) ) {
       $emu_type = $c{'default_interface'} || "normal";
    }
                                       
    $rebuild_home	= 1 if ($flag =~ /rebuild$/i);
    $flush_msgs		= 1 if ($flag =~ /flush_msgs$/i);
    $purge 			= 1 if ($flag =~ /purge$/i);
    $force_pop3		= 1 if ($flag =~ /pop3$/i);
    $force_imap 	= 1 if ($flag =~ /imap$/i || $c{pure_imap});
    $restore_db 	= 1 if ($flag =~ /restore_db$/i);
    $check_cache 	= 1 if ($flag =~ /check_cache$/i);

#   debug "user_name $user_name";

    my ($u, $h) = split('@', $user_name, 2);

    $h = $h || $c{'default_pop'};
    $user_name = "$u\@$h";

    $homedir = getpath($user_name) unless $homedir; 
#   debug "homedir=$homedir";

    if ( !allowed_domain($host) )
    {
		write_tmp("login_error", convert($msg{'MSG_DomainDeniedAccess'}, $host));
		$password = undef;
		return login(1),0;
    }

    # Allow other stuff (like statistics or password changing to be configured by
    # the user in EMU::Custom

    my ($new_user, $new_host);

    if ($c{"pre_login_sub"})
    {
	load_module("EMU::Custom");
	debug "Evaling pre_login($user_name)";
	eval
	{
		($new_user, $new_host) = &EMU::Custom::pre_login($user_name);
            	debug "pre_login returned $new_user, $new_host";
	};
    }

    $user = $new_user if ($new_user);
    $pophost = $new_host if ($new_host);

    # First we have to consult the user's options to see what their protocol is.
    # When a user is logging in, we check with $c{'login_protocol'} to see
    # how we should be connecting to the server. This variable should contain
    # a comma separated list of the protocols to try (right now only imap and
    # pop).  We will try connecting to the server using the first protocol,
    # then if that fails try again with the second protocol. (if a second is
    # listed). If this variable isn't set then we use 'imap,pop'
    LOGIN_TO_SERVER:
    {
	my (@default, @prot, $priprot);

        @default = split( /\s+/, lc( $c{'login_protocol'} ) );
        debug "homedir $homedir";

        # if user doesnt exist yet, or we dont maintain local data,
        # default as if no data exists
        if ($c{'disable_account_persistence'} ||!-e $homedir || !-e "$homedir/userdb")
        {
	    	@prot = @default;
        }
        else
        {
            $no_db_version = open_db($restore_db) unless $db_opened;
            if ( !$userdb{"options.protocol"} )
            {
	        	@prot = @default;
            }
            else
            {
                if ( $userdb{"options.dont_try_other_protocols"} )
                {
                    @prot = ($userdb{"options.protocol"});
                }
                else
                {
                    @prot = ($userdb{"options.protocol"}, grep {!/$userdb{"options.protocol"}/} @default);
                }
            }
        }

	# gotta have some protocol
	@prot = ('imap', 'pop3') unless scalar @prot;

        # override protocol if requested on login
        @prot = ('pop3') if ($force_pop3);
        @prot = ('imap') if ($force_imap);

#       debug "will try these protocols: @prot  user default is ".$userdb{"options.protocol"};

	# note that we're setting the protocol in this loop
	my ($proto, $host); #for clarity #04/30/99 MM

      	PROTOCOL_LOOP:
        {
	    	foreach $proto (@prot)
	    	{
	                debug "prot $proto  pophost=$pophost";

        	        # if we have a saved pophost, (prior successful login) 
                	# then use it
                	if ( $userdb{"pophost"} )
                	{
                    		debug "using pophost from cache, " . $userdb{"pophost"};
#                   		$pophost = $userdb{"pophost"};
                    		$host = $userdb{"pophost"};
                	}
                	else
                	{
                    		# initialize $host to pophost
                    		$host = $pophost;
                	}

                	# try to login with this protocol
                	($success,$host,$user) = do_login_sequence($proto, 
                                                         $user, 
                                                         $password, 
                                                         $host, 0, 1);

                	if ($success)
                	{
                    		$protocol = $proto;
                    		$pophost = $host;
                    		$save_user = $user;
                    		debug "here, proto $proto user $user host $host";
                 	   	last PROTOCOL_LOOP ;
                	}

                	debug "failed attempt $pophost, $proto";
            	}
        }


        # exit loop once we've managed to connect
        if ($pop)
        {
            debug "connection ok, proto $protocol";
            $pop_connected = 1;
	    last LOGIN_TO_SERVER;
        }

#	why do we have this crap, if we have the code below? RB, 10-2003
# 	if we get here then we haven't been able to login!
#        debug "server connect failed" unless( $pop );
#
#	# HM 09/13/00 - Hrm, this is just so much cleaner
#	my @pieces = reverse split(/\./, $host);
#	
#	write_tmp("login_error",convert($msg{'ERR_FailedLogin'}, $u, @pieces));
#
#	debug "wrote: " .convert($msg{'ERR_FailedLogin'}, $u, @pieces);
#        debug "Pieces:",join(' ; ', @pieces);
#	$password = undef;
#	
#	login();
#	return;
    }

    # Hrm. Getting here indicates that we have successfully logged in 
    # valid_hostname sometimes leaves stale error messages. Lets clear that now;
    set_status('');
    debug "user=$user"; #  password=$password";

    if( $success != 1 )
    # we failed all attempts at logging in
    {
        # HM 09/13/00 - Hrm, this is just so much cleaner
        my @pieces = reverse split(/\./, $host);

	my $error_code;
	if( $pop )
	{
        	$error_code = convert( $msg{'MSG_LoginError'}, $pop->errcode );
        }
        else
        {
        	$error_code = convert( $msg{'ERR_FailedLogin'}, $u, @pieces);
	}
        debug "Failed login, errcode is ". $error_code;
        write_tmp("login_error", $error_code);
	$password = undef;

	TRACK_BAD_LOGINS:
	{
	    	if ( $c{"failed_login_counter"} ) 
	    	{
			my ($user) = $user_name;
			# Attempt to make sure they can't do bad stuff easily
			$user =~ s/\||\`//g;
			$user =~ s/^\.//g;
			$user = lc($user);
			trim(\$user);

			debug "FLC: $user";
		
			my $bads = 0;
			last unless $user;
					
			if ( -e "$page_root/tmp/bad$user" && $user )
			{
		    		open(BADLOG, "< $page_root/tmp/bad$user");
		    		$bads = <BADLOG>; chomp $bads;
		    		close BADLOG;
		    		debug "Have $bads login(s) already";
			}
			$bads++;
			open (BADLOGWRITE, "> $page_root/tmp/bad$user");
			print BADLOGWRITE $bads;
			close BADLOGWRITE;

			my ($max_bads) = $c{"failed_login_max"} || 6;

			if ($bads >= $max_bads)
			{
				debug "Too many bad logins ($bads), max bad logins is $max_bads";
		    		unless ($c{"failed_login_sub"})
		    		{
					my $url = $c{"failed_login_url"} || "badlogin.html";
		    			debug "Redirecting to failed_login_url $url";
					&redirect($url);
					return;
		    		}
	    			# Use custom sub
	    			debug "Calling custom routine bad_login";
		    		load_module("EMU::Custom");
	    			eval { &EMU::Custom::bad_login($user) };
			}
	    	}
	}

	login();
	return;
		
    }
    else
    {
        $initial_login = 1;
#       $delay = time;
    }

    #Reset Bad password counter
    if ($c{"failed_login_counter"}) 
    {
	my ($user) = $user_name;
	# Attempt to make sure they can't do bad stuff easily
	$user =~ s/\||\`//g;
	$user =~ s/^\.//g;
	$user = lc($user);
	trim(\$user);
	unlink "$page_root/tmp/bad$user";
    }

    # got here, so must have been successful login
    $do_uidl = 1;
    $firstlogin = 1;

    # successfull login, so delete any possibly pending LOCK files
    $ELocks->lock_remove('LOCK');
    debug "protocol is $protocol";
    $no_db_version = &open_db($restore_db) if (!$db_opened);

    $userdb{"pophost"} = $pophost;
    $userdb{"options.protocol"} = $v{"protocol"} = $protocol;
    debug "protocol is $protocol";

    # now the user has been authenticated and they're from an allowed
    # host. If they REALLY want to rebuild their home directory then
    # let them do it.
    if ($rebuild_home)
    {
	die "Content-type: text\/html\n\nNo Home Directory $!" unless $homedir; # eeks!
        close_db();
	deltree($homedir);
	set_status($msg{'MSG_RebuildComplete_S'});
	EMUerror($msg{'MSG_RebuildComplete_T'}, $msg{'MSG_RebuildComplete_B'}, 0);
	return;
    }

    unless ( $c{"disable_sessionID"} || $query->param("disable_sessionID") )
    {
        debug "session ID ".$query->param('sessionID');
        if ($query->param('first') && $query->param('sessionID') !~ /[0-9]+/)
        {
            my $errmsg = $msg{'ERR_ImproperLogin'} || "Improper Login sequence. Please refresh your login page and log in again.";
            set_status($errmsg);
            debug "Missing Session ID!";
            wildrm("$homedir/tmp", '^session\.');
            write_tmp("title", $status, 1);
            write_tmp("phrase", $status, 1);
            write_tmp("logintext", 1);
            load_page("errors.html");
            return;
        }
    }

    # we've connected to the server now! make sure that we save the protocol!
    debug "Saved PROTOCOL: $protocol";
    $userdb{"folder:$inbox:protocol"} = $userdb{"options.protocol"} = $protocol;
    
    # the login is validated, now make sure that all the correct files exist
    session_home();

    $qs = session_start($user_name);
    debug "qs is $qs";

    unless ($qs)
    {
        write_tmp("title", $status, 1);
        write_tmp("phrase", $status, 1);
        write_tmp("logintext", 1);
        load_page("errors.html");
        return;
    }

    if ($check_cache)
    {
        check_msg_cache();
        set_status($msg{'MSG_CacheCheck_S'});
        EMUerror($msg{'MSG_CacheCheck_T'}, $msg{'MSG_CacheCheck_B'}, 0);
        return;
    }
    
    if ($flush_msgs)
    {
	flush_msg_cache();
	set_status($msg{'MSG_FlushComplete_S'});
	EMUerror($msg{'MSG_FlushComplete_T'}, $msg{'MSG_FlushComplete_B'}, 0);
        return;
    }

    if ($purge)
    {
	deltree("$homedir/messages");
	deltree("$homedir/folders");
        unlink "$homedir/foldmap";
	set_status($msg{'MSG_PurgeComplete_S'});
	EMUerror($msg{'MSG_PurgeComplete_T'}, $msg{'MSG_PurgeComplete_B'}, 0);
        return;
    }

    $v{"last_folder"} = $folder;
    $v{"time"} = time if ( isActivity4Session() );
    
    # Clear folder caches
    $v{imap_fcache} = undef;
    $v{imap_sfcache} = undef;

    if ($c{force_msg_flush})
    {
        debug "Flushing message cache";
        flush_msg_cache();
    }
   
#   debug "$extra_head";
    #Setup folder info for INBOX
    $folderdb{"username"} = $userdb{"folder:$inbox:username"} = $save_user;
    debug "saved username: $save_user";
    $folderdb{"password"} = $userdb{"folder:$inbox:password"} = code($password);
    $folderdb{"hostname"} = $userdb{"folder:$inbox:hostname"} = $pophost;
    $v{"protocol"} = $folderdb{"protocol"} = $userdb{"folder:$inbox:protocol"} = $protocol;
    $v{"mailcheck_popup"} = $userdb{"options.mailcheck_popup"};

    COOKIES:
    {
	last COOKIES if ( $c{'disable_cookies'} );
	
	my ($type, $date, @date);
	$type = $query->param('type') || $c{'default_interface'};
	
	# 07/08/98: this date lowered from 922752e4 so that it doesn't overflow the
	# computer's date buffer (ooops!)
	# @date = split(' ', scalar(get_date( (time + 60*60*24*30),1))); # persist for a month use GMT time
	@date = split(' ', scalar(get_date( (time + 60*60*24*5),1,1))); # persist for 5 days use GMT time
	$date = sprintf("%s %s-%s-%s %s %s", @date);
	
	debug "new cookie expiration=$date";
	my ($user, $host) = map_mailserver($user, $host, undef, 1);
	my $path = $c{'cookie_path'} || "/";
        my $cookie_domain;
	$cookie_domain = "; Domain=" . $c{'cookie_domain'} if ( $c{'cookie_domain'} );
        
        # check for request to not redisplay user/mailhost
        debug "noInfo: ".$query->param('noInfo');
        my $noInfo = $query->param('noInfo') ? "1" : "0";

        write_tmp("noInfo", $noInfo ? "CHECKED":"");
        # create one cookie string
        my $cookie_string = "$user\|\|$host\|\|$qs\|\|$noInfo\|\|".time."\|\|$emu_type";

	debug "cookie_string: $cookie_string";
        # 05/15/98: print cookies always
        $extra_head  = "Set-Cookie: emu_cookies=$cookie_string; Path=$path$cookie_domain\r\n";
    }

    # If enabled, log the user into Calendar
    CalendarLogin($user_name) if ( $c{cal_path} );
    
    #Allow other stuff (like statistics or password changing to be 
    # configured by the administrator in EMU::Custom
    my $success_login_status = 0;

    # On a login, force a refresh of quota from db. This allows for 
    # quota changes to be reflected.
    delete($userdb{"quota"})
        if ($c{"quota_source"} =~ /custom/i && $query->param('first'));

    if ($c{"success_login_sub"})
    {
		load_module("EMU::Custom");
		debug "Calling success_login($user_name)";
        $success_login_status = &EMU::Custom::success_login($user_name);
        debug "status $success_login_status";
    }

	debug "extra_head: $extra_head";
    # we allow EMU::Custom::sucess_login to return a failure condition
    # which would indicate "don't go on". Normally, success_login won't
    # return a value so we would continue on from here
    if ($success_login_status == -1)
    {
        $v{"success_login_failed"} = 1;
        return;
    }
    
    debug "do_uidl $do_uidl";
    if ( (ref($pop) eq "EMU::POP3") && $do_uidl && $pop )
    {
        my $uids = $pop->uidl;
        if ( !$uids )
        {
            $folderdb{"nouidl"} = 1;
            
        } else {
            debug "getting uids...";
            undef %poplist;
            %poplist = %{$uids} if $uids;
            debug "there are " . scalar(keys %poplist)." uids";
            $folderdb{"nouidl"} = 0;
        }
    }
    
    # Ensure a valid skin
    if ( !$userdb{'options.skin'} || $c{skins} !~ /$userdb{'options.skin'}/ )
    {
        $userdb{'options.skin'} = $c{default_skin} || 'EMU_Original';
    }

    # Jah: 11/26/98. Allow us to go to different parts of emumail
    # through a url
    if ( my $next = $query->param('next') )
    {
		$query->param('next','');
		jump($next);
    } else {
		jump('go_index', 1);
    }

    unless ( $userdb{"options.save_outbox"} )
    {
        $userdb{"options.save_outbox"} = ($c{'save_outbox'}) ? bool($c{'save_outbox'}) : 1;
    }
    debug "save_outbox: " . $userdb{"options.save_outbox"};

    # enable voice by default :
    if ( !defined($userdb{'options.user_voice_enabled'}) && $c{'site_voice_enabled'} )
    {
		$userdb{'options.user_voice_enabled'} = 1;
		debug("set user default preference for voice = 1");
    }
}

sub dump_file
{
    my ($filename, $blksize) = @_;
    my $block;

    $blksize ||= 5120;
    
    open(IN, "<$filename") || debug "Couldn't open file $filename: $!";

    # binmode  IN;

    while (read(IN, $block, $blksize))
    {
	print $block;
    }
    close IN;
}

sub folders
{
    my $r;
    my $prot;
    my ($selected);

    ($r, $passed) = split('=', $v{"returnto"}, 2);
    if (!$r)
    {
	$r = "go_index";
	$v{"returnto"} = $r;
    }

    $selected = get_var("folder_selected") || $folder;

    debug "selected is $selected";

    # 08/05/98: make the local folder checked if none other are checked
    write_tmp("proto", get_var("proto"));
    write_tmp("folder_selected", $selected);

#    write_tmp("local_checked", "CHECKED") unless  (get_var("pop_checked") || get_var("imap_checked")
#                                                  || get_var("local_checked") );

    my ($total_msgs, $unread_msgs, $read_msgs, $answered_msgs);

    if ($selected eq $folder) {
        ($total_msgs, $unread_msgs, $read_msgs, $answered_msgs) = get_curr_folder_msginfo();
    }
    else {
        ($total_msgs, $unread_msgs, $read_msgs, $answered_msgs) = get_folder_msginfo($selected, 1);
    }

    write_tmp("total_msgs",$total_msgs||0);
    write_tmp("unread_msgs", $unread_msgs||0);
    write_tmp("read_msgs", $read_msgs||0);
    write_tmp("answered_msgs", $answered_msgs||0);

    if ($v{'editfolder'})
    {
	write_tmp("showcount", 1);
    }


    load_page("folder.html");
}

sub get_signature
{
    my ($signature);
    
    $signature = $userdb{"options.signature"};
    
    return ($signature);
}

sub options
{
    my ($r, $real_name, $email, $passed,%options,$signature, $autoload);
    my ($maillocal,$checkmail,$mailcheck_popup,$counter,$i, $checked, $organization, $max_messages);
    my ($countersave,$prefix,$synchronize,$user_voice_enabled);
    my ($show_html, $no_html_images, $real_time_filter, $manual_filtering, $full_header, $quoted_reply, $show_folder_stats);    
	my ($filter_spam, $filter_spam_folder);

    quota_check(1);
    my $used = $v{"quota_used"};
  
    # 8/25/98: add support for forwarding.
    my ($forward);
    if (!$c{'disable_forwarding'})
    {
	my ($file);
	my ($user,$host) = split(/@/,$user_name);

	if ($c{'perlsub_forward_file'})
	{
            $file = do_perlsub($c{'perlsub_forward_path'},$user).$c{'forward_file'};
	    debug "found file = $file";
	}
	else
	{
	    $file = "$homedir/tmp/". $c{'forward_file'};
	}

	debug "forward file=$file";

	# only if it exists
	if (-e $file)
	{
            if (bool($c{'forward_file_multiple_aliases'})) {
                open (FWD, "$file");
                my @aliases = <FWD>;
                close FWD;

                $forward = grep { /^$user:/ } @aliases;
                $forward =~ s/^$user://;
            }
            else {
	        my $fh = new IO::File "<$file";
	        chomp($forward = $fh->getline);
	        debug "file exists. forward=$forward";
	        $fh->close;
	    }
        }
    }

    # 07/24/98: gotta keep track of the primary protocol used to connect with
    my ($pri_protocol);

    if ($over_quota)
    {
	set_status(convert($msg{'ERR_QuotaExceeded_T'},
                           $v{"quota_allowed"},
                           $c{'help_url'}));
    }

    $prefix       = $userdb{"options.prefix"};
    $real_name    = $userdb{"options.real_name"};
    $email        = $userdb{"options.email"} || $user_name;
    $signature    = $userdb{"options.signature"};
    $maillocal    = bool($c{"force_mail_local"});
    $synchronize  = bool($userdb{"options.DontsynchronizePOP"});
    $checkmail    = $userdb{"options.checkmail"} || 7200;
    
    $mailcheck_popup = bool($userdb{"options.mailcheck_popup"});

    $autoload     = $userdb{"options.autoload"};
    $organization = $userdb{"options.organization"};
    $pri_protocol = is_set($c{'force_protocol'}) ? $c{'force_protocol'} : $userdb{"options.protocol"};
    $max_messages = $userdb{"options.max_messages"};

    $real_time_filter = $userdb{"options.do_realtime_filter"};
    $manual_filtering = $userdb{"options.manual_filtering"};
    $show_html = $userdb{"options.show_html"};
    $no_html_images = $userdb{"options.no_html_images"};

    $quoted_reply = $userdb{"options.quoted_reply"};
	$filter_spam = $userdb{"options.filter_spam"};
	$filter_spam_folder = $userdb{"options.filter_spam_folder"};

    # For upgrades we need to default quoted reply to on
    if (!defined($quoted_reply)) {
        $quoted_reply = 1;
    }

    $full_header = $userdb{"options.full_header"};

    $user_voice_enabled = $userdb{"options.user_voice_enabled"};
    debug("user_voice_enabled = " . $userdb{'options.user_voice_enabled'});

    ($r,$passed) = split(/=/, $v{"returnto"});
    $r = "go_index" unless $r;

    debug "autoload is $autoload";
    $autoload = 1 if ($autoload eq undef); # default to autoload

    debug "pri_protocol=$pri_protocol";

    # make sure that a protocol is highlighted on default

    $counter = $userdb{"filters.total"};
    $countersave = ++$counter;

    write_tmp("synchronize", $synchronize);
    write_tmp("user_voice_enabled", $user_voice_enabled);
    write_tmp("mailloc", $maillocal);
    write_tmp("prefix", $prefix);
    write_tmp("autoload", $autoload);
    write_tmp("countersave", $countersave, 1);
    write_tmp("protocol", $pri_protocol);
    write_tmp("max_messages", $max_messages, 1);
    write_tmp("checkmail", $checkmail, 1);
    write_tmp("mailcheck_popup", $mailcheck_popup, 1);
    write_tmp("email", $email, 1);
    write_tmp("real_name", $real_name || "", 1);
    write_tmp("signature", $signature || "");
    write_tmp("sigwap", safe_html($signature) || "") if ($licensed{"wap"});
    write_tmp("organization", $organization || "", 1);
    write_tmp("quota_used", commas($used), 1);
    write_tmp("forward", $forward);
#    write_tmp("show_folder_stats", $show_folder_stats, 1);
#    my ($q) = &get_quota(split(/\@/,$user_name));
    write_tmp("quota_allowed", $v{"quota_allowed"} ? commas($v{"quota_allowed"}) : 0, 1);
    write_tmp("status", $status, 1);
    write_tmp("disable_forwarding", $c{"disable_forwarding"}, 1);
    write_tmp("show_html", $show_html, 1);
    write_tmp("no_html_images", $no_html_images, 1);
    write_tmp("do_realtime_filter", $real_time_filter, 1);
    write_tmp("manual_filtering", $manual_filtering, 1);
    write_tmp("filter_spam", $filter_spam, 1);
    write_tmp("filter_spam_folder", $filter_spam_folder, 1);
    write_tmp("quoted_reply", $quoted_reply, 1);
    write_tmp("full_header", $full_header, 1);

    print_header(undef, 0, 1);

    load_page("options.html");
} # options()

sub print_emufiles
{
    my ($show_msgs) = shift;    # whether or not to print postponed messages as well
    my(@files, %heldmsgs);
    
    opendir DIR, "$homedir/files";
    @files = grep ( !/^\./, readdir DIR);
    closedir DIR;
    
    # map the filenames correctly
    map {
	if ($show_msgs && /^[0-9a-f]{32}$/i)
	{
	    $_ .= substr(":" . get_heldmsg_name($_, $userdb{"postponed.$_"}), 0, 25);
	}
	$_;
    } @files;
    
#    dbmclose(%userdb);
    
    @files = sort @files;
    foreach (@files)
    {
	if (/^([0-9a-f]{32}):(.*)/i)
	{
	    print qq{   <OPTION VALUE="$1">$2\n};
	    next;
	}
	print qq{   <OPTION VALUE="$_">}, substr($_, 0, 30), "\n";
    }
    
    if (@files == 0)
    {
	print qq{   <OPTION VALUE="">\n};
    }
    
    print qq{   <OPTION VALUE="">$msg{'MSG_SystemFiles'}\n};
    
    opendir DIR, $SYSFILEDIR;
    @files = grep (!/^\./, readdir DIR);
    closedir DIR;
    
    foreach (@files)
    {
	print qq{    <OPTION VALUE="sys0:$_">}, substr($_, 0, 30), "\n";
    }


    if ($SYSXTRADIR)
    {
	opendir DIR, $SYSXTRADIR;
	@files = grep (!/^\./, readdir DIR);
	closedir DIR;
	
	foreach (@files)
	{
	    print qq{    <OPTION VALUE="sys1:$_">}, substr($_, 0, 30), "\n";
	}
    }
}


sub print_attachs {
    my $html = "";
    my $selected = "";
    my @attachs = split(' ', get_var("here_atts"));

    
    if (!@attachs) {
        @attachs = ($msg{"MSG_ATTFileNone"});
    }
    else {
        @attachs = ($msg{"MSG_ATTSelDel"}, @attachs);
    }

    debug "attachments (".scalar(@attachs)." are @attachs, ". get_var("here_atts");

    $html .= "<SELECT name=\"which_att\" width=15>\n";
    foreach (@attachs) {
        # Always default SelDel to selected
        $selected = ($_ eq $msg{"MSG_ATTSelDel"}) ? "SELECTED" : "";
        $html .= "<OPTION value=\"$_\" $selected>$_</OPTION>\n";
    }
    $html .= "</SELECT>\n";
    return $html;
}


sub print_filters
{
    my ($i, $counter);
    my $isRegex;
    my ($type, $action);

    $counter = $userdb{"filters.total"} + 1;
    debug "counter is $counter";
    
#    my @filtertype = grep (!/$msg{'V_FilterDefaultType'}/, 
    my @filtertype = ($msg{'V_FilterNameOff'}, $msg{'V_FilterNameTo'},
	    $msg{'V_FilterNameFrom'}, $msg{'V_FilterNameSubject'},
	    $msg{'V_FilterNameBody'}, $msg{'V_FilterNameAny'},
	    $msg{'V_FilterNameHeader'}, $msg{'V_FilterNameDelete'});

    my %filtervals = ();
    $filtervals{$msg{'V_FilterNameOff'}} = FILTER_OFF;
    $filtervals{$msg{'V_FilterNameTo'}} = FILTER_TO;
    $filtervals{$msg{'V_FilterNameFrom'}} = FILTER_FROM;
    $filtervals{$msg{'V_FilterNameSubject'}} = FILTER_SUBJ;
    $filtervals{$msg{'V_FilterNameHeader'}} = FILTER_HEAD;
    $filtervals{$msg{'V_FilterNameBody'}} = FILTER_BODY;
    $filtervals{$msg{'V_FilterNameAny'}} = FILTER_ANY;
    $filtervals{$msg{'V_FilterNameDelete'}} = FILTER_DELETE;

    my $folders;

    for ($i = 1; $counter > 0; $i++, $counter--)
    {
	$type   = $userdb{"filters.type$i"};
	$action = $userdb{"filters.action$i"};

        debug "type $type  aciton $action";
#        $userdb{"filters.type$i"}   ||= $msg{'V_FilterDefaultType'};
#        $userdb{"filters.action$i"} ||= $msg{'V_FilterDefaultAction'};

	# 07/26/98:
	# if the filter type isn't gonna be the default type then we need to add the default type to the list
#	if ($userdb{"filters.type$i"} != FILTER_OFF) # $msg{'V_FilterDefaultType'})
#	{
#	    push(@filtertype, filter_name(FILTER_OFF)); #grep(!/$msg{'V_FilterDefaultType'}/, @filtertype);
#	}

	# If type
	my $name = filter_name($type);
	print qq{ <TR>\n};
	print qq{  <TD>$FONT_IND\n};
	print qq{   <SELECT NAME="type$i">\n};
	print "    <OPTION SELECTED VALUE=$filtervals{$name}>$name\n";

	# 07/23/98: print out the filter options. Allow user to configure the text
	for (@filtertype)
	{
	    # skip the ones that are blank
	    next if (/^(?:\s*|$name)$/);
	    print "    <OPTION VALUE=$filtervals{$_}>$_\n";
	}

	print qq{   </SELECT>\n};
	print qq{  </FONT></TD>\n};
	
	# Modifier
      MODIFIER:
	{
	    my($s1, $s2);

	    if ($userdb{"filters.modifier$i"} == FILTER_CONTAINS)
	    {
		$s1 = "SELECTED";
	    }
	    else
	    {
		$s2 = "SELECTED";
	    }

	    print qq{  <TD>$FONT_IND\n};
	    print qq{   <SELECT NAME="modifier$i">\n};
	    print "    <OPTION $s1 VALUE=", FILTER_CONTAINS, ">$msg{'V_FilterContains'}\n";
	    print "    <OPTION $s2 VALUE=", FILTER_DEVOID, ">$msg{'V_FilterNoContains'}\n";
	    print qq{   </SELECT>\n};
	    print qq{  </FONT></TD>\n};
	}

	# Data
	print qq{  <TD>$FONT_IND <INPUT NAME="data$i" value=\"}, $userdb{"filters.data$i"}, qq{\"> </FONT></TD>\n};
	
	# Action
	print qq{  <TD>$FONT_IND\n};
	
	print qq{   <SELECT NAME="action$i">\n};

#	print_folders($userdb{"filters.action$i"}, $msg{'V_FilterMoveto'} . " ", "<OPTION>$msg{V_FilterMoveto} $msg{V_FilterTrash}");
        $folders = print_folders($userdb{"filters.action$i"}, $msg{'V_FilterMoveto'} . " ");
        print $folders;
        debug "$folders";

        # If FilterTrash hasn't been printed, do it...
        if ($folders !~ /$msg{'V_FilterTrash'}/) {
            print qq{   <OPTION };
            if ($folders !~ /SELECTED/) {
                print qq{ SELECTED };
            }
            print qq{ VALUE=$msg{'V_FilterTrash'}>$msg{'V_FilterMoveto'} $msg{'V_FilterTrash'}\n};
        }

	print qq{   </SELECT>\n};
        debug "FilterTrash is $msg{'V_FilterTrash'}";

	$isRegex = $userdb{"filters.bRegex$i"} ? "CHECKED" : "";

	print qq{  </FONT></TD>\n};
	print qq{ <TD ALIGN=CENTER VALIGN=MIDDLE>$FONT_IND <INPUT TYPE=CHECKBOX NAME=bRegex$i VALUE=1 $isRegex></TD>\n};
	print qq{ </TR>\n};
    }
}

sub get_folders_imap_nodes
{
    # Do some Sanity Checks: do we have an IMAP object?

    if (ref($pop) ne "EMU::IMAP")
    {
	my ($u,$p,$host) = get_folder_credentials($inbox);
        if ($u=~/@/)
	{
            my ($uu,$h) = split(/\@/,$u);
            $u = $uu if (!exists($c{"appendhost_$h"}));
	}

        unless ((do_login_sequence("imap",$u,$p,$host))[0]) {
#        unless (&make_imap_object($host,$u,$p)) {
	    debug "ERROR '$u' '$host' '$p'";
            return "";
        }
    }

    my ($imap_prefix) = $userdb{'options.prefix'} || $c{'default_imap_prefix'};
    $imap_prefix =~ s/\/+$//g;

    debug "Getting folders from IMAP server...with prefix: $imap_prefix";

    my (@folders) = $pop->list_folders_nodes();
#    my (@f);
#    map { push(@f) if ($_) } @folders;

    if ($imap_prefix)
    {
	#remove mail/, "'s, etc...
	map { s/^"*$imap_prefix.(.*)/$1/; s/"*$//; } @folders;
    }

    map { s/\n|\r//g } @folders; #remove lf's

    return (@folders);
}

sub get_folders_imap
{
    my ($force) = @_;

    # No IMAP object? Use the cache (unless forced)
    if (!$force) {
       my $fc = &get_imap_fcache();
       return @$fc if ref $fc;
    } else {
       debug "Forcing folder retrieval!";
    }

    # Do some Sanity Checks: do we have an IMAP object?

    if (ref($pop) ne "EMU::IMAP")
    {
	my ($u,$p,$host) = get_folder_credentials($inbox);
        debug "no imap object? $u $p $host";
        if ($u=~/@/)
	{
            my ($uu,$h) = split(/\@/,$u);
            $u = $uu if (!exists($c{"appendhost_$h"}));
	}
        unless (&do_imap_login($u, $p, $host, $inbox,1)) {
	    debug "ERROR '$u' '$host' '$p'";
            return "";
        }
    }

    my ($imap_prefix) = get_outbox_prefix();

    debug "Getting folders from IMAP server...with prefix: $imap_prefix";

    # Is the current folder external & imap? If so, need to get new imap object
    debug "external ".$userdb{"folder:$folder:external"}." and prot ". $userdb{"folder:$folder:protocol"}." for $folder";
    if ($userdb{"folder:$folder:external"} == 1 && $userdb{"folder:$folder:protocol"} eq "imap") {
	my ($u,$p,$host) = get_folder_credentials($inbox);
        ($u, $host) = map_mailserver($u, $host, $inbox);
        undef $pop;
        do_login_sequence("imap",$u,$p,$host);
#        make_imap_object($host,$u,$p);

        # change prefix because we're looking at another folder
        $imap_prefix = (defined $userdb{"options.prefix"})?$userdb{"options.prefix"}:$c{"default_imap_prefix"};
    }

    # Only append the delimiter if the imap prefix exists.
    my $base = $imap_prefix.&get_imap_delimiter if ($imap_prefix);
    my @folders = $pop->list_folders($base);

    debug "base path '$base' produced folders: @folders";

    # If folders were not found, either the prefix was bad or there just aren't any folders.
    # If the prefix is blank, the prefix cannot be bad.
    if ($imap_prefix && !@folders) {
       # Check to see if the prefix directory was found
       if (!grep { $_ eq $base } @{ $pop->{dirs} }) {
          debug "Creating prefix folder '$imap_prefix'";
          # Since the directory was not found, we should make it
          $pop->create_folder($base);
       }
    }

    

    my (%folders, @f);
    foreach my $f (@folders) {
       $f =~ s/\n|\r//g;            # Remove newlines
       $f =~ s/^"(.*)"$/$1/;        # Remove quotes
       $f =~ s/^$base// if ($base); # Remove prefix
       if (!$folders{$f}) {
          push(@f, $f);
          $folders{$f} = 1;         # Don't store duplicates
          $userdb{"folder:$f:protocol"} = 'imap'; # Force protocol
       }
    }
    
    # Folder cache
    &set_imap_fcache(@f);
    
    return @f;
}

sub get_imap_fcache
{
   debug "Getting folders from fcache! fcache: $v{imap_fcache}";
   if (my $fc = $v{imap_fcache}) {
      my $fcache = eval($fc);
      return $fcache if ref $fcache;
   }
   
   return;
}

sub set_imap_fcache
{
   my @fcache = @_;
   
   debug "Setting fcache to: @fcache";
   
   local $Data::Dumper::Terse = 1;
   local $Data::Dumper::Indent = 0;

   $v{imap_fcache} = Dumper(\@fcache);
}

sub flush_imap_fcache
{
   delete($v{imap_fcache});
}

sub addto_imap_fcache
{
   my ($f) = @_;
   my $fc = get_imap_fcache;

   debug "Adding folder '$f' to imap fcache";
   
   # This is needed for folder_exists to operate correctly.
   $checked_existence{$f} = 1;

   if (ref $fc) {
      push (@$fc, $f);
      &set_imap_fcache(@$fc);
      return 1;
   } else {
      # No fcache, don't want to create one. This is not really a problem.
      return 0;
   }
}

sub delfrom_imap_fcache
{
   my ($f) = @_;
   my $fc = get_imap_fcache;
   
   debug "Removing folder '$f' from imap fcache";
   
   if (ref $fc) {
      my @newfc = grep { $_ ne $f  } @$fc;
      &set_imap_fcache(@newfc);
      return 1;
   } else {
      # No fcache, don't want to create one. This is not really a problem.
      return 0;
   }
}

## MM: 12/14/98
#
# Trying to abstract how we get folder info
sub get_folders
{
    my (@f,@local_fold,@temp) = ();
    my (@imap, %imap, @local, @external);
    debug "get folders with $protocol !";

    #Always make INBOX show up, as first folder
    push(@f, $inbox);

    #Get IMAP Folders from Cache
    if ( ($protocol =~ /imap/i) || ($c{"pure_imap"}) )
    {
        map { push(@imap, $_) if (!/^inbox$/i && $_ ne ""); } get_folders_imap();
        map { $imap{$_} = 1; } @imap;
    }

    # get local folders
    if (opendir(FOLD, "$homedir/folders")) {
        my @tmpf;  
        push(@tmpf, grep { !/^\.|\.loc?k$/i } readdir(FOLD));
        closedir FOLD;
        foreach my $f (@tmpf) {
            push (@local, $f) if (!exists($imap{$f}) && $f ne $inbox);
        }
    }

    # Let's get external account folders (POP/IMAP)
    if (opendir(FOLD, "$homedir/folders/.external")) {
        push(@external, grep { !/^\.|\.loc?k$/ } readdir(FOLD));
        closedir FOLD;
    }

    my @tmpf;
    push (@tmpf, @imap) if (scalar(@imap) >= 1);
    push (@tmpf, @local) if (scalar(@local) >= 1);
    push (@tmpf, @external) if (scalar(@external) >= 1);

    #Neaten it up
    @tmpf = sort { lc($a) cmp lc($b) } @tmpf;

    push(@f, @tmpf);
    debug "folders @f";

    return (@f);
}

 
# HM 09/21/00
# Subscribed folders are the results of an LSUB instead of a LIST to the
# IMAP server. However, since IMAP folders and Local folders must exist side
# by side in Emumail, we also have subscribable Local folders.
# All of these folders return arrays (versus arrayrefs) to maintain
# consistancy with existing functions.
sub get_subscribed_folders
{
   debug "Getting subscribed folders!";

   my @folders = &get_subscribed_local;

   if ($userdb{"folder:$inbox:protocol"} eq 'imap') {
      push(@folders, &get_subscribed_imap);
   }

   # We are not going to sort folders at this point, because sorting is
   # something that largely depends on the usage of this data. So, why waste
   # time now, when we may need to resort later?
   return @folders;
}

sub get_subscribed_imap
{
   my ($force) = @_;
   my @folders;
   
   if (!$force) {
      my $folders = &get_session_obj('imap_sfcache');
      if (ref $folders) {
         @folders = @{ $folders };
         debug "Found sfcache ($folders): @folders";
         return @folders;
      }
   }

   my ($u,$p,$host) = get_folder_credentials($inbox);
   if ($u=~/@/) {
      my ($uu,$h) = split(/\@/,$u);
      $u = $uu if (!exists($c{"appendhost_$h"}));
   }

   if (ref $pop ne "EMU::IMAP" || $pop->{user} ne $u || $pop->{host} ne $host) {
      if (!&do_imap_login($u, $p, $host, $inbox,1)) {
         debug "Failed imap login with info - u: $u ; host: $host ; ;";
         return;
      }
   }
   
   # Only append the delimiter if the imap prefix exists.
   my $base = &get_outbox_prefix($inbox);
   $base .= &get_imap_delimiter if ($base);

   debug "Getting subscribed imap folders for base '$base'";

   my %folders;
   foreach my $f ($pop->list_subscribed_folders($base)) {
      if (check_imap_folder_existence($f)) {
         $f =~ s/^$base//;
         if (!$folders{$f}) {
            push(@folders, $f);
            $folders{$f} = 1;
         }
      } else {
         # Unsubscribe non-existant folders
         $pop->unsubscribe_folder($f);
      }
   }
   
   # Update the subscribed folder cache
   debug "Setting the sfcache to: @folders";
   &set_session_obj('imap_sfcache', \@folders);
   
   return @folders;
}
 
sub get_subscribed_local
{
   my @folders;
   foreach my $f (&get_folders_local) {
      if (exists($userdb{"folder:$f:subscribed"})) {
         push(@folders, $f) if $userdb{"folder:$f:subscribed"};
      } else {
         # Default pre-subscription folders to subscribed
         $userdb{"folder:$f:subscribed"} = 1;
         push(@folders, $f);
      }
   }
   return @folders;
}

sub get_folders_local
{
   my @folders;

   # get local folders
   if (opendir(FOLD, "$homedir/folders")) {
      foreach my $f (readdir(FOLD)) {
         next if ($f eq $inbox || $f =~ /^\.|\.loc?k$/i);
         push (@folders, $f);
      }
      closedir FOLD;
   }   
   
   return @folders;
}

sub get_folders_external
{
   my @folders;

   # Let's get external account folders (POP/IMAP)
   if (opendir(FOLD, "$homedir/folders/.external")) {
      push(@folders, grep { !/^\.|\.loc?k$/ } readdir(FOLD));
      closedir FOLD;
   }
   
   return @folders;
}
                                                     
sub set_folder_subscription
{
   my ($fold, $value) = @_;

   debug "Setting Folder subscription of '$fold' to '$value'";   
   my $prot = &get_folder_protocol($fold);
   
   if ($prot eq 'imap') {
      return &set_folder_subscription_imap($fold, $value);
   } 
   elsif ($prot eq 'local' || $prot eq 'pop3') {
      return &set_folder_subscription_local($fold, $value);
   } else {
     debug "Error, unknown protocol of '$prot' for folder '$fold'";
     set_status("Folder '$fold' has an invalid protocol");
     return 0;
  }
}

sub set_folder_subscription_imap
{
   my ($fold, $value) = @_;

   if (ref $pop ne "EMU::IMAP") {
      my ($u,$p,$host) = get_folder_credentials($inbox);
      if ($u=~/@/) {
         my ($uu,$h) = split(/\@/,$u);
         $u = $uu if (!exists($c{"appendhost_$h"}));
      }
      if (!&do_imap_login($u, $p, $host, $inbox)) {
         debug "Failed imap login with info - u: $u ; host: $host ; ;";
         return;
      }
   }
  
   # Since we're changing the subscription list, lets flush the sfcache
   &set_session_obj('imap_sfcache',undef);

   if ($value) {
      return $pop->subscribe_folder(get_fold_and_prefix($fold));
   } else {
      return $pop->unsubscribe_folder(get_fold_and_prefix($fold));
   }
}

sub set_folder_subscription_local
{
   my ($fold, $value) = @_;
   
   $userdb{"folder:$fold:subscribed"} = bool($value);
   
   return 1;
}

sub get_folders_with_nodes
{
    my (@f,@local_fold,@temp);

    #Get IMAP Folders from Cache
    if ( ($protocol =~ /imap/i) || ($c{"pure_imap"}) )
    {
	push(@f, &get_folders_imap_nodes());
    }
    else
    {
        if (opendir(FOLD, "$homedir/folders")) {
            @f = grep { !/^\./ } readdir(FOLD);
            closedir FOLD;
        }
#	push(@f,split('%%smoo1919',$userdb{"variable:folders"}));
    }

    #Always make INBOX show up
    push(@f, $inbox);

    #Neaten it up
    @f = sort { lc($a) cmp lc($b) } @f;
    foreach (@f) { debug "look folder: $_"; }

    return (@f);
}

sub get_ldap_hosts
{
   my $ldap_host = $c{"ldap_search_host"} || "ldap.bigfoot.com";
   my @hosts = split(' ', $ldap_host);
   return @hosts;
}

sub print_ldap_hosts
{
    my @hosts = &get_ldap_hosts();
    my $ldap_host = $hosts[0];
    my $data;

    debug "hosts @hosts";
    if (scalar(@hosts) > 1) {
        $data = "<select name=\"ldap_search_host\">\n";
        foreach (@hosts) {
            $data .= "<OPTION VALUE=\"$_\">$_\n";
        }
        $data .= "</select>\n";
    }
    else {
        $data = "<input type=hidden name=\"ldap_search_host\" value=$ldap_host>\n";
    }

    debug "$data";
    return $data;
}


sub print_folders
{
    my ($option, $prefix, $folder_selected) = @_;
    my (@folders, $fold, $i, $selected);
    my ($data) = ("");

    debug "$option $prefix $folder_selected";
    $folder_selected ||= $folder;

    @folders = get_folders();

    for (@folders)
    {
        debug "folder $_";
	if ( ($_ eq $option) || (($_ eq $folder_selected) && !$prefix) )
	{
            $data .= "<OPTION VALUE=\"$_\" SELECTED>$prefix$_\n";
	    $selected = 1;
	}
	else
	{
            $data .= "<OPTION VALUE=\"$_\">$prefix$_\n";
	}
    }

    # if we haven't printed the selected folder already, 
    # then we need to print it out right now.
    if (!$selected)
    {
	if ($option)
	{
            $data .= "<OPTION VALUE=\"$option\" SELECTED>$prefix$option\n";
	    $selected = 2;
	}
    }

    # 07/26/98: this was checking if $selected != 2. Because of that it was reproducing
    # the current selected folder in the list.  /Jah
    if ($option && !$selected)
    {
	$data .= "<OPTION VALUE=\"$option\">$prefix$option\n";
    }

    my $garbage = $msg{"GARBAGE_Filter_Name"} || "GARBAGE";
    if ($option eq $garbage) {
        write_tmp("garbage", "SELECTED");
    }
    else {
        write_tmp("garbage", "");
    }
    
    return($data);
}

sub print_folders2
{
    my ($html) = @_;
    my (@folders, $fold, $i, $selected);

    my ($data) = ("");
    
    my $folder_selected = $folder;
    
    @folders = get_folders();
    
    for (@folders)
    {
	my $html_subed = $html;
	$html_subed =~ s/#FOLDERNAME#/$_/g;
	$data .= $html_subed;
    }
    
    return($data);
}

sub options_parse
{
    my ($offset, $c, $i, $counter);

    # see if they want to reset the options
    if ($query->param('reset.x'))
    {
	set_default_options();
	set_status($msg{'MSG_OptionsReset'});
	options();
	return;
    }

    if ($query->param('type'))
    {
	$v{"emu_type"} = $query->param('type'); #MM 11/28/98 Set Interface type
        if (! grep( $v{emu_type} eq $_, split(/[\s,]+/, $c{ifaces})) ) {
	   $v{emu_type} = $c{'default_interface'} || "normal";
	}
	                                       
    }


    $counter = $userdb{"filters.total"} = $query->param("total");
    debug "total filters: $counter";

    $offset = $i = 0;
    my @goodfilters;
    
    while ($counter--)
    {
	$i++;

	# don't add blank entries. (have to decrement i here)
#	do { --$i, next } if ($query->param("data$i") =~ /^\s*$/);
	next if ($query->param("data$i") =~ /^\s*$/);

	$c = $i - $offset;
        debug "processing filter $i";
	
	if ($query->param("type$i") != FILTER_DELETE)
	{
            push(@goodfilters, $i);
            debug "adding filter $i type ".$query->param("type$i");
            debug "action is ".$query->param("action$i");

	    $userdb{"filters.type$i"}     = filter_valid($query->param("type$i"));
	    $userdb{"filters.modifier$i"} = $query->param("modifier$i");
	    $userdb{"filters.data$i"}     = $query->param("data$i");
	    $userdb{"filters.action$i"}   = $query->param("action$i");
	    $userdb{"filters.bRegex$i"}   = bool($query->param("bRegex$i"));
# 07/26/98: don't need this anymore
#           $userdb{"action$c"}   =~ s/^\Q$msg{'V_FilterMoveto'} //;
	}
	else
	{
            debug "deleting filter $i";
	    delete($userdb{"filters.type$i"});
	    delete($userdb{"filters.modifier$i"});
	    delete($userdb{"filters.data$i"});
	    delete($userdb{"filters.action$i"});
	    delete($userdb{"filters.bRegex$i"});
	    $offset++;
	}
    }

    $c = 0;
    foreach (@goodfilters) {
        $c++;
        next if ($c == $_);
        # rearrange filters
        $userdb{"filters.type$c"}     = $userdb{"filters.type$_"};
        $userdb{"filters.modifier$c"} = $userdb{"filters.modifier$_"};
        $userdb{"filters.data$c"}     = $userdb{"filters.data$_"};
        $userdb{"filters.action$c"}   = $userdb{"filters.action$_"};
        $userdb{"filters.bRegex$c"}   = $userdb{"filters.bRegex$_"};
        delete($userdb{"filters.type$_"});
        delete($userdb{"filters.modifier$_"});
        delete($userdb{"filters.data$_"});
        delete($userdb{"filters.action$_"});
        delete($userdb{"filters.bRegex$_"});
    }

#    $userdb{"filters.total"} = $i - $offset;
    $userdb{"filters.total"} = $c;
 
  EMUFILES:
    {
      VIEW_FILE:
	if ($query->param('view.x'))
	{
	    view_emufile(($query->param('selected_file'))[0] || "", "options");
	    return;
	}
	
      DELETE_FILE:
	if ($query->param('delete.x'))
	{
	    del_emufile(($query->param('selected_file'))[0] || "", "options");
            if ($query->param('close_window') == 1) {
                debug "window close requested" ;
                &load_page("close_window.html");
            }
            else {
	        &load_page("options.html");
            }
	    return;
	}
	
      UPLOAD_FILE:
	if ($query->param('upload.x'))
	{
	    upload_emufile(($query->param('uploaded_file'))[0] || "", "$homedir/files", "options");
#           &load_page("options.html");
	    return;
	}
    }

    # Save our options
    set_status($msg{'MSG_OptionsSaved_S'}) if (save_options() != -1);

    options();
}


sub validate_login {
    # almost the same as validate_protocol, but actually tries a login

    my ($host,$proto) = @_;

    $hostnames{$host} = validate_hostname($host)
        if (!defined($hostnames{$host}));

    return -1 if (!$hostnames{$host});

    if (my $c = find_connection($proto, $host, $v{"mail_user"}, $v{"mail_pass"})) {
       return 1;
    }

    $pop = undef;
    my $timeout = $c{"tcp_timeout"} || 10;
    $pop = $proto eq 'imap' ? EMU::IMAP->new($host,Timeout=>$timeout) : EMU::POP3->new($host,Port=>$pop_port,Timeout=>$timeout);

    return 0 if (!$pop or $pop eq undef);

    debug "v{mail_user} is ".$v{"mail_user"};
    if ($proto eq "pop3") {
        $pop->user($v{"mail_user"});
        my $stuff = $pop->pass($v{"mail_pass"});
        debug "stuff is $stuff";
        return 0 if ($stuff eq undef);
    }
    else {
        return 0 if (!$pop->login($v{"mail_user"}, $v{"mail_pass"}));
    }
    
    &store_connection($pop,$proto,$host, $v{"mail_user"}, $v{"mail_pass"});

    debug "OK! login validated";
    return 1;
}


sub validate_protocol {
    # if someone is attempting to access a server with a certain protocol,
    # make sure we can communicate with that server with that protocol

    my ($host, $proto) = @_;

    $hostnames{$host} = validate_hostname($host)
        if (!defined($hostnames{$host}));

    return -1 if (!$hostnames{$host});

    $pop = undef;
    my $timeout = $c{"tcp_timeout"} || 10;
    $pop = $proto eq 'imap' ? EMU::IMAP->new($host,Timeout=>$timeout) : EMU::POP3->new($host,Port=>$pop_port,Timeout=>$timeout);

    return -1 if (!$pop or $pop eq undef);

    # alright, made a connection... but does it actually give us a response?
    my $good = checkpoint_pop();
    debug "good is $good";
    return -1 if (!$good || $good eq undef);

    return 1;
}


sub save_options
{
   my $prot;               # protocol

   # 07/24/98: just do a little checking on what the user has submitted. if they
   # don't have a valid protocol then we fall back on pop3.

   my $oldprot = $userdb{"options.protocol"};
   my $host = $userdb{"folder:$inbox:hostname"};
   my $err = "";
 
   # ACK. We cannot go setting people's protocol to POP3 just 
   # because they removed it from the template.
   if (($prot = $query->param('protocol')) && 
          $userdb{"options.protocol"} ne $prot) {
      $prot = $query->param('protocol');
      $prot = $prot =~ /^(?:imap|pop3)$/ ? $prot : 'pop3';

       if (validate_protocol($host, $prot) == -1) {
           debug (convert($msg{'ERR_InvalidProtocol'}, $prot, $host));
           $err = $msg{'ERR_InvalidProtocol'} || "Error: \%1 is an invalid protocol for server/domain \%2";
           set_status(convert($err, $prot, $host));
           $prot = $oldprot ;
       }

   } 
   else {
      $prot = $oldprot;
   }

   # Option to synchronize POP upon login
   $userdb{"options.DontsynchronizePOP"} = bool($query->param('synchronize')) || 0;

   foreach my $o ( qw/	show_html full_header quoted_reply 
   			use_trash_folder do_realtime_filter 
   			manual_filtering no_html_images/ ) 
   {
      my $val = $query->param($o);
      $userdb{"options.$o"} = bool($val) if (defined $val);
   }
   
   my $v_fspam = bool($query->param('filter_spam'));
   my $v_fspam_folder = $query->param('filter_spam_folder');
   $userdb{"options.filter_spam"} = $v_fspam;
   $userdb{"options.filter_spam_folder"} = $v_fspam_folder if ($v_fspam);
   
   $userdb{"options.skin"} = $query->param('skin') || $c{default_skin} || 'EMU_Original';
   
#   $userdb{"options.show_folder_stats"} = $query->param('show_folder_stats');
   $userdb{"options.protocol"}     = $prot;
   $userdb{"folder:$inbox:protocol"} = $prot;
   debug "set protocol to ".$userdb{"options.protocol"};
   # we only set the protocol here if we are currently in the main mailbox
   $v{"protocol"} = $protocol = $prot unless ($v{'bRemoteBox'});

   # Allow user to limit "protocol walking"
debug "try other protocols? ".$query->param('dont_try_other_protocols');
   if ($query->param('dont_try_other_protocols')) {
      $userdb{"options.dont_try_other_protocols"} = 1;
   }
   else {
      # turn off if it's on
      $userdb{"options.dont_try_other_protocols"} = 0
          if ($userdb{"options.dont_try_other_protocols"} == 1);
   }

debug "limit protocol walking? ".$userdb{"options.dont_try_other_protocols"};

   # if we're changing primary protocols, then we really have to 
   # clear out the INBOX folder db because the uids are completely
   # different from imap to pop and we dont want to keep old uids around
   if ($oldprot ne $prot)
   {
      # Not only delete the db file but also the message files.
      my (%folddb, @messages);
      debug "folder $folder msgs ".$folderdb{"messages"};
      if ($folder !~ /^inbox$/i)
      {
      	    if ( $ELocks->lock_create("$homedir/folders/$inbox", \%folddb, {mode => 'read', nb => 1}) )
      	    {
            	tie %folddb, $db_package, "$homedir/folders/$inbox", O_RDONLY, 0660;
            	@messages = split(':',$folddb{"messages"});
            	%folddb = ();
            	untie %folddb;
            	$ELocks->lock_remove(\%folddb);
            }
      } else {
            @messages = split(':', $folderdb{"messages"});
            %folderdb = ();
            untie %folderdb;
            my $foldfile = process_fold_type($folder);
            $ELocks->lock_remove(\%folderdb);
      }

         debug "@messages";
         foreach (@messages)
         {
            	next if $_ eq "";
		unlink "$homedir/messages/$_";
   	 }
   }

   debug "protocol=$protocol  bRemoteBox=$v{'bRemoteBox'}";

   if (defined( my $prefix = $query->param('prefix') )) {
   debug "prefix: $prefix";
   
      my $delim = &get_imap_delimiter(1);
      debug "delim $delim";
      $prefix =~ s/\Q$delim\E+$//g;
      debug "prefix: $prefix ; usbpx: ",$userdb{"options.prefix"};
      # We need to update the folder cache if the prefix has changed!
      if ($prefix ne $userdb{"options.prefix"}) {
         $userdb{"options.prefix"} = $prefix;
         &get_folders_imap(1);
      } else {
         $userdb{"options.prefix"} = $prefix;
      }
   }

   $userdb{"options.timezone"}     = $query->param('timezone');
   $userdb{"options.sentfolder"}   = $query->param('sentfolder') || "";
   $userdb{"options.signature"}    = $query->param('signature');
   $userdb{"options.real_name"}    = safe_html($query->param('yourname'));
   $userdb{"options.email"}        = $query->param('yourmail') if ($query->param('yourmail'));
   # $userdb{"options.mailloc"}      = bool($query->param('mailloc'));
   $userdb{"options.checkmail"}    = digit($query->param('checkmail'));
   $userdb{"options.checknewmail"}    = digit($query->param('checknewmail'));
   $v{"mailcheck_popup"} = $userdb{"options.mailcheck_popup"} = bool($query->param('mailcheck_popup'));

   # limit the checkmail reload to a minimum of 2 minutes
   $userdb{"options.checkmail"} = 120
   if ($userdb{"options.checkmail"} < 120);
   
   $userdb{"options.autoload"}     = bool($query->param('autoload'));
   $userdb{"options.organization"} = $query->param('organization');

   $userdb{"options.max_messages"} = digit($query->param('max_messages'));
   my $max_limit = $c{"max_messages_limit"} || 100;
   $userdb{"options.max_messages"} = $max_limit
        if ($userdb{"options.max_messages"} > $max_limit);

   $userdb{"options.user_voice_enabled"} = bool($query->param('user_voice_enabled'));

   # added msword control
   $userdb{"options.disable_msword"} = bool($query->param('disable_msword')) if ($query->param('disable_msword'));

   if (!$c{'disable_forwarding'}) {
      my ($file,$user);
      my ($forward) = $query->param('forward');

      if ($c{'perlsub_forward_path'}) {
         if ($userdb{"options.email"} =~ /@/) {
             $user = (split(/@/, $userdb{"options.email"}))[0];
         }
         else {
             $user = $userdb{"options.email"};
         }
 
         $file = do_perlsub($c{'perlsub_forward_path'},$user).$c{'forward_file'};
         debug "=======> found file = $file";
      } else {
         $file = "$homedir/tmp/". $c{'forward_file'};
      }

      # no pipelines
      $forward =~ s/\|//g;

      # do we want to overwrite the file or is it an aliases-type file with
      # multiple entries? If it has multiple entries we want to edit instead.
      if (bool($c{'forward_file_multiple_aliases'})) {
          open (FWD, "$file");
          my @aliases = <FWD>;
          close FWD;

          @aliases = grep { !/^$user:/ } @aliases;
          push (@aliases, "$user:$forward");
          @aliases = sort @aliases;

          open (FWD, ">$file");
          print FWD join("\n", @aliases);
          close FWD;
      }
      else {
          my ($fh) = new IO::File ">$file";
          if ($fh) {
	
             debug "setting forward address to $forward";
	
             $fh->print("$forward\n");
         
             $fh->close;
         
          } else {
             debug ("CANT OEPN: $!");
          }
      }
   }

   return -1 if ($err ne "");
}

# 02/12/99 RMK Added sub to export messages
sub export_messages {
    my ($line, $head, $body, $from, $date, $file);
    my ($wday, $month, $day, $hh, $mm, $ss, $year);
    my ($fold) = $_[0];# shift(@_);
    my ($messages) = $_[1];
    my $type = $_[2]; #indicator. we should send to user zip with .eml

    debug "foldertype is $type";
#    load_module("Date::Parse",0,'str2time');

    if ($type){
    	print "Content-type: application/zip\n";
    	print "Content-disposition: attachment; filename=$fold.zip\n\n";
    	
    load_module( "Archive::Zip qw(:CONSTANTS :ERROR_CODES)" );
	use IO::Scalar;
	my $zipContents = '';
	my $SH = IO::Scalar->new(\$zipContents);
	my $zip = Archive::Zip->new();
	my (%details, $i, $it);
	
	foreach my $msg (@$messages)
	{	
		$i++;
		next if (! check_msg_location($msg,$fold));
	        my $head = MIME::Head->from_file("$homedir/messages/$msg");
		    
	        chomp(my $subj = $head->get('Subject'));
	        chomp(my $date = $head->get('Date'));
	        $date = get_date(str2time($date), 1);
	        debug "DATE is $date";
	        
	        $details{$i}{'date'} = $date;
	        $details{$i}{'subj'} = $subj;
	        
	       	my $body = new MIME::Body::File "$homedir/messages/$msg";
		    
		my $member = $zip->addString($body->as_string(), "$i.eml");
		eval
		{
		  $member->desiredCompressionMethod('COMPRESSION_DEFLATED');
		  my $status = $zip->writeToFileHandle( $SH );
	      debug "THE STATUS IS: $status";
		};
		  
	}
	
	
	my $cont = "Filename:\tSubject:\tDate:\r\n\r\n";
	
	
	for ($it=1; $it<=$i;$it++)
	{
		$cont .= "$it       	$details{$it}{'subj'}	$details{$it}{'date'}\r\n";
	}
	
	$cont .= "\r\n Powered by EMU Webmail - www.emumail.com";
	
	my $member = $zip->addString($cont, 'index.txt');
	$member->desiredCompressionMethod('COMPRESSION_DEFLATED');
	
	
	$zip->writeToFileNamed("$homedir/tmp/$fold.zip");
	
	open (FHA, "$homedir/tmp/$fold.zip");
	binmode FHA;
	print <FHA>;
	close FHA;
	
	unlink "$homedir/tmp/$fold.zip";
    	
    }else
    {
    	print "Content-type: application/x-mbox\n";
    	print "Content-disposition: attachment; filename=$fold.mbox\n\n";
    	
	foreach my $msg (@$messages)
	    {
	        debug "exporting $msg";
	
	        #Make sure we have the message (IMAP)
	        next if (! check_msg_location($msg,$fold));
	        $head = MIME::Head->from_file("$homedir/messages/$msg");
		    
	        chomp($from = (addr_split($head->get('From')))[1]);
		    
	        chomp($date = $head->get('Date'));
	        debug "DATE is $date";
	
	        $date = get_date(str2time($date), 1);
	        print "From $from  $date\n";
	        $body = new MIME::Body::File "$homedir/messages/$msg";
		    
	        $body->print();
	        print "\n";
	    }
    }
}




sub folders_parse
{
 # Parse results from folders page
    my $next = shift;

    my ($pop_checked,$imap_checked,$local_checked,$new_foldername,$new_username,$new_password);
    my ($new_hostname,$new_folder);

#    my $delim = &get_imap_delimiter(1);

    # Three ways we got here: Save Changes, Edit Folder, or Delete Folder
    if ($query->param('save.x'))
    {
        debug "save";
	# Check for input
	if (!$query->param("new_fold"))
	{
	    set_status($msg{'ERR_FolderEmptyName_S'});
	}
	else
	{
	    my ($uu,$hh) = split(/\@/,$user_name);
            if ($user_name =~ /@/ && exists($c{"appendhost_$hh"})) {
                $uu = $user_name;
                $hh = $c{"map2pop_$hh"};
            }
            debug "uu=$uu hh=$hh";
	    
	    #See if Input is legal
            my ($folddir) = $query->param('folddir');

	    my ($new_fold) =  $query->param('new_fold');
	    my ($fold_fold) = $query->param("fold_fold") || $inbox;
	    my ($fold_host) = $query->param("fold_host") || $hh; #Folder Host
	    my ($fold_pass) = $query->param("fold_pass") || decode($folderdb{"password"}) || $password;

	    my ($fold_user) = $query->param("fold_user") || $uu;
	    my ($fold_type) = lc(legalize($query->param("fold_type")));

            if (!$fold_host && $fold_user =~ /@/ && !exists($c{"appendhost_$fold_host"})) {
                # allow for creating mailboxes via simple email address
                ($fold_user, $fold_host) = split(/@/, $fold_user);
            }

            # default fold_type if not provided
            if (!$fold_type) {
                if ($protocol =~ /pop/i) {
                    $fold_type = "local";
                }
            }
            my $external = ($fold_type ne "" && $fold_type ne "local") ? 1 : 0;

            debug "protocol $protocol type $fold_type";
	    if ($fold_type ne "local" && ($protocol =~ /imap/i) && ($fold_type ne "pop3") && (!$external))
	    {
		$fold_type = "imap";
#                $new_fold = $folddir . $delim . $new_fold;
	    }

            # if we end up with something like "/folder" or "//folder" because
            # of not using a prefix, then remove the slashes

	    debug "nf: $new_fold ff: $fold_fold fh: $fold_host fp: $fold_pass fu: $fold_user ft: $fold_type ";

            # remove both leading and trailing spaces
            trim(\$new_fold);

            # ok, now let's look at our current folder list and see if we
            if (folder_exists($new_fold)) {
                set_status(convert($msg{'MSG_FolderExists_S'}, $new_fold));
            }
	    elsif ($new_fold eq $inbox)
	    {
		set_status($msg{'ERR_DeleteInbox'});
	    }
            # RMK 19990315 added check for " and : they screw up hashes
	    elsif ( (!$new_fold) || (!$fold_type) 
                    || $new_fold =~ /[":\{\}\%\$]\// || $new_fold =~ /^\.|\.loc?k$/ )
	    {
		#No Legal Chars in name
		set_status($msg{'ERR_FolderIllegalName_S'});
	    }
	    elsif ($fold_type ne "pop3" && $fold_type ne "imap" && $fold_type ne "local")
	    {
		set_status($msg{'MSG_MBoxBadProtocol'});
	    }

	    # if we are using a remote mailbox but the user has either not 
            # supplied a password or a valid email address (one with an @) 
            # then we fail.
	    elsif ($external && 
                    (!$fold_user || !$fold_pass || !$fold_host))
	    {
		debug "fold fold_host: $fold_host";
		# Need a user w/ @ and pass for remote folders
		set_status($msg{'ERR_MissingEmail'});
	    }
	    elsif ( ($c{'remote_only'}) && ($fold_type eq "local") )
	    {
		set_status($msg{'MSG_MBoxBadProtocol'});
	    }
	    else
	    {
		# We're Legal!  Let's create the folder
		&create_folder($new_fold,$fold_type,$fold_user,$fold_host,$fold_pass,$external,$folddir,$fold_fold);

                # hack... need to call get_imap_folders so that the fcache
                # can be refreshed
                if ($fold_type eq "imap") {
                    get_folders_imap(1);
                }
	    }
	    
	}
    }
    elsif ($query->param('edit.x'))
    {
	my $currfold = $query->param("folder_selected");
	
	debug "Folder selected: $currfold";
	
	if ($currfold eq $inbox)
	{
	    set_status($msg{'MSG_NoEditInbox'});
	    folders();
	    return;
	}
	
	if (!$query->param("new_fold") && $userdb{"folder:$currfold:protocol"} eq "local")
	{
	    set_status($msg{'ERR_FolderEmptyName_S'});
	    folders();
	    return;
	}

        my $new_name = $query->param("new_fold");
        my $external = $userdb{"folder:$currfold:external"};
#	my $proto = ($external == 1) ? $userdb{"folder:$currfold:protocol"} : "";
	my $proto = $userdb{"folder:$currfold:protocol"};
	
	write_tmp("proto", $proto);

	#Set for coming back to page

	($new_username,$new_hostname) = split(/\@/,$userdb{"folder:$currfold:username"}) if ($external);

        $new_folder = $userdb{"folder:$currfold:extra_fold"};
	
	# have to write this so that if they change the name of the folder
	# we know what the original name was and can remove it from the list
	$v{"editfolder"} = $currfold;

        create_folder($new_name,$proto);
	debug "editing entry with username=$new_username  proto=$proto";
    }
    elsif ($query->param('delete.x'))
    {
	$new_foldername = $query->param("folder_selected");

        debug "selected $new_foldername for delete";
        &delete_folder("$new_foldername");

	$new_foldername = "";
	$new_password = "";
	$new_username = "";
    }
    elsif ($query->param('export.x'))
    {
        my $orig_fold = $folder;
	my($fold, @messages);
	$fold = $query->param('folder_selected');
	
	debug "exporting $fold ".$query->param('folder_selected');

        folder_or_mailbox() if (!$fold);

	unless (folder_exists($fold))
	{
	    set_status(convert($msg{'ERR_FolderMissing_S'}, $fold));

            folder_or_mailbox();
	    return;
	}
	
	debug "Got here";

        my $folder_changed = 0;
        my $foldfile;

      OPEN_FOLDER_DB:
        {
            last if ($orig_fold eq $fold);

            # we have to temporarily untie the folderdb because the list
            # subs write to it...
            untie %folderdb;
            $foldfile = process_fold_type($orig_fold);
            $ELocks->lock_remove(\%folderdb);

            $foldfile = process_fold_type($fold);
	    if ( $ELocks->lock_create("$homedir/folders/$foldfile", \%folderdb, {mode => 'write', nb => 1}) )
	    {
            	tie %folderdb, $db_package, "$homedir/folders/$foldfile", O_CREAT|O_RDWR, 0660;
            	debug "opened $foldfile";
            	$folder_changed = 1;
            }
        }


      EXPORT_MAILBOX:
        {
            # for externals or any imap folder, must get the list

            last if (!$userdb{"folder:$fold:external"} &&
                      $userdb{"folder:$fold:protocol"} !~ /imap/i);

            # set this, it's useful later on
            $v{"external"} = $userdb{"folder:$fold:external"};

            debug "will get list of messages for folder $fold";
            my ($user,$host,$p) = ($userdb{"folder:$fold:username"},
                                   $userdb{"folder:$fold:hostname"},
                                   decode($userdb{"folder:$fold:password"}));

            get_list_pop($user, $p, $fold)
                if ($userdb{"folder:$fold:protocol"} =~ /pop/i);

	    get_list_imap_full($host,$user,$p,$fold)
                if ($userdb{"folder:$fold:protocol"} =~ /imap/i);
        }

	@messages = split(':', $folderdb{"messages"});

	if (scalar(@messages) <= 0)
	{
	    set_status($msg{'ERR_FolderEmpty_S'});

            folder_or_mailbox();

            $ELocks->lock_remove(\%folderdb) if ($folder_changed);
	    return;
	}

#        debug "messages to export: @messages";

#        export_messages($fold, @messages);

	if ($query->param('export_type'))
	{
		export_messages($fold, \@messages, 1);
	}else
	{	        
        	export_messages($fold, \@messages);
	}

      RESTORE_FOLDERDB:
        {
            last if (!$folder_changed);

            # now that we've exported, re-acquire folderdb
            untie %folderdb;
            $ELocks->lock_remove(\%folderdb);
            
            $foldfile = process_fold_type($orig_fold);
            if ( $ELocks->lock_create("$homedir/folders/$foldfile", \%folderdb, {mode => 'write', nb => 1}) )
            {
            	tie %folderdb, $db_package, "$homedir/folders/$foldfile", O_CREAT|O_RDWR, 0660;
            }
        }

        return;
    }
    elsif ($query->param('select.x'))
    {
	my ($fold) = $query->param('folder_selected');
        debug "selected folder $fold";

	if (folder_exists($fold))
	{
	    debug "changing selected folder to $fold";
	    set_status(convert($msg{'MSG_FolderSelected'},$fold));
	    write_tmp("folder_selected", $fold);
	}
	else
	{
	    set_status(convert($msg{'ERR_FolderSelected'},$fold));
	}
    }
    elsif ($query->param('rename.x'))
    {
	my ($fold) = $query->param('rename_from');
	if (folder_exists($fold))
	{
	    my ($rename_to) = $query->param('rename_to');

	    # See if the new name exists
	    if (folder_exists($rename_to))
	    {
		set_status(convert($msg{'ERR_FolderIllegalName_S'}, $fold));
	    }
	    else
	    {
		#Looks like we're legal
                my @the_keys = grep { /^folder:$fold:/ } keys %userdb;
                foreach my $key (@the_keys) {
                    my $new_key = $key;
                    $new_key =~ s/:$fold:/:$rename_to:/;
                    $userdb{$new_key} = $userdb{$key};
                    delete($userdb{$key});
                    debug "renaming $key to $new_key";
                }

                debug "rename: here";
		&delfrom_imap_fcache($new_foldername);
      
                my $foldfile = process_fold_type($new_foldername);
                if (-e "$homedir/folders/$foldfile") {
                   debug "deleting file $homedir/folders/$foldfile";
                   unlink "$homedir/folders/$foldfile";
                }
                
		my ($fold_type) = lc(legalize($query->param("fold_type")));

		if ($fold_type eq "imap")
		{
		    my ($user,$p,$host) = &get_folder_credentials($fold);
		    eval 
		    {
			&do_imap_login($user,$p,$host);
			$pop->rename($fold,$rename_to);
		    }
		}
	    }
	}
	else
	{
	    set_status(convert($msg{'ERR_FolderMissing_S'}, $fold));
	}
    }    
    elsif ($query->param('empty.x'))
    {
	  my $fold =  $query->param("folder_selected");
	  if ($fold) {
	     empty_folder($fold);
	     set_status(convert($msg{'ERR_FolderEmpty'}, $fold));
	  }
    }
    else
    {
	warn("going to non-existant branch in folders_parse");
	set_status($msg{'MSG_InvalidSelection'});
	folders();
	return; #huh?
    }
    
    # Write temporary variables
    write_tmp("folder_selected", ($query->param('delete.x') ? "" : $query->param('folder_selected')));
    write_tmp("new_username",$new_username,1);
    write_tmp("new_password",$new_password,1);
    write_tmp("new_hostname",$new_hostname,1);
    write_tmp("new_folder",$new_folder,1);
    write_tmp("new_foldername",$new_foldername,1);
    # Go here next
    if ($next) {
        &{$next}();
    } else {
        folders();
    }
    return;
}

sub empty_folder
{
   my ($fold) = @_;

   debug "Emptying (delete then recreate) folder $fold";
   
   my ($fold_user, $fold_pass, $fold_host) = get_folder_credentials($fold);
   my $fold_type = get_folder_protocol($fold);

   debug "deleting $fold";
   &delete_folder($fold);
   debug "creating $fold ";
   &create_folder($fold, $fold_type, $fold_user, $fold_host, $fold_pass);
}

sub delete_folder{
	my $new_foldername = shift;

        $folder = $inbox;
        $v{"folder"} = $folder;
        write_tmp("folder",$folder,1);

	if ($new_foldername eq $inbox)
	{
	    set_status($msg{'ERR_DeleteInbox'});
	    folders();
	    return;
	}

        my $searchfold = $msg{"FOLD_Search_Results"} || "Search Results";
	if ($new_foldername eq $searchfold)
	{
	    set_status($msg{'ERR_DeleteSearch'});
	    folders();
	    return;
	}

	my ($fold_type) = lc(legalize($query->param("fold_type")));

        my ($del_error) = 0;
        debug "folder to delete: $new_foldername, protocol ".$userdb{"folder:$new_foldername:protocol"}." $protocol";

        # Unsubscribe the folder
        &set_folder_subscription($new_foldername, 0)
            if (!$userdb{"folder:$new_foldername:external"});

        my $its_imap =
            bool(!$userdb{"folder:$new_foldername:external"} &&
                 ($fold_type eq "imap" ||
                  $userdb{"folder:$new_foldername:protocol"} =~ /imap/i ||
                  ($protocol =~ /imap/i &&
                  !exists($userdb{"folder:$new_foldername:protocol"}))));

        debug "is it imap? $its_imap";

	if ($its_imap)
	{
	    my ($user,$p,$host) = &get_folder_credentials($new_foldername);

	    if ($user =~ /@/) {
	        my ($u, $h) = split(/@/, $user, 2);
	        $user = $u if (!exists($c{"appendhost_$h"}));
	    }

            debug "deleting folder $new_foldername";
	    eval
	    {
                my $fn = get_fold_and_prefix($new_foldername);
		&do_imap_login($user,$p,$host,$fn);
		unless ($pop->delete_folder($fn))
		{
		    set_status(convert($msg{'ERR_DeleteHierarchy'},$new_foldername));
                    $del_error = 1;
		}
	    }
	}

        unless ($del_error)
        {
            my %folddb;
            my $messages;
            my $currentfolder = $folder;
            my $foldfile = process_fold_type($new_foldername);

            # ok, first things first... if we're going to delete, then
            # we need to open the current folder...
            if ($new_foldername ne $folder) {
                if ( $ELocks->lock_create("$homedir/folders/$foldfile", \%folddb, {mode => 'write', nb => 1}) )
                {
                	tie %folddb, $db_package, "$homedir/folders/$foldfile", O_CREAT|O_RDWR, 0660;
                	debug "opened $foldfile";
                }
                $messages = $folddb{"messages"};
            }

            # temporarily reset $folder since it's used elsewhere
            $folder = $new_foldername;

            if ($trash_bin && ($new_foldername ne $trash_folder)) {
                if ($folderdb{"messages"}) {
                    $query->param(-name=>'d', -value=>$messages);
                    move_msg(1,1);
                    set_status('<br>');
                }            # housekeeping... don't leave any trace of this folder in
            # foldmap
            }
            else {
                # first delete messages in folder
                my @msgs = split(/:/, $messages);
#                debug "messages from $new_foldername to delete: @msgs";

                # we should really just delete them locally, don't actually
                # go out to the server and delete messages.
                del_local_msg(\@msgs);

            }

            &delfrom_imap_fcache($new_foldername);

            # now restore $folder;
            $folder = $currentfolder;

	    my $local_checked = "checked";

	    set_status(convert($msg{'MSG_FolderDelete_S'},$new_foldername));

            # remove the userdb entries as well
            debug "removing userdb entries for $new_foldername";

            delete($userdb{"folder:$new_foldername:hostname"});
            delete($userdb{"folder:$new_foldername:username"});
            delete($userdb{"folder:$new_foldername:email"});
            delete($userdb{"folder:$new_foldername:password"});
            delete($userdb{"folder:$new_foldername:protocol"});
            delete($userdb{"folder:$new_foldername:extra_fold"});
            delete($userdb{"folder:$new_foldername:external"});
            delete($userdb{"folder:$new_foldername:subscribed"});

            # housekeeping... don't leave any trace of this folder in
            # foldmap
            foreach my $key (keys %foldmap) {
                delete($foldmap{$key}) if ($foldmap{$key} eq $new_foldername);
            }
            
            # Removed cached indexes
            wildrm("$homedir/folders-ordered", "^$new_foldername");

            untie %folddb;
            unlink "$homedir/folders/$foldfile" or debug "Can't unlink $homedir/folders/$foldfile folder: $!";
			$ELocks->lock_remove(\%folddb);
        }
}


sub create_folder
{
 # Create a folder (local, POP3, or IMAP)
    my ($new_fold,$fold_type,$fold_user,$fold_host,$fold_pass,$external,$folddir,$fold_fold) = @_;
    my ($editflag, $u, $host);
    my $extra_fold;

    $new_fold =~ s/[:\[\]\(\)\#\$<>\{\}]//g;

    # Default to inbox properties if none are passed in (but only for imap)
    if (@_ == 1) {
        if ($userdb{"folder:$inbox:protocol"} =~ /imap/i) {
            ($fold_user, $fold_pass, $fold_host) = get_folder_credentials($inbox);
            $fold_type = get_folder_protocol($inbox);
            $external = 0;
        }
        else {
            # must be a local folder if proto isnt imap
            $fold_type = "local";
        }
    }

    debug "nf: $new_fold fh: $fold_host ft: $fold_type fu: $fold_user fp: $fold_pass external $external";

    # usage in undef instance before
    return undef unless ($new_fold && $fold_type); #error msg??

    # this determines which status message to print
    $editflag = 1 if ($v{'editfolder'} || $query->param('editfolder'));
    debug "editflag $v{'editfolder'} ".$query->param('editfolder')." $editflag";

    if ($fold_type eq 'pop3')
    {
        undef %poplist;
#	$pop->quit() if $pop;
	undef $pop;
        $pop_connected = 0;

#        ($u, $host) = split(/@/, $fold_user);
        ($u, $host) = map_mailserver($fold_user, $fold_host, $new_fold);

	# Try connection
        my $success;
        ($success,$host,$u) = do_login_sequence("pop3",$u,$fold_pass,$host,0);

        debug "u $u  host $host";
        if (!$success) {
            if ($pop) {
                my $error = convert($msg{'MSG_LoginError'}, $pop->errcode);
                set_status($error);
            }
	    set_status(convert($msg{'ERR_FolderFailedCreate_S'}));
            return 0;
        }

#        $pop->quit if $pop;
        undef $pop;
        $pop_connected = 0;

    }
	
    elsif ($fold_type eq 'imap')
    {
	# Get user/host
#        ($u, $host) = split(/@/, $fold_user);

        # OK, with imap folders we need to determine the folder path,
        # applying delimiter and whatever else needed.

        ($u, $host) = map_mailserver($fold_user, $fold_host, $new_fold);

	# Allow for extra IMAP path at end of hostname:
	# user@imapserver.com/MYMAILBOX/HERE/AND/HERE/AND...
	($host,$extra_fold) = split('/',$host,2);       #$host =~ /^([^\/]+)\/*(.*)/;

        $extra_fold = $fold_fold if (!$extra_fold && $fold_fold);
	$extra_fold = $extra_fold || $new_fold;

	debug "u=$u  host=$host extra_fold=$extra_fold";

	# set it back (without the trailing / part)
	$fold_user = "$u\@$host";

      CREATE_IMAP_MAILBOX:
        {
            last if (!$external || $editflag);

            # we're not creating an imap folder, we're accessing
            # an external imap mailbox

            debug "creating imap mailbox";
            # Try connection
            my $success;
            ($success,$host,$u) = do_login_sequence('imap',$u,$fold_pass,$host,0);
            debug "u $u  host $host";
            if (!$success) {
                if ($pop) {
                    my $error = convert($msg{'MSG_LoginError'}, $pop->errcode);
                    set_status($error);
                }
                return 0;
            }
    
#            $pop->quit if $pop;
            undef $pop;
            $pop_connected = 0;
        }


      CREATE_IMAP_FOLDER:
        {
            last if ($external || $editflag);

            debug "creating imap folder";
	    unless (&create_folder_imap($host,$u,$fold_pass,$new_fold,$folddir))
	    {
                my $error = $pop->errcode if $pop;
                $error =~ s/(:.*)$//;
                $error = $1;
	        set_status(convert($msg{'ERR_FailedCreateFolder'}, "$new_fold $error"));
	        return 0;
	    }
        }

    }
    elsif ($fold_type ne "local")
    {
	set_status($msg{'MSG_MBoxBadProtocol'});
	return 0;
    }

    if ($editflag)
    {
        my $editfolder = $v{'editfolder'} || $query->param('editfolder');
        $editfolder = get_fold_and_prefix($editfolder)
            if ($userdb{"folder:$editfolder:protocol"} =~ /imap/i);
	debug "new_folder=$new_fold  editfolder=$editfolder";

	# since we were editing, we need to check if they've modified the name of the folder
	if ($new_fold ne $editfolder)
	{
            my $editfile = remove_fold_prefix($v{'editfolder'} || $query->param('editfolder'));
            $editfile =~ s/\//./g;
            my $foldfile = remove_fold_prefix($new_fold);
            $foldfile =~ s/\//./g;
            debug "$editfile and $foldfile";

            debug "protocol $protocol external $external";
            if ($userdb{"folder:$editfile:protocol"} =~ /imap/i ||
               ($protocol =~ /imap/i && $userdb{"folder:$editfile:protocol"} !~ /local/i && !$external))
            {
                debug "original protocol is imap, not external";

               my ($user,$p,$host) = &get_folder_credentials($editfolder);
                eval
                {
                    &do_imap_login($user,$p,$host);
                    $pop->rename($editfolder,$new_fold);
                    $query->param(-name=>'folder_selected', 
                                  -value=>remove_fold_prefix($new_fold));
                }
            }

            my @the_keys = grep { /^folder:$editfile:/ } keys %userdb;
            foreach my $key (@the_keys) {
                my $new_key = $key;
                $new_key =~ s/:$editfile:/:$foldfile:/;
                $userdb{$new_key} = $userdb{$key};
                delete($userdb{$key});
                debug "renaming $key to $new_key";
            }

            # Oh... we have to take care of the foldmap as well!!
            foreach my $key (keys %foldmap) {
                $foldmap{$key} = $foldfile if ($foldmap{$key} eq $editfile);
            }

#            $userdb{"folder:$foldfile:external"} =
#                $userdb{"folder:$editfile:external"};
#            delete($userdb{"folder:$editfile:external"});
#            $userdb{"folder:$foldfile:password"} =
#                $userdb{"folder:$editfile:password"};
#            delete($userdb{"folder:$editfile:password"});
#            $userdb{"folder:$foldfile:hostname"} =
#                $userdb{"folder:$editfile:hostname"}; 
#            delete($userdb{"folder:$editfile:hostname"}); 
#            $userdb{"folder:$foldfile:email"} =
#                $userdb{"folder:$editfile:email"};
#            delete($userdb{"folder:$editfile:email"}); 
#            $userdb{"folder:$foldfile:username"} =
#                $userdb{"folder:$editfile:username"};
#            delete($userdb{"folder:$editfile:username"}); 
#            $userdb{"folder:$foldfile:protocol"} =
#                $userdb{"folder:$editfile:protocol"}; 
#            delete($userdb{"folder:$editfile:protocol"}); 
#            $userdb{"folder:$foldfile:extra_fold"} =
#                $userdb{"folfnder:$editfile:extra_fold"}; 
#            delete($userdb{"folder:$editfile:extra_fold"}); 

#            $editfile = process_fold_type($editfile);
#            $foldfile = process_fold_type($foldfile);

            my $path = "$homedir/folders/";
            
            if ($userdb{"folder:$foldfile:external"}) {
                $path .= '.external/';
            } 
            elsif (lc($userdb{"folder:$foldfile:protocol"}) eq 'imap') {
                $path .= '.imap/';
            }

            debug "moving $path/$editfile to $path/$foldfile";
           
            move("$path/$editfile", "$path/$foldfile");
	    $v{"editfolder"} = "";

	    # If we have renamed the current folder, we must update our state
	    if ($folder eq $editfile) {
	        $folder = $v{"folder"} = $new_fold;
	    }

	}
        else {
            # simply save in new data.
            $new_fold =~ s/\//./g;
            debug "setting external to $external for $new_fold";
            $userdb{"folder:$new_fold:external"} = $external;
            $userdb{"folder:$new_fold:password"} = code($fold_pass);
            $userdb{"folder:$new_fold:hostname"} = $host;
            $userdb{"folder:$new_fold:email"} = $fold_user;
            $userdb{"folder:$new_fold:username"} = $u;
            $userdb{"folder:$new_fold:protocol"} = $fold_type;
            $userdb{"folder:$new_fold:extra_fold"} = $extra_fold if ($external);
            debug "saved extra_fold ".$userdb{"folder:$new_fold:extra_fold"}." for folder $new_fold";
            debug "saving host ".$userdb{"folder:$new_fold:hostname"}." and user ".$userdb{"folder:$new_fold:username"}." and email ".$userdb{"folder:$new_fold:email"};
        }

	set_status(convert($msg{'MSG_FolderEdited'},remove_fold_prefix($new_fold)));
    }
    else
    {
        $new_fold = remove_fold_prefix($new_fold);

        # Is this a folder or a directory??
        if ($fold_type eq "imap" && $new_fold =~ /\/$/) {
	    set_status(convert($msg{'MSG_DirCreated'},$new_fold));
        }
        else {
            # Successful: Add entries to DB
            my (%newfold);
	    set_status(convert($msg{'MSG_FolderCreated'},$new_fold));
    
            $new_fold =~ s/\//./g;

            debug "(1) setting external to $external for $new_fold";
            $userdb{"folder:$new_fold:external"} = $external;
            $userdb{"folder:$new_fold:protocol"} = $fold_type;

            my $foldfile = process_fold_type($new_fold);
	    if ( $ELocks->lock_create("$homedir/folders/$foldfile", \%newfold, {mode => 'write', nb => 1}) )
	    {
            	tie %newfold, $db_package, "$homedir/folders/$foldfile", O_CREAT|O_RDWR, 0660;
            	$newfold{'protocol'} = $fold_type;
            	untie %newfold;
            	$ELocks->lock_remove(\%newfold);
            	debug "created folder |$foldfile|";
            }

            $userdb{"folder:$new_fold:password"} = code($fold_pass);
            $userdb{"folder:$new_fold:hostname"} = $host;
            $userdb{"folder:$new_fold:email"} = $fold_user;
            $userdb{"folder:$new_fold:username"} = $u;
            $userdb{"folder:$new_fold:extra_fold"} = $extra_fold if ($external);
            debug "saved extra_fold ".$userdb{"folder:$new_fold:extra_fold"}." for folder $new_fold";
            debug "$new_fold: saving host ".$userdb{"folder:$new_fold:hostname"}." and user ".$userdb{"folder:$new_fold:username"}." and email ".$userdb{"folder:$new_fold:email"};
        }
    }

    # Auto-subscribe new folders
    &set_folder_subscription($new_fold||$extra_fold, 1) if(!$userdb{"folder:$new_fold:external"});

    return 1;
}

sub create_folder_imap
{
    my ($host,$u,$p,$fold,$folddir) = @_;

    debug "Creating $fold on $host with $u and $p";

    do_login_sequence("imap",$u,$p,$host);

    if ($pop)
    {
        # Now apply any prefix and delimiter...
        my $prefix = get_outbox_prefix();
        my $delim = &get_imap_delimiter(1);

        debug "fold: $fold ; folddir: $folddir ; delim: $delim ; prefix: $prefix";
        $fold = $folddir.$delim.$fold if ($folddir && $delim && $folddir ne $delim);
        $fold = $prefix.$delim.$fold if ($prefix && $fold !~ /^$prefix/);
        debug "fold is now $fold";

	debug "trying to create folder...";
        my $success = $pop->create_folder($fold);
        debug "success: $success";
	if (!$success || $success eq undef)
	{
	    debug "Failed IMAP folder ($fold) creation!";
	    return undef;
	}
	else
	{
            debug "Selecting new folder $fold";
            # Add to fcache
            &addto_imap_fcache(remove_fold_prefix($fold));
            # Subscribe folder (If you think this doesn't belong here,
            # you are correct. But it allows us to avoid a more serious
            # bug for now. Feel free to remove this and fix the other bug)
            $fold =~ s/\Q$delim\E+/$delim/g;
            $pop->subscribe_folder($fold);
            
            return 1;
	}
		
    }
    else
    {
        set_status($msg{'MSG_LoginError'}."Bad Pass: $u and $host");
        return 0;
    }
}

# like the unix command
sub touch
{
    open(MLAH, ">$_[0]") || return 0;
    close MLAH;
}

sub legalize
{
    local($_) = shift;

    1 while s/^\.?\.\///;       # ../'s or ./'s are gone!
    
    s/[\|><\`:\"\']//g;		# .. : , " '

    return $_;
}

## EMU STYLES     ##

# sub show_ad
#
# Parameters: none
# 
# Returns: a string that has the HTML to print an AD.VERT banner
#
sub show_ad
{
    my $noad = shift;

    return if ($AD_VERT == VERSION_DEFAULT || $AD_VERT == VERSION_STANDARD);

    return if ($noad || $img_printed);          # we'll take it that the ad has been printed already

    # also do nothing if configuration indicates override_ads
    return if ($licensed{"override_ads"} && $c{"override_ads"});

    $img_printed = 1;

    if ($AD_VERT || ($AD_VERT == VERSION_PROFESSIONAL() && $c{"show_ads"}))
    {
        my $email = $userdb{"options.email"} || "";
        if ($email) { 
            my @stuff = ($email);
#            load_module("Digest::MD5");
            my $md5 = new Digest::MD5;
            $md5->add(@stuff);
            $email = $md5->hexdigest();
        }

	$AD_VERT_STR     = join('+', $c{'default_pop'}, time, $EMU::Version, $c{'__os_type'}, $c{"country"}, $c{"postal_code"}, $c{"site_type"}, $c{"language"}, $c{"average_age"}, $email);

#        debug "AD_VERT_STR = $AD_VERT_STR";
	my $ad_server = lc $c{"ad_server"} || "ad";

	$TOP_IMAGE = &get_top_image($ad_server, $AD_VERT_STR) || qq{<A HREF="http://ad.vert.net/href.cgi?$AD_VERT_STR" target="_blank"><IMG SRC="http://ad.vert.net/advert.cgi?$AD_VERT_STR" BORDER=0 ALT="[AD VERT BANNER]" HEIGHT="$AD_VERT_HEIGHT" WIDTH="$AD_VERT_WIDTH"></A>\n};

    }
    else
    {

	$TOP_IMAGE = $c{"adcode"} || $c{'TOP_IMAGE'};
#        debug "TOP_IMAGE $TOP_IMAGE";
    }

  SET_CACHE_BUSTER:
    {
	my ($time) = time;
	$TOP_IMAGE =~ s/%time/$time/g;
    }

    if ($TOP_IMAGE)
    {
	# Why do we use prints here?  Return?
	print qq{$TOP_IMAGE};
    }
}


# return the status or an empty string. If we are over our quota then we
# prepend (over quota) to the string
sub get_status2
{
    my $tog = shift;

    $tog &&= $c{'publisher_name'};

#    print "<h1>STATUS is $status</h1>";
    return $status ? ($over_quota ? "$tog: (over quota) $status" : "$tog: $status") : "$tog";
}

sub get_status
{
    if ($status)
    {
	my ($msg);
	$msg = $over_quota ? $msg{'MSG_StatusFormatOverQuota'} : $msg{'MSG_StatusFormat'};
	return convert($msg, $status);
    }
    return "";
}

### Easy HTML

# privatize a string for placement in the QUERY STRING
sub private_str
{
    my $str = shift;
    $str =~ s/(\W)/sprintf("%%%02x", ord($1))/ge;
    $str;
}

sub make_url
{
    my ($next, $value, %extra) = @_;
    my ($p, $string);
    
#    $p = private_str(code($private));

    my $fold = get_var("folder");
	debug "folder is $folder and fold from var 'folder' is $fold";
    $folder = $fold; # WHY? FIX IT
    
    # this is for search results which are shown using go_index.
    # so we want to show original msg folder, not search results!
    my $searchfolder = $msg{"FOLD_Search_Results"} || "Search Results";
    if ($fold eq $searchfolder)
    {
    	$fold = $extra{'folder'};
    	delete $extra{'folder'};
    }

    $fold = private_str($fold);
    $string = "$EMU_URL?folder=$fold";

    if ($next)
    {
		$p = private_str($next);
		$string .= "&passed=$p";
    }

    if ($value)
    {
		$p = private_str($value);
		$string .= "&variable=$p";
    }

    if (%extra)
    {
		foreach my $k (keys %extra)
		{
	    	$p = private_str($extra{$k});
	    	$string .= "&$k=$p";
		}
    }

    # if we are in WAP mode, replace "&" with "&amp;"
    # in WML, "&amp" must be used instead of "&" when specifying 
    # CGI arguments within URL strings
    # -RS 7/10/00
   
	$string =~ s/\&/\&amp;/ig if ( $licensed{"wap"} && $c{"is_wap"} );

    return ($string);
}


sub code
{
    my $cat = shift;
    
    $cat = pack("u",$cat);
    $cat =~ s/\%/a/og;
    $cat =~ s/\//b/og;
    $cat =~ s/\=/c/og;
    $cat =~ s/\n/d/og;
    $cat =~ s/\?/e/og;
    $cat =~ s/\</f/og;
    $cat =~ s/\>/g/og;
    $cat =~ s/\(/h/og;
    $cat =~ s/\)/i/og;
    $cat =~ s/\!/j/og;
    $cat =~ s/\&/k/og;
    $cat =~ s/\[/l/og;
    $cat =~ s/\$/m/og;
    $cat =~ s/\+/n/og;
    $cat =~ s/\'/o/og;
    $cat =~ s/\"/p/og;
    $cat =~ s/\#/q/og;
    $cat =~ s/\]/r/og;
    $cat =~ s/\`/s/og;
    $cat =~ s/\\/t/og;
    $cat =~ s/\_/u/og;
    $cat =~ s/\,/v/og;
    $cat =~ s/\:/w/og;
    $cat =~ s/\*/x/og;
    $cat =~ s/\./y/og;
    $cat =~ s/\-/z/og;
    $cat =~ s/\;/ /og;

    return ($cat);
}

sub decode
{
    my $cat = shift;

    $cat =~ s/a/\%/g;
    $cat =~ s/b/\//g;
    $cat =~ s/c/\=/g;
    $cat =~ s/d/\n/g;
    $cat =~ s/e/\?/g;
    $cat =~ s/f/\</g;
    $cat =~ s/g/\>/g;
    $cat =~ s/h/\(/g;
    $cat =~ s/i/\)/g;
    $cat =~ s/j/\!/g;
    $cat =~ s/k/\&/g;
    $cat =~ s/l/\[/g;
    $cat =~ s/m/\$/g;
    $cat =~ s/n/\+/g;
    $cat =~ s/o/\'/g;
    $cat =~ s/p/\"/g;
    $cat =~ s/q/\#/g;
    $cat =~ s/r/\]/g;
    $cat =~ s/s/\`/g;
    $cat =~ s/t/\\/g;
    $cat =~ s/u/\_/g;
    $cat =~ s/v/\,/g;
    $cat =~ s/w/\:/g;
    $cat =~ s/x/\*/g;
    $cat =~ s/y/\./g;
    $cat =~ s/z/\-/g;
    $cat =~ s/ /\;/g;

    $cat = unpack("u",$cat);

    return ($cat);
}


sub code2
{
    my $cat = shift;

    $cat = pack("u",$cat);
    $cat =~ s/\%/a/og;
    $cat =~ s/\//b/og;
    $cat =~ s/\=/c/og;
    $cat =~ s/\n/d/og;
    $cat =~ s/\?/e/og;
    $cat =~ s/\</f/og;
    $cat =~ s/\>/g/og;
    $cat =~ s/\(/h/og;
    $cat =~ s/\)/i/og;
    $cat =~ s/\!/j/og;
    $cat =~ s/\&/k/og;
    $cat =~ s/\[/l/og;
    $cat =~ s/\$/m/og;
    $cat =~ s/\+/n/og;
    $cat =~ s/\'/o/og;
    $cat =~ s/\"/p/og;
    $cat =~ s/\#/q/og;
    $cat =~ s/\]/r/og;
    $cat =~ s/\`/s/og;
    $cat =~ s/\\/t/og;
    $cat =~ s/\_/u/og;
    $cat =~ s/\,/v/og;
    $cat =~ s/\:/w/og;
    $cat =~ s/\*/x/og;
    $cat =~ s/\./y/og;
    $cat =~ s/\-/z/og;

    return ($cat);
}

sub decode2
{
    my $cat = shift;

    $cat =~ s/a/\%/g;
    $cat =~ s/b/\//g;
    $cat =~ s/c/\=/g;
    $cat =~ s/d/\n/g;
    $cat =~ s/e/\?/g;
    $cat =~ s/f/\</g;
    $cat =~ s/g/\>/g;
    $cat =~ s/h/\(/g;
    $cat =~ s/i/\)/g;
    $cat =~ s/j/\!/g;
    $cat =~ s/k/\&/g;
    $cat =~ s/l/\[/g;
    $cat =~ s/m/\$/g;
    $cat =~ s/n/\+/g;
    $cat =~ s/o/\'/g;
    $cat =~ s/p/\"/g;
    $cat =~ s/q/\#/g;
    $cat =~ s/r/\]/g;
    $cat =~ s/s/\`/g;
    $cat =~ s/t/\\/g;
    $cat =~ s/u/\_/g;
    $cat =~ s/v/\,/g;
    $cat =~ s/w/\:/g;
    $cat =~ s/x/\*/g;
    $cat =~ s/y/\./g;
    $cat =~ s/z/\-/g;

    $cat = unpack("u",$cat);

    return ($cat);
}

#
# Create the form header with the appropriate action and some optional
# input hidden input fields.
sub form_header
{
    my ($next, $mode, $var) = @_;
    
    if ($mode)
    {
	print qq{<FORM METHOD="POST" ACTION="$EMU_URL" ENCTYPE="multipart/form-data">\n};
    }
    else
    {
	print qq{<FORM METHOD="POST" ACTION="$EMU_URL">\n};
    }

    if ($next)
    {
	print qq{<INPUT TYPE="HIDDEN" NAME="passed" VALUE="$next">\n};
    }

    if ($var)
    {
	print qq{<INPUT TYPE="HIDDEN" NAME="variable" VALUE="$var">\n};
    }

#    print form_header_private();
}

sub create_directory
{
    #Usage:  &create_directory(filename, mode) -> sets group, mode, etc.
    my ($filename,$mode) = @_;
    my ($newdir, $create);

    $filename =~ s/\/$//;
    $mode = (00700 & ~$umask) || 00700;           # fall back on drwx------

#    debug "directory=$filename  mode=$mode";

    # make sure that directories are created before subdirectories
    my @dirs = split('\/', $filename);
    foreach (@dirs) {
        $newdir .= "$_/";
        $create = $newdir;
        $create =~ s/\/$//;
#        debug "$newdir $create";
        if (!-e $create && $create ne "") {
            debug "creating $create";
            if (mkdir($create, $mode))
            {
	        chmod($create, $mode);
            }
            else
            {
	        set_status("Unable to create $create: $!\n");
	        error($status);
# Why call cleanup here?
#	        cleanup();
            }
        }
    }
}

# Copies file A to file B
# Usage: copy_file(source,destination); 
#        if destination is omitted, source+.bak is assumed.
sub copy_file
{
    my ($source, $destination, $remove) = @_;

    if (!($destination))
    {
	$destination = "$source.bak";
    }
    $destination =~ s/\|//g; #weed out pipes
    if (-e $source)
    {
	if ($remove)
	{
	    move($source, $destination) || debug "Error moving $source to $destination for $user_name!";
	}
	else
	{
	    copy($source, $destination) || debug "Error copying $source to $destination for $user_name!";
	}

	return 1;
    }
    else
    {
	return 0;
    }
}

### Session File ###

# Removes files older than one day
sub session_cleanup
 {
  #REMOVES FILES OLDER THAN ONE DAY
     
     unless ($c{"disable_session_cleanup"})
     {
	 srand(time|$$);
	 my ($rand) = rand(1);

	 load_module("File::Find",0,'find');
	 if ($rand > .98)  #Every so often, check for expiry
	 {
	     # Changed -M to -A.  Gave problems under mod_perl/fastcgi 10/18/98 MM
	     my $subref = sub { ((int(-A $_) > 1) && unlink("$homedir/tmp/$_")); };
	     if ($homedir)
	     {
		 find(\&$subref, "$homedir/tmp");
	     }
	 }
     }
}

# session_start: Begin a new session
#
# Session file format:
# 
# variable1=value 1
# variable2=value 2
#  ...
# variablen=value n
#
#
sub session_start
{
    my $user_name = shift;
    my ($random, $number, $temp,$h,$host,$curr_session);

    debug "starting session for user $user_name";

    if (!$user_name)
    {
	debug "session_start without username!";
	EMUerror($msg{'ERR_SessionStartUsername_T'}, $msg{'ERR_SessionStartUsername_B'});
    }
   
    # user's homedir/tmp is session file path. Look for existing session file
    if (! -e "$homedir/tmp") {
        # new user, no homedir yet...
        $curr_session = 0;
    }
    else {
        debug $c{'disable_sessionID'} ." ". $query->param('disable_sessionID');
        unless ($c{"disable_sessionID"} || $query->param("disable_sessionID")==1) {
            # first thing: check session ID
            debug "check sessionID";
            my $session = $query->param('sessionID');
            if (open(SESS, "$homedir/LASTSESSION")) {
                my $lastsession = <SESS>;
                close SESS;
                if ($lastsession =~ $session) {
                    # oops, we have a repeat session... BAD
                    set_status($msg{'ERR_ImproperLogin'});

                    # make sure to remove any session files to prevent refresh
                    # # the  <...> form with unlink relies on &glob
                    # unlink <$homedir/tmp/session.*>;
                    wildrm("$homedir/tmp", '^session\.');
                    return;
                }
            }
            open(SESS, ">$homedir/LASTSESSION");
            print SESS "$session\n";
            close SESS;
        }
    }

    opendir (DIR, "$homedir/tmp");
    ($curr_session) = grep { /^session\./ } readdir(DIR);
    closedir DIR;
    debug "found session $curr_session";

    if ($curr_session ne "") {
        $curr_session =~ s/session\.(\d+)/$1/;
    }
    else {
        $curr_session = 0;
    }

    $curr_session++;
    $session_file = "$homedir/tmp/session.$curr_session";

    # OK, assigned a new session filename. We should delete all tmp files
    # in user's tmp directory because they should only be valid for a particular
    # session
    # # the  <...> form with unlink relies on &glob
    # unlink <$homedir/tmp/*>;
    wildrm("$homedir/tmp", '.*');

    debug "The session is session.$curr_session";
    
    # Lets actually touch this session file so that we have a valid session
    open(SESSION, ">$homedir/tmp/session.$curr_session") if ($curr_session);
    close(SESSION);
    return("session.$curr_session");
}


sub create_dirtree {
    my ($setdefaults);

    $setdefaults = 0;
    if (!(-e "$homedir"))
    {
	create_directory("$homedir");

        debug "creating $homedir, setdefaults=1";
	# tell the caller that we need to set the defaults
	$setdefaults = 1;
    }
    if (!(-e "$homedir/messages"))
    {
	create_directory("$homedir/messages");
        $setdefaults += 1;
    }
    if (!(-d "$homedir/tmp"))
    {
        unlink ("$homedir/tmp") if (-e "$homedir/tmp");
	create_directory("$homedir/tmp");
        $setdefaults += 1;
    }
    if (!(-e "$homedir/files"))
    {
	create_directory("$homedir/files");
        $setdefaults += 1;
    }
    if (!(-e "$homedir/folders"))
    {
	create_directory("$homedir/folders");
        $setdefaults += 1;
    }
    if (!(-e "$homedir/folders-ordered"))
    {
	create_directory("$homedir/folders-ordered");
        $setdefaults += 1;
    }

    if ($c{"custom_process_dir"}) {
        load_module("EMU::Custom");
        debug "Forcing Call to process_dir($user_name)";
        &EMU::Custom::process_dir($user_name);
    }

    # only indicate setdefaults if not remote_only or userdb hasnt been created
    $setdefaults = 0 if (bool($c{"remote_only"}) && -e "$homedir/userdb");

    debug "setdefaults is $setdefaults after create_dirtree";

    return $setdefaults;
}


#
# setup the user's environment. home directories and stuff.
sub session_home
{
    return if (exists($v{"SESSION_HOME"}));

    my $setdefaults = 0;

    # MM 12/14/98: Cleanup for remoteonly/no persistance types
    # delete all of the user's file if account persistance is turned off
    if ($c{'disable_account_persistence'})
    {
        untie %userdb;
        untie %folderdb;
	deltree($homedir);
        $setdefaults = 1;

        # clear out session info
        %v = ();
    }

    # Delete messages/tmp files if the EMUtype is remote_only
    if ($c{'remote_only'})
    {
	deltree("$homedir/messages");
#	deltree("$homedir/tmp");
	deltree("$homedir/folders", '.external');
# Hmm, we don't want to remove external mailboxes.
#	deltree("$homedir/folders/.external");
	deltree("$homedir/folders/.imap");
	deltree("$homedir/folders-ordered");
    
#        delete_in_db("folder:.*");
#        foreach my $k (grep(/^folder:/, keys %userdb)) {
#           $k =~ /folder:(.+?):.*/;
#           my $f = $1;
#           if (!$userdb{"folder:$f:external"}) {
#                delete $userdb{$k};
#           }
#        }   

        # clear out session info
        %v = ();
    }


    if (!-d "$homedir" || !-d "$homedir/messages" || !-d "$homedir/tmp") {
        create_dirtree();
    }

    # OK, for the above types we delete... but must re-create in order
    # to go on...

    # Allow admin to do his own setup stuff
    if ($c{"first_login_sub"})
    {
	load_module("EMU::Custom");

	debug "Evaling first_login($user_name)";

	eval
	{
	    &EMU::Custom::first_login($user_name);
	};
    }

    open_session_file(1) unless (exists($v{"SESSION_OPEN"}));

    # 07/27/98: let the admin configure...
    if (not $c{'disable_ipaddr_check'})
    {
	$v{"remote_addr"} = $ENV{"REMOTE_ADDR"};
	debug "set remoteaddr to ",$ENV{'REMOTE_ADDR'};
    }

    #Moved this block to the bottom of session_home.  Was causing an error on some OS.
    # 10/25/98 
    $v{"user_name"} = $user_name;
    $v{"popuser"} = $popuser;
    $v{"pophost"} = $pophost;
    $v{"password"} = code($password);
    $v{"emu_type"} = $emu_type;
    $v{"protocol"} = $protocol; #04/30/99 MM: Why does this need to be here?

    debug "setdefaults $setdefaults";
    set_default_options() if ($setdefaults);

    $v{"SESSION_HOME"} = 1;
}

# session_check
#
# verify that the session is valid by checking for available session
# file, matching hostnames, and activity timeout
sub session_check
{
    my ($username, $remote_addr, $time, %tmp);
    
    session_home() if ($query->param('first'));

    # read in data from the session file
    if (open_session_file(1) < 0)
    {
	set_status($msg{'ERR_SessionCheckNoFile_S'});
	error($status);
	return 0;
    }

    # 07/27/98: allow the admin to configure whether or not to check ipaddresses. Times when the
    # admin would want to disable this is when most of the users are coming through a proxy server.
    if (not $c{'disable_ipaddr_check'})
    {
	if ( ($v{"remote_addr"} ne $ENV{"REMOTE_ADDR"}) )
	{
	    set_status("Remote addresses do not match!");
	    debug("Remote addresses don't match for $user_name ($v{'remote_addr'}/$ENV{REMOTE_ADDR})");
	    return 0;
	}
    }

    return 1 if ($c{"ignore_session_expiration"});

    my $delta = time - $v{"time"};
#    debug "delta is $delta";

    if (defined $v{time} && $delta > $c{'max_time'})
    {
        # only do activity timeout if this is not a message composition
        # return 1 if ($query->param('passed') eq "compose_parse");

        debug "expired. max_time is ".$c{'max_time'};
	set_status(convert($msg{'ERR_SessionActivity'}, $delta));
	return 0;
    }


    # enable voice based on system setting and user preference :
#    debug("userdb{'options.user_voice_enabled'} = ". $userdb{'options.user_voice_enabled'} .", c{'site_voice_enabled'} = $c{'site_voice_enabled'}");
#    if( $userdb{'options.user_voice_enabled'} == 1 && $c{'site_voice_enabled'} == 1 )
#    {
#	$voice_enabled = 1;
#	debug("voice_enabled set to 1");
#    }
#    else
#    {
#	debug("voice_enabled = 0");
#    }


#    debug "session_check exiting fine";
    
    return 1;
}


# sub open_session_file
#
# If called with a string of either "CHECK" or "READ", this function
# opens the session file to the appropriate filehandle. When called
# with neither CHECK nor READ it opens the filehandle TMP as a
# {session}.tmp file.
# This function should only be called within the lib.
#
# Returns: 0 on open failure, 1 otherwise
#
#  open_session_file("FHNAME"); # if FHNAME != (CHECK or READ) then a temp file is used

sub open_session_file
{
    my ($from_sess_home) = @_;

    return if (exists($v{"SESSION_OPEN"}));

    if (!-f "$homedir/tmp/$qs") {
        debug "session file $homedir/tmp/$qs not found!";
        return -1;
    }

    debug "open session file $homedir/tmp/$qs";
    
    if ( $from_sess_home && !$c{"remote_only"} && -e "$homedir/tmp/SESSIONLOCK") {
        # FIXME; RB: what this timeout for?
        # db_timeout("$homedir/tmp/SESSIONLOCK",1); 
        # after going thru timeout, if there's also a regular LOCK, remove it
        $ELocks->lock_remove('LOCK');
    }

    $ELocks->lock_remove('SESSIONLOCK'); # RB: is it ok?
    $ELocks->lock_create("$homedir/tmp/SESSIONLOCK", 'SESSIONLOCK', {mode => 'write', nb => 1}, 1);
    %v = read_config("$homedir/tmp/$qs");
    $v{"SESSION_OPEN"} = 1;

    return 1;
}

sub get_session_obj
{
   my ($var) = @_;
   
   my $data = $v{$var};

   if (defined $data) {
      my $val = eval($data);   
      return $val if ref $val;
   }
   
   return;
}
 
sub set_session_obj
{
   my ($var, $obj) = @_;
   
#   debug "Setting session var '$var' to '$obj'";

   # Allow the session var to be undefined. Check to make sure that an 'undef' was actually passed in, though.
   if (!defined($obj) && @_ == 2) {
      $v{$var} = undef;
   } 
   elsif (defined($obj)) {
      $v{$var} = Dumper($obj);
   }
}

sub read_config {
    my ($file) = @_;
    my (%config);
    my ($var, $value);

     open (CONFIG, "< $file") || return %config;
     while (my $cfgline = <CONFIG>)
     {
		chomp $cfgline;
		$cfgline =~ s/#.*//;
		trim(\$cfgline);
		next unless length $cfgline;
		($var, $value) = split(/\s*=\s*/, $cfgline, 2);
		$config{$var} = $value;
    }
    close CONFIG;
    return %config;
}


sub escape
{
    my $str = shift;

    # This function's existance is silly
    
#    $str =~ s/</&lt;/g;
#    $str =~ s/>/&gt;/g;
#    $str =~ s/\r|\n//g;
#    return $str;

   return &safe_html($str, '<>');    
}

# sub decode_qp
# {
#     my $res = shift;
#     debug "$res";
# 
#     if (ref($res) eq "ARRAY")
#     {
# 	my $i;
# 
# 	for ($i = 0; $i < @{$res}; $i++)
# 	{
# 	    $res->[$i] =~ s/\s+(\r?\n)/$1/g;
# 	    $res->[$i] =~ s/=\r?\n//g;
# 	    $res->[$i] =~ s/=([\da-fA-F]{2})/pack("C", hex($1))/ge;
# 	}
# 
# 	return;
#     }
# 
#     $res =~ s/\s+(\r?\n)/$1/g;  # rule #3 (trailing white space must be deleted)
#     $res =~ s/=\r?\n//g;        # rule #5 (soft line breaks)
#     $res =~ s/=([\da-fA-F]{2})/pack("C", hex($1))/ge;
# 
#     return $res;
# }

# get the filename the md5 digest -> emu postponed message filename
sub get_heldmsg_name
{
    my ($digest, $headers) = @_;
    my ($date, $subj, @headers, @date);

    # if we don't have headers then don't look it up
    return $digest unless defined($headers);

    @headers = split("\0", $headers);

    debug "headers are @headers";

    @date = localtime($headers[0]);
    $date = join("/", $date[4]+1, $date[3], $date[5]+1900);
    $subj = $headers[1] || "no subject";

    return "$date: $subj";
}

# parse_message
#
# this function reads in a message held in the given filename
# and returns, as an array, the the first part of the message,
# excluding any attachments.
sub parse_message
{
    my $filename = shift;
    my ($head, @msg, $foundbound, $i);
    my ($parser, $entity, @parts);

#    open(IN, $filename) || set_status("Error opening message $filename.");

    $parser = new MIME::Parser;
    $parser->ignore_errors(1);
    $parser->decode_headers(1); 
    $parser->extract_uuencode(1);
    $parser->extract_nested_messages(0);
    $parser->output_dir("$homedir/tmp");
    $parser->output_prefix(""); # empty prefix

    $entity = $parser->parse_open($filename);

    if ($entity->is_multipart) {
        @msg = getFirstPart($entity->parts());
    }
    else {
        if (my $io = $entity->open("r")) {
            while (defined($_ = $io->getline)) { push(@msg, $_) }
            $io->close;
        }
#        @msg = @{$entity->body()};
    }

#    close(IN);

#    chomp(@msg); #Get rid of newlines.
#debug "msg is ". join("",@msg);
    return @msg;
}


# sub view_postponed_msg (\@$)
#
sub view_postponed_msg
{
    my ($headers, $filename) = @_;
    my (%headers, $date);

    $date = shift @$headers;

    foreach (0..$#HEADER_ORDER)
    {
	$headers{lc $HEADER_ORDER[$_]} = $headers->[$_];
    }

    $date = scalar(get_date($date));

    $headers{from} ||= $user_name;

    print <<"EOD";
From: $headers{from}
To: $headers{to}
Cc: $headers{cc}
Bcc: $headers{bcc}
Subject: $headers{subject}
Date: $date

EOD

    dump_file("$homedir/files/$filename");

    # get_heldmsg_name($filename, $heldmsgs{$filename})
 
# 07/22/98: let's get rid of these darned goto's!   
#    goto end_of_line;
#    return;
}

# delete one of the "temporary" attachments
sub delete_att
{
    my $file;

    $file = decode(basename(legalize($query->param('variable'))));

    if (!$file)
    {
	set_status("No such file $file");
	compose();
	return;
    }

    if (-e "$homedir/tmp/$file")
    {
	unlink "$homedir/tmp/$file";
	set_status(convert($msg{'MSG_AttachmentDeleted'}, $1));
    }
    else
    {
	set_status(convert($msg{'ERR_AttachmentMissing'}, $file));
    }

    compose();
    return;
}


# delete the message currently being viewed and then toss the user
# back to the index page
sub delete_msg
{
    my $message;
    my $index=0;

    debug "deleting currently selected message";

    my $searchfold = $msg{"FOLD_Search_Results"} || "Search Results";
    if ($folder eq $searchfold) {
        set_status($msg{"ERR_DeleteSearchMsg"});
        go_index();
        return;
    }

    #delete a message
    $message = $query->param('variable');
    $message =~ s%/%%g;

    my @msg = ($message);
    $index = del(\@msg, 0, $folder);

    set_status($msg{'MSG_MessageDeleted_S'});

    delete($foldmap{$message});

  POP_MUST_QUIT:
    {
        last if (!$pop || $userdb{"folder:$folder:protocol"} !~ /pop/i ||
                 ref $pop ne 'EMU::POP3');

        # Quit to make sure we really delete    
        undef %poplist;
        $pop->quit() if $pop;
#        debug "quitting pop";
        undef $pop;
        $pop_connected = 0;
    }

  IMAP_EXPUNGES:
    {
        last if (!$pop || $userdb{"folder:$folder:protocol"} !~ /imap/i ||
                 ref $pop ne 'EMU::IMAP');

        $pop->expunge();
    }

    go_index(1);
# Why call cleanup here?
#    cleanup();
    return $index;
}


sub allowed_domain
{
    my ($host) = @_;
    my $domains = $licensed{mailhosts} || $c{allowed_domains};
            
    return 1 if (!$domains);

    foreach my $allowed (split(/\s+/, $domains))
    {
	# mooh. compare the domain parts... if we have ALLOWED as dotshop.com and we need to check
	# if smoo.dotshop.com is allowed, what it does is get an offset in the host (which
	# should always be longer than the domain) and then compare the string from that offset.
	# The offset is the difference of the lengths of the addresses, so with the above example
	# we'd get index("dotshop.com", "dotshop.com", 5). If the host were something like oh.saidar.net
	# then we'd get index(".saidar.net", "dotshop.com", 2). This would, of course, fail. So
	# we know that whatever that host was, it's not in the allowed domain
	return 1 if (index(lc $host, lc $allowed, abs(length($allowed) - length($host))) != -1);
    }

    return 0;
}


sub allowed_host ($$)
{
    my ($uhost, $qhost) = @_;

    return index(lc $uhost, lc $qhost, abs(length($qhost) - length($uhost))) != -1;
}

sub print_header
{
    my ($str) = @_;

    return if ($header_printed);

    if (!$header_printed && !$waiting_printed)
    {
	my $ct = $c{global_content_type} ||  "text/html";
	print "Content-type: $ct\r\n";
	$header_printed = 1;
    }

    unless ($c{"disable_cache_headers"})
    {
	my $cache;
	$cache = $c{"cache_headers"} || "Cache-Control: no-store, private";
	print "$cache\r\n";
#        debug "$cache";
    }

    # RMK 19990319 added Pragma: no-cache as user-configurable
    if (bool($c{"disable_caching"})) {
        print "Pragma: no-cache\r\n";
#        debug "Pragma: no-cache";
    }
    
    if ($extra_head)
    {
	print $extra_head;
    }

    print "\r\n";               # end it all
}


# convert size bytes into a more readable form
sub get_size
{
    my $size = shift;

    if ($size < 100000)
    {
	$size =~ s/(.*\d)(\d\d\d)/$1,$2/; # makes the numbers (n,nnn)
	$size =~ s/(.*)/$1/;
	if ($size eq "") { $size = "???"; }
    }
    elsif ( ($size> 99999) && ($size< 1000000) )
    {
	$size =~ s/(\w\w\w)(.*)/$1K/;
    }
    elsif ( ($size > 999999) && ($size < 10000000) )
    {
	$size =~ s/(\w)(.*)/$1+ MB/;
    }
    else
    {
	$size = "BIG";
    }

    return $size;
}

# view_emufile
#
# This function allows the user to view a file from their list of
# EMUfiles. The only parameter it needs is a function reference
# which is used as a callback to return to.
#
sub view_emufile
{
    no strict 'refs';

    my ($filename, $callback) = @_;
    my ($content_type, $force);

    debug "FILE is $filename, callback is $callback";
    if (!$filename)
    {
	($filename, $callback) = split(/:/, $query->param('variable'));
	debug "GETTING FILENAME FROM URL";
    }

    if (!$callback)
    {
	# 08/21/98: instead of taking them to an error page, take them back to the index
#       set_status($msg{'ERR_MissingCallback'});
	go_index();
	return;
    }
	
    debug "callback=$callback";

    if (!$filename)
    {
	set_status($msg{'ERR_EmufileInvalid'});
	&$callback();
	return;
    }
   
    $force = $query->param('force');
    
    if ($filename =~ m{^[\./]}) # illegal
    {
	debug("Illegal filename: $user_name: @_: $filename");
	set_status($msg{'ERR_EmufileIllegal'});
	&$callback();
	return;
    }

    # sys0 is SYSTEMFILEDIR, sys1 is SYSXTRADIR
    if ($filename =~ /^(sys[01]):(.*)/)
    {
	my $syst = $1;

	$filename = legalize(basename($2));
	
	if ( ($syst eq "sys0" && !-e "$SYSFILEDIR/$filename")
	     || ($syst eq "sys1" && !-e "$SYSXTRADIR/$filename") )
	{
	    set_status($msg{'ERR_SysfileMissing'}, $filename);
	    &$callback();
	    return;
	}

	$content_type = find_mime_type($filename);

	if (!$force && (lc($content_type) eq "application/msword") && 
            !bool($c{'disable_msword'}) && 
            !bool($userdb{"options.disable_msword"}))
	{
	    print "Content-type: text/html\n\n";
	    write_tmp("attachurl",make_url("view_emufile", "$filename:$callback", force => 1));
            my $wb = word_convert($filename);
            write_tmp("word_body",$wb);
	    &load_page("wordview.html");
	    return;
	}
	else
	{
	    my $f = $filename;
	    $f =~ s/\"|\s/_/g;
	    print "Content-disposition: attachment; filename=$f\n";
	    print "Content-type: $content_type\n\n";
	    debug "Content-type: $content_type\n\n";
	    dump_file( ($syst eq "sys0" ? $SYSFILEDIR : $SYSXTRADIR) . "/$filename" );
	}
	
	return;
    }
    
    if (!-e "$homedir/files/$filename")
    {
	$filename = get_heldmsg_name($filename, $userdb{"postponed.$filename"});
	
	set_status(convert($msg{'ERR_EmufileMissing'}, $filename));
	&$callback();
    }
    else                        # file exists
    {
	# if it's a message then we format it and output a nice page for the user to view
	if ($filename =~ /^[0-9a-f]{32}$/)
	{
	    my @headers = split("\0", $userdb{"postponed.$filename"});
#            print "Content-type: message/rfc822\n\n";
#           print "Content-type: text/plain\n\n";
	    view_postponed_msg(\@headers, $filename);
	}
	else
	{
	    $content_type = find_mime_type($filename);     

	    debug "CT: $content_type !";
	    
	    # 08/20/98: allow the user to disable word support
	    if (!$force && (lc($content_type) eq "application/msword") && 
                !bool($c{'disable_msword'}) && 
                !bool($userdb{"options.disable_msword"}))
	    {
		debug "WORD DOCUMENT";
		write_tmp("attachurl",make_url("view_emufile", "$filename:$callback", force => 1));
                my $wb = word_convert("$homedir/files/$filename");
                write_tmp("word_body",$wb);
		&load_page("wordview.html");
	    }
	    else
	    {
#               print "Content-type: $content_type\n\n";
		&print_content_headers($content_type,$filename);
		dump_file("$homedir/files/$filename");
	    }
	}
    }
    
#    dbmclose(%userdb);
    return;
}

	    
# word_convert
#
# given a filename or an array ref corresponding to a word document,
# conver the data to plain text and then dump it to STDOUT
sub word_convert
{
    my $filename = shift;
    my $wb;

    legalize ($filename);

    debug "converting $filename";
    if (ref $filename ne "ARRAY" && !-e $filename)
    {
	set_status($msg{'ERR_WordConvert'});
	return;
    }

    if ($licensed{"custom_msword"} &&
            bool($c{"fancy_msword_conversion"}) && 
            -e $c{"msword_converter"} &&
            -x $c{"msword_converter"}) {
        debug $c{"msword_converter"};
        debug "running ".$c{"msword_converter"}." $filename";
        my $convert = $c{"msword_converter"};
        $wb = `$convert $filename`;
        write_tmp("custom_wc", 1);
    }
    else {
        # 04/30/99 -- Moved this to here doing it only as needed.
        load_module("EMU::WConvert");

        write_tmp("custom_wc", 0);
        eval {
            $wb = EMU::WConvert::convert($filename);
        };
    }

    debug "word body = $wb";
    return $wb;
}


# del_emufile
#
# This function will delete the selected file (if valid and not out
# of our security scope). 
sub del_emufile
{
    my ($filename) = @_;
    my %heldmsgs;
 
    if (!$filename || $filename =~ /^\s*$/)
    {
	set_status($msg{'ERR_EmufileInvalid'});
	return;
    }
    
    # if it's a system file, they can't delete it
    if ($filename =~ /^(sys[01]):(.*)/)
    {
	my $syst = $1;

	$filename = $2;
	
	# SYSFILEDIR
	if ( ($syst eq "sys0" && -e "$SYSFILEDIR/$filename")
	     || ($syst eq "sys1" && -e "$SYSXTRADIR/$filename") )
	{
	    set_status(convert($msg{'ERR_EmufileDelete'}, $2));
	    return;
	}
    }
    
    if ($filename =~ m{^[\./]})
    {
	debug ("Illegal filename: $user_name: @_: $filename");
	set_status($msg{'ERR_EmufileIllegal'});
	return;
    }
    
    $filename = legalize(basename($filename));
    if (!-e "$homedir/files/$filename")
    {
	$filename = get_heldmsg_name($filename, $userdb{"postponed.$filename"});
	
	set_status(convert($msg{'ERR_EmufileMissing'}, $filename));
	return;
    }
    
    if (unlink "$homedir/files/$filename")
    { 
	$filename = get_heldmsg_name($filename, $userdb{"postponed.$filename"});
	
	set_status(convert($msg{'MSG_EmufileDeleted'}, $filename));
    }
    else
    {
	$filename = get_heldmsg_name($filename, $userdb{"postponed.$filename"});
	
	set_status(convert($msg{'ERR_EmufileDelete'}, $filename));
    }
    
#    dbmclose %userdb;

    return;
}

# upload_emufile
#
# This function will read in the data from a file upload field and place
# it into the directory specified.
#
# Parameters are:
#   1. the uploaded filename (just gimme the field's param from CGI object)
#   2. the directory to move the file to
sub upload_emufile
{
    my ($filename, $dir, $callback) = @_;
    my $file;

    no strict 'refs';

    $file     = legalize(basename($filename));

    debug "file=$filename  dir=$dir  callback=$callback";

    if (!$file || $file =~ /^\s*$/)
    {
	set_status($msg{'ERR_EmufileUploadSelected'});
	return &$callback();
    }

    open(FILEOUT, "$homedir/tmp/$file");
    binmode(FILEOUT);

    my $fh = $query->upload('tmpupload');

    if (!$fh)
    {
        set_status(convert($msg{'ERR_UploadFailed'}, $query->param('tmpuload'), $query->cgi_error));
        return &$callback();
    }

    while (<$fh>) {
        print FILEOUT $_;
    }

    close(FILEOUT);

    if (-z $file)       # 0 byte file!
    {
        debug("$user_name uploading a 0 byte file");

        set_status(convert($msg{'ERR_EmufileUploadEmpty'}, $file));
        return &$callback();
    }

    set_status(convert($msg{'MSG_EmufileUploaded'}, $file));

    &$callback();
}

sub set_status
{
    debug "Setting status to $_[0]";
    debug "extra_status $extra_status";
    $status = shift;
    $status = "$extra_status, $status" if ($extra_status);
}


sub FatalError
{
    my ($title, $phrase) = @_;

    print_header();

    print <<"EOD";
<HTML>
<HEAD>
<TITLE>$title</TITLE>
</HEAD>
<BODY BGCOLOR="ffffff" TEXT="000000">
<P><BR>
<CENTER>
<H2>
$phrase
</H2>
</CENTER>
</BODY>
</HTML>
EOD

    exit 1;
}

# print a header, print an error message and then exit (cleanup())
sub EMUerror
{
    my ($title, $text, $nologintext) = @_;

    write_tmp("phrase", $text, 1);
    write_tmp("title", $title || "Error", 1);
    write_tmp("status", $status, 1);
    write_tmp("logintext", !$nologintext);

    load_page("errors.html");

# Why call cleanup here?
#    cleanup();
}



sub get_ihelp
{
    my ($helpname, $props, $font) = @_;

    $font ||= $FONT_IHELP;

    if (get_var("ihelp_checked") && exists $ihelp{$helpname})
    {
	return "<TD COLSPAN=3 $props>$font $ihelp{$helpname}</FONT></TD></TR>\n<TR>\n";
    }

    return undef;
}


sub print_emufiles_compose
{
    my (@files, @arr, $a, $selected);

    opendir DIR, "$homedir/files";
    @files = grep ( !/^\.|^[0-9a-f]{32}$/, readdir DIR);
    closedir DIR;
    
    debug "selected is ", $query->param('selected_file');
    
    @arr = $query->param('selected_file');
    @arr = map { $_ =~ s/^(sys[01])://; $_; } @arr;
 
    if (!@arr)
    {
	$arr[0] = $query->param('selected_file');
	$arr[0] =~ s/^(sys[01])://;
    }
    
    foreach (@files)
    {   
	$selected = "";
	foreach $a (@arr)
	{ 
	    if ($a eq $_)
	    {
		$selected = "SELECTED";
		last;
	    }
	}
	
	print qq{   <OPTION VALUE="$_" $selected>}, substr($_, 0, 30), "\n";
    }
    
    if (@files == 0)
    {
	print qq{   <OPTION VALUE="">\n};
    }
    
    print qq{   <OPTION VALUE="">-- System Files --\n};
    
    opendir DIR, $SYSFILEDIR;
    @files = grep (!/^\./, readdir DIR);
    closedir DIR;
    
    foreach (@files)
    {
	print qq{    <OPTION VALUE="sys0:$_">}, substr($_, 0, 30), "\n";
    }


    if ($SYSXTRADIR)
    {
	opendir DIR, $SYSXTRADIR;
	@files = grep (!/^\./, readdir DIR);
	closedir DIR;
	
	foreach (@files)
	{
	    print qq{    <OPTION VALUE="sys1:$_">}, substr($_, 0, 30), "\n";
	}
    }
}

sub basename
{
    my $fullpath = shift;
    my $basename;

    $fullpath =~ s/\%20/_/g;    # switch spaces to underscores
    
    if ($fullpath =~ m/[\\|\/]/)
    {
	($basename) = $fullpath =~ m/.*[\\|\/](.*)/;
    }
    else
    { 
	$basename = $fullpath;
    }

    return $basename;
}


#
# expand and unexpand tabs as per the unix expand and 
# unexpand programs.
#
# expand and unexpand operate on arrays of lines.  
#
# David Muir Sharnoff <muir@idiom.com>
# Version: 4/19/95
sub expand
{
    my (@l) = @_;
    my ($l, @k);
    my $nl;
    for $l (@l) {
	$nl = $/ if chomp($l);
	@k = split($/,$l);
	for $_ (@k) {
	    1 while s/^([^\t]*)(\t+)/
		$1 . (" " x 
		      (8 * length($2)
		       - (length($1) % 8)))
		    /e;
	}
	$l = join("\n",@k).$nl;
    }
    return @l if $#l > 0;
    return $l[0];
}

sub unexpand
{
    my (@l) = &expand(@_);
    my @e;
    my ($k, @k);
    my $nl;
    my $x;
    
    for $k (@l) {
	$nl = $/ if chomp($k);
	@k = split($/,$k);
	for $x (@k) {
	    @e = split(/(.{8})/,$x);
	    for $_ (@e) {
		s/  +$/\t/;
	    }
	    $x = join('',@e);
	}
	$k = join("\n",@k).$nl;
    }
    return @l if $#l > 0;
    return $l[0];
}


# 07/22/98
# Different types of input verification that we can perform. All of these types will
# accept a blank space
sub v_Alpha { shift =~ /^\w*$/ }                # true if plain alphanumeric, no spaces
sub v_Num { shift =~ /^\d*$/ }                  # true if numeric
sub v_Any { 1 }                                 # always true
sub v_AlphaWithSpace { shift =~ /^[\w\s]*$/ }   # true if alphanumeric with spaces

sub version
{
    my $exp = $EMU::expire || "never";
    print <<"INEND";
Content-type: text/html

<html>
<head><title>EMUmail Version Information</title></head>
<body bgcolor=white>
<font size=4>
<table border=1>
<tr><td>OS</td><td>$^O</td></tr>
<tr><td>Version</td><td>$EMU::Version</td></tr>
<tr><td>Edition</td><td>$EMU::Edition&nbsp;</td></tr>
<tr><td>Revision</td><td>$EMU::Revision</td></tr>
<tr><td>Date</td><td>$EMU::Date</td></tr>
<tr><td>Distribution</td><td>$EMU::dist</td></tr>
<tr><td>Path</td><td>$0</td></tr>
<tr><td>Language</td><td>$EMU::Language</td></tr>
<tr><td>Exp</td><td>$exp</td></tr>
</table>
</font>
</body>
</html>
INEND
}


sub set_default_compose {
    # Set the default state of the compose message options
    my (@compose_opts) = split(/\s*,\s*/, $c{'default_compose'});
    debug "default compose_opts @compose_opts";

    for (@compose_opts)
    {
	if (/^(?:attach|emufile|cc|bcc|from|replyto|priority|ihelp)$/)
	{
            debug "Setting $_ as default.\n";
	    $userdb{"options.$_.show"} = 1;
	}
    }
}


sub set_default_addresses {
    my @addresses = sort addrly(grep/^default_address\d+$/, keys %c);
    if (@addresses)
    {
	my ($nick, $name, $email, %addrbook);

	debug "Addresses are @addresses";

	for (@addresses)
	{
	    debug "address line is $c{$_}";
	    
	    ($nick, $name, $email) = split(/\|\|/, $c{$_}, 3);
	    $userdb{"addresses.$nick"} = join(':', $email, $name)
                if (!exists($userdb{"addresses.$nick"}));
	}
    }
}


sub set_default_filters {
    my @filters = sort alpha grep(/^default_filter\d+$/, keys %c);
    if (@filters)
    {
	my ($field, $modifier, $data, $dest, $flag, $i);

	$i = 1;

	debug "Filters are @filters";

	for (@filters)
	{
	    debug "filter line is $c{$_}";

	    ($field, $modifier, $data, $dest, $flag) = split(/\|\|/, $c{$_});

	    # we've gotta be sure that the filter name they're adding actually exists.

	    debug "field=$field   modifier=$modifier  data=$data  dest=$dest  flag=$flag";

	    $userdb{"filters.type$i"}     = filter_type($field);
	    $userdb{"filters.modifier$i"} = $modifier eq "notcontains" ? FILTER_DEVOID : FILTER_CONTAINS;
	    $userdb{"filters.data$i"}     = $data;
	    $userdb{"filters.action$i"}   = $dest;
	    $userdb{"filters.bRegex$i"}   = $flag eq "yes" ? 1 : 0;

	    $i++;
	}
	$userdb{"filters.total"} = $i - 1;
    }
}


sub set_default_options
{
    my $email=$user_name;

    debug "email $user_name";

	$userdb{'options.filter_spam'}      = 0;
	$userdb{'options.filter_spam_folder'} = '';
    $userdb{'options.prefix'}           = $c{'default_imap_prefix'};
    $userdb{'options.prefix'}           =~ s/\/+$//g;
    $userdb{'options.encoding'}         = $c{'default_encoding'};
    $userdb{'options.email'}            =  do_perlsub($c{'perlsub_default_email'},$email) || parse_default_email($email) || $email;

    #$userdb{'options.mailloc'}          = bool($c{'default_mail_local'}) || bool($c{'force_mail_local'}) || 0;
    $userdb{'options.signature'}        = $c{'default_signature'};
    $userdb{'options.real_name'}        = $c{'default_real_name'};
    $userdb{'options.organization'}     = $c{'default_organization'};
    $userdb{'options.checkmail'}        = $c{'default_checkmail'} || 300;
    $userdb{'options.mailcheck_popup'}  = $c{'default_mailcheck_popup'};
    $userdb{'options.quoted_reply'}     = 1;
#    $userdb{'show_folder_stats'}        = 1;

    # Default the top level folder menu to being open
    $userdb{'options.menu.main'} = 1;

    if ($c{'default_autoload'} eq undef) {
        $userdb{'options.autoload'}     = 1;
    }
    else {
        $userdb{'options.autoload'}     = bool($c{'default_autoload'});
    }

    $userdb{'options.show_html'}        = bool($c{'default_interpret_html'}) || bool($c{"view_display_HTML"});
    $userdb{'options.basic_header'}     = bool($c{'default_show_headers'});
    $userdb{'options.max_messages'}     = positive($c{'max_messages'}) || 15;
    $userdb{'options.DontsynchronizePOP'}   = bool($c{'dont_sync_pop'}) || 0;

    # Added msword conversion control
    $userdb{'options.disable_msword'} = bool($c{'disable_msword'}) || 0;

    $userdb{"options.use_trash_folder"} = 0;

    $userdb{'options.skin'} = $c{default_skin} || 'EMU_Original';

    
    # Default Filters
    # ===============
    # delete the filters that are currently there...
    &delete_in_db("filters\.");

    set_default_filters();

    # Default Addresses
    # =================
    set_default_addresses();
    
    # Default Compose
    # ===============
    # reset compose options
    for (qw[attach emufile manager cc bcc from replyto priority ihelp])
    {
	$userdb{"options.$_.show"} = 0;
    }

    # fill it with default options
    set_default_compose();

    # Default Folders
    # ===============
    # possible security problem if they specify default_folder1 = ../../mooh
    # .. but if the admin is doing that.... /Jah
    my @folders;
    map { push(@folders,$c{$_}); } (grep(/^default_folder\d+$/, keys %c));
    map { create_folder("$_","local") if (!folder_exists($_)) } @folders;
}


# parse an email
sub parse_default_email
{
    my $email = shift;
    my (@hostpart, $newemail);

    if ($c{'add_domain_to_user'} ne "") { return undef; }

    my ($user, $host) = split('@', $email, 2);
    @hostpart = reverse split(/\./, $host);

    $newemail = $c{'default_email'};
    $newemail =~ s/\%u/$user/g;
    $newemail =~ s/\%h/$host/g;
    $newemail =~ s/\%(\d+)/$hostpart[$1 - 1]/g;

    debug "newemail is $newemail";
    return $newemail;
}

sub filter_images
{
    my ($html) = @_;
    
    $html =~ s/<img\s.*?>/<img src='$c{img_url}\/image_filtered.gif'>/ig;
    return $html;
}
    
sub get_address_string
{
    my ($field, @selected) = @_;

    return unless ($field || @selected);

    my (@fields, $i);

    $field =~ s/ //g;           # no spaces

    # get the comma separated addresses (from the textfield)
    @fields = split(",", $field);

    debug "\@fields are @fields. size is ", scalar(@fields);

    for ($i = 0; $i < @fields; $i++)
    {
	# if there isn't an @ sign then look it up in the addressbook
	if (-1 == index($fields[$i],"@")) # check it up in the addressbook
	{
	    if ($userdb{"addresses.$fields[$i]"})
	    {
		# grab the email address
		$fields[$i] = (split(':', $userdb{"addresses.$fields[$i]"}, 2))[0];
		debug "fields[$i] = $fields[$i]";

	    }
	    else
	    {
                my $sendhost = (split(' ', $c{'default_send_host'}))[0];
                $fields[$i] .= "\@" . $sendhost;
	    }
	}
    }

    $field = join(", ", @fields, @selected);
    return $field;
}


sub filter_name
{
    my $num = shift;
    my $name;

    $name = "Off" if $num == FILTER_OFF;
    $name = "Body" if $num == FILTER_BODY;
    $name = "To" if $num == FILTER_TO;
    $name = "From" if $num == FILTER_FROM;
    $name = "Subject" if $num == FILTER_SUBJ;
    $name = "Header" if $num == FILTER_HEAD;
    $name = "Any" if $num == FILTER_ANY;

    debug "returning name $name for $num";

    return $msg{"V_FilterName$name"};
}


sub filter_type
{
    my $name = shift;
    my $num;

    debug "==============================================";
    
    $name = lc($name);

    $num = FILTER_OFF if $name eq "off"; #$msg{'V_FilterNameOff'};
    $num = FILTER_BODY if $name eq "body"; #$msg{'V_FilterNameBody'};
    $num = FILTER_TO if $name eq "to:"; #$msg{'V_FilterNameTo'};
    $num = FILTER_FROM if $name eq "from:"; #$msg{'V_FilterNameFrom'};
    $num = FILTER_SUBJ if $name eq "subject:"; #$msg{'V_FilterNameSubject'};
    $num = FILTER_HEAD if $name eq "header"; #$msg{'V_FilterNameHeader'};
    $num = FILTER_ANY if $name eq "any"; #$msg{'V_FilterNameAny'};

    $num ||= FILTER_OFF;

    debug "returning type $num for name '$name'";
    return $num;
}

sub help
{
    print "Content-type: text/html\n\n";
    debug "Content-type: text/html\n\n";
    print qq!<META HTTP-EQUIV="Refresh" CONTENT="0; URL=$c{'help_url'}">!;
}

sub map_config
{
    my ($file,$rh) = @_;
    my ($ob,$key,$value);

    debug "$file";
    $ob = new EMU::Config $file;
    if (!$ob) {
        debug "BAD: $file wasn't able to produce a valid EMU::Config object!";
        return;
    }

    if (!$ob->readConfig()) {
        debug "BAD: EMU::Config::readConfig returned false (file: $file)";
        return;
    }

    my $r = $ob->getConfig;
   
    if (!$r || ref($r) ne 'HASH') {
        debug "BAD: EMU::Config::getConfig didnt return a valid ref ($r) for file: $file";
        return;
    }

    while ( ($key,$value)=each(%$r) ) {
#   debug "Assigning: $key => $value";
        $rh->{$key} = $value;
    }
   
    return 1;
}


# Jah. Evaluate a perlsub and return the value
sub do_perlsub
{
    my ($perlsub, @vars) = @_;

    return unless defined($perlsub);

    $perlsub =~ s/^\s*{// && $perlsub =~ s/\s*}\s*$//;

    if ($perlsub)
    {
	my ($subref) = eval("sub { $perlsub }");

	debug "sub=$perlsub";

	if (defined($subref))
	{
	    return &$subref(@vars);
	}
	else
	{
	    error("Unable to use $perlsub: check for validity: $@");
	}
    }
    
    undef;
}

sub getpath
{
    my ($user, $sub) = @_;

    $user =~ s/\s//g;
    $user = lc($user);
    $sub = $sub || $c{'perlsub_user_home'};

debug "user $user";
    $sub =~ s/^\s*{// && $sub =~ s/\s*}\s*$//;

    if ($sub)
    {
	my ($subref) = eval("sub { my(\$emailaddr) = \$_[0]; $sub }");

#	debug "sub=$sub";

	if (defined($subref))
	{
	    return &$subref($user);
	}
	else
	{
	    error("Unable to use perlsub_user_home: check for validity: $@");
	}
    }
    
    # ok, not using perlsub. Normally just return $user, but if we have
    # double @'s or other combinations, then let's do it differently
    if ($user =~ /.*@.*@/ || $user =~ /.*#.*@/) {
        # grab last set after @ and make it the "domain"
        my $last_at = rindex($user, "@");
        my $domain = substr($user, $last_at+1);
        my $tmp_user = substr($user, 0, $last_at);
#        debug "split user name: $tmp_user, $domain";
        return "$page_root/homes/$domain/$tmp_user";
    }

    return "$page_root/homes/".lc($user);
}


sub safe
{
    my ($cit, $k) = @_;
    my ($c);

    return unless length($cit);

    for (1..length($cit))
    {
	$c = substr($cit,$_-1,$_);
	$k =~ s/$c/"%".unpack("c*",$c).";"/ge;
    }

    return $k;
}

sub desafe
{
    my ($s) = @_;

    $s =~ s/\%([\da-f]+);/debug("1=$1"),pack("c",$1)/ge;

    return $s;
}


sub is_set
{
    my ($s) = @_;

    return $s ne "";
}

sub trim 
{
    my ($s) = @_;

    $$s =~ s/^\s*//;
    $$s =~ s/\s*$//;

    1;
}

sub folder_exists
{
    my ($fold) = @_;
    my $ret;

#    debug "folder $fold exists? ".defined($userdb{"folder:$fold:protocol"});

    my $prot = get_folder_protocol($fold) or return;

    return 0 if (!defined($userdb{"folder:$fold:protocol"}));

#    debug "f: $fold prot: $prot ;  \$protocol: $protocol ; userdb: ".$userdb{"folder:$fold:protocol"}." external ".$userdb{"folder:$fold:external"};

    # if userdb tells us the folder exists, but we can't find any trace of
    # it (local or external and folder file doesn't exist) then return 0
    if ( ($prot eq "local" && ! -e "$homedir/folders/$fold") ||
         ($userdb{"folder:$fold:external"} && ! -e "$homedir/folders/.external/$fold") ) {
        return 0;
    }

    # if it's an external mailbox or not imap, just check the db
    return 1 if ($userdb{"folder:$fold:external"} ||
                 $userdb{"folder:$fold:protocol"} !~ /imap/i);

    # for imap servers, let's verify existence in the server
    if ( $prot || $c{"pure_imap"} || $protocol =~ /imap/i)
    {
        $fold = remove_fold_prefix($fold) if ($prot =~ /imap/i);
	debug "Case 0";
         
#	if ( $prot !~ /imap/i || $userdb)
#	{
#	    debug "Case 1";
#            my $foldfile = process_fold_type($fold);
#	    $ret = -e "$homedir/folders/$foldfile" ? 1 : 0;
#	}
#	else
#	{
	    debug "Case 2";

            my $fc = &get_imap_fcache;
#            debug "Fcache: $fc;";

            if (ref $fc) {
                debug "Trusting fcache!\n";
                $ret = grep($_ eq $fold, @$fc)?1:0;
            }
            elsif (!exists($checked_existence{$fold})) {
	        $checked_existence{$fold} = $ret =  &check_imap_folder_existence($fold);
            }
            else {
                $ret = $checked_existence{$fold};
            }
#	}
    }
    else  # Unknown folder...
    {
	debug "Case 3";
	$ret = 0;
    }
#    debug "Folder exists? $ret";

    return $ret;
}

sub check_imap_folder_existence
{
    my ($fold) = shift;
    my ($user,$p,$host) = &get_folder_credentials($fold);
    my ($junk,$ret);

    if ($user=~/@/) {
        my ($uu,$h) = split(/\@/,$user);
        $user = $uu if (!exists($c{"appendhost_$h"}));
    }

    if ($userdb{"folder:$fold:external"} == 1 and
            $userdb{"folder:$fold:protocol"} =~ /imap/i) {
        $fold = $userdb{"folder:$fold:extra_fold"} ;
    }
    else {
        $fold = get_fold_and_prefix($fold);
    }

    debug "checking for folder $fold";

    #Wrap in an eval incase the folder select fails...
    eval 
    {

        if (ref $pop ne 'EMU::IMAP' || $pop->{user} ne $user || $pop->{host} ne $host) {
            debug "Forcing imap login... \$pop: $pop ;";
            &do_imap_login($user,$p,$host,$fold,1);
        }

        debug "calling check_node_existence";
	$ret = $pop->check_node_existence($fold);
    };

    debug "returning $ret";
    return $ret;
}

# return the passed filter type if it's valid, otherwise return FILTER_OFF
sub filter_valid
{
    if ($_[0] == FILTER_OFF || $_[0] == FILTER_TO || $_[0] == FILTER_FROM || $_[0] == FILTER_SUBJ
	|| $_[0] == FILTER_HEAD || $_[0] == FILTER_BODY || $_[0] == FILTER_ANY || $_[0] == FILTER_DELETE)
    {
	return $_[0];
    }
    else
    {
	return FILTER_OFF;
    }
}

sub dumpstack
{
    my $i=1;
    my ($func, $file, $line, $indent, $args);
    my (@args);

    while ( ($func)=(caller($i++))[3] )
    {
	$args = join(', ',@args);
	($file, $line) = (caller($i-2))[1,2];
	$func =~ s/^EMU:://;
	debug "$indent &$func($args) [$file, line $line]";
	$indent.=" ";
    }
}

sub deltree
{
    my ($dir, @exclude) = @_;
    my (@files, $file);

    opendir(DIR,$dir);
    @files = grep(!/^\.\.?/, readdir(DIR));
    closedir(DIR);

    for $file (@files)
    {
	next if grep { $_ eq $file } @exclude;

	# it's really a directory...
	if (-d "$dir/$file")
	{
	    deltree("$dir/$file");
	}
	else
	{
	    debug "Deleting $dir/$file\n";
	    unlink "$dir/$file";
	}
    }

    debug "Deleting $dir";

    my $deleted = rmdir($dir);
    debug "deleted? $deleted $!";
}

# our ceil fun
sub ceil
{
    if (int($_[0]) != $_[0])
    {
	return int(++$_[0]);
    }
    return int($_[0])
}

sub parse
{
    my ($file) = @_ ? $_[0] : $query->param('variable');
    
    # substitutions! don't let them fuck with it.
    $file =~ s/\.\.\\//g;
    $file =~ s/\/\.\.//g;

    1 while ($file =~ s/^\///);

    if (!$file)
    {
	FatalError("Parse Failed", "Unable to parse file $file");
    }

    if ($file eq "options.html")
    {
	options();
    }
    elsif ($file eq "compose.html")
    {
	compose();
    }
    elsif ($file eq "folder.html")
    {
	folders();
    }
    elsif ($file eq "lookup.html")
    {
	do_lookup();
    }
    elsif ($file eq "spelling.html")
    {
	spelling_parse();
    }
    elsif ($file eq "address.html")
    {
	address();
    }
    elsif ($file eq "logout.html")
    {
	logout();
    }
    else
    {
	debug "Loading normally ($file)";
	load_page($file);
    }
}

sub AUTOLOAD
{
    debug "Autoload called with args: ", join(" | ", @_);
}


sub do_directory
{
    my ($param,%search_fields,@params,$search_fields_list,$search_values_list);
    
  GET_FORM_DATA_TO_SEARCH_WITH:
    {
	@params = $query->param();
        debug "search params @params";
	foreach $param (@params)
	{
	    next if ($search_fields{$1} eq $query->param($param));
	    
	    if ($param =~ /^search_(.*)/)
	    {
		$search_fields{$1} = $query->param($param);
		if ($search_fields{$1})
		{
		    # It's defined, add to our search list...
		    #Build search list:
		    $search_fields_list .= "$1"."|";
		    $search_values_list .= $search_fields{$1}."|";
		    
		    #Save form data
		    write_tmp("searched_for_$1",$search_fields{$1});
		    debug "GINGER $1 ". $search_fields{$1};
		}
	    }
	}
	
	chop($search_fields_list); #Clean last '|'
	chop($search_values_list); #Clean last '|'
    }
    
    
    my ($entries, @html);
    my $doing_ldap = 1;
    
  DO_SEARCH:
	{
	    my $ldap_host = $query->param("ldap_search_host") || $c{"ldap_search_host"} || "ldap.bigfoot.com";
	    debug "searched for $search_fields_list value: $search_values_list GINGER";
	    eval 
	    {
		$entries = ldap_search($ldap_host,$search_fields_list,$search_values_list) if ($search_fields_list);
	    };
            return undef if ($entries eq undef);
            debug "did search: GINGER3 $entries";
	}	

#    $v{"ldap_entries"} = get_var("ldap_entries");
    $v{"ldap_entries"} = $entries;
    $v{"per_page"} = $c{"ldap_entries_per_page"}  || 10;
    write_tmp("next_ldap_page", 2);
    write_tmp("total_ldap_pages", ceil($v{"ldap_entries"} / $v{"per_page"}));
    write_tmp("more_ldap", $v{"ldap_entries"} > $v{"per_page"} ? 1 : 0);
    
    $v{"ldap_search_results"} = join("ldappdal", @html);
    write_tmp("have_results", 1) if (scalar(@html));
    debug "ldap_entries $v{'ldap_entries'}   per_page $v{'per_page'}  more_ldap ".get_var("more_ldap");

#    debug "yohan returning... ".scalar(@{$entries})." yohan ";
    return $entries;
}


sub directory
{
    #This will search an LDAP directory for given fields
    #
    # Any form element may be used to narrow down the search
    # if you prepend "search_" to the field name, ex. search_name
    #
    # A list of returned fields is in "to_return" or config'ed by admin

    if ($query->param('ldap_jump.x')) 
    {
	debug "POSITION ".$query->param('ldap_position');
	my $total = ceil($v{"ldap_entries"} / $v{"per_page"});
	write_tmp("next_ldap_page", $query->param('ldap_position') < $total ? $query->param('ldap_position')+1 : 1);
	write_tmp("total_ldap_pages", $total);
	write_tmp("have_results",1);
	write_tmp("more_ldap",1);
    }

    my @ldap_hosts = split(/\s+/, $c{"ldap_search_host"});

    my $ldap_host = $ldap_hosts[0] || "ldap.bigfoot.com";

    if (scalar(@ldap_hosts) > 1) {
        write_tmp("multi_host", 1);
    }
    else {
        write_tmp("multi_host", 0);
    }

    debug "ldap host is $ldap_host";
    my ($param,$searched_for);
    my $and = $msg{'MSG_results_and'} || "and";
    $and = " $and ";

    foreach $param ($query->param)
    {
	if ($param =~ /^search_/)
	{
	    $searched_for .= $query->param($param).$and if $query->param($param);
	    write_tmp($param,$query->param($param));
	}
    }

    my $len = length($searched_for) - length($and);

    $searched_for = substr($searched_for,0,$len) if $searched_for;
    
    write_tmp("searched_for",$searched_for);
    
    my ($next) = $query->param("variable") || "directory.html";

    my $st;
    $st = stat("$homedir/ldap_results") if (-e "$homedir/ldap_results");

    if (!$query->param('jump.x') && $st && (time - $st->mtime) > 600) {
        unlink "$homedir/ldap_results";
        debug "removing ldap_results cache";
    } 
    elsif ($searched_for) {
        unlink "$homedir/ldap_results" if (-e "$homedir/ldap_results");
        do_directory();
    }

    load_page($next);
}


sub ldap_search
{
    my ($ldap_host,$search_by,$search_value) = @_;

    load_module("Net::LDAP");
    load_module("IO::Select");

    $ldap_host = $ldap_host || "ldap.bigfoot.com"; 

    debug "Username is: $user_name";
    my ($user, $host) = split(/\@/,$user_name,2);

    # Get DN from config file, substitute user's name...
    my $ldap_dn = $c{"ldap_dn_$ldap_host"};
    $ldap_dn =~ s/USER/$user/g;

    my $ldap_pw = $c{"ldap_password_$ldap_host"} || $password;
    $ldap_pw = "" if ($ldap_pw == "__NONE__");

    debug "DN: $ldap_dn PW: $ldap_pw host: $ldap_host";

    #my $ldap = Net::LDAP->new($ldap_host);
    my $ldap = Net::LDAP->new($ldap_host, port => $c{"ldap_port"}, version => $c{"ldap_version"}, debug=>$c{'ldap_debug'});
    # sometimes the server refuses connection, let's try up to twice more
		
		#$ldap = Net::LDAP->new($ldap_host, port => $c{"ldap_port"}, version => $c{"ldap_version"}) if (!$ldap);
    #$ldap = Net::LDAP->new($ldap_host, port => $c{"ldap_port"}, version => $c{"ldap_version"}) if (!$ldap);    
    
    debug "can't connect to $ldap_host! $@" if (!$ldap);
    return undef if (!$ldap);

    debug "created LDAP object";
		debug "User is: $user";
		
		#$user = $user."@".$c{"ldap_user_domain"};
		
		debug "User now is: $user Pssword: $ldap_pw";
		
		my $mesg;
		
		if ($c{"ldap_login_anonymous"})
		{
			$mesg = $ldap->bind();
		}else
		{
			$mesg = $ldap->bind($user, password => $ldap_pw);;
		} 
		
		#my $mesg = $ldap->bind($user, password => $password);
		
		if ( $mesg->code()) {debug ("bind error:", $mesg->code(),"\n"); return} 

#    if (!$ldap_dn || !$ldap_pw) { # anonymous bind if missing data
#        if (!$ldap->bind) {
#            debug "failed to do anonymous bind: $@";
#            return undef;
#        }
#    }
#    else {
#        if (!$ldap->bind( dn => $ldap_dn, password => $ldap_pw, port => 389)) {
#            debug "failed to do bind with $ldap_dn,$ldap_pw: $@";
#            return undef;
#        }
#    }

    debug "bound to ldap server";

    my (%x500);
    $x500{"city"} = "l";
    $x500{"state"} = "st";
    $x500{"organization"} = $c{"ldap_organization_code_$ldap_host"} || "o";
    $x500{"department"} = $c{"ldap_department_code_$ldap_host"} || "ou";
    $x500{"title"} = "title";
    $x500{"telephone"} = "telephoneNumber";
    $x500{"fax"} = "facsimilieNumber";
    $x500{"country"} = "c";
    $x500{"name"} = "cn";
    $x500{"email"} = "mail";
    $x500{"surname"} = "sn";

    debug "Search type: type=$search_value";
#    $search_value =~ s/\*/\\2a/g;
    $search_value =~ s/\(/\\28/g;
    $search_value =~ s/\)/\\29/g;
    $search_value =~ s/\\/\\5c/g;

    my $filter;

    my ($type, @search_bys,$search_bys);
    $search_by = $query->param("ldap_search_fields") || 
                 $c{"ldap_search_fields"} || $search_by;

    @search_bys = split(/\|/,$search_by);

#    $filter = $query->param("filter_start") || $c{"ldap_object_class_$ldap_host"} || "(&(objectClass=Person)";
    $filter = $query->param("filter_start") || $c{"ldap_object_class_$ldap_host"} || "";
		
		debug "FILTER is: $filter";
		
    foreach $search_bys (@search_bys)
    {
        $type = $search_bys || "cn";
        debug "seach by $search_bys\n";

        if ($search_value ne "*")
        {
#           $filter = "(&(objectClass=Person)($type=*$search_value*))";
            if ($search_value !~ /\|/)
            {
                $filter .= "($type=*$search_value*)";
            }
            else
            {
                #Multi search...
#                my ($first,$second) = split(/\|/,$search_value);
#                $filter .= "(|($type=*$first*)($type=*$second*))";
                my (@fields) = split(/\|/,$search_value);
                my ($f);
                $filter .= "(|";
                foreach $f (@fields)
                {
                    $filter .= "($type=*$f*)";
                }
                $filter .= ")";
            }
        }
        else
        {
        }
    }

    $filter = "(|$filter)" if (scalar @search_bys > 1);
#    $filter .= ")";

    debug "FilteR: $filter GINGER2";
		debug "LDAP host: $ldap_host LDAP is: $ldap";
		
#    my $entries = do_ldap_search($ldap_host, $ldap, $filter);
    return do_ldap_search($ldap_host, $ldap, $filter);
}

sub do_ldap_search
{
    my ($ldap_host, $ldap, $filter) = @_;

    my $base = $c{"ldap_base_$ldap_host"};

    debug "base $base, filter $filter";
		
		debug "BASE is: ".$c{'ldap_dn_'.$c{'ldap_search_host'}};
		
    my $mesg = $ldap->search(
                              base => $base, 
                              filter => $filter 
                             );
		
		if ($mesg->code()) { debug ("search error:", $mesg->code()) }
		
    # save results in hash for accessing later
    my (%ldap_results,%ldap_tmp);
    my $ms = $mesg->as_struct;
    my %ldap_data = %{$ms} if $ms;

    tie %ldap_results, $db_package, "$homedir/ldap_results", O_CREAT|O_RDWR, 0660;
    my $total = scalar(keys %ldap_data);
    debug "total $total";
    my $i=0;
    foreach (keys %ldap_data) {
        my %subdata = %{$ldap_data{$_}};
        foreach (keys %subdata) {
            my @values = @{$subdata{$_}};
            $ldap_tmp{"$i:$_"} = join(' ', @values);
#            debug "ldap_tmp $i:$_ = ".$ldap_tmp{"$i:$_"};
        }
        $i++;
    }

    # need to sort alphabetically by givenname
    my @keys = sort { lc($ldap_tmp{"$a:cn"}) cmp lc($ldap_tmp{"$b:cn"})} 0..$total-1;
    my @ldap_keys = keys %ldap_tmp;
#    debug "ldap_keys @ldap_keys";
#    debug "sorted keys @keys";
    my $count=0;
    my $key;
    foreach $key (@keys) {
        my @tmpkeys = grep {/^$key:/} @ldap_keys;
#        debug "tmpkeys $key @tmpkeys";
        foreach (@tmpkeys) {
            my ($i,$dn) = split(':',$_);
            $ldap_results{"$count:$dn"} = $ldap_tmp{$_};
#            debug "$count:$dn=".$ldap_results{"$count:$dn"};
        }
        $count++;
    }

    $ldap_results{"total"} = $total;
    untie %ldap_results;
    return $total;
}


sub convert2x_addrbook {
    my ($dbfile) = @_;
    $dbfile = "$homedir/$dbfile";

    my (%olddb, $name, $email);
    my $file_type = $c{"convert2x_file_type"} || "GDBM_File";

    load_module("$file_type");
    tie %olddb, $file_type, "$dbfile", O_CREAT|O_RDWR,0660 or debug "Error Converting Addressbook: $!";

    foreach (keys %olddb) {
        ($name,$email) = split(':', $olddb{$_});
        $userdb{"addresses.$_"} = "$email:$name";
        debug "adding addresses.$_ = $email:$name";
    }
    untie %olddb;

debug "Done converting, heh.";
    unlink "$dbfile";
}


sub convert2x_options {
    my ($dbfile) = @_;
    $dbfile = "$homedir/$dbfile";
    my (%olddb );

    my $file_type = $c{"convert2x_file_type"} || "GDBM_File";

    load_module("$file_type");

    tie %olddb, $file_type, "$dbfile", O_CREAT|O_RDWR,0660 || die "Content-type: text\/html\n\nError Converting Options: $!";

    foreach (keys %olddb) {
        $userdb{"options.$_"} = "$olddb{$_}";
        debug "adding options.$_ = $olddb{$_}";
    }
    untie %olddb;
    unlink "$dbfile";
}


sub convert2x_filters {
    my ($dbfile) = @_;
    $dbfile = "$homedir/$dbfile";
    my (%olddb, %typemap, %contmap);

    my $file_type = $c{"convert2x_file_type"} || "GDBM_File";

    $typemap{"To:"} = 1;
    $typemap{"From:"} = 2;
    $typemap{"Subject:"} = 4;
    $typemap{"Body:"} = 8;
    $typemap{"any"} = 15;
    $typemap{"Header"} = 7;
    $contmap{"contains"} = 1;
    $contmap{"doesn't contain"} = 0;

    load_module("$file_type");
    tie %olddb, $file_type, "$dbfile", O_CREAT|O_RDWR,0660 || die "Content-type: text\/html\n\nError Converting Filters: $!";

    foreach (keys %olddb) {
        if (/type/) {
            $userdb{"filters.$_"} = $typemap{$olddb{$_}};
        }
        elsif (/modifier/) {
            $userdb{"filters.$_"} = $contmap{$olddb{$_}};
        }
        else {
            $userdb{"filters.$_"} = $olddb{$_};
        }
        debug "adding filters.$_ = $olddb{$_}";
    }
    untie %olddb;
    unlink "$dbfile";
}


sub convert2x_folders {
    my ($dbfile) = @_;
    $dbfile = "$homedir/$dbfile";
    my $skip_inbox = 1;
    my $untied = 0;
    my ($dir, %inbox, @msgs, $subj, $date, $from, $stat, $pri);
    my (%olddb, %folddb);

    # Do not convert INBOX unless we have an option of mailloc
    if ($userdb{"options.mailloc"} && !(bool($c{"force_mail_local"}))
            && $protocol !~ /imap/i) {
        $skip_inbox = 0;
        debug "mailloc option is set, will copy inbox contents";
    }
    
    if ($skip_inbox && -e "$homedir/folders/$inbox") {
        # we have an INBOX file but don't want to convert it, so delete
        untie %folderdb;
#        $untied = 1;
        unlink "$homedir/folders/$inbox";
    }

    opendir(DIR, "$homedir/folders");
    my @dirs = grep { !/^\./ } readdir(DIR);
    closedir DIR;

    debug "folders dir @dirs";
    if (!(-d "$homedir/messages"))
    {
	create_directory("$homedir/messages");
    }

    my $file_type = $c{"convert2x_file_type"} || "GDBM_File";
    load_module("$file_type");
    tie %olddb, $file_type, "$dbfile", O_CREAT|O_RDWR,0660 || die "Content-type: text\/html\n\nError opening database: $!";

    foreach $dir (@dirs) {
        next if ($dir eq "");
        debug "adding folder $dir";

        if (!($dir =~ /$inbox/i)  || !$skip_inbox) {

            if ($dir =~ /$inbox/i) {
                untie %folderdb;
                $untied = 1;
                move("$homedir/folders/$dir", "$homedir/folders/$dir.old");
                open(MSGS, "<$homedir/folders/$dir.old");
                $dir = "OLD_INBOX";
                my $s = $msg{'MSG_INBOX_moved'} || "Your original INBOX messages have been moved to folder OLD_INBOX";
                set_status($s);
                debug "creating OLD_INBOX";
            }
            else {
                move("$homedir/folders/$dir", "$homedir/folders/$dir.old");
                open(MSGS, "<$homedir/folders/$dir.old");
            }

            # if we're converting INBOX, really just create a folder OLD_INBOX
            tie %folddb, $db_package, "$homedir/folders/$dir", O_CREAT|O_RDWR, 0660;
            debug "opened folder |$dir|";

            @msgs = ();

            while (<MSGS>) {
                s/\n//;
                push(@msgs, $_);
            }

            close(MSGS);

            if ($dir =~ /$inbox/i) {
                unlink "$homedir/folders/$inbox.old";
            }
            else {
                unlink "$homedir/folders/$dir.old";
            }

            debug "messages for $dir @msgs";

            $inbox{$_} = 1 if ($dir =~ /$inbox/i);

            foreach (@msgs) {
                debug "skipping, file $homedir/messages/$_ doesnt exist!" if (!-e "$homedir/messages/$_");
                next if (!-e "$homedir/messages/$_" && !-e "$homedir/messages.old/$_");

                # because we suggest that people copy/move the messages 
                # dir to "messages.old" we could end up not having the
                # message in the expected location... so take care of that
                copy ("$homedir/messages.old/$_", "$homedir/messages")
                    if (-e "$homedir/messages.old/$_" && 
                       !-e "$homedir/messages/$_");

                $folddb{"$_:folder"} = $dir;
                debug "adding message $_, folder $dir";
                $folddb{"$_"} = "local"; 
                $folddb{"$_:nouidl"}   = 0;
                $folddb{"$_:downloaded"} = 1;

                ($subj,$date,$from,$stat,$pri) = split("\0", $olddb{$_});
                debug "$_: $subj $date $from $stat $pri";
                debug "skip_inbox $skip_inbox";
                next if ($skip_inbox && exists($inbox{$_}));
                $folddb{"$_:subj"} = $subj;
                $folddb{"$_:date"} = $date;
                $folddb{"$_:from"} = $from;
                $folddb{"$_:stat"} = $stat;
                $folddb{"$_:pri"} = $pri;
                $folddb{"$_:size"} = -s "$homedir/messages/$_";
                debug "added $_ ";

                $foldmap{$_} = $dir;
                debug "set foldmap of $_ to $dir";
            }

            $userdb{"folder:$dir:protocol"} = "local";
            $folddb{"protocol"} = "local";

            $folddb{"messages"} = join(':', reverse @msgs);
            debug "set messages of $dir to ".$folddb{"messages"};
            untie %folddb;
        }
    }

    if ($untied) {
        tie %folderdb, $db_package, "$homedir/folders/$inbox", O_CREAT|O_RDWR, 0660;
    }
    untie %olddb;
    unlink "$dbfile";
}


sub convert_newfolders {
    my @folders = @_;

    @folders = split('%%smoo1919', $userdb{"variable:folders"})
        if (scalar(@folders) <= 0) ;
    debug "folders to convert: @folders";

    my ($fold, @msgs, %newfold, @keys, $key, $msg);
    my $foldname;

    # error recovery... are tehre folders but no variable?
    if (scalar(@folders) <= 0) {
        # grab folders from userdb, only other way possible
        my %tmpfold;
        map { $tmpfold{$_} = 1; } grep { /:folder$/ } keys %userdb;
        foreach (keys %tmpfold) {
            push(@folders, $_) if $_ ne "";
        }
    }

    unlink "$homedir/popmap" if (-e <$homedir/popmap*>);

    # first close out the current folderdb, open it again later.
    untie %folderdb;

    push(@folders, $inbox) if (scalar(grep(/^inbox$/i, @folders)) == 0);
    debug "folders @folders";
    create_directory("$homedir/folders") if (! -e "$homedir/folders");

    debug "db_package $db_package";
    foreach $fold (@folders) {
        next if ($fold eq "");

        # take care of a bug in earlier versions that created sent-mail 
        # folder names with a prefix (imap prefix). Only way to do it is 
        # assume the prefix is still defined in site.emu and remove it 
        # from folder names.
        my $localf = $fold;
        trim(\$localf);

        if ($localf ne $folder) {
            # we had to remove leading/trailing spaces. Need to fix userdb
            $userdb{"folder:$localf:protocol"} = $userdb{"folder:$fold:protocol"
};
        }

        if ($localf =~ /^$c{"default_imap_prefix"}\//) {
            debug "found folder with prefix... removing it";
            $localf =~ s/^$c{"default_imap_prefix"}\///;
        }

        # we have to take care of a situation where the original system
        # had mail_local set and the new one doesnt
        $mailloc = bool($c{'force_mail_local'}) || 
                   bool($c{'default_mail_local'}) || 0;
#                   bool($userdb{"options.mailloc"}) || 0;

        if ( ($userdb{"options.mailloc"} || bool($c{'original_mail_local'}))
                && !$mailloc && $fold =~ /^inbox$/i) {
            # converting old mailbox that used mailloc... we need to save
            # it into a separate folder, say "OLD_INBOX"
            debug "creating OLD_INBOX";
            $localf = "OLD_INBOX";
            $userdb{"folder:$localf:protocol"} = "local";
            $userdb{"options.mailloc"} = 0;
        }

        if (($userdb{"folder:$fold:protocol"} =~ /pop/i 
                || $userdb{"folder:$fold:protocol"} =~ /imap/i) and
                $fold !~ /^inbox$/i) {
            # external folder...
            create_directory("$homedir/folders/.external")
                if (! -e "$homedir/folders/.external");

            debug "opening folder $homedir/folders/.external/$localf";
            unlink "$homedir/folders/.external/$localf" 
                if (-e "$homedir/folders/.external/$localf");
	    
	    if ( $ELocks->lock_create("$homedir/folders/.external/$localf", \%newfold, {mode => 'write', nb => 1}) )
            {
            	tie %newfold, $db_package, "$homedir/folders/.external/$localf", O_CREAT|O_RDWR, 0660;
            	$foldname = "$homedir/folders/.external/$localf";
            	debug "opened folder |.external/$localf|";
            }
        }
        else {
            debug "opening folder $homedir/folders/$localf";
            # we don't want any legacy folder files if we're converting...
            unlink "$homedir/folders/$localf" if (-e "$homedir/folders/$localf");

	    if ( $ELocks->lock_create("$homedir/folders/$localf", \%newfold, {mode => 'write', nb => 1}) )
	    {
            	tie %newfold, $db_package, "$homedir/folders/$localf", O_CREAT|O_RDWR, 0660;
            	$foldname = "$homedir/folders/$localf";
            	debug "opened folder |$localf|";
            }
        }

        @msgs = reverse split(':',$userdb{"folder:$fold:msgs"});
        $newfold{"messages"} = join(':', @msgs);
#        debug "set messages to ".$newfold{"messages"};

        if (scalar(@msgs) > 0) {
            foreach $msg (@msgs) {
                debug "adding $msg to folder $localf";
                $newfold{"$msg"} = $userdb{"msgs:$msg"} || $userdb{"folder:$localf:protocol"};
                $newfold{"$msg"} = $userdb{"msgs:$msg"};
                delete($userdb{"msgs:$msg"});
                $newfold{"$msg:subj"} = $userdb{"msgs:$msg:subj"};
                delete($userdb{"msgs:$msg:subj"});
                $newfold{"$msg:from"} = $userdb{"msgs:$msg:from"};
                delete($userdb{"msgs:$msg:from"});
                $newfold{"$msg:cc"} = $userdb{"msgs:$msg:cc"};
                delete($userdb{"msgs:$msg:cc"});
                $newfold{"$msg:bcc"} = $userdb{"msgs:$msg:bcc"};
                delete($userdb{"msgs:$msg:bcc"});
                $newfold{"$msg:to"} = $userdb{"msgs:$msg:to"};
                delete($userdb{"msgs:$msg:to"});
                $newfold{"$msg:date"} = $userdb{"msgs:$msg:date"};
                delete($userdb{"msgs:$msg:date"});
                $newfold{"$msg:pri"} = $userdb{"msgs:$msg:pri"};
                delete($userdb{"msgs:$msg:pri"});
                $newfold{"$msg:stat"} = $userdb{"msgs:$msg:stat"};
                delete($userdb{"msgs:$msg:stat"});
                $newfold{"$msg:folder"} = $localf;
                delete($userdb{"msgs:$msg:folder"});
                $newfold{"$msg:nouidl"} = $userdb{"msgs:$msg:nouidl"};
                delete($userdb{"msgs:$msg:nouidl"});
                $newfold{"$msg:downloaded"} = $userdb{"msgs:$msg:downloaded"};
                delete($userdb{"msgs:$msg:downloaded"});
                $newfold{"$msg:size"} = $userdb{"msgs:$msg:size"};
                delete($userdb{"msgs:$msg:size"});
                $newfold{"$msg:replyto"} = $userdb{"msgs:$msg:replyto"};
                delete($userdb{"msgs:$msg:replyto"});

                $foldmap{$msg} = $fold;
            }
        }

        $newfold{"protocol"} = $userdb{"folder:$localf:protocol"};
        $newfold{"password"} = $userdb{"folder:$fold:password"};
        $newfold{"username"} = $userdb{"folder:$fold:username"};
        $newfold{"email"}    = $userdb{"folder:$fold:email"};
        $newfold{"hostname"} = $userdb{"folder:$fold:hostname"};

        untie %newfold;
        debug "closing folder $foldname";
        $ELocks->lock_remove(\%newfold);

        delete($userdb{"folder:$fold:msgs"});
    }

    delete($userdb{"variable:folders"});

    my %newdb;
    if ( $ELocks->lock_create("$homedir/newdb", \%newdb, {mode => 'write', nb => 1}) )
    {
    	tie %newdb, $db_package, "$homedir/newdb", O_CREAT|O_RDWR, 0660;
    } else {
    	debug "can't lock newdb";
    }

    while(my($k,$v) = each %userdb)
    {
        $newdb{$k} = $v;
    }

    untie %userdb;
    untie %newdb;
    $ELocks->lock_remove(\%newdb);
    move("$homedir/newdb", "$homedir/userdb");
    $ELocks->lock_remove(\%userdb);
    
    if ( $ELocks->lock_create("$homedir/userdb", \%userdb, {mode => 'write', nb => 1}) )
    {
    	tie %userdb, $db_package, "$homedir/userdb", O_CREAT|O_RDWR, 0660;
    }

    debug "keys in userdb: ".scalar(keys %userdb);

#    flush_msg_cache();

    # Now reopen folderdb
    $ELocks->lock_remove(\%folderdb);
    if ( $ELocks->lock_create("$homedir/folders/$folder", \%folderdb, {mode => 'write', nb => 1}) )
    {
    	tie %folderdb, $db_package, "$homedir/folders/$folder", O_CREAT|O_RDWR, 0660;
    	debug "opened folder |$folder|";
    }
}


### HM 06/27/00
### Trying to abstract data - extracted several routines and formed them
### into functions of their own

# Extracted from load_page, "if ($array eq 'message') {"
sub get_msg_array
{
    my (@msgs, $i, $msg, %loophash, @looparr);
    
    @msgs = get_x_msgs();
#    debug scalar(@msgs)." messages: @msgs";
    
    @looparr = (0..$#msgs);
    
    $i = 0;
    for $msg (@msgs)
    {
#	debug "processing $msg";
	$msg =~ s/\n//;
	
	# when we're doing a search, messages from other
	# folders will appear (not in $folderdb) so we must
	# account for that.
	my %h;
    LOAD_HEADER_INFO:
	{
	    # How are we going to find out this header info?
	    # Either from our database (preferred)
	    # or by reparsing a message file (slower)
	    
	    # First try by loading stuff from the database:
	    
	    $h{"stat"} = $folderdb{"$msg:stat"};
	    $h{"from"} = $folderdb{"$msg:from"};
	    $h{"to"} = $folderdb{"$msg:to"};
	    $h{"date"} = $folderdb{"$msg:date"};
	    #Fix me AM 22/10/15
	    use Encode qw(decode);
	    
	    
	    $h{"subj"} = $folderdb{"$msg:subj"};
	    
	    debug "SUbj was: ".$h{"subj"};
	    
        $h{"subj"} = decode("MIME-Header", $h{"subj"},Encode::FB_CROAK);
        debug "SUbj becomes: ".$h{"subj"};
        
	    if (!$folderdb{"$msg:size"})
	    {
			$folderdb{"$msg:size"} = -s "$homedir/messages/$msg";
			$folderdb{"$msg:size"} = undef if ($folderdb{"$msg:size"} == 0);
	    }

	    $h{"size"} = $folderdb{"$msg:size"};
	    $h{"pri"} = $folderdb{"$msg:pri"};
		$h{"ct"} = $folderdb{"$msg:ct"};
		debug "status for $msg is ".$h{"stat"};
		CUSTOM_HEADERS:
	    {
			# debug "custom_headers: @custom_headers";
			foreach my $chead (@custom_headers) 
			{
		    	if ($folderdb{"$msg:$chead"})
		    	{                            
					$h{$chead} = $folderdb{"$msg:$chead"};
		    	}
			}
	    }

	    # If that doesn't work, we better try something else
	    # How about from a file?
	    
	  	TRY_FROM_FILE:
	    {
			debug "$msg ".$folderdb{"$msg"}." date ".$folderdb{"$msg:date"};

			last if (defined($folderdb{"$msg"}) && 
                     defined($folderdb{"$msg:date"}) &&
                     defined($folderdb{"$msg:stat"}));

	        debug "Hmm, didn't find anything in our db.  maybe we have it on disk?";
	        if (-e "$homedir/messages/$msg")
	        {
		    	debug "Yup, msg $msg probably in different folder, get header from file";
		    	my $h_ref = header_from_file($msg);
		    	last TRY_FROM_FILE unless $h_ref;

                # only restore those items which are not defined in folderdb
                my @h_items = grep { /^$msg:/ } keys %folderdb;
				foreach my $h_item (qw/from to date subj cc stat pri ct/)
				{
                	next if (defined($folderdb{"$msg:$h_item"}) || !defined($h_ref->{$h_item}));
                    debug "reassigning $h_item to ".$h_ref->{$h_item};
                    $folderdb{"$msg:$h_item"} = $h{$h_item} = $h_ref->{$h_item} if (defined($h_ref->{$h_item}));
                }
			}
		}


	    # If we still don't have something useful, let's try from the server
	    # doing a complete download.
	    
	  	GET_FROM_MAILSERVER:
	    {
			unless (join('',values %h))
			{
		    	debug "Going to attempt to get the message from the mail server.";
		    	if ($userdb{"folder:$folder:protocol"} =~ /imap/)
		    	{
					# This is normal with IMAP...the way it's done in fact.
					# We do just in time message fetching...it only looks weird.

					my ($uid_validity,$u,$p,$host);

		      		LOGIN_TO_IMAP:
					{
			    		($u,$p,$host) = get_folder_credentials($inbox);
					    if ($u=~/\@/)
					    {
							my ($uu,$h) = split(/\@/,$u);
							$u = $uu if (!exists($c{"appendhost_$h"}));
			    		}
					    $uid_validity = &do_imap_login($u, $p, $host, $folder,1);
					}

		      		GET_HEADERS_FROM_SERVER:
					{
			    		last unless $pop;
						my (@uids) = split(/:/, $folderdb{"messages"});
						map { s/^$uid_validity// } @uids;
						process_msg_list(\@uids,$uid_validity,"imap",$folder,$u,$p);
					}
		    	}

		    	# How did this happen? message disappeared?
				if (! -e "$homedir/messages/$msg")
				{
		        	debug "What!? No message file? Let's redownload it $msg";
		        	if (!download_msg($msg,$folder))
		        	{
                    	set_status($msg{'ERR_MSGNotInServer'});
					}
				}

				my $h_ref = header_from_file($msg);
		    	%h = %{$h_ref} if ($h_ref);
			}
	    }
	}
	
	#Ok, now hopefully we've got our data. (pretty please data god?)
	# Let's populate the data structures (?) so we can display stuff

	SET_DISPLAY_VARS:
	{
	    $loophash{"status$i"} = $c{"Status" . $h{"stat"}};
	    $loophash{"hash$i"} = $msg;
	    $loophash{"from$i"} = $h{"from"};
	    $loophash{"from$i"} =~ s/\n|\r//g;
	    
	    if ($c{'index_sender_mode'} > 0)
	    {
		my @addrpart = addr_split($loophash{"from$i"});
		# mode 1 is just the real name
		if ($c{'index_sender_mode'} == 1)
		{
		    $loophash{"from$i"} = $addrpart[0];
		    if (!$loophash{"from$i"})
		    {
			# fall back on the email address
			$loophash{"from$i"} = $addrpart[1];
		    }
		}
		# mode 2 is just the email
		elsif ($c{'index_sender_mode'} == 2)
		{
		    $loophash{"from$i"} = $addrpart[1];
		}
	    }
			
	    $loophash{"from$i"} = substr($loophash{"from$i"}, 0, $c{'index_sender_length'});
	    $loophash{"from$i"} = safe_html($loophash{"from$i"});
	    # 05/15/98: must have something here (when blank it's 
	    # usually not null but spaces)
	    $loophash{"from$i"} =~ /^\s*$/  and  $loophash{"from$i"} = $msg{'MSG_NoFrom'};

	    $loophash{"to$i"} = $h{"to"};
	    $loophash{"to$i"} =~ s/\n|\r//g;
	    
	    if ($loophash{"to$i"} =~ /@/) 
	    {
		my @addrpart = addr_split($loophash{"to$i"});
		$loophash{"to$i"} = $addrpart[1] || $addrpart[0];
		$loophash{"to$i"} = substr($loophash{"to$i"}, 0, $c{'index_sender_length'});
	    }
	    
	    $loophash{"to$i"} = safe_html($loophash{"to$i"});

	    # make the href
	    debug "Making href for msgindex, folder in db for this message is " . $folderdb{"$msg:folder"};
	    $loophash{"href$i"} = make_url("msg", $msg, 'folder' => $folderdb{"$msg:folder"});
	    
	    # get the date
	    $loophash{"date$i"} = $h{"date"};
	    $loophash{"date$i"} =~ s/^(.*?)(\d+\s\w\w\w)(.*)/$2/;
	    $loophash{"date$i"} = "0".$loophash{"date$i"} if (length($loophash{"date$i"}) == 5);
	    
	    my (undef, $day, $month) = get_date(str2time($h{"date"}), undef, 1);
	    ($loophash{"day$i"},$loophash{"month$i"}) = ($day, $month);
	    
	    ($loophash{"day_name$i"}, undef, $loophash{"month_name$i"}, $loophash{"year$i"}, 
	    $loophash{"hour$i"}, $loophash{"minute$i"}, $loophash{"second$i"}, 
	    $loophash{"ampm$i"}, $loophash{"gmt$i"}) = get_date(str2time($h{"date"}), undef, undef, 1);
	    
	    # the subject
	    $loophash{"subject$i"} = $h{"subj"};
	    $loophash{"subject$i"} = substr($loophash{"subject$i"}, 0, $c{'index_subject_length'});
	    $loophash{"subject$i"} = safe_html($loophash{"subject$i"});
	    # apply "No Subject" if at this point subject is blank
	    $loophash{"subject$i"} = $msg{'MSG_NoSubject'}
	    if (!$loophash{"subject$i"});
	    
	    # the size
	    my $z = $h{"size"} || $folderdb{"$msg:size"};
	    $loophash{"size$i"} = get_size($z);
	    $loophash{"size_k$i"} = get_size($z,1);
	    
	    # priority
	    my ($pri) = $h{"pri"} || $folderdb{"$msg:pri"};

	    if ($c{'PRIORITY_URGENT'} && $pri =~ /^urgent|^[12]/i)
	    {
		$loophash{"color$i"} = $c{'PRIORITY_URGENT'};
	    }
	    elsif ($c{'PRIORITY_NURGENT'} && $pri =~ /non-urgent|^[45]/i)
	    {
		$loophash{"color$i"} = $c{'PRIORITY_NURGENT'};
	    }
	    elsif ($c{'PRIORITY_NORMAL'})
	    {
		$loophash{"color$i"} = $c{'PRIORITY_NORMAL'};
	    }
	    
	    # process custom headers and add any column data
	    if ($licensed{"custom_headers"}) 
	    {
		process_custom_headers(\%h, \%loophash, $i);
	    }
	}
	
	$i++;   # gotta increment!
    }

    return (\@looparr, \%loophash);
}

sub get_header_array
{
   my ($msg) = get_var("message");
   my (@arr, @headarr, @looparr, %loophash);
   my ($lastkey, $key, $val, $hashkey);

#debug "getting header for $msg";
   # Check to see if we have a cached MIME::Head object
   my $head = get_var('header_obj');

   if (!ref $head) {
#      debug "reading from file";
      $head = MIME::Head->from_file("$homedir/messages/$msg");
   }

   $head->decode;
   $head->unfold;

   # RMK 01/19/99 use full header, not tags...
   @headarr = split('\n', $head->original_text());
#                    debug "looparr @looparr";
		    
   my $j=0;
   for my $h_line (@headarr)
   {
      ($hashkey, $val) = split(/:/, $h_line, 2);

#debug $h_line;
#debug "$hashkey = $val";
      if ($h_line =~ /^From:|^To:|^Cc:|^Bcc:/i && $val =~ /[\w\.\-]+\@[\w\.\-]+/) {
          # if we have an email address, convert it to hyperlink to add
          # to addressbook. 
          debug "parsing address for $val";

        eval {
          my @addrs = Mail::Address->parse($val);

          foreach my $addr (@addrs) {
              my $orig = $addr->format;
              $val =~ s/$orig/&add2addr($addr->format)/e;
          }
        };

      }
      else {
          $val = &safe_html($val,'<>');
      }

      # modify date using our format
      if ($h_line =~ /^Date:/)
      {
      	$val = get_date(str2time($val), undef, undef, 1);
      }

      if (exists($loophash{$hashkey})) {
          # RMK 01/19/99 insert spaces into hash so we can have multiple entries
          my $spaces = " " x $j;
          $hashkey = $hashkey . $spaces;
      }

      $looparr[$j++] = $hashkey;
      $loophash{$hashkey} = $val;
#debug "hashkey '$hashkey', value $val";
   }

#                   @looparr = sort alpha keys %loophash;
#   debug "From is $loophash{From}";
   return (\@looparr, \%loophash);
}

sub get_addrs_array {
   my (@addrs, $email, $full, $count, @data, $index, $desig, $org, $phone, $fax);
   my (@looparr, %loophash);
   
   debug "using addresses array";
   
   @addrs = grep (/^addresses\./, keys %userdb);
   @addrs = sort alpha @addrs;
   
   $count = 0;
   
   debug "addrs are @addrs";
   
   for (@addrs)
   {
      @data = split(/:/, $userdb{$_});

      $email = $data[0];
      $full  = $data[1];
      $index = 2;

      my @addrbk = ();

      # Now let's process user-definable addressbook 
      # fields, if any
      if ($licensed{"custom_addrbook"}) {
          @addrbk = keys %AddressbookDefs::addrbook_fields;

          for (my $i=1; $i<=scalar(@addrbk); $i++) {
              my $entry = "addrbook_$i";
              $loophash{"$entry$count"} = $data[$index++];
              $loophash{"$entry"."_encode$count"} = 
                  private_str($data[$index]);
          }
      }

      # get rid of addresses. pre
      s/^addresses\.//;

      $loophash{"n$count"} = $_;
      $loophash{"e$count"} = $email;
      $loophash{"f$count"} = $full;

      #04/25/99 -- MM
      $loophash{"n_encode$count"} = private_str($_);
      $loophash{"e_encode$count"} = private_str($email);
      $loophash{"f_encode$count"} = private_str($full);

      ++$count;
   }
   
   # looping with just numbers
   @looparr = (0..$count-1);

   return (\@looparr, \%loophash);
}

sub get_addrstr {
   my ($key, $val, $str);

   if ($EMU::{"$user_name\_addrstr"})
   {
      return $EMU::{"$user_name\_addrstr"};
   }
   else
   {
      foreach $key (sort addrly grep(/^addresses\./, keys %userdb))
      {
         # get the email address from the database
         $val = (split(':', $userdb{$key}, 2))[0];

         # get rid of the addresses, and limit the nickname to 20 chars
         $key = substr(substr($key, 10), 0, $c{'addressbook_length'} || 20);

         $str .= qq{    <OPTION VALUE="$val">$key\n};
      }
       
      add_cleanup("$user_name\_addrstr");
      $EMU::{"$user_name\_addrstr"} = $str;

      return $str;
   }

   return undef;
}

# Silly, yucky, weird. These are words describing this data structure.
sub get_priority_data {
   my @parray = ( "1 (Highest)",
                  "2 (High)",
                  "3 (Normal)",
                  "4 (Low)",
                  "5 (Lowest)" 
                );
                    
   my %phash = ( "1 (Highest)" => "1 ($msg{'MSG_Priority_Highest'})",
                 "2 (High)"    => "2 ($msg{'MSG_Priority_High'})",
                 "3 (Normal)"  => "3 ($msg{'MSG_Priority_Normal'})",
                 "4 (Low)"     => "4 ($msg{'MSG_Priority_Low'})",
                 "5 (Lowest)"  => "5 ($msg{'MSG_Priority_Lowest'})"
                );

   return (\@parray, \%phash);
}

sub attach_file
{
   my($attached, $tmpfile, $fullfile, $filename, $file);                # files currently "attached" to the message

   $fullfile = $query->param('tmpupload');

   if ($query->param('attach.x') && !$fullfile)
   {
      set_status($msg{'ERR_UploadNoSelect'});
      return ($fullfile, $filename, 1);
   }

   $attached = $query->param('attached');
   my $attach_ix = scalar(split(' ', $attached));

   $filename     = legalize(basename($fullfile));
   $filename =~ s/[\s|\/]/_/g;
   $filename .= "_$attach_ix";

   debug "fullfile $fullfile, file $filename";

   $file = "$homedir/tmp/$filename";
   
   open(FILEOUT, ">$file");
   binmode(FILEOUT);

   my $fh = $query->upload('tmpupload');

   if (!$fh)
   {
      set_status(convert($msg{'ERR_UploadFailed'}, $query->param('tmpuload'), $query->cgi_error));
      return ($fullfile, $filename, 1);
   }

   while (<$fh>) {
      print FILEOUT $_;
   }

   close(FILEOUT);
   close($fh);

   if (-z $file)       # 0 byte file!
   {
      debug("$user_name uploading a 0 byte file");

      set_status(convert($msg{'ERR_UploadEmpty'}, $filename));
      return ($fullfile, $filename, 1);
   }

   debug "uploaded and saved $file";

   # setup the attach line
   $attached = $attached ? "$attached $filename" : $filename;

   debug "attached is $attached";

   $query->param('attached', $attached);

   return ($fullfile, $filename, 0);
}

sub remove_attachments
{
   my (@remove) = @_;
   my @attachments;

debug "removing attachments:",join(',',@remove);
   foreach my $a ( split(/\s+/, $query->param('attached')) ) {
      push(@attachments, $a) if (!grep($_ eq $a, @remove));
   }
   
   # This is here to mimic the existing code
   $query->param('attached', join(' ', @attachments));
}

sub process_attachment
{

   print_header();

   if ($query->param('attach.x')) {

      &attach_file();

      # HM 07/07/00 - I dislike this for so many reasons.
      write_tmp('here_atts', $query->param('attached'));
      
      load_page('attachment_popup.html');
      return;
      
   } elsif ($query->param('delete.x')) {

      my @selected = $query->param('selected');

      &remove_attachments(@selected);

      # HM 07/07/00 - I dislike this for so many reasons.
      debug "attached: ",$query->param('attached');
      write_tmp('here_atts', $query->param('attached'));

      load_page('attachment_popup.html');
      return;
   } else {
      
      # We'll give them a second chance
      load_page('attachment_popup.html');
   }
      
}

sub process_options
{
   print_header();

   # see if they want to reset the options
   if ($query->param('reset.x'))
   {
      set_default_options();
      set_status($msg{'MSG_OptionsReset'});
   } else {
      set_status($msg{'MSG_OptionsSaved_S'}) if (save_options() != -1);
   }

   options();
}   

sub get_postponed_msgs 
{
   opendir DIR, "$homedir/files";
   my @files = grep ( /^[0-9a-f]{32}$/, readdir DIR);
   closedir DIR;
        
   # map the filenames correctly
   map { $_ .= substr(":" . get_heldmsg_name($_, $userdb{"postponed.$_"}), 0, 30) } @files;
   my @ff;
   foreach my $f (@files)                        
   {
      my ($msgid, $date, $subject) = split(/:/, $f, 3);
      if (!$subject) {
         $subject = $date;
         $date = '';
      }
      push (@ff,[$msgid, $date, $subject]);
   }

   return @ff;
}
# HM 07/12/00 - This is being done here versus clientside so that we can
# really manipulate things without having to deal with differing browser
# issues. Plus, Perl grants us a lot more power.
sub address_select
{
   my %contacts;

   # Typed in addresses
   # These hashes will help take care of duplicates
   my %to  = map { $_ => 1 } split(/[;,\s]+/, $query->param('to'));
   my %cc  = map { $_ => 1 } split(/[;,\s]+/, $query->param('cc'));
   my %bcc = map { $_ => 1 } split(/[;,\s]+/, $query->param('bcc'));

   # Addressbook addresses
   my @data = &EMU::get_addrs_array();
   my @addrnums = @{ $data[0] } if $data[0];
   my %addrdata = %{ $data[1] } if $data[1];

   foreach $a (@addrnums) {
      my $n = $addrdata{"n$a"};
      my $e = $addrdata{"e$a"};
      $contacts{$n}{email} = $e; 
      
      if ($to{$e} || $to{$n}) {
         $contacts{$n}{to}  = 1;
         delete($to{$e});
         delete($to{$n});
      }
      if ($cc{$e} || $cc{$n}) {
         $contacts{$n}{cc}  = 1;
         delete($cc{$e});
         delete($cc{$n});
      }
      if ($bcc{$e} || $bcc{$n}) {
         $contacts{$n}{bcc}  = 1;
         delete($bcc{$e});
         delete($bcc{$n});
      }
         
      
   }

   write_tmp('to', [ sort keys %to ]);
   write_tmp('cc', [ sort keys %cc ]);
   write_tmp('bcc',[ sort keys %bcc ]);
   write_tmp('contacts', \%contacts);
   
   print_header();

   parse('address_popup.html');

}      

sub mailboxes
{
   &parse('mailboxes.html');
}

sub process_mailboxes
{
   
   &folders_parse(\&mailboxes);
}

sub get_organized_folders
{

   my @folders = grep { $_ ne $inbox && $_ ne 'Search Results' } &EMU::get_subscribed_folders();
   
   # Always show mailboxes
   push(@folders, &get_folders_external);

   my $fh;
      foreach my $f (@folders) {
         my $protocol = lc(&EMU::get_folder_protocol($f));
         if ($EMU::userdb{"folder:$f:external"}) {
            $fh->{mailboxes}->{$f} = $protocol;
            next;
         } elsif ($protocol eq 'local') {
            $fh->{local}->{$f} = $protocol;
         } elsif ($protocol eq 'imap') {
            $fh->{imap}->{$f} = $protocol;
         } else {
            debug "Folder '$f' has unknown protocol '$protocol'";
            $fh->{other}->{$f} = $protocol;
         }
      }
  
   return $fh;
}



sub get_imap_dirs
{
   my (@looparr);

   return if ($protocol !~ /imap/i);

   my $delim = &get_imap_delimiter();
   
#   This isn't needed
#   push(@looparr, $delim);

   # get_folders();
   my $prefix;
   if ($userdb{"folder:$folder:external"} == 1) {
      $prefix = $userdb{"options.prefix"} || $c{"default_imap_prefix"};
   }
   else {
      $prefix = get_outbox_prefix();
   }

   # Hrm, I guess we should force a folder list so that we can have those dirs. We should cache those dirs.
   &get_folders_imap(1);

   foreach my $fold (@{$pop->{dirs}}) {
      $fold =~ s/^$prefix//; 
      next if ($fold eq ""); 
      push(@looparr, $fold);
   }

   return @looparr;
}

sub toggle_menu
{
   my $menu = $query->param('menu');
   my $next = $query->param('next');
   
   $menu =~ s/\W//g;
   
   my $val = &get_menu_setting($menu);
   &set_menu_setting($menu, !$val);

   &jump($next, 0);
}

sub expand_menu
{
   my $menu = $query->param('menu');
   my $next = $query->param('next');

   $menu =~ s/\W//g;
   &set_menu_setting($menu, 1);

   &jump($next, 0);
}

sub collapse_menu
{
   my $menu = $query->param('menu');
   my $next = $query->param('next');
   
   $menu =~ s/\W//g;
   &set_menu_setting($menu, 0);

   &jump($next, 0);
}

sub get_menu_setting
{
   my $menu = shift;
   return $userdb{"options.menu.$menu"};
}

sub set_menu_setting
{
   my ($menu, $val) = @_;
   $userdb{"options.menu.$menu"} = $val;
}

sub get_directory
{
   my (@looparr, %loophash);

   debug "printing entries";
   # results were done previously and saved in a hash
   my %ldap_results;
   tie %ldap_results, $db_package, "$homedir/ldap_results",
   O_RDONLY, 0660;

   debug "entries ".$ldap_results{"total"};
   my $to_return = $c{"ldap_search_fields"} || $query->param('ldap_search_fields') || "name";
   my $sort_order = $c{"ldap_search_sort"} || $query->param('ldap_search_sort') || "givenname";

   my ($entry);
   my ($count) = 0;

   my $per_page = $v{"per_page"} || $c{"ldap_entries_per_page"}  || 10;
   $v{"per_page"} = $per_page;

   my $position = $query->param("ldap_position") || 1;
   $position = $position -1;
   my $tot_msgs = $ldap_results{"total"};

   debug "position $position";
   write_tmp("ldap_entries",$tot_msgs );

   write_tmp("total_ldap_pages",ceil($tot_msgs/$per_page) );
   my $np = ($position+2)%(ceil($tot_msgs/$per_page)+1) || 1;
   write_tmp("next_ldap_page",$np);
   write_tmp("more_ldap", $tot_msgs > $per_page ? 1 : 0);
   write_tmp("position",$position);
   my $start = $position*$per_page;
   my $end = $start + $per_page;
   $end = $tot_msgs if ($end > $tot_msgs);
   
   write_tmp("start",($start+1));
   write_tmp("end",$end);
   debug "start $start end $end";

   debug "MARYANN1";
   return([],{}) unless $end;

   # read in results from hash
   for ($entry=$start; $entry < $end; $entry++) {
      my @keys = grep {/^$entry:/} keys %ldap_results;
      $count++;
      push(@looparr,$count);
      foreach my $field (split(/\|/,$to_return))
      {
         $loophash{"$field$count"} = $ldap_results{"$entry:$field"};
         debug "$field$count = ".$loophash{"$field$count"};
      }

      my $fullname = $ldap_results{"$entry:cn"};
      my $name = $ldap_results{"$entry:givenname"};
      $name = $name || $ldap_results{"$entry:cn"};
      $loophash{"_name$count"} = $name;
      $loophash{"_fullname$count"} = $fullname;
      my $org = $ldap_results{"$entry:organizationalUnitName"};
      $org = $org || $ldap_results{"$entry:o"};
      $loophash{"_org$count"} = $org;
      my $unit = $ldap_results{"$entry:ou"};
      $loophash{"_unit$count"} = $unit;
      my $title = $ldap_results{"$entry:title"};
      $loophash{"_title$count"} = $title || "";
      my $fone = $ldap_results{"$entry:telephoneNumber"};
      $loophash{"_phone$count"} = $fone;
      my $fax = $ldap_results{"$entry:facsimiletelephoneNumber"};
      $loophash{"_fax$count"} = $fax;

      my @emails;
      @emails = map   {
         my %extra;
         $extra{"full"} = $fullname if $fullname;
         $extra{"nick"} = $name if $name;
         $extra{"telephone"} = "$fone" if $fone;
         $extra{"fax"} = $fax if ($fax);
         $extra{"org"} = $org if $org;
         $extra{"desig"} = $title if $title;
         $extra{"email"} = $_ if $_;
         ($extra{"key"}) = split(/\@/) if $_;
         my %extra2;
         $extra2{"email"} = $_;
         "$_ <a href=\"".make_url("new_msg",$_, %extra2). "\">[".$msg{'DIR_COMPOSE_NAME'}."]</a> | <a href=\"".make_url("address", $_, %extra)."\">[".$msg{'DIR_ADDRESSBOOK_NAME'}."]</a>";
      } $ldap_results{"$entry:mail"};

      $loophash{"_email_link$count"} = join(",",@emails);
      $loophash{"_email$count"} = $ldap_results{"$entry:mail"};
   }
                   debug "MARYANN2";

   return (\@looparr, \%loophash);
}

sub process_filters
{

   my @order = split(/\s+/, $userdb{'options.filters'});
   my $filterid = $query->param('filterid');
   $filterid =~ s/\D//g;

   if ($query->param('save.x')) {
   
      # Before we get to creating stuff, lets make sure the target exists
      if (!folder_exists($query->param('target'))) {

         # check for action, is this a filter to folder, or delete?
         my $garbage = $msg{"GARBAGE_Filter_Name"} || "GARBAGE";
         my $action = $c{"GARBAGE_Filter_Action"} || "Folder";

         debug "action for GARBAGE is $action" if ($query->param('target') eq $garbage);
         # If its not there, make it.
         create_folder($query->param('target')) or return parse('filters.html')
             if ($query->param('target') ne $garbage || $action eq "Folder");
      }
      
      if (!$filterid) {
         $filterid = &create_filter();
      } 
      elsif (!grep(/$filterid/, @order)) {
         set_status("Invalid Filter ID: $filterid");
         return parse('filters.html');
      }
      
      foreach my $k (qw/name key operator data action target active/) {
         $userdb{"filters:$filterid:$k"} = $query->param($k);
      }
   } 
   elsif ($query->param('move_up.x') || $query->param('move_down.x')) {
      my $dir;

      if ($query->param('move_up.x')) {
         $dir = -1;
      } else {
         $dir = +1;
      }

      for (my $i=0; $i<@order; $i++) {
         if ($order[$i] == $filterid) {
            my $dest = $i + $dir;
            my $tmp = $order[ $dest ];

            $order[$dest] = $filterid;
            $order[$i] = $tmp;
            
            last;
         }
      }
      
      $userdb{'options.filters'} = join(' ', @order);
   }
   elsif ($query->param('delete.x')) {
      my @selected = $query->param('selected');
      my (@neworder, $deleted);

      # No need to delete keys. If we just remove them from the index, they will be reused later.
      foreach my $f (@order) {
         if ( grep($_ eq $f, @selected) ) {
            $deleted++;
         } else {
            push (@neworder, $f);
         }
         
      }

      $userdb{'options.filters'} = join(' ', @neworder);
      
      set_status("$deleted filters deleted.");
   }
   #elsif ($query->param('toggle_realtime.x'))
   #{
   #   $userdb{'options.do_realtime_filter'} = bool($query->param('do_realtime_filter'));
   #}

   # Update the old style filter data for compatibility
   &update_old_filters();
   parse('filters.html');
}

# Store the new style filters into the old style data space.  This is a
# little bit ... wrong, because it prevents people from flawlessly swapping
# between both interfaces. But, to fix this I'll need to rewrite the filter
# routine, which is not something I am going to do right now.
sub update_old_filters
{

   my @filters = &get_filters();
   my $count = 1;
   foreach my $f (@filters) {
      next if (!$f->{active});
      $userdb{"filters.action$count"} = $f->{target};
      $userdb{"filters.bRegex$count"} = 0;
      $userdb{"filters.data$count"} = $f->{data};
      $userdb{"filters.modifier$count"} = ($f->{operator} eq 'contains')?FILTER_CONTAINS:FILTER_DEVOID;
      if ($f->{key} eq 'to') {
         $userdb{"filters.type$count"} = FILTER_TO;
      } 
      elsif ($f->{key} eq 'from') {
         $userdb{"filters.type$count"} = FILTER_FROM;
      }
      elsif ($f->{key} eq 'subject') {
         $userdb{"filters.type$count"} = FILTER_SUBJ;
      }
      elsif ($f->{key} eq 'headers') {
         $userdb{"filters.type$count"} = FILTER_HEAD;
      }
      elsif ($f->{key} eq 'body') {
         $userdb{"filters.type$count"} = FILTER_BODY;
      }
      elsif ($f->{key} eq 'all') {
         $userdb{"filters.type$count"} = FILTER_ANY;
      } else {
         next;
      }
      
      $count++;
   }
   
   $userdb{"filters.total"} = $count - 1;

}        

sub create_filter 
{

   my @filters = split(/\s+/, $userdb{'options.filters'});   
   my %filters = map { $_ => 1 } @filters;
   my $id;

   # Find the first unused ID.
   for (my $i=1; $i < @filters; $i++) {
      if (!$filters{$i}) {
          $id = $i;
          debug "found missing slot: $i";
          last;
      }
   }

   # If there were no gaps, use the next available ID
   $id ||= @filters + 1;
   
   # Clear Filter
   $userdb{"filters:$id:name"} = '';
   $userdb{"filters:$id:key"} = '';
   $userdb{"filters:$id:operator"} = '';
   $userdb{"filters:$id:data"} = '';
   $userdb{"filters:$id:action"} = '';
   $userdb{"filters:$id:target"} = '';
   $userdb{"filters:$id:active"} = 0;
   
debug "DEDEBUG: new id: $id";
   push (@filters, $id);
   
   $userdb{'options.filters'} = join(' ', @filters);
   
   return $id;
}

# Hrm. Long name.
sub get_filter_lookup_table
{

   # Features unavailable at this time are commented out

   my $keys = { 
      from    => 'Sender',
      to      => 'Recipient',
      subject => 'Subject',
      body    => 'body',
#      cc      => 'CC',
#      date    => 'Date',
      headers => 'Headers',
      all     => 'Headers and Body',
   };

   my $operators = {
#      eq         => 'equals',
#      ne         => 'doesn\'t equal',
      contains   => 'contains',
      nocontains => 'doesn\'t contain',
#      begins     => 'begins with',
#      ends       => 'ends with'
   };

   my $actions = {
      move => 'Move',
#      copy => 'Copy'
   };
    
   my $h = {
      keys => $keys,
      operators => $operators,
      actions => $actions
   };
   
   return $h;
}

sub get_filters
{
   my @filters; 
   
   # Backwards compatibility
   if (!exists $userdb{'options.filters'}) {
      debug "importing filters";
      # Import old-style filters
      &import_filters();
   }
   
   my @sort = split(/\s+/, $userdb{'options.filters'});
   my @keys = grep(/^filters:/, keys %userdb);

   foreach my $f (@sort) {
      my %filter;
      my @keys = grep(/^filters:$f:/, keys %userdb);

      foreach my $k (@keys) {
         my $v = $userdb{$k};
         $k =~ s/^filters:$f://;
         $filter{$k} = $v;
      }
      
      if (%filter) {
         $filter{filterid} = $f;
         push(@filters, \%filter);
      }
   }
   
   return @filters;
}

sub import_filters
{
   my @filters;
   
   my $total = $userdb{"filters.total"};
   for (my $i=1; $i <= $total ; $i++) {

      my $type = $userdb{"filters.type$i"};
      next if ($type & FILTER_DELETE);

      my $id = &create_filter;
      push(@filters, $id);
      
      if    ($type & FILTER_TO)   { $userdb{"filters:$id:key"} = 'to' }
      elsif ($type & FILTER_FROM) { $userdb{"filters:$id:key"} = 'from' }
      elsif ($type & FILTER_SUBJ) { $userdb{"filters:$id:key"} = 'subject' }
      elsif ($type & FILTER_HEAD) { $userdb{"filters:$id:key"} = 'headers' }
      elsif ($type & FILTER_BODY) { $userdb{"filters:$id:key"} = 'body' }
      elsif ($type & FILTER_ANY)  { $userdb{"filters:$id:key"} = 'all' }

      if ($type & FILTER_OFF) { 
         $userdb{"filters:$id:active"} = 0;
      } else {
         $userdb{"filters:$id:active"} = 1;
      }

      my $modifier = $userdb{"filters.modifier$i"};
      if ($modifier & FILTER_CONTAINS) {
         $userdb{"filters:$id:operator"} = 'contains';
      } else {      
         $userdb{"filters:$id:operator"} = 'nocontains';
      }

      $userdb{"filters:$id:data"}   = $userdb{"filters.data$i"};
      $userdb{"filters:$id:action"} = 'move';
      $userdb{"filters:$id:target"} = $userdb{"filters.action$i"};

   }

   $userdb{"options.filters"} .= ' '.join(' ', @filters);
}      


sub try_mx_hosts {
    my ($proto, $pophost, @params) = @_;
    my $validpop = "";

    my $orig_pop = $pophost;
    $pop = undef;

    debug "trying mx hosts";

#  TRY_POP_PREFIX:
#    {
#        last if ($proto !~ /pop/i);
#        last if (defined($hostnames{"pop.$orig_pop"}) && 
#                 !$hostnames{"pop.$orig_pop"});
#        last if ($orig_pop =~ /^pop\./i);
#
#        $hostnames{"pop.$orig_pop"} = validate_hostname("pop.$orig_pop",1)
#            if (!defined($hostnames{"pop.$orig_pop"}));
#
#        last if (!$hostnames{"pop.$orig_pop"});
#
#        debug "trying pop.$orig_pop protocol $proto";
#
#        return "pop.$orig_pop" if (validate_login("pop.$orig_pop", $proto));
#
#        debug "pop.$orig_pop failed";
#        $validpop = "pop.$orig_pop";
#    }
#
#  TRY_MAIL_PREFIX:
#    {
#        last if (defined($hostnames{"mail.$orig_pop"}) && 
#                 !$hostnames{"mail.$orig_pop"});
#        last if ($orig_pop =~ /^mail\./i);
#
#        $hostnames{"mail.$orig_pop"} = validate_hostname("mail.$orig_pop",1)
#            if (!defined($hostnames{"mail.$orig_pop"}));
#
#        last if (!$hostnames{"mail.$orig_pop"});
#
#        debug "trying mail.$orig_pop protocol $proto";
#
#        return "mail.$orig_pop" if (validate_login("mail.$orig_pop", $proto));
#
#        debug "mail.$orig_pop failed";
#        $validpop = "mail.$orig_pop";
#    }
#
#  TRY_IMAP_PREFIX:
#    {
#        last if ($proto !~ /imap/i);
#        last if (defined($hostnames{"imap.$orig_pop"}) && 
#                 !$hostnames{"imap.$orig_pop"});
#        last if ($orig_pop =~ /^imap\./i);
#
#        $hostnames{"imap.$orig_pop"} = validate_hostname("imap.$orig_pop",1)
#            if (!defined($hostnames{"imap.$orig_pop"}));
#
#        last if (!$hostnames{"imap.$orig_pop"});
#
#        # one more try, for IMAP
#        debug "trying imap.$orig_pop protocol $proto";
#        return "imap.$orig_pop" if (validate_login("imap.$orig_pop", $proto));
#
#        debug "imap.$orig_pop failed";
#        $validpop = "imap.$orig_pop";
#    }


    # OK... failed login or creating $pop. Let's try some
    # other options. Do an MX lookup and try it that way,
    # and as a last resort try to add pop. and/or mail. prefix
    my @mx = mx($pophost);
        
    if ($mx[0]) {
        my $mxhost = $mx[0];
        $mxhost = $mxhost->exchange;
        debug "trying mx host $mxhost protocol $proto";

        # We'll assume the mx host is valid, since it comes from DNS
        $hostnames{$mxhost} = 1;

        return $mxhost if (validate_login($mxhost, $proto));

        debug "$mxhost failed";
        $validpop = $mxhost;
    }

    return undef;
#    return $validpop if ($pop);
}



# Figure out the current IMAP delimiter
sub get_imap_delimiter
{
   my ($force) = @_;

   if ($protocol =~ /imap/i && ref $pop ne 'EMU::IMAP') {
      debug "logging in.";
      my $user = $userdb{"folder:$inbox:username"};
      my $p = decode2($userdb{"folder:$inbox:password"});
      
      my $host = $userdb{"folder:$inbox:hostname"};
      &do_imap_login($user,$p,$host,$inbox,1);
   }

   if (ref $pop eq 'EMU::IMAP') {
      
      # Force? Then lets go fetch the delimiter
      if ($force && !$pop->{delimit}) {
         $pop->fetch_delimiter;
      }

      debug "imap delimiter: ", ($pop->{delimit} || $c{default_imap_delim} || '/'), " ; \$pop->{delimit}:", $pop->{delimit}," ; default_imap_delim: $c{default_imap_delim} ;"; 
      return $pop->{delimit} || $c{default_imap_delim} || '/';

   } else {
      return $c{default_imap_delim} || '/';
   }
}   

sub update_subscriptions
{

   my @newfolders = $query->param('subscribed');
   my @curfolders = &get_subscribed_folders;

   my (@add, @del);
   
   foreach my $f (@curfolders) {
      if ($f && !grep($f eq $_, @newfolders)) {
         push(@del, $f);
      }
   }
   
   foreach my $f (@newfolders) {
      if ($f && !grep($f eq $_, @curfolders)) {
         push(@add, $f);
      }
   }
   
   foreach (@del) {
      &set_folder_subscription($_, 0);
   }
   
   foreach (@add) {
      &set_folder_subscription($_, 1);
   }
   
   folders();
}

sub questionaire
{
   my ($data, $msg) = @_;

   set_status($msg);
   write_tmp('data', $data);
   write_tmp('first', 1); 
   load_page('questionaire.html');
}

sub questionaire_parse
{
   my $recipient = 'emuuser@emumail.com';
   my $host = 'smtp.emumail.com';
   
   # Allow professional licenses to use the questionaire for their own purposes
   if ($AD_VERT == 0) {
      $recipient = $c{questionaire_recipient} if $c{questionaire_recipient};
      $host = $smtp_host[0] if $smtp_host[0];
   }

   debug "recipient: $recipient ; host: $host";
   
   my %vars;
   my @missing;

   write_tmp("first", 1);

   foreach my $k ($query->param) {
      my $v = $query->param($k);
      if ($k =~ /^\!/ && $v !~ /\S/) {
         push(@missing, $k);
      } else {
         debug "Setting $k => $v";
         $vars{$k} = $v;
      }
   }

   # We don't want this cluttering our data
   delete $vars{passed};
   
   # Send them back to the questionaire if they are missing required fields.
   if (@missing) {
      debug "Missing fields: @missing";
      my $err = $msg{"ERR_MISSING_DEMO_DATA"} || "Missing data for required fields:";
      my $msg = $err.join(', ', map { substr($_,1) } @missing);
      return &questionaire(\%vars, $msg );
   }

   my $msg = <<"EOD";
To: $recipient
From: emuuser\@emumail.com
Subject: Emumail User

#### System Info

Server Host: $ENV{HTTP_HOST}
OS: $^O
Server Software: $ENV{SERVER_SOFTWARE}
Emu Version: $EMU::Version
Emu Revision: $EMU::Revision
Date: $EMU::Date
Distribution: $EMU::dist
Language: $EMU::Language

#### User Info

Email: $userdb{'options.email'}
User Agent: $ENV{HTTP_USER_AGENT}

EOD
   
   foreach my $k (keys %vars) {
      $k =~ s/^\!//g;
      $msg .= "$k: $vars{$k}\n";
   }
   
   eval { 
      my $smtp = Net::SMTP_auth->new($host, Port=>$smtp_port);
      $smtp->auth('CRAM-MD5', $user_name, $password) if defined $c{smtp_auth};
      $smtp->mail('emuuser@emumail.com');
      $smtp->to($recipient);
      $smtp->data($msg);
      $smtp->quit();
   };
   
   # Log any errors, but don't die.
   if ($@) {
      debug "Error enountered when attempting to email questionaire: $@";
   }

   $userdb{"questionaire_complete"} = 1;
           
   go_index(1);
}


sub get_search_key {
    # returns a search key string for a given filter type

    my ($type, $str) = @_;

    debug "filter_type $type, string $str";

    if ($type == FILTER_BODY) {
       return qq/BODY "$str"/;
    }
    elsif ($type == FILTER_HEAD) {
       # Yes, this seems to be the correct syntax.
       return qq/OR OR OR OR OR OR OR OR FROM "$str" TO "$str" SUBJECT "$str" CC "$str" BCC "$str" HEADER "Content-type" "$str" HEADER "Date" "$str" HEADER "Reply-to" "$str" HEADER "Priority" "$str"/;
    }
    elsif ($type == FILTER_ANY) {
       return qq/TEXT "$str"/;
    }
    elsif ($type == FILTER_FROM) {
       return qq/FROM "$str"/;
    }
    elsif ($type == FILTER_SUBJ) {
       return qq/SUBJECT "$str"/;
    } 
    elsif ($type == FILTER_TO) {
       return qq/OR TO "$str" CC "$str"/;
    } else {
       debug "Uknown filter type '$type'!";
    }
}

sub filter_messages_imap
{
	# This is the imap filtering method. Will filter messages in the current
	# folder using imap search commands... rather than doing manual filtering
	# in the messages files...

	my ($flag) = @_;
	my ($filterto, $filter);

	# no filters? then outta here
	return if (!$userdb{"filters.total"});

	# if trashbin
	return 0  if ($trash_bin && ($folder eq $trash_folder));

	# let's allow for filtering only on mailboxes and the inbox
	return 0 if (!$userdb{"folder:$folder:external"} && $folder ne $inbox);

	my $uid_validity = $pop->{uidvalidity};
	debug "grabbed uidvalidity: $uid_validity";

	my $savefolder = remove_fold_prefix($folder);

	my @substatuses = ();
	$v{"filtered to"} = 0;
	my $hasResults = 0;

	LOOP_THRU_FILTERS:
	{
		for (my $i = 1; $i <= $userdb{"filters.total"}; $i++)
		{
			# skip ones turned off (disabled)
			next if ($userdb{"filters.type$i"} == FILTER_OFF);

			# set the name of the folder that we're filtering to
			$filterto = $userdb{"filters.action$i"};
			debug "filterto=$filterto type is ".$userdb{"filters.type$i"};

			# the regex to filter by. if the user has specified that they 
			# want this to be a perl5 regex
			# then don't quote it, otherwise quote the meta characters.
			$filter = $userdb{"filters.data$i"};
			debug "filter=$filter";

			my $search_key = get_search_key($userdb{"filters.type$i"}, $filter);

			$search_key = "NOT ".$search_key
				if ($userdb{"filters.modifier$i"} != FILTER_CONTAINS);

			$search_key = "$flag ".$search_key if ($flag);

			# after building the search expression, we need to add
			# the "undeleted" qualifier so we dont search over messages
			# already deleted!
			$search_key = "UNDELETED $search_key";
			debug "built a search key: $search_key";
			next unless $search_key;

			push (my @matches, @{$pop->search($search_key)});

			# we have to add the validity prefix!
			@matches = map { "$uid_validity$_" } @matches;
			debug "we have ".($#matches+1)." matches" if ($#matches >=0);

			FILTER_OUT_MATCHES:
			{
				debug "folder is $savefolder";
				last if (scalar @matches <= 0 || ($savefolder eq $filterto));
				$folder = $filterto;
				$v{"last_folder"} = $savefolder;
				$v{"wait_count"} = 0;
				debug "lf: $savefolder";

				# check for action, is this a garbage (simply delete)?
				my $garbage = $msg{"GARBAGE_Filter_Name"} || "GARBAGE";
				my $action = $c{"GARBAGE_Filter_Action"} || "Folder";

				$v{"wait_title"} = $msg{"WAIT_FilterMsgs"} || "Filtering Messages...";
				$v{"wait_action"} = convert( $msg{"WAIT_FilterAction"}, 
							($#matches+1), $filterto );

				# we need to reverse @matches because move_msg already
				# reverses so we end up moving out of chrono order
				@matches = reverse @matches;

				if ($filterto eq $garbage && $action =~ /delete/i)
				{
					# also check trash action
					if ( $trash_bin )
					{
						debug "moving to trash...";
						for my $uid (@matches)
						{
							$uid =~ s/^$uid_validity//;
							my $subject = $folderdb{"$uid_validity$uid:subj"} || $pop->get_subject($uid);
							debug "Got subject of moved email: $subject";
							$hasResults++;
							push @substatuses, convert($msg{'MSG_Filtered_Trash'}, $subject)
								if ( $hasResults <= $c{'verbosefiltering_threshhold'} );
						}

						my $match_list = join(':', @matches);
						$query->param(-name=>'d', -value=>$match_list);
						move_msg(1,1);
					}
					else
					{
						foreach my $match (@matches)
						{
							my $uid = $match;
							$uid =~ s/^$uid_validity//;
							my $subject = $folderdb{"$uid_validity$uid:subj"} || $pop->get_subject($uid);
							debug "Got subject of deleted email: $subject";
							$hasResults++;
							push @substatuses, convert($msg{'MSG_Filtered_Deleted'}, $subject)
								if ( $hasResults <= $c{'verbosefiltering_threshhold'} );
							debug "eliminating message $match";
							remove_from_folder($match,$savefolder,1);
						}
					}
				}
				else
				{
					for my $uid (@matches)
					{
						$uid =~ s/^$uid_validity//;
						my $subject = $folderdb{"$uid_validity$uid:subj"} || $pop->get_subject($uid);
						debug "Got subject of moved email: $subject";
						$hasResults++;
						push @substatuses, convert($msg{'MSG_Filtered_Moved'}, $subject, $filterto)
							if ( $hasResults <= $c{'verbosefiltering_threshhold'} );
					}
					my $match_list = join(':', @matches);
					$query->param(-name=>'d', -value=>$match_list);
					move_msg(0,1);
					debug "Filtered to $filterto from $folder";
				}

				$v{"filtered to"} += scalar @matches;
			}

			$folder = $savefolder;
			debug "set folder back to $folder";

			$changed{$filterto} = 1 if ($filterto ne $inbox);
		}
	}

	push @substatuses, "<br>\n" . $msg{'MSG_Filtered_TooMany'} if ( $hasResults > $c{'verbosefiltering_threshhold'} );
	return ( scalar @substatuses ) ? "<br>\n" . join("<br>\n", @substatuses) : '';
}


sub print_progress_new {
    my ($incr_counter,$nointerval) = @_;

    return if ($no_waitscreen || bool($c{"disable_waitscreen"}));

    $v{"wait_count"} += 1 if ($incr_counter);

    return if (time - $delay < ($v{"delay_max"} || 10));

    display_waitscreen() if (!$waiting_printed);

#    debug "no_waitscreen=$no_waitscreen waiting_printed=$waiting_printed";

#debug "wait_count $v{'wait_count'}, wait_interval $v{'wait_interval'}";
    $v{'wait_interval'} = 1 unless ($v{'wait_interval'}); # illegal modulus zero!
    return if (!$nointerval && ($v{"wait_count"} % $v{"wait_interval"} != 0));

    my $text = $v{"wait_action"};

#    debug "$text";
    print "<script language=JavaScript>\n";
    print "waitscr.document.writeln('".$text."')";
    print "\n</script>\n";

    return 1;
}

sub find_connection
{
   my ($proto, $host, $user, $pass) = @_;
   
   debug "Looking for connection with proto: $proto, user: $user, host: $host, ";
   
   my $obj = $connections{$proto}{$host}{$user}{$pass};

   if (ref $obj && $obj->isValid) {
      debug "Found connection!";      
      return $obj;
   } else {
      debug "No connection found.";
      return;
   } 
}

sub store_connection
{
   my ($obj, $proto, $host, $user, $pass) = @_;
   
   debug "Storing connection with info - obj: $obj ; proto: $proto ; user: $user ; host: $host ; ";
   if (!ref($obj) || !$proto || !$user || !$host || !$pass) {
      debug "Missing connection info!";
      return 0;
   } else {
      $connections{$proto}{$host}{$user}{$pass} = $obj;
      return 1;
   }
}

# Call 'quit' on all pooled connections
sub flush_connections
{

   my @connections = grep { ref $_ } # Only objects
                     map { values %$_ } # pass hashes
                     map { values %$_ } # user hashes
                     map { values %$_ } # host hashes
                     values %connections; # proto hashes
   
   debug "Found ",scalar(@connections)," connections";
   foreach my $c (@connections) {
      $c->quit;
   }

   undef %connections;
   
   # Can't forget about $pop
   if (ref $pop && $pop->isValid) {
      $pop->quit;
   }
   debug "All connections closed.";   

   undef $pop;
}


sub handle_signal {
    my ($signal) = @_;

    debug $signal;
#    &dumpstack(); 
#    &dump_data; 
#    error $signal;
    &flush_connections();
    &close_db() if ($db_opened); 

    # Check if special (custom) processing is necessary
    &EMU::Custom::quit() if ($EMU::Custom::call_on_quit == 1);

    exit;
}


sub folder_or_mailbox {
    # with the new iface we can have either folders or mailboxes page
    if ($passed =~ /folders/) {
        folders();
    }
    elsif ($passed =~ /mailbox/) {
        mailboxes();
    }
}


sub rescue_dbs {
    # this is a safety net because db files for some reason have a tendency
    # to grow huge, maybe corrupted?

    load_module("File::Find",0,'find');
    
    my @dbfiles = ("$homedir/userdb");
    my $subref = 
        sub { return if (! -f $File::Find::name);
              push(@dbfiles, $File::Find::name);
            };

    find(\&$subref, "$homedir/folders");

    my (%orig,%new);
    foreach my $dbfile (@dbfiles) {
        next if (!tie (%orig, $db_package, $dbfile, O_CREAT|O_RDONLY, 0660));
        next if (!tie (%new, $db_package, "$dbfile.tmp", O_CREAT|O_RDWR, 0660));

        debug "refreshing $dbfile";
        foreach (keys %orig) {
           my ($k, $v) = ($_,$orig{$_});
           $new{$k} = $v;
        }

        untie %new;
        untie %orig;

        move("$dbfile.tmp", $dbfile);
    }
}

# Removes from a directory files that match a regexp
sub wildrm
{
   my ($dir, $regexp, $negate) = @_;
   my @files;
   
   opendir DIR, $dir;

   @files = $negate ? 
        map  { "$dir/$_" }  grep { -f "$dir/$_" && !/$regexp/ } readdir DIR :
        map  { "$dir/$_" }  grep { -f "$dir/$_" && /$regexp/ } readdir DIR ;

   closedir DIR;

   debug "dir: $dir ; regexp: $regexp ; negate? $negate ; removing: @files"; 
   unlink @files;
}

sub text_wrap {
    my ($prefix, @lines) = @_;
    my $tolerance = 5;
    my @newlines;

    my $columns = $wrap_columns;

    $columns -= (length($prefix)+2) if (length($prefix));

    foreach my $l (@lines) {
    if ($l =~ /http:\/\//i && $l !~ /\s/){push (@newlines, $prefix.$l); next};#alex fix corrupted http url's
        
        $l =~ s/\r//g if ($c{'delete_new_line'});

#debug "$l";
        if (length($l) <= ($columns+$tolerance) || $l !~ /\S\s\S/) {
            #We no need to add the new line after message. Alex
	    #$l .= "\n" if ($l !~ /\n$/);
            push (@newlines, $prefix.$l);
#debug "nowrap $prefix$l";
        }
        else {
            while (length($l) > ($columns+$tolerance)) {
                my $tmp = substr($l, 0, $columns);
                my $ix = length($tmp);

                if ($tmp =~ /^([^\n]+)\n/) {
                    $tmp = "$1\n";
                    push(@newlines, $prefix.$tmp);
                    $ix = length($tmp);
#debug "0.pushing $prefix$tmp";
                }
                elsif ($tmp =~ /\s$/) {
                    $tmp .= "\n" if ($tmp !~ /\n$/);
                    push(@newlines, $prefix.$tmp);
#debug "1.pushing $prefix$tmp";
                }
                else {
                    $tmp =~ s/\s+\S+$//;
                    $ix = length($tmp);
                    $tmp .= "\n" if ($tmp !~ /\n$/);
                    push(@newlines, $prefix.$tmp);
#debug "2.pushing $prefix$tmp";
                }

                $l = substr($l, $ix);
                $l =~ s/^\s+//g if ($l !~ /^\n/);  # don't remove newlines
#debug "rest is $l";
            }

            if (length($l)) {
                $l .= "\n" if ($l !~ /\n$/);
                $l =~ s/^\s+//g;
                push(@newlines, $prefix.$l);
#debug "3.pushing $prefix$l";
            }
        }
    }

    return @newlines;
}

sub editor
{
   my @admins = split(/(,|\s)+/, $c{admins});
   
   if (! grep { $_ eq $user_name } @admins) {
      write_tmp('phrase', $msg{ERR_PermissionDenied});
      load_page('errors.html');
      return;
   }
   
   load_module('File::Find');
   load_module('Cwd');

   my $cwd = cwd();

   my $file = $query->param('file') || 'site.emu';
   my $type = $query->param('filetype') || 'config';

   $file =~ s/[^\w\.\/]|^\///g;

   write_tmp('file', $file);
   write_tmp('type', $type);

   if ($type eq 'config' || $type eq 'tmpl') {
      $file = "$page_root/$file";
   } elsif ($type eq 'html') {
      $file = "$cwd/$file";
   }

   if ( $query->param('save.x') ) {
      my $content = $query->param('content');
      $content =~ s/\r//g;
      
      open(FILE, ">$file");
      print FILE $content;
      close(FILE);
      write_tmp('content', $content);
      write_tmp('message', $msg{MSG_FileSaved});
   } else {
      open(FILE, $file);
      local $/ = undef;
      write_tmp('content', <FILE>);
      close(FILE);
   }

   my $files = ["site.emu", "lang.emu"];
   
   # First, find all config files
   my $sub = sub { return if !/\.emu$/; 
                   (my $f = $File::Find::name) =~ s/^\Q$page_root\E\///;
                   push(@$files, $f);
                 };
   File::Find::find( $sub, "$page_root/iface/" );
   
   @$files = sort @$files;
   write_tmp('config_files', $files);
   
   # Next, find all templates
   $files = [];
   $sub = sub { return if !/\.html$/i; 
                (my $f = $File::Find::name) =~ s/^\Q$page_root\E\///;
                push(@$files, $f);
              };
   File::Find::find( $sub, "$page_root/iface/" );
   @$files = sort @$files;
   write_tmp('tmpl_files', $files);
   
   # Lastly, find all static html files
   $files = ["index.html"];
   $sub = sub { return if !/\.(html|css|js|txt)$/i; 
                (my $f = $File::Find::name) =~ s/^\Q$cwd\E\///;
                push(@$files, $f);
              };
   File::Find::find( $sub, "html/" );
   
   @$files = sort @$files;
   write_tmp('html_files', $files);

   load_page("admin_file_editor.html");
}


sub export_addressbook {
    debug "here";
    load_module("EMU::Addressbook");

debug "format ".$query->param("export_format");
    my $ab = EMU::Addressbook->new("export");

    $ab->export() if ($ab);

}


sub import_addressbook {
    debug "here";
    my $fh = $query->upload('import_file');

    if (!$fh) {
        set_status(convert($msg{'ERR_UploadFailed'}, $query->param('import_file'), $query->cgi_error));
        address();
        return;
    }

    open (ADDR, ">$homedir/tmp/addressbook.in");
    while (my $line = <$fh>) {
        print ADDR $line;
    }

    close ADDR;

    load_module("EMU::Addressbook");
    debug "here2";

    my $ab = EMU::Addressbook->new("import");
    debug "here3";
    debug $ab;
    $ab->import() if ($ab);

    address();
}


sub CalendarLogin
{
    my ($username,$hostname) = split('@', $_[0]);

    debug "Logging $username into Calendar";

    # Temporarily release the userdb
    my %savedb = %userdb;
    untie %userdb;
    $ELocks->lock_remove( \%userdb );
    undef %userdb;

    # Calendar libraries
    eval("use lib '$c{cal_path}/bin'");
    load_module('EMU');
    load_module('Emucal');

    my $CFG = &EMU::LoadConfig("$c{cal_path}/bin/config.ini");
    my $LICENSE = &EMU::LoadConfig("$c{cal_path}/bin/license.ini");
    my $VERSION = $LICENSE->val('','version');
    my $Helper = EMU::Helper->new( $CFG );
    my $Driver = $Helper->getDriver;

    my $user = $Driver->getUser($username, $hostname);

    # Create the user if they are not valid
    if (! $user->isValid ) {
      $user = $Driver->createUser($username, $hostname);
    }

    my $session = $Driver->getSession;
    $session->set('userid', $user->getID);

    my $timeout = $CFG->val('Sessions', 'Timeout') || 30;
    my $cookie = CGI::Cookie->new( -name  => $CFG->val('Sessions','CookieName'),
                                   -path  => $CFG->val('Sessions','CookiePath') || '/'
                                 );

    debug "Calendar version: $VERSION";

    if ($VERSION > 1.0) {
       $session->setTimeout( $timeout );
       $session->touch;
       $session->validate;
    } else {
       $cookie->expires("+${timeout}m"); 
       $session->validate;
    }
    
    $cookie->value( [$session->getID] );

    $extra_head .= "Set-Cookie: ".$cookie->as_string."\r\n";

    # Rebind the userdb
    if ( $ELocks->lock_create("$homedir/userdb", \%userdb, {mode => 'write', nb => 1}) )
    {
    	tie(%userdb, $db_package, "$homedir/userdb", O_CREAT|O_RDWR, 0660) or debug "What? Can't tie userdb! Call 911!";
    	if( $^O =~ /Win32/ )
    	{
    		%userdb = %savedb;
    		# FIXME this place is cursed
    		# it doesn't work: nothing is stored in userdb there, because tie failed
    	}
    }
    else
    {
    	debug "GOSH! Fatal error. Can't lock and tie userdb. Everything is ruined! Call Heath, Ruslan or 911!";
    }
    
    $session->finish;
    $Helper->finish;
}

sub address_exists {
    my ($nick) = @_;
    return (grep { lc($_) eq lc("addresses.$nick")} keys %userdb);
}

sub mailcheck {

   my ($total_messages_old) = get_total_msgs();

   # This is the stupid crap we have to do to
   # force a refresh in get_index
   $v{"force_check"} = 1;
   
   get_index();

   my ($total_messages_now) = get_total_msgs();

   my $data = $total_messages_now - $total_messages_old;

   write_tmp('refresh_frame', $userdb{"options.checkmail"}); #01/13/03: How often to check for new mail /popup-window/ Alex
   write_tmp('data', $data);
   load_page('iframe_update_message.html');
}

sub group_exists {
    my ($orig) = @_;
    return (grep { lc($_) eq lc("addressgroup.$orig")} keys %userdb);
}

sub address_groups{

    my @addrs = grep(/^addressgroup\./, keys %userdb);
    @addrs = sort alpha @addrs;
    my $addrs = join(' ', @addrs);

    write_tmp('data', $addrs);
    load_page('groups.html');

}

sub edit_address_group{

debug("editing address group...");

if ($query->param('delete.x')){
    my $orig = $query->param('deleted');
    debug("deleting ".$userdb{"addressgroup.$orig"});
    delete $userdb{"addressgroup.$orig"};
    my @addrs = grep(/^addressgroup\./, keys %userdb);
    @addrs = sort alpha @addrs;
    debug("now address book have ".@addrs." addresses"); 
    my $addrs = join(' ', @addrs);
    write_tmp('log', $orig);
    write_tmp('data', $addrs);
    load_page('groups.html');
}

elsif ($query->param('new_group')){
    my $orig = $query->param('new_group');
    my $old = $query->param('editfolder');
		
		debug ("original is $orig old is $old");
		
    $orig =~ s/ /_/g;
    $orig =~ s/[:\@]//g;

    if (group_exists($orig)) {
            set_status(convert($msg{'MSG_GroupExists'}, $orig));
        }
        else {
            if ($old){

               my $draft=$userdb{"addressgroup.$old"};
               delete $userdb{"addressgroup.$old"};
               $userdb{"addressgroup.$orig"}=$draft;
               set_status(convert($msg{'MSG_GroupRenamed'}, $old, $orig));
            }else{$userdb{"addressgroup.$orig"} = "";
               set_status(convert($msg{'MSG_GroupAdded'}, $orig));
            }
        }

    my @addrs = grep(/^addressgroup\./, keys %userdb);
    @addrs = sort alpha @addrs;
    my $addrs = join(' ', @addrs);

    write_tmp('log', $old);
    write_tmp('data', $addrs);
    load_page('groups.html');
}

elsif ($query->param('group')){

    my @addr = grep(/^addresses\./, keys %userdb);
    @addr = sort alpha @addr;
    my $addr = join('||', @addr);

    write_tmp('data', $addr);
    my $group = $query->param('group');
    write_tmp('log', $group);
    load_page('groups_editor.html');
}

elsif ($query->param('select2')){
    my $group = $query->param('select_group');
    my @val = $query->param('select2');
    my $val = join (":", @val);
    my $newname = $query->param('groupname');

    $newname =~ s/ /_/g;
    $newname =~ s/[:\@]//g;

    delete $userdb{"addressgroup.$group"};
    $userdb{"addressgroup.$newname"}="$val";

    my @addr = grep(/^addressgroup\./, keys %userdb);
    @addr = sort alpha @addr;
    my $addr = join(' ', @addr);

    write_tmp('data', $addr);
    write_tmp('log', $val);
    load_page('groups.html');

}
elsif ($query->param('groupname')){

    my @val = $query->param('select2');
    my $val = join (":", @val);
    my $newname = $query->param('groupname');
    my $group = $query->param('select_group');
    
    $newname =~ s/ /_/g;
    $newname =~ s/[:\@]//g;
    
    $userdb{"addressgroup.$newname"} = $userdb{"addressgroup.$group"};

    delete $userdb{"addressgroup.$group"};

    my @addr = grep(/^addressgroup\./, keys %userdb);
    @addr = sort alpha @addr;
    my $addr = join(' ', @addr);

    write_tmp('data', $addr);
    write_tmp('log', $val);
    load_page('groups.html');

}else{
    
    my @addrs = grep(/^addressgroup\./, keys %userdb);
    @addrs = sort alpha @addrs;
    my $addrs = join(' ', @addrs);

    write_tmp('data', $addrs);
    load_page('groups.html');
    }
}

sub send_readreceipt
{
	my ($msg, $folder, $dontshowpages) = @_;
	my ($msg_id) = $msg || $query->param('variable');
	unless ($msg_id)
	{
		debug "ERROR: there is no message id specified, so we can't send read receipt";
		if ($dontshowpages) { return 0; } else { go_index(); }
	}
	
	debug "folder is: $folder, msg_id: $msg_id; we are ready to send read receipt";

	SEND_READ_RECEIPT:
	{
		# we don't want to send dups
		last SEND_READ_RECEIPT if ($folderdb{"$msg_id:mdn-sent"});

		if ($query->param('option') eq 'dontsend')
		{
			debug "user refused to send read receipt";
			$folderdb{"$msg_id:mdn-sent"} = 0;
			last SEND_READ_RECEIPT;
		}
	
		$folderdb{"$msg_id:mdn-sent"} = 1;
		# message attrs
		my $e_from = $folderdb{"$msg_id:from"};
		my $e_subj = $folderdb{"$msg_id:subj"};
		my $e_date = $folderdb{"$msg_id:date"};
		my $e_mid  = $folderdb{"$msg_id:messageid"};
		my $e_mdnemail = $folderdb{"$msg_id:mdn"} || $e_from;
	
		# get full FROM address
		my $from = $userdb{"options.email"} || $user_name;
	    	my $real_name = reverse_html($userdb{"options.real_name"});
		my $addr_parse = Mail::Address->new($real_name, $from);
	    	my $fullfrom = $addr_parse->format();
	    	
	    	# get MDN (i.e. TO) address
	    	my $obj_mdnaddr = (Mail::Address->parse($e_mdnemail))[0];
	    	my $mdn_justemail = ($obj_mdnaddr) ? $obj_mdnaddr->address : '';
	
		my $mdnsubject = $msg{'MSG_MDNSubject'} || '';
		$mdnsubject = convert($mdnsubject, $e_subj); # replace %d+
		
		if ($from && $mdn_justemail)
		{
			my %hash =
			(
			'Date' 			=> scalar get_date(0,0,1),
			'From' 			=> $fullfrom,
			'Reply-To' 		=> $fullfrom,
			'To'			=> $e_mdnemail,
			'Subject'		=> $mdnsubject,
			'Mime-Version'		=> '1.0',
			'Type'			=> 'multipart/report; report-type=disposition-notification',
			'Disposition'		=> undef,
			'X-Mailer' 		=> get_xmailer_string() || undef,
			"X-Browser"    		=> "$ENV{'HTTP_USER_AGENT'}",
			'X-Priority'		=> '3 (Normal)',
			'X-Browser-IP'	=> $ENV{"REMOTE_ADDR"},
			'X-webmail-user'	=> $user_name,
			'X-HTTP_HOST'		=> $ENV{'HTTP_HOST'},
			);
			
			my $entity = new MIME::Entity;
			$entity->build(%hash);
			
			my $readabletext = $msg{'MSG_MDNHumanReadable'};
			$readabletext = convert($readabletext, $e_date, $e_subj, $e_mdnemail); # replace %d+
			my $tagline = convert($msg{'MSG_MDNTagline'}, $EMU::Version);
		
			# human readable part
			my %firstpart = 
			(
			'Data'		=> $readabletext . ' ' . $tagline,
			'Type'		=> 'text/plain',
			'Encoding'	=> '7bit',
			'-Disposition'	=> undef,
			'Charset'	=> 'iso-8859-1'
			);
			$entity->attach(%firstpart);
			
			# next part
			my %nextpart =
			(
			'Data'		=> "Reporting-UA: $from; EMUmail $EMU::Version (http://www.emumail.com/)\nFinal-Recipient: rfc822; $from\nOriginal-Message-ID: $e_mid\nDisposition: automatic-action/MDN-sent-manually;displayed\n",
			'Type'		=> 'message/disposition-notification',
			'-Disposition'	=> undef,
			'-Encoding'	=> undef,
			);
			$entity->attach(%nextpart);
	
			# send it
			my $smtp;
			foreach my $host (@smtp_host)
			{
				#$smtp = Net::SMTP->new($host, Port=>$smtp_port);
				$smtp = Net::SMTP_auth->new($host, Port=>$smtp_port);
        			$smtp->auth('CRAM-MD5', $user_name, $password) if defined $c{smtp_auth};
				debug "$host is no good, going on to next!" unless $smtp;
				next unless $smtp;
	        		last;
			}
	
			if ($smtp)
			{
				my $errors = 0;
				
				my $result = $smtp->mail($from);
				unless ($result)
				{
					debug "SERVER CODE: ", $smtp->code, "; MESSAGE:", $smtp->message;
					$errors++;
				}
				
				$result = $smtp->to($mdn_justemail);
				unless ($result) 
				{
					debug "SERVER CODE: ", $smtp->code, "; MESSAGE:", $smtp->message;
					$errors++;
				}
	
				unless ($errors)
				{
					$smtp->data();
					for my $lineh ($entity->header)
					{
						$smtp->datasend($lineh);
					}
					for my $lineb ($entity->body)
					{
						$smtp->datasend($lineb);
					}
					$smtp->dataend();
					$smtp->quit();
					
					set_status($msg{'MSG_MDNSent'}); # OK
				}
			}
			else
			{
				set_status($msg{'ERR_SmtpServConnect_S'});
				debug "read receipt can't be sent to $e_mdnemail because of smtp error";
			} # endif $smtp
		}
		else
		{
			set_status($msg{'ERR_MDNSent'}); # FAIL
		} #endif from && mdnemail
	} # end of SEND_READ_RECEIPT
	
	msg($msg_id) unless $dontshowpages;
}

sub isActivity4Session
{
	# do we or we don't need to refresh session data?
 	my $fake_refresh = ($passed eq 'mailcheck' 
 			    || $query->param('passed') eq "compose_parse" 
 			    || ($passed eq 'go_index' && $query->param('variable') eq 'refresh')
 			    );
	return !$c{"disable_auto_session_freshen"} && !$fake_refresh;
}

sub get_xmailer_string
{
	my $xmailer = $c{xmailer} || "EMUmail " . $EMU::Version;
	return $xmailer;
}

sub proLinker{
	my $text = shift;
	my $target = get_target();

	return $text if $text !~ /http|https|ftp|www\.|\@/;

	my @yes;
	my $i;
	$text =~ s/\n/`````` /g;
	my @text = split (/ /,$text);
	foreach $i (@text)
		{
		 	if ($i =~ s {http://(((?!\&\#)[^\s\'\"\`\{\}\[\]\(\)\*\|\>\<])+)} {<A HREF="http://$1" target=$target>http://$1</A>}i)
			{push (@yes, $i); next};
			if ($i =~ s {https://(((?!\&\#)[^\s\'\"\`\{\}\[\]\(\)\*\|\>\<])+)} {<A HREF="https://$1" target=$target>https://$1</A>}i)
			{push (@yes, $i); next};
			if ($i =~ s {ftp://(((?!\&\#)[^\s\'\"\`\{\}\[\]\(\)\*\|\>\<])+)} {<A HREF="ftp://$1" target=$target>ftp://$1</A>}i)
			{push (@yes, $i); next};
			if ($i =~ s {([^\=\&\;\[\]\(\)\{\}\"\'\<\>\s\`,]+\@[^\[\]\{\}\*\&\^\(\)\"\'\<\>\s,\`]+)} {url_mailto($1)}sgei)
			{push (@yes, $i); next};
			$i =~ s~(www\.[^<>\@\s\n\]\[]+?\.[^<>\@\s\n\]\[]+)~<a href="http://$1" target=$target>$1</a>~i;
			push (@yes, $i);
		}


	$text = join(' ', @yes);
	$text =~ s/``````( |)/\n/g;

	return $text;
}

sub calevent_add
{
	# Calendar libraries
	print_header();
	if ( $c{cal_path} )
	{
	    eval("use lib '$c{cal_path}/bin'");
	    load_module('EMU');
	    load_module('Emucal');
	
		eval
		{
		    my $CFG = &EMU::LoadConfig("$c{cal_path}/bin/config.ini");
		    my $LICENSE = &EMU::LoadConfig("$c{cal_path}/bin/license.ini");
		    my $VERSION = $LICENSE->val('','version');
		    my $Helper = EMU::Helper->new( $CFG );
		    my $Driver = $Helper->getDriver;
		    my $User = $Driver->getUser(split('@', $user_name));
	    	my $Event = $User->getEvent(undef);
			my $start  = Date::Calc->new( 
									$query->param('start_year'), 
									$query->param('start_month'), 
									$query->param('start_day'), 
									$query->param('start_hour'), 
									$query->param('start_minute'), 
									0);
			my $finish = Date::Calc->new( 
									$query->param('finish_year'), 
									$query->param('finish_month'), 
									$query->param('finish_day'), 
									$query->param('finish_hour'), 
									$query->param('finish_minute'), 
									0);
			my @cals = $User->getCalendars;
			my $DefaultCal;
			for my $c (@cals)
			{
				if ( $c->get('name') eq 'default' )
				{
					$DefaultCal = $c; last;
				}
			}
			die "Can't find default calendar to add event" unless $DefaultCal; # it's safe to die in eval block
			
			debug "Found default calendar to add event with ID " . $DefaultCal->getID;
			
			$Event->set( 'calendar', $DefaultCal );
	    	$Event->set( 'start', $start );
	    	$Event->set( 'finish', $finish );
	    	$Event->set( 'start_time', Date::Calc->new(1, 0, 0, 0, $start->time) );
	    	$Event->set( 'finish_time', Date::Calc->new(1, 0, 0, 0, $finish->time) );
	    	$Event->set( 'title', $query->param('title') );
	    	$Event->set( 'description', $query->param('description') );
	    	$Event->set( 'location', $query->param('location') );
	    	$Event->set( 'category', $query->param('category') );
	    	my $rs = Emucal::RecurSet->new;
	    	$Event->set( 'recurrence', $rs );
	    	
	    	if ($Event->isValid)
	    	{
	    		$Event->commit;
	    	} else
	    	{
				$User->addEvent($Event);
			}
		    $Helper->finish;
		};
		if ( $@ ) 
		{
			print "<center><font color='red'><b>Error:</b> Event NOT Added, because something went wrong!</font><br>\n($@)</center><br>\n";
		} else {
			print "<center><b>Success:</b> Event Added</center><br>\n";
		}
	}
	else
	{
		print "<center><font color='red'><b>Error:</b> Sorry, Calendar is not installed properly. See your Calendar's manual.</font></center>\n<br>\n";
	}
	print "<center>&nbsp;<br><input type=button value='Close Window' onclick='window.close()'></center>\n";
}

sub has_spam_header
{
	my ($messageid) = @_;
	return undef unless $c{'spam_determinative_header'};
	return undef if (!$userdb{'options.filter_spam'} 				# no action if user doesn't want it 
						&& !$userdb{'options.filter_spam_folder'}); # or no folder to move message
	
	debug "going to check message for spam header...";
	
	my $head = eval { MIME::Head->from_file( "$homedir/messages/$messageid" ) };
	if ( !$head || $@ )
	{
		debug "error parsing message header";
		return undef;
	}
	
	$head->unfold($c{'spam_determinative_header'}); # get rid of inner newlines
	my $field = $head->get($c{'spam_determinative_header'}, 0);
	$field =~ s/\r?\n$//; # get rid of trailing newline

	return 0 unless defined $field;

    if ( load_module("EMU::Custom") )
    {
	    debug "call to Custom::spam_filter_by_header($field)";
    	my $result = EMU::Custom::spam_filter_by_header($field);
    	debug "Custom::spam_filter_by_header returned $result";
    	if ( defined $result )
    	{
    		return $result;
    	}
    	return 1; # we have this header field and custom function returned undef (means we ignore it)
    }
}

sub filter_spam_header
{
	my ($messageid, $originalfolder) = @_;
	return unless $messageid;
	my $f_folder = $userdb{'options.filter_spam_folder'};
	$v{"filteredspam"}++;
	my $garbage = $EMU::msg{'V_FilterTrash'} || 'GARBAGE';

	$query->param(-name=>'d', -value=>$messageid);
	my $old_lst_fldr = $v{'last_folder'}; $v{'last_folder'} = $originalfolder;
    if ($f_folder eq $garbage)
    {
        # also check trash action
        if ( $trash_bin )
        {
            debug "moving to trash...";
			move_msg(1, 1, 1);
        }
        else
        {
            debug "eliminating message $messageid";
            remove_from_folder($messageid, $originalfolder, 1, 1);
        }
    }
    else
    {
    	debug "filtering to \"$f_folder\" $messageid from $originalfolder";
		my $old_folder = $folder; $folder = $f_folder;
        move_msg(0, 1, 1);
        $folder = $old_folder;
    }
	$v{'last_folder'} = $old_lst_fldr;

	debug "setting status...";
	if ( !$trash_bin && $f_folder eq $garbage )
	{	set_status( convert($msg{'MSG_DeletedSpamMessages'}, $v{'filteredspam'}) );
	} else
	{	set_status( convert($msg{'MSG_MovedSpamMessages'}, $v{'filteredspam'}, $f_folder) );
	}	
}

sub disable_style_mod
{
#this sub will remove some tags from html messages.
my $text = $_[0];
	$text =~ s!< ?style.*?>.+?< ?/ ?style.*?>!!gsi;
        $text =~ s!< *script.*?>.+?< ?/ ?script.*?>!!gsi;
        $text =~ s!< *meta.*?>!!gsi;
        $text =~ s!< *link.*?>!!gsi;

return $text;	
}

sub mark_read_unread
{
    my @msgID = @_;
	if (scalar(@msgID) == 1){
		set_status($msg{'MSG_MarkedMessage'});
	}else{
		set_status( convert ($msg{'MSG_MarkedMessageMulti'}, scalar @msgID));	
	}
		
	foreach my $uid (@msgID){
		$folderdb{"$uid:stat"} = ($folderdb{"$uid:stat"} == 0) ? 1 : 0; 
	}
						    
	go_index(1);	
}

sub folder_stats
{	
	my $new_emails;
	for (keys %folderdb)
	{
	 if ($_ =~ m'stat')
	 {
	 	if ( $folderdb{$_} == STAT_NEW )
	 	{
	 		$new_emails++;
	 	}
	 }
	}	
	return "(".$new_emails.")" if $new_emails;
}

1;
