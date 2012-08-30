# EMU::Config package -- stores and exports the configuration variables
#  This package helps the security of the program by only exporting config
#  variables that we need to use and therefore not allowing the user to clobber
#  special data.
package EMU::Config;

use IO::File;
use Exporter ();
use strict;

use vars qw/@ISA @EXPORT/;

@ISA = qw(Exporter);
@EXPORT = qw(%dictionary);

sub new
{
    my ($class)    = shift;
    my $configFile = shift;
    my $self = {};

    # initialize the configuration
    $self->{'Config'} = {};
    $self->{'configFile'} = $configFile;

    # Now read in and parse the configuration file

    bless $self, $class;

    return $self;
}

# getConfig
#
# return the Config section of our object.
#
sub getConfig { return shift->{'Config'} };

sub get { return $_[0]->{'Config'}->{$_[1]} }

# readConfig
#
# We allow the user to end lines in \'s, which will
# make it so that the key is continued on the next line.
#
# Comments beginning with # are allowed
#
# Drawbacks: quotes aren't supported in a special way!
sub readConfig 
{
    my $self = shift;
    my ($line, $val, $key);
    my $lineContinue = 0;	# do we continue def on next line ?

    local($^W) = 0;

    my $configFile = $self->{'configFile'};
    my $rh_config  = $self->{'Config'};
    
    open (FILE, $configFile) or return;
    my @lines = <FILE>;
    close(FILE);

    for (my $i=0; $i<@lines;$i++)
    {
        my $line = $lines[$i];
#&EMU::debug("Line $i is $line");        
#	print $line;
	chomp($line);
	next if ($line =~ /^\s*\#/);
	
	if ($lineContinue) {
	    $val = $line;
	} else {
            next if ($line !~ /=/);
	    ($key, $val) = split(/\s*=\s*/, $line, 2);

	    next if (!defined $key);

	    $key = trim($key);
	}
	
	if ($val =~ s[\\$][]) {
	    $lineContinue = 1; # continue the definition on the next line
	} else {
	    $lineContinue = 0; # stop it now
	}
	
	$val = trim($val);
	
	if ($key eq '%INCLUDE') {
	
#&EMU::debug("Handling %INCLUDE of $val");
	
	   my $filename = $val;
	   
	   if ($filename !~ /^\//) {
	      $filename = $EMU::page_root.'/'.$filename;
	   }
	   
	   if ($filename ne $configFile && open(FILE, $filename)) {
              my @file = <FILE>;
	      splice(@lines, $i+1, 0, @file);
	      close(FILE);
	   }
	   
	   next;
        }


#&EMU::debug("Assigning $key => $val");

	$rh_config->{$key} .= $val;
    }     
    
    # Now do whatever little processing we need to do to the configuration
    # data in order to make it valid.  Examples of this include replacing
    # key references ([xxx]) with their appropriate values.  If the [xxx]
    # pointed to in the config doesn't exist, then the literal [xxx] is
    # replaced in.  Is this how it should be ?
  PROCESS_CONFIG:
    {
	my ($key, $val);
	
	map {
	    # process [xxx]'s.
	    $rh_config->{$_} =~ s/\[([\w_]+)\]/exists $rh_config->{$1} ? $rh_config->{$1} : "[$1]"/ge;

	    # convert false's to 0's and true's to 1's --- no longer case sensitive, 99/08/19, mike
	    $rh_config->{$_} = 0 if (lc($rh_config->{$_}) eq "false");
	    $rh_config->{$_} = 1 if (lc($rh_config->{$_}) eq "true");

	    # 07/22/98: replace \n's and \r's
	    $rh_config->{$_} =~ s/\\r/\r/g;
	    $rh_config->{$_} =~ s/\\n/\n/g;
	    
	} keys %$rh_config;
    }

    $self;
}

# This is causing some errors on multi lines that you want a space at the end
# But I can't think how to fix it right now. &nbsp I guess?    
sub trim { my $str = shift; $str =~ s/^\s*|\s*$//g; return $str }

1;

