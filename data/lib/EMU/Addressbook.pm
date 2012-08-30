#!/usr/bin/perl

package EMU::Addressbook;

#use strict;
#use vars qw(%addrbook_export_formats %addrbook_import_formats %ldap_fields);

require "EMU/AddressbookDefs.pl";

# Currently the constructor doesn't do anything, only blesses and returns
# the object. 
sub new {
    my $class = shift;
    my ($type) = @_;
    my $self = {};

    if ($type eq "import") {
	#The filter for translation from a format Outlook Express
	# to format Outlook 2000
	open (TMP, "+<$EMU::homedir/tmp/addressbook.in");
	seek TMP,0,0;
	my @file = <TMP>;
	
	if ($EMU::query->param('import_format') =~ /^Outlook/)
	{
						foreach (@file){
						if ($_=~ m/^(;|\w)/)
									{
									$wrp=","x48;
									$_=~s/^(;*)//g;
									$_=~s/^(.)/,$1/;
									$_=~s/;/,/g;
									$_=~s/([\w| |\.|\@]+)(,|,,)([\w|\@|\.]+)(,*)/\"$1\"$wrp\"0.0.00\",,,\"0.0.00\",,,,$3,$3/g;
									$_=~s/^(,\"F)(.*)$//;
									}
						}
						
						s/(,*)\s$/\n/g foreach (@file); 
		}
		

	
	seek TMP,0,0;
	
	print TMP @file;
	close(TMP);

        $self->{infile} = "$EMU::homedir/tmp/addressbook.in";
        $self->{type} = $EMU::query->param('import_type');
        $self->{format} = $EMU::query->param('import_format');
        if (!defined($AddressbookDefs::addrbook_import_formats{$self->{format}})) {
            &EMU::debug("Error! Unsupported addressbook format $self->{format}");
            return undef;
        }
    }
    else {
        $self->{type} = "csv";
        $self->{format} = $EMU::query->param('export_format');
        if (!defined($AddressbookDefs::addrbook_export_formats{$self->{format}}) || !$AddressbookDefs::addrbook_export_formats{$self->{format}}{fields}) {
            &EMU::debug("Error! Unsupported addressbook format or missing fields specification for $self->{format}");
            return undef;
        }
    }

    bless $self, $class;
}


sub import_ldif {
    my $self = shift;

    &EMU::load_module("Net::LDAP::LDIF");

#    my $ldif = Net::LDAP::LDIF->new($self->{infile}, "r", onerror=>'undef');
    my $ldif = Net::LDAP::LDIF->new($self->{infile}, "r");

    if (!$ldif) {
        &EMU::debug("Error creating LDIF object! $self->{infile}");
        return undef;
    }

    my %data;

#    while (not $ldif->eof()) {
    while (my $entry = $ldif->read_entry()) {

        if ($ldif->error()) {
            &EMU::debug("Error msg: ",$ldif->error(),"\n");
            &EMU::debug("Error lines:\n",$ldif->error_lines(),"\n");
        }
        else {
            foreach my $e ($entry->attributes) {
                my $val = $entry->get_value($e);
                chomp($val);

                if ($e =~ /^$ldap_fields{full}$/) {
                    $data{full} = $val;
&EMU::debug("setting full to $data{full}");
                }
                elsif ($e =~ /^$ldap_fields{email}$/) {
                    $data{email} = $val;
&EMU::debug("setting email to $data{email}");
                }
                elsif ($e =~ /^$ldap_fields{nick}$/) {
                    $data{nick} = $val;
&EMU::debug("setting nick to $data{nick}");
                }

                # Now let's process user-definable addressbook fields, if any
                # AddressbookDefs.pl MUST be modified to contain more data
                # points if there are custom fields. The default number of
                # data points we process is only 3.
                if ($EMU::licensed{"custom_addrbook"} && scalar(keys %ldap_fields) > 3) {
                    # go through the added keys...
                    foreach my $k (sort grep { /^addrbook_/ } keys %AddressbookDefs::ldap_fields) {
                        if ($e =~ /^$ldap_fields{$k}$/) {
                            $data{$k} = $val;
&EMU::debug("setting $k to $data{$k}");
                        }
                    }
                }
            }

            $data{nick} = $data{full} if (!$data{nick});
        }

        $self->insert_entry(\%data);
    }

    $ldif->done();

}


sub export_csv {
    my $self = shift;
    my ($f) = @_;

    my %f = %$f;

    my $filename = $f{filename} || 'emumail_addressbook.csv'.
    
    print "Content-type: text/CSV\n";
    print "Content-disposition: attachment; filename=\"$filename\"\n\n";

    my @addresses = sort grep {/^addresses\./} keys %EMU::userdb;

    # special headers
    print "$AddressbookDefs::export_headers{$self->{format}}\n" 
        if (defined $AddressbookDefs::export_headers{$self->{format}});

    foreach my $a (@addresses) {
        my @data = split(':', $EMU::userdb{$a});
        $a =~ s/^addresses\.//;

        # Yahoo doesn't like nicks with spaces
        $a =~ s/ //g if ($self->{format} eq "Yahoo");

        my @output;
        my ($first, $middle, $last) = split(' ', $data[1], 3);

        for (my $field=0; $field < $f{fields}; $field++) {
            if (!defined $f{$field}) {
                push(@output, '""');
            }
            else {
                if ($f{$field} eq "nick") {
                    push(@output, "\"$a\"");
                }
                elsif ($f{$field} =~ /^first/) {
                    push(@output, "\"$first\"");
                }
                elsif ($f{$field} =~ /^middle/) {
                    if ($last) {
                        push(@output, "\"$middle\"");
                    }
                    else {
                        push(@output, '""');
                    }
                }
                elsif ($f{$field} =~ /^last/) {
                    if ($last) {
                        push(@output, "\"$last\"");
                    }
                    else {
                        push(@output, "\"$middle\"");
                    }
                }
                elsif ($f{$field} =~ /^\d+$/) {
                    push(@output, "\"$data[$f{$field}]\"");
                }
                else {
                    push(@output, '""');
                }
            }
        }

        print join(',', @output)."\n";
    }
}


sub import_csv {
    my $self = shift;
    my ($f) = @_;

    my %f = %$f;

    if (!open(IN, "<$self->{infile}")) {
        &EMU::debug("unable to open addressbook import file $self->{infile}!");
        return undef;
    }

    &EMU::load_module("Text::CSV");

    my $csv = Text::CSV->new();

    my %data;

    my $total_fields = 0;
    my $lines = 0;
    my $line;
    while ($line .= <IN>) {

	# if we have -1 return status that means an end-of-line was 
	# detected within double quotes... 
	# keep joining lines while we still get that error
	if ($csv->parse($line) == -1) {
		$line =~ s/\n$|\r\n$/ /;
		next;
	}

	# different error... discard line
        if (!$csv->parse($line)) {
		$line = "";
		next;
	}

        # Both Yahoo and Outlook first output a line with the column names.
        # This can be used to determine the total fields expected in each line.
        #
        if ( ($self->{format} =~ /Outlook/i || $self->{format} =~ /Yahoo/i) &&
                $total_fields == 0 ) {
            $total_fields = scalar($csv->fields);
	    $line = "";
            next;
        }

        my @data = $csv->fields;

        # Note... handling Outlook requires a stupid hack! It doesn't always
        # output the exact same number of fields, so we can't depend on that
        # number in order to know our starting point! So for now I'll use
        # a "range" to calculate the starting point.
        if (!$total_fields || scalar(@data) > $total_fields-10) {

            %data = $self->process_array(\%f, \@data);
            $self->insert_entry(\%data);
        }

	# default, clear line
	$line = "";
    }
}


sub import_text {
    my $self = shift;
    my ($f) = @_;

    my %f = %$f;
    if (!open(IN, $self->{infile})) {
        &EMU::debug("unable to open addressbook import file $self->{infile}!");
        return undef;
    }

    my $data_ok = ($self->{format} =~ /Outlook/i) ? 0 : 1;
    my %data;

    # only allowing comma or tab-delimited
    my $type = $self->{type} eq "comma" ? ',':'\t';

    while (my $line = <IN>) {
        my @data = split($type, $line);
        next if (!@data);

        # Outlook exports in a non-standard way (surprise!). Even in csv,
        # it outputs some additional lines of text, so we must advance
        # into the file in order to find the first "real" line of data
        # Right now our best guess is to look for a line that contains
        # "For more information about working with contacts"
        next if (!$data_ok && $self->{format} =~ /Outlook/i && $line !~ /^For more informationabout working with contacts/);
        if (!$data_ok && $self->{format} =~ /Outlook/i && $line =~ /^For more informationabout working with contacts/) {
            $data_ok = 1;
            next;
        }

        if ($data_ok) {
            %data = $self->process_array(\%f, \@data);
        }
        $self->insert_entry(\%data);
    }
}


sub process_array {
    my $self = shift;
    my ($f, $data) = @_;

    my %f = %$f;
    my @data = @$data;

    my %data;

    if ($f{full} !~ /[a-zA-Z]/ && $f{full} !~ /,/) {
        $data{full} = $data[$f{full}];
    }
    elsif ($f{full} =~ /,/) {
        my @parts = split(',', $f{full});
        $data{full} = join(' ', map($data[$_], @parts));
    }

    $data{email} = $data[$f{email}];

    if (defined $f{nick}) {
        $data{nick} = $data[$f{nick}];
    }

    $data{nick} = $data{full} if (!$data{nick});

    # Now let's process user-definable addressbook fields, if any
    # AddressbookDefs.pl MUST be modified to contain more data
    # points if there are custom fields. The default number of
    # data points we process is only 3.
    if ($EMU::licensed{"custom_addrbook"} && scalar(keys %f) > 3) {
        # go through the added keys...
        foreach my $k (sort keys %AddressbookDefs::addrbook_fields) {
            next if (!defined $f{$k});
            $data{$k} = $data[$f{$k}];
            &EMU::debug("custom field $k = $data{$k}");
        }
    }

    return %data;
}


sub import {
    my $self = shift;

    my %f;

    # Grab the format definitions from the Defs file. 
    if (defined($AddressbookDefs::addrbook_import_formats{$self->{format}})) {
        # Take the static format from the AddressbookDefs.pl file
        %f = %{$AddressbookDefs::addrbook_import_formats{$self->{format}}};
    }
    else {
        &EMU::debug("Error in processing format $self->{format}");
        return;
    }

    if ($self->{type} eq "ldif") {
        $self->import_ldif();
    }
    else {
        $self->import_text(\%f) if ($self->{type} ne "csv");
        $self->import_csv(\%f) if ($self->{type} eq "csv");
    }

}


sub export {
    my $self = shift;

    my %f;

    # Grab the format definitions from the Defs file. 
    if (defined($AddressbookDefs::addrbook_export_formats{$self->{format}})) {
        # Take the static format from the AddressbookDefs.pl file
        %f = %{$AddressbookDefs::addrbook_export_formats{$self->{format}}};
    }
    else {
        &EMU::debug("Error in processing format $self->{format}");
        return;
    }

    # Currently we're only handling export to CSV
    if ($self->{type} eq "csv") {
        $self->export_csv(\%f);
    }
}


sub insert_entry {
    my $self = shift;
    my ($data) = @_;

    my %data = %$data;

    $data{email} =~ s/://g;
    $data{full} =~ s/://g;
    $data{nick} =~ s/://g;

    $data{nick} = $data{email} if (!$data{nick});
    my @val = ($data{email},$data{full});

    # Now let's process user-definable addressbook fields, if any
    # AddressbookDefs.pl MUST be modified to contain more data
    # points if there are custom fields. The default number of
    # data points we process is only 3.
    if ($EMU::licensed{"custom_addrbook"} && scalar(keys %data) > 3) {
        # go through the added keys...
        foreach my $k (sort keys %AddressbookDefs::addrbook_fields) {
            if (!defined $data{$k}) {
                push(@val, "");
            }
            else {
                my $entry = $data{$k};
                $entry =~ s/://g;
                push(@val, $entry);
            }
        }
    }

    # only add if the particular nick doesnt already exist
    $EMU::userdb{"addresses.$data{nick}"} = join(':', @val)
        if ($data{nick} && !defined($EMU::userdb{"addresses.$data{nick}"}));
}

