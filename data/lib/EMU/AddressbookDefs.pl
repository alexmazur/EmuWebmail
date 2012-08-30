
#use vars qw(%addrbook_fields %addrbook_import_formats %addrbook_export_formats
#	%ldap_fields);

package AddressbookDefs;


# Configurable system-wide options for Addressbook

# Customized Addressbook fields
# Here's the default list addrbook fields. They are ordered and the order is
# IMPORTANT! They can be customized and fields can be added if necessary.
# However, the entire addressbook system is dependent on these definitions
# including the contact_editor.html template.
#
# ANY CHANGES TO THESE FIELDS MUST BE MAPPED ACCORDINGLY TO THE HASHES
# BELOW AND ALSO ON THE contact_editor.html TEMPLATE.
#
# ALSO BE AWARE THAT IF YOU HAVE PRE-EXISTING ADDRESSBOOK ENTRIES IN A 
# DIFFERENT FORMAT AND YOU CHANGE THE FORMAT, ALL DATA WILL BE OUT OF ORDER.
#
%addrbook_fields = (
addrbook_01 => "Company Name",
addrbook_02 => "Home Phone",
addrbook_03 => "Website",
addrbook_04 => "Email Address 2",
addrbook_05 => "Email Address 3",
addrbook_06 => "Business Phone",
addrbook_07 => "Cell Phone",
addrbook_08 => "Fax",
addrbook_09 => "Job Title",
addrbook_10 => "Company Street 1",
addrbook_11 => "Company Street 2",
addrbook_12 => "Company City",
addrbook_13 => "Company State / Province",
addrbook_14 => "Company Post Code",
addrbook_15 => "Company Country",
addrbook_16 => "Home Street 1",
addrbook_17 => "Home Street 2",
addrbook_18 => "Home City",
addrbook_19 => "Home State / Province",
addrbook_20 => "Home Postal Code",
addrbook_21 => "Home Country",
addrbook_22 => "Notes"
);


# Given a delimited file, determine the column positions (0-based) for
# each of the pertinent addressbook fields. Some exported formats don't
# have a "full name" or "complete name" field, so the full name is created
# from First,Middle,Last... If there is no "nickname" field, then the
# full name is used for nickname

# Map application's output format to internal addressbook
%addrbook_import_formats = (
    "Netscape"	=> { "nick"	=> 16,
                     "full"	=> 0,
                     "email"	=> 6,
                     "addrbook_01"	=> 15,
                     "addrbook_02"	=> 14,
                     "addrbook_06"	=> 12,
                     "addrbook_07"	=> 17,
                     "addrbook_08"	=> 13,
                     "addrbook_09"	=> 7,
                     "addrbook_16"	=> 9,
                     "addrbook_18"	=> 4,
                     "addrbook_19"	=> 5,
                     "addrbook_20"	=> 10,
                     "addrbook_21"	=> 11,
                     "addrbook_22"	=> 3},

    "Yahoo"	=> { "nick"	=> 3,
                     "full"	=> "0,1,2",
                     "email"	=> 4,
                     "addrbook_01"	=> 21,
                     "addrbook_02"	=> 8,
                     "addrbook_03"	=> 18,
                     "addrbook_04"	=> 16,
                     "addrbook_05"	=> 17,
                     "addrbook_06"	=> 9,
                     "addrbook_07"	=> 12,
                     "addrbook_08"	=> 11,
                     "addrbook_09"	=> 20,
                     "addrbook_10"	=> 22,
                     "addrbook_12"	=> 23,
                     "addrbook_13"	=> 24,
                     "addrbook_14"	=> 25,
                     "addrbook_15"	=> 26,
                     "addrbook_16"	=> 27,
                     "addrbook_18"	=> 28,
                     "addrbook_19"	=> 29,
                     "addrbook_20"	=> 30,
                     "addrbook_21"	=> 31,
                     "addrbook_22"	=> 38},

    "Outlook9798"	=> { "nick"	=> "full",
                     "full"	=> "1,2,3",
                     "email"	=> 55,
                     "addrbook_01"	=> 5,
                     "addrbook_02"	=> 37,
                     "addrbook_03"	=> 81,
                     "addrbook_04"	=> 57,
                     "addrbook_05"	=> 59,
                     "addrbook_06"	=> 31,
                     "addrbook_07"	=> 40,
                     "addrbook_08"	=> 30,
                     "addrbook_09"	=> 7,
                     "addrbook_10"	=> 8,
                     "addrbook_11"	=> 9,
                     "addrbook_12"	=> 11,
                     "addrbook_13"	=> 12,
                     "addrbook_14"	=> 13,
                     "addrbook_15"	=> 14,
                     "addrbook_16"	=> 15,
                     "addrbook_17"	=> 16,
                     "addrbook_18"	=> 18,
                     "addrbook_19"	=> 19,
                     "addrbook_20"	=> 20,
                     "addrbook_21"	=> 21,
                     "addrbook_22"	=> 69},

    "Outlook2000"	=> { "nick"	=> "full",
                     "full"	=> "1,2,3",
                     "email"	=> 56,
                     "addrbook_01"	=> 5,
                     "addrbook_02"	=> 37,
                     "addrbook_03"	=> 89,
                     "addrbook_04"	=> 59,
                     "addrbook_05"	=> 62,
                     "addrbook_06"	=> 31,
                     "addrbook_07"	=> 40,
                     "addrbook_08"	=> 30,
                     "addrbook_09"	=> 7,
                     "addrbook_10"	=> 8,
                     "addrbook_11"	=> 9,
                     "addrbook_12"	=> 11,
                     "addrbook_13"	=> 12,
                     "addrbook_14"	=> 13,
                     "addrbook_15"	=> 14,
                     "addrbook_16"	=> 15,
                     "addrbook_17"	=> 16,
                     "addrbook_18"	=> 18,
                     "addrbook_19"	=> 19,
                     "addrbook_20"	=> 20,
                     "addrbook_21"	=> 21,
                     "addrbook_22"	=> 77},

	 "Outlook2002"	=> { "nick"	=> "full",
                     "full"	=> "1,2,3",
                     "email"	=> 57,
                     "addrbook_01"	=> 5,
                     "addrbook_02"	=> 37,
                     "addrbook_03"	=> 89,
                     "addrbook_04"	=> 59,
                     "addrbook_05"	=> 62,
                     "addrbook_06"	=> 31,
                     "addrbook_07"	=> 40,
                     "addrbook_08"	=> 30,
                     "addrbook_09"	=> 7,
                     "addrbook_10"	=> 8,
                     "addrbook_11"	=> 9,
                     "addrbook_12"	=> 11,
                     "addrbook_13"	=> 12,
                     "addrbook_14"	=> 13,
                     "addrbook_15"	=> 14,
                     "addrbook_16"	=> 15,
                     "addrbook_17"	=> 16,
                     "addrbook_18"	=> 18,
                     "addrbook_19"	=> 19,
                     "addrbook_20"	=> 20,
                     "addrbook_21"	=> 21,
                     "addrbook_22"	=> 77}
);


# Map emumail's internal addressbook to application's format
%addrbook_export_formats = (
    "Netscape"	=> {  filename => 'emumail_addressbook.csv',
                     fields	=> 20,
                     16	=> "nick",
                     0	=> 1,
                     2	=> "first",
                     1	=> "last",
                     6	=> 0,
                     15	=> 2,
                     14	=> 3,
                     12 => 7,
                     17	=> 8,
                     13	=> 9,
                     7	=> 10,
                     9	=> 17,
                     4	=> 19,
                     5	=> 20,
                     10	=> 21,
                     11	=> 22,
                     3	=> 23},

    "Yahoo" => {     filename => 'emumail_addressbook.csv',
                     fields	=> 39,
                     3	=> "nick",
                     0	=> "first",
                     1	=> "middle",
                     2	=> "last",
                     4	=> 0,
                     21	=> 2,
                     8	=> 3,
                     18	=> 4,
                     16	=> 5,
                     17	=> 6,
                     9	=> 7,
                     12	=> 8,
                     11	=> 9,
                     20	=> 10,
                     22	=> 11,
                     23	=> 13,
                     24	=> 14,
                     25	=> 15,
                     26	=> 16,
                     27	=> 17,
                     28	=> 19,
                     29	=> 20,
                     30	=> 21,
                     31	=> 22,
                     38	=> 23},

    "Outlook9798"	=> { 
                     filename => 'emumail_addressbook.csv',
                     fields => 82,
                     1	=> "first",
                     2	=> "middle",
                     3	=> "last",
                     55	=> 0,
                     5	=> 2,
                     37	=> 3,
                     81	=> 4,
                     57	=> 5,
                     59	=> 6,
                     31	=> 7,
                     40	=> 8,
                     30	=> 9,
                     7	=> 10,
                     8	=> 11,
                     9	=> 12,
                     11	=> 13,
                     12	=> 14,
                     13	=> 15,
                     14	=> 16,
                     15	=> 17,
                     16	=> 18,
                     18	=> 19,
                     19	=> 20,
                     20	=> 21,
                     21	=> 22,
                     69	=> 23},

    "Outlook2000"	=> {
                     filename => 'emumail_addressbook.csv',
                     fields => 90,
                     1	=> "first",
                     2	=> "middle",
                     3	=> "last",
                     56	=> 0,
                     5	=> 2,
                     37	=> 3,
                     89	=> 4,
                     59	=> 5,
                     62	=> 6,
                     31	=> 7,
                     40	=> 8,
                     30	=> 9,
                     7	=> 10,
                     8	=> 11,
                     9	=> 12,
                     11	=> 13,
                     12	=> 14,
                     13	=> 15,
                     14	=> 16,
                     15	=> 17,
                     16	=> 18,
                     18	=> 19,
                     19	=> 20,
                     20	=> 21,
                     21	=> 22,
                     77	=> 23}

);


# These are ldap field mappings (for .ldif input files)
%ldap_fields = (
    "nick"	=> ".*nick.*",
    "full"	=> "cn",
    "email"	=> "mail",
    "addrbook_1"	=> "o",
    "addrbook_2"	=> "homephone"
);


# Header line for Yahoo file. This seems to be required in order for Yahoo to
# correctly import data. This header line represents the format/order in which
# fields are output
%export_headers = (
    "Yahoo" => qq{"First","Middle","Last","Nickname","Email","Category","Distribution Lists","Yahoo! ID","Home","Work","Pager","Fax","Mobile","Other","Yahoo! Phone","Primary","Alternate Email 1","Alternate Email 2","Personal Website","Business Website","Title","Company","Work Address","Work City","Work State","Work ZIP","Work Country","Home Address","Home City","Home State","Home ZIP","Home Country","Birthday","Anniversary","Custom 1","Custom 2","Custom 3","Custom 4","Comments"},

    "Outlook9798" => qq{"Title","First Name","Middle Name","Last Name","Suffix","Company","Department","Job Title","Business Street","Business Street 2","Business Street 3","Business City","Business State","Business Postal Code","Business Country","Home Street","Home Street 2","Home Street 3","Home City","Home State","Home Postal Code","Home Country","Other Street","Other Street 2","Other Street 3","Other City","Other State","Other Postal Code","Other Country","Assistant's Phone","Business Fax","Business Phone","Business Phone 2","Callback","Car Phone","Company Main Phone","Home Fax","Home Phone","Home Phone 2","ISDN","Mobile Phone","Other Fax","Other Phone","Pager","Primary Phone","Radio Phone","TTY/TDD Phone","Telex","Account","Anniversary","Assistant's Name","Billing Information","Birthday","Categories","Children","E-mail Address","E-mail Display Name","E-mail 2 Address","E-mail 2 Display Name","E-mail 3 Address","E-mail 3 Display Name","Gender","Government ID Number","Hobby","Initials","Keywords","Language","Location","Mileage","Notes","Office Location","Organizational ID Number","PO Box","Private","Profession","Referred By","Spouse","User 1","User 2","User 3","User 4","Web Page"},

    "Outlook2000" => qq{"Title","First Name","Middle Name","Last Name","Suffix","Company","Department","Job Title","Business Street","Business Street 2","Business Street 3","Business City","Business State","Business Postal Code","Business Country","Home Street","Home Street 2","Home Street 3","Home City","Home State","Home Postal Code","Home Country","Other Street","Other Street 2","Other Street 3","Other City","Other State","Other Postal Code","Other Country","Assistant's Phone","Business Fax","Business Phone","Business Phone 2","Callback","Car Phone","Company Main Phone","Home Fax","Home Phone","Home Phone 2","ISDN","Mobile Phone","Other Fax","Other Phone","Pager","Primary Phone","Radio Phone","TTY/TDD Phone","Telex","Account","Anniversary","Assistant's Name","Billing Information","Birthday","Categories","Children","Directory Server","E-mail Address","E-mail Type","E-mail Display Name","E-mail 2 Address","E-mail 2 Type","E-mail 2 Display Name","E-mail 3 Address","E-mail 3 Type","E-mail 3 Display Name","Gender","Government ID Number","Hobby","Initials","Internet Free Busy","Keywords","Language","Location","Manager's Name","Mileage","Notes","Office Location","Organizational ID Number","PO Box","Priority","Private","Profession","Referred By","Sensitivity","Spouse","User 1","User 2","User 3","User 4","Web Page"}
);


