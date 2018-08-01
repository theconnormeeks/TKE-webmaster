#!/usr/bin/perl

#Written by Berto
#Using parse_qstring by Frank Campagna

my $pic_folder="/usr/home/pi-ep/www/scrapbook";
my $root_url="http://www.pi-ep.org";

my $event_folder="";

print "Content-type: text/html\n\n";
print "<html>\n";
print "<body>\n";
print "<link rel=\"stylesheet\" href=\"$root_url/global.css\" type=\"text/css\">\n";
print "<center>\n";
print "<div id=\"content\">\n";
print "<h2 id=\"pageName\">\n";
&parse_qstring;



if ($Form{'semester'} eq ''){
	print "Pi-Ep Scrapbooks</br>\n";
	&toplevel;
	print "</h2>\n";
}elsif (($Form{'semester'} ne '') && ($Form{'event'} eq '')){   
	$mysemester=$Form{'semester'};
	($year)=substr($mysemester,0,2);
	($season)=substr($mysemester,2,10);

	print "$season '$year\n</br>";
	$event_folder="$pic_folder/$mysemester";
	&eventlevel( $mysemester);
	print "</h2>\n";
}else{
	$mysemester=$Form{'semester'};
	($year)=substr($mysemester,0,2);
	($season)=substr($mysemester,2,10);

	$myevent=$Form{'event'};
	print "$season '$year: $myevent<br>\n";
	print "</h2>\n";
	&thumbs($mysemester,$myevent);
}
print "</center>\n";
print "</div>\n";
print "</body>\n";
print "</html>\n";

sub toplevel{
	if(-d $pic_folder){
		opendir(PICS,$pic_folder);
		print"<br>\n";
		foreach $semester (readdir(PICS)){
			if( $semester =~ m/^(\d{2})(spring|summer|fall)$/ ){
				print "<a href=\"picomatic.cgi?semester=$semester\">$2 '$1</a><br>\n";
			}
		}
	}else{
		print "The toplevel dir: $pic_folder is wrong\n Please change this setting";
	}
}

sub eventlevel{
	$mysemester = $_[0];
	if(-d $event_folder){
		opendir(EVENTS,$event_folder);
		print"<br>\n";
		foreach $event (readdir(EVENTS)){
			if( $event =~ m/(\w)$/ ){
				print "<a href=\"picomatic.cgi?semester=$mysemester&event=$event\">$event</a><br>\n";
			}
		}
	}else{
		print "The event dir: $pic_folder is wrong\n It may not exist";
	}
}

sub thumbs{
	$mysemester = $_[0];
	$myevent = $_[1];
	$thumb_folder="$pic_folder/$mysemester/$myevent";
	$count=0;
	if(-d $thumb_folder){
		print"<table border=0>\n";
		print"<tr>\n";
		opendir(THUMBS,$thumb_folder);
		foreach $pic (readdir(THUMBS)){
			if( $pic =~ m/(\w)$/ ){
				if($count > 5){
					print "</tr>\n";
					print "<tr>\n";
					$count=0;
				}
			print "<td>\n";	
			print "<a href=\"$root_url\/scrapbook\/$mysemester\/$myevent\/$pic\">";
			print "<img src=\"$root_url\/scrapbook\/$mysemester\/$myevent\/$pic\" height=75 width=75>";
			print "</a>\n";
			print "</td>\n";
			$count++;
			}
		}
		print "</tr>\n";
		print "</table>\n";
	}else{
		print "This folder: $thumb_folder is wrong\n It may not exist";
	}
}



sub parse_qstring {
  if ($ENV{'REQUEST_METHOD'} eq 'GET') {
    @pairs = split(/&/, $ENV{'QUERY_STRING'});
  }
  elsif ($ENV{'REQUEST_METHOD'} eq 'POST') {
    read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
    @pairs = split(/&/, $buffer);
  }

  foreach $pair (@pairs)
  {
        # Split the pair up into individual variables.                       #
        local($name, $value) = split(/=/, $pair);
 
        # Decode the form encoding on the name and value variables.          #
        $name =~ tr/+/ /;
        $name =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;

        $value =~ tr/+/ /;
        $value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;

        # If they try to include server side includes, erase them, so they
        # aren't a security risk if the html gets returned.  Another 
        # security hole plugged up.
        $value =~ s/<!--(.|\n)*-->//g;

        # If the field name has been specified in the %Config array, it will #
        # return a 1 for defined($Config{$name}}) and we should associate    #
        # this value with the appropriate configuration variable.  If this   #
        # is not a configuration form field, put it into the associative     #
        # array %Form, appending the value with a ', ' if there is already a #
        # value present.  We also save the order of the form fields in the   #
        # @Field_Order array so we can use this order for the generic sort.  #
        if (defined($Config{$name})) {
            $Config{$name} = $value;
        }
        else {
            if ($Form{$name} && $value) {
                $Form{$name} = "$Form{$name}, $value";
            }
            elsif ($value) {
                push(@Field_Order,$name);
                $Form{$name} = $value;
            }
        }
  }
}
