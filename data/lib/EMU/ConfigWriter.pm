package EMU::ConfigWriter;

use strict;

use File::Copy;

sub new
{
   my $class = shift;
   my ($file) = @_;
   
   my $self = {};
   
   bless($self, $class);
   
   $self->readFile( $file );
   
   return $self;
}

sub readFile
{
   my $self = shift;
   my ($file) = @_;
   
   # Clear out all our values (but remain defined)
   %$self = ();
   
   open(IN, $file) or return;
   
   while (<IN>) {
      # Ignore comments
      next if /^\s*#/;

      # Split to key and value, removing any buffering whitespace.
      # Also, ignoring any invalid lines
      my ($k, $v) = /^\s*(.+?)\s*=\s*(.*?)\s*$/ or next;
      
      # Read in multi-line values
      while ($v =~ s/\\$//) {
         # Append next line, and remove trailing whitespace
         ($v .= "\n".<IN>) =~ s/\s*$//;
      }

      $self->{$k} = $v;
   }
   
   close(IN);
}

sub writeFile
{
   my $self = shift;
   my ($file) = @_;
   
   # Our input file
   open(IN, $file);
   # Our temporary output file
   open(OUT, ">$file.tmp") or return;
   
   my %data = %$self;
   
   while (<IN>) {
      # Pass through comments and anything not a key/val pair
      if (/^\s*#/ || !/^\s*(.+?)\s*=\s*(.*?)\s*$/) {
         print OUT $_;
         next;
      } elsif (!exists $data{$1}) {
         # Ignore out any key/val pairs we have no knowledge of
         if (/\\$/) {
            # Slurp away
            1 while (<IN> =~ /\\$/);
         }
      } else {
         # Replace any key/val pairs we have values for
         my ($k, $v) = ($1, $data{$1});
         if (/\\$/) {
            # Slurp away
            1 while (<IN> =~ /\\$/);
         }
         
         # For multi-line entries
         $v =~ s/\n/\\\n/g;
         
         print OUT "$k = $v\n";

         # We've processed this key
         delete $data{$k};
      }
   }

   # Lastly, append any new key/vals
   foreach my $k (keys %data) {
      print OUT "$k = $data{$k}\n";
   }
   
   close(IN);
   close(OUT);
      
   copy("$file.tmp", $file) or return;
   unlink("$file.tmp");

   1;
}

1;
