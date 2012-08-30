package EMU::Init;

use strict;
use Config;

sub load_init
{
   local($/) = 1;
   open(INI, "init.emu") 
   or die "Content-type: text\/html\n\nFATAL: Unable to open init.emu: $! This file should be in the same directory as your CGI.\n";

   # grab the first valid entry
   <INI> =~ /page_root\s*=\s*(\S+)/m;
   close(INI);

   return "$1/lib";
}

# Load the init file, this will assign our page root and
# return the path to our libraries
use lib &load_init();
use lib &load_init().'/'.$Config{'archname'};

1;
