#!/usr/bin/perl

#Written by Berto
#Using parse_qstring by Frank Campagna
my $pic_folder="/usr/home/pi-ep/www/scrapbook";

        if(-d $pic_folder){
                opendir(PICS,$pic_folder);
                #print"<br>\n";
                foreach $semester (readdir(PICS)){
                        if( $semester =~ m/^(\d{2})(spring|summer|fall)$/ ){
                                print "DIR: $2 $1\n";
                                #print "<a href=\"picomatic.cgi?semester=$semester\">$2 '$1</a><br>\n";
                        }
                }
        }else{
                print "The toplevel dir: $pic_folder is wrong\n Please change this setting";
        }
