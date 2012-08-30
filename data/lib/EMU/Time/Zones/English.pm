##############################################################################
##                                                                          ##
##  >> Timezone Names for Time::Zones <<                                    ##
##  Copyright (c) 2001 Diederik van der Boor - All Rights Reserved          ##
##                                                                          ##
##############################################################################
#
# Revision = q$Id: English.pm,v 1.7 2003/11/14 13:18:52 ruslan Exp $;
# Date = q$Date: 2003/11/14 13:18:52 $;

package EMU::Time::Zones::English;
use strict;
use vars qw/$VERSION %Names/;

$VERSION = 1.00;


##############################################################################
## Timezone names

%Names = (
'GDST'  => [24, 'Greenwich Mean Time: Dublin, Edinburgh, Lisbon, London', '', 'GMT', '+0100', 'GMT+0100'], 
'GMT'   => [25, 'Casablanca, Monrovia', '', 'GMT'], 
'WEUR'  => [26, 'Amsterdam, Berlin, Bern, Rome, Stockholm, Vienna', '+0100', 'GMT+0100', '+0200', 'GMT+0200'], 
'CEUR1' => [27, 'Belgrade, Bratislava, Budapest, Ljubljana, Prague', '+0100', 'GMT+0100', '+0200', 'GMT+0200'],
'ROM'   => [28, 'Brussels, Copenhagen, Madrid, Paris', '+0100', 'GMT+0100', '+0200', 'GMT+0200'],
'CEUR2' => [29, 'Sarajevo, Skopje, Sofija, Vilnius, Warsaw, Zagreb', '+0100', 'GMT+0100', '+0200', 'GMT+0200'],
'WCAFR' => [30, 'West Central Africa', '+0100', 'GMT+0100'],
'GTB'   => [31, 'Athens, Istanbul, Minsk, Kiev', '+0200', 'GMT+0200', '+0300', 'GMT+0300'],
'EEUR'  => [32, 'Bucharest', '+0200', 'GMT+0200', '+0300', 'GMT+0300'],
'EGYPT' => [33, 'Cairo', '+0200', 'GMT+0200', '+0300', 'GMT+0300'],
'SAFR'  => [34, 'Harare, Pretoria', '+0200', 'GMT+0200'],
'FLE'   => [35, 'Helsinki, Riga, Tallinn', '+0200', 'GMT+0200', '+0300', 'GMT+0300'],
'JERUS' => [36, 'Jerusalem', '+0200', 'GMT+0200'],
'ARAB1' => [37, 'Baghdad', '+0300', 'GMT+0300', '+0400', 'GMT+0400'],
'ARAB2' => [38, 'Kuwait, Riyadh', '+0300', 'GMT+0300'],
'RUSS'  => [39, 'Moscow, St. Petersburg, Volgograd', '+0300', 'GMT+0300', '+0400', 'GMT+0400'],
'EAFR'  => [40, 'Nairobi', '+0300', 'GMT+0300'],
'IRAN'  => [41, 'Tehran', '+0330', 'GMT+0330', '+0430', 'GMT+0430'],
'ARAB3' => [42, 'Abu Dhabi, Muscat', '+0400', 'GMT+0400'],
'CAUCA' => [43, 'Baku, Tbilisi, Yerevan', '+0400', 'GMT+0400'],
'AFGH'  => [44, 'Kabul', 'GMT+0430', 'GMT+0430'],
'EKAT'  => [45, 'Ekaterinburg', '+0500', 'GMT+0500', '+0600', 'GMT+0600'],
'WASIA' => [46, 'Islamabad, Karachi, Tashkent', '+0500', 'PKT'],
'INDIA' => [47, 'Calcutta, Chennai, Mumbai, New Delhi', '+0530', 'GMT+0530'],
'NEPAL' => [48, 'Kathmandu', '+0545', 'GMT+0545'],
'NCAS'  => [49, 'Almaty, Novosibirsk', '+0600', 'GMT+0600', '+0700', 'GMT+0700'],
'CASIA' => [50, 'Astana, Dhaka', '+0600', 'GMT+0600'],
'SRI'   => [51, 'Sri Jayawardenepura', '+0600', 'GMT+0600'],
'MYAN'  => [52, 'Rangoon', '+0630', 'GMT+0630'],
'SEAS'  => [53, 'Bangkok, Hanoi, Jakarta', '+0700', 'GMT+0700'],
'NASIA' => [54, 'Krasnoyarsk', '+0700', 'GMT+0700', '+0800', 'GMT+0800'],
'CHINA' => [55, 'Beijing, Chongqing, Hong Kong, Urumqi', '+0800', 'GMT+0800'],
'NEAS'  => [56, 'Irkutsk, Ulaan Bataar', '+0800', 'GMT+0800', '+0900', 'GMT+0900'],
'MALAY' => [57, 'Kuala Lumpur, Singapore', '+0800', 'GMT+0800'],
'WAUS'  => [59, 'Perth', '+0800', 'GMT+0800'],
'TAIPE' => [60, 'Taipei', '+0800', 'GMT+0800'],
'JAPAN' => [61, 'Osaka, Sapporo, Tokyo', '+0900', 'GMT+0900'],
'KOREA' => [62, 'Seoul', '+0900', 'GMT+0900'],
'YAKUT' => [63, 'Yakutsk', '+0900', 'GMT+0900', '+1000', 'GMT+1000'],
'CAUS'  => [64, 'Adelaide', '+0930', 'GMT+0930', '+1030', 'GMT+1030'],
'AUSC'  => [65, 'Darwin', '+0930', 'GMT+0930'],
'EAUS'  => [66, 'Brisbane', '+1000', 'GMT+1000'],
'AUSE'  => [67, 'Canberra, Melbourne, Sydney', '+1000', 'EAST', '+1100', 'EADT'],
'WPAS'  => [68, 'Guam, Port Moresby', '+1000', 'GMT+1000'],
'TASM'  => [69, 'Hobart', '+1000', 'GMT+1000', '+1100', 'GMT+1100'],
'VLAD'  => [70, 'Vladivostok', '+1000', 'GMT+1000', '+1100', 'GMT+1100'],
'CPAS'  => [71, 'Magadan, Solomon Is., New Caledonia', '+1100', 'GMT+1100'],
'NZEA'  => [72, 'Auckland, Wellington', '+1200', 'NZST', '+1300', 'NZDT'],
'FIJI'  => [73, 'Fiji, Kamchatka, Marshall Is.', '+1200', 'GMT+1200'],
'TONGA' => [74, 'Nuku\'alofa', '+1300', 'GMT+1300'],
'AZORE' => [23, 'Azores', '-0100', 'GMT-0100', '+0000', 'GMT+0000'],
'CAPE'  => [22, 'Cape Verde Is.', '-0100', 'GMT-0100'],
'MATL'  => [21, 'Mid-Atlantic', '-0200', 'GMT-0200', '-0100', 'GMT-0100'],
'ESAM'  => [20, 'Brasilia', '-0300', 'GMT-0300', '-0200', 'GMT-0200'],
'SAME'  => [19, 'Buenos Aires, Georgetown', '-0300', 'GMT-0300'],
'GREEN' => [18, 'Greenland', '-0300', 'GMT-0300', '-0200', 'GMT-0200'],
'NEWF'  => [17, 'Newfoundland', '-0330', 'GMT-0330', '-0230', 'GMT-0230'],
'ALTL'  => [16, 'Atlantic Time (Canada)', '-0400', 'AST', '-0300', 'ADT'],
'SAMW'  => [15, 'Caracas, La Paz', '-0400', 'GMT-0400'],
'PASSA' => [14, 'Santiago', '-0400', 'GMT-0400', '-0300', 'GMT-0300'],
'SAPAS' => [13, 'Bogota, Lima, Quito', '-0500', 'GMT-0500'],
'EAST'  => [12, 'Eastern Time (US & Canada)', '-0500', 'EST', '-0400', 'EDT'],
'USEAS' => [11, 'Indiana (East)', '-0500', 'EST'],
'CAM'   => [10, 'Central America', '-0600', 'CST'],
'CENTR' => [9, 'Central Time (US & Canada)', '-0600', 'CST', '-0500', 'CDT'],
'MEX'   => [8, 'Mexico City', '-0600', 'GMT-0600', '-0500', 'GMT-0500'],
'CANC'  => [7, 'Saskatchewan', '-0600', 'GMT-0600'],
'USMOU' => [6, 'Arizona', '-0700', 'MST'],
'MOUNT' => [5, 'Mountain Time (US & Canada)', '-0700', 'MST', '-0600', 'MDT'],
'PAS'   => [4, 'Pacific Time (US & Canada); Tijuana', '-0800', 'PST', '-0700', 'PDT'],
'ALASK' => [3, 'Alaska', '-0900', 'GMT-0900', '-0800', 'GMT-0800'],
'HAWAI' => [2, 'Hawaii', '-1000', 'GMT-1000'],
'SAMOA' => [1, 'Midway Island, Samoa', '-1100', 'GMT-1100'],
'DATE'  => [0, 'Eniwetok, Kwajalein', '-1200', 'GMT-1200'],
);

1;

__DATA__

=head1 SYNOPSIS

  For internal use only; this package should by loaded as
  use Time::Zones qw(LanguageName);

=cut