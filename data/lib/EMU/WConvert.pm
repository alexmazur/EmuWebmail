#!/usr/bin/perl
# word converting stuff

package EMU::WConvert;

require "EMU/laola.pl";
require "EMU/textutil.pl";

use vars qw($msg);

my ($msg);

sub convert
{
    local $infile = shift @_;
    
    laola_open_document($infile);
    return main_work();
}

sub main_work
{
   $warning = undef;
   $textout = undef;
   $footout = undef; 
   $word_textl = 0;
   $word_footl = 0;
   $word_destl = 0;
   local($wpps);

 is_opened: { 
       eval {
	   get_worddocument_pps($wpps);
	   get_document_text($wpps);
       };

       last if ($@);

       convert_text();
       
       #Actually this just slurps into scalar.
       	print_document();

#       return laola_close_document();
	 laola_close_document();
   }

#   return laola_close_document(), 0;
   laola_close_document(), 0;
   return $msg;
}

sub get_worddocument_pps
{
#
# Assume Word Document, if there is a stream "WordDocument".
#
   local(%dir) = laola_get_directory(0);

   if (defined $dir{"WordDocument"})
   {
       $_[0] = $dir{"WordDocument"};
       return "ok";
   }
   else
   {
       warn "Not a Word document!\n";
   }
}

sub get_document_text
{
#
# Read text section out of $inbuf and store this in global $textout
#
   local($pps)=shift;

   local($begin, $end, $len);
   local($header)="";
   local($status);
   local($tmp);
   local($word_status);
   local($word_fast, $word_protected); local($word_version_ok)=0;
   local($l, $lstr, $qstr);
   
   $status = &laola_get_file($pps, $header, 0, 0x300);
   return $status if $status ne "ok";

   # Document status
   $word_status  = &get_word(0x0a, $header);
   $word_fast    = $word_status & 2**2;
   $word_crypted = $word_status & 2**8;
   $tmp = &get_byte(5, $header);
   $word_version_ok=1 if ($tmp==0xc0) || ($tmp==0xe0);

   return "Document is password protected!" if $word_crypted;

   $begin=&get_long(0x18, $header);  # start of 1st text chunk
   $end=&get_long(0x1c, $header);    # end of 1st text chunk
   $len=$end-$begin;

   if ($word_version_ok) {
      $word_textl = &get_long(0x34, $header);
      $word_footl = &get_long(0x38, $header);
      $word_destl = &get_long(0x3c, $header);
      $status = &get_text();
   } else {
      $status = &get_text();
      $word_textl = &get_long(0x4c, $header); 
   }
   return $status if $status ne "ok";

   # Give a little warning, even if it's not very sensible.
   $l = $word_textl+$word_footl+$word_destl-length($textout);
   eval { substr($textout, $word_textl+$word_footl)=""; };

   if ($l) {
      $lstr = &abs($l)." byte" . (&abs($l)>1 && "s" || "");
#      $qstr = ($l>0) ? "missing" : "to much";
#      $warning = "!! Attention: $lstr of text $qstr !!\n";
   }

   "ok";
}

sub get_text {
   &laola_get_file($pps, $textout, $begin, $len);
}

sub convert_text {   
    local($num);

    eval {
	$footout = substr($textout, $word_textl, $word_footl);
	substr($textout, $word_textl) = "";
    };

    silly_convert();
    strip_control($textout);
    strip_control($footout);

    set_maxcolumn(78);
    set_breaking_mode(1);
    set_hypen_char("-");
    set_line_delimitra("\n");
    set_tab_delimitra("\t");

    # Line breaking
    format_lines($textout);
    format_lines($footout);
}

sub silly_convert
{
   # footnotes
   $num = 1; while ($textout =~ s/\x02/[$num]/) { $num++ }
   $num = 1; while ($footout =~ s/\x02/[$num]/) { $num++ }

   # fields
   $textout =~ s/\x13[^\x14]*\x14([^\x15]*)\x15/$1/g;
   $textout =~ s/\x13[^\x15]*\x15//g;
   $footout =~ s/\x13[^\x14]*\x14([^\x15]*)\x15/$1/g;
   $footout =~ s/\x13[^\x15]*\x15//g;
}

sub strip_control {
   # Here some characters could be converted like:
   $_[0] =~ s/[\x07-\x09]/\t/g;		
   $_[0] =~ s/[\xa0]/ /g;		
   $_[0] =~ s/[\x0b\x0c\x0e]/\x0d/g;		
   $_[0] =~ tr/\x1e\x84\x91\x92\x93\x94/-"`"""/;

   # Away with Words control characters 
   $_[0] =~ s/[\x00-\x06\x0f-\x1f\x80-\x9f]//g;

   $_[0] =~ s/\x0d/\n/g;
}

sub print_document
{
   binmode STDOUT;
   
   $msg .= "$warning\n" if ($warning);
   $msg .= "$textout$footout\n";
}

##
## Little helps
##

sub get_byte { unpack("C", substr($_[1], $_[0], 2)) }
sub get_word { unpack("v", substr($_[1], $_[0], 2)) }
sub get_long { unpack("V", substr($_[1], $_[0], 4)) }
sub abs { ($_[0] < 0) ? -$_[0] : $_[0] }

sub msg  { @_ && print (shift) || 1 }

sub msg2 {
    local($status) = shift;
    
    if ($status eq "ok") {
	return &msg(shift);
    } else {
	$msg .= "Error: $status\n" if $status;
	return 0;
    }
}

sub basename {
    (substr($_[0], rindex($_[0],'/')+1) =~ /(^[^.]*)/) && $1;
}


1;
