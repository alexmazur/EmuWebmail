package EMU::Theme;

use strict;

sub new
{
   my $class = shift;
   my $self ={};
   
   bless($self, $class);
   
   return $self;
}

sub get
{
   my $self = shift;
   my ($key) = @_;
   
   return $EMU::c{$key};
}

1;

   
