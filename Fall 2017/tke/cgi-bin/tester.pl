#!/usr/bin/perl
my $pic_folder="/usr/home/pi-ep/www/scrapbook";

        if(-d $pic_folder){
                opendir(PICS,$pic_folder);
                print"<br>\n";
		@folders=readdir(PICS);

                foreach $semester (reverse sort @folders){
                        if( $semester =~ m/^(\d{2})(spring|summer|fall)$/ ){
		print "SEMESTER: $semester\n";
#                                print "<a href=\"picomatic.cgi?semester=$semester\">$2 '$1</a><br>\n";
                        }
                }
        }else{
                print "The toplevel dir: $pic_folder is wrong\n Please change this setting";
        }

sub by_value { $ary{$a} cmp $ary{$b}; }
