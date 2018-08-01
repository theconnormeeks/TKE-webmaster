#!/usr/bin/perl

#This code was written by Frank Campagna.  Keep your criticisms to yourself!

#rem input layout:
#scroll number          length=3  fields 1-3
#frater name            length=28 fields 5-32
#bbro scroll num        length=3  fields 34-36
#active status flag     length=2  fields 38-39
#nickname               length=25 fields 41-65
#transfer's chapter     length=2  fields 67-68
#transfer's scroll num  length=3  fields 70-72
#demit flag             length=1  fields 74

#rem scroll array:
#$scroll_arry[$i][1] = scroll number
#$scroll_arry[$i][2] = frater name         
#$scroll_arry[$i][3] = bbro number         
#$scroll_arry[$i][4] = active status flag
#$scroll_arry[$i][5] = nickname
#$scroll_arry[$i][6] = bbro name
#$scroll_arry[$i][7] = bbro active flag
#$scroll_arry[$i][8] = transfer's chapter
#$scroll_arry[$i][9] = transfer's scroll num
#$scroll_arry[$i][10] = demit flag

#rem tree array:
#$tree_arry[$i][1] = frater name
#$tree_arry[$i][2] = level number
#$tree_arry[$i][3] = nickname
#$tree_arry[$i][4] = active flag
#$tree_arry[$i][5] = scroll number

#Set up environment variables and print header
#$title = "Pi Epsilon Scroll";
$ver = "11/18/00";
$scroll_file = "scroll_db.txt";
$script_name = "scroll.cgi";
$num_recs = 0;
$num_branches = 0;
$num_act_branches = 0;

#Parse the variables passed to report
&parse_qstring;

&print_hdr;

#Suck up the scroll and put it in memory
&make_scroll_array;

#If the nickname is blank, change it to "(none)"
&change_blank_nicks;

#Convert demit'd names to Xxx by default, but skip this if demit=show
if ($Form{'demit'} ne "show") {
  &hide_demit_names;
}

#Check to see if only a portion of scroll was requested, and decrease the
#num_rec counter to match the new scroll number
if ($Form{'thru'} ne "") {
  &shorten_array(int($Form{'thru'}));
}

#Add the bbro's name to array
&add_bbro_to_array;

#Main loop
#if ($ENV{'QUERY_STRING'} ne '') {

   #check what kind of report we want to output
   if ($Form{'bbro'} ne '') {

      #Show Lineage for a given scroll number
      #This segment finds your big bro, his big bro, etc...
      $scroll_num = $Form{'bbro'};
      print "<center><b><font color=ff0000 size=+1>",$title," - Big Brother Lineage</font></b></center><br>\n";
      print "<!-- bbro=", $Form{'bbro'}, " -->\n";
      &find_name_and_bbro ($scroll_num);
      print "<center><b>Big Brother Lineage for ",$name_out,", Scroll Number ";

      if ($bbro_num_out eq "TRA") {

        print "<font face=symbol>",$tra_cha_out,"</font>&nbsp;";

        printf "%d",$tra_num_out;

      }

      else {

        printf "%d",$scroll_num;

      }

      print "</b><br><br>\n";

      &print_name_and_bbro ($scroll_num);
      while ($bbro_num_out != "FOU"){
        &print_name_and_bbro ($bbro_num_out);
      }
      print "<br><br></center>";
      #End of Big Brother segment

   }
   elsif ($Form{'tree'} ne '') {
   
      if ($Form{'tree'} eq 'all') {
      
        #print "Display entire chapter scroll<br><br>\n\n";
        print "<center><b><font color=ff0000 size=+1>",$title," - Entire Chapter Tree</font></b></center><br>\n";
        print "<!-- tree=", $Form{'tree'}, " -->\n";
        for ($w = 1; $w <= $num_recs; $w++) {
           if ($scroll_arry[$w][3] eq "FOU") {
             $scroll_num = $scroll_arry[$w][1];
      
             $num_branches++;
             $tree_arry[$num_branches][1] = $scroll_arry[$w][2];
             $tree_arry[$num_branches][2] = 1;
             $tree_arry[$num_branches][3] = $scroll_arry[$w][5];
             $tree_arry[$num_branches][4] = "AL";
             $tree_arry[$num_branches][5] = $scroll_arry[$w][1];
      
             $level = 2;
             &find_little_bros($scroll_num,$level);
           }
        }
      
        for ($w = 1; $w <= $num_recs; $w++) {
           if ($scroll_arry[$w][3] eq "HON") {
             $scroll_num = $scroll_arry[$w][1];
      
             $num_branches++;
             $tree_arry[$num_branches][1] = $scroll_arry[$w][2];
             $tree_arry[$num_branches][2] = 1;
             $tree_arry[$num_branches][3] = $scroll_arry[$w][5];
             $tree_arry[$num_branches][4] = "AL";
             $tree_arry[$num_branches][5] = $scroll_arry[$w][1];

           }
        }

        for ($w = 1; $w <= $num_recs; $w++) {

           if ($scroll_arry[$w][3] eq "TRA") {

             $scroll_num = $scroll_arry[$w][1];

             $num_branches++;
             $tree_arry[$num_branches][1] = $scroll_arry[$w][2];
             $tree_arry[$num_branches][2] = 1;
             $tree_arry[$num_branches][3] = $scroll_arry[$w][5];
             $tree_arry[$num_branches][4] = $scroll_arry[$w][4];
             $tree_arry[$num_branches][5] = $scroll_arry[$w][1];
             $tree_arry[$num_branches][6] = $scroll_arry[$w][3];
             $tree_arry[$num_branches][7] = $scroll_arry[$w][8];
             $tree_arry[$num_branches][8] = $scroll_arry[$w][9];

             $level = 2;

             &find_little_bros($scroll_num,$level);

           }

        }
      
        #print family tree for entire chapter;
        $rtype="all";
        &print_ftree;
      
      }
      else
      {
        #This segment finds the Family Tree for a scroll number...
        $scroll_num = $Form{'tree'};
        print "<center><b><font color=ff0000 size=+1>",$title," - Family Tree</font></b></center><br>\n";
        print "<!-- tree=", $Form{'tree'}, " -->\n";
        &find_name_and_bbro($scroll_num);
 
        print "<center><b>Family Tree for ",$name_out,", Scroll Number ";

        if ($bbro_num_out eq "TRA") {
          print "<font face=symbol>",$tra_cha_out,"</font>&nbsp;";

          printf "%d",$tra_num_out;

        }

        else {

          printf "%d",$scroll_num;

        }
        print "</b></center><br><br>\n";

        #find all the little brothers - this subroutine is recursive and finds all descendents
        $level = 1;
        &find_little_bros($scroll_num,$level);
      
        #print family tree;
        &print_ftree;

        #print some info about how many little brothers we found...
        &ftree_summary;

        print "<br>\n";
        #End of Family Tree segment
      }

   }
   elsif ($Form{'scroll'} ne '') {

      if ($Form{'scroll'} eq 'actives') {
        #Actives only scroll
        #print "<center><b><font color=ff0000 size=+1>Jugdish's Scroll-o-matic!</font></b></center><br>\n";
        print "<center><b><font color=ff0000 size=+1>",$title," - Actives</font></b></center><br><br>\n";
        print "<!-- scroll=", $Form{'scroll'}, " -->\n";
        &filter_array;
        &print_scroll;
      }
      elsif ($Form{'scroll'} eq 'all') {
        #Show entire scroll - same as default
        &show_all_scroll;
      }
      else {
        #Error handling
        print "<center><b><font color=ff0000 size=+1>",$title," - Error</font></b></center><br>\n";
        print "<center>I don't understand your request.</center><br>\n";
      }

   }
   elsif ($Form{'type'} eq 'info') {

      #Info report
      print "<center><b><font color=ff0000 size=+1>",$title," - Info</font></b></center><br>\n";
      print "<center><b>About this Application</b></center><br><br>\n";
      print "<blockquote>\n";
      print "<b>What family trees from the original founders are still active?</b>&nbsp;&nbsp;The only family trees that are still active are descendants of <a href=",$script_name,"?tree=005>Matt Mulroy</a>, <a href=",$script_name,"?tree=008>Pat O'Roark</a>, <a href=",$script_name,"?tree=009>Robert Romeo</a>, and <a href=",$script_name,"?tree=014>Terry Westbrook</a>.<br>\n";

      print "<br>\n";
      print "<b>Who is Chris Albonetti?  Why is he on the scroll?</b>&nbsp;&nbsp;Chris Albonetti was transferred to Pi Epsilon from another chapter, but is included here in the scroll because he has a little brother in our chapter.<br>\n";

      print "<br>\n";
      print "<b>How was this written?  Is there some sort of database involved?</b>&nbsp;&nbsp;This was written using a Perl script that reads a flat text datafile into an array, and then does processing against the array.<br>\n";

      print "<br>\n";
      print "<b>Why are some names like Xxx Xxxx?  Are these missing names?</b>&nbsp;&nbsp;There are some names that have been struck from the scroll because these people demitted.  To see the a page with the names restored, add '&demit=show' to the end of the URL (eg <a href=",$script_name,"?scroll=all&demit=show>",$script_name,"?&scroll=all&demit=show</a>).<br>\n";

      print "<br>\n";
      print "<b>What if I want to see what the chapter looked like when I was active?</b>&nbsp;&nbsp;If you want to see only the portion of the scroll up to a certain point, add '&thru=<i>scrollnum</i>' to the end of the URL (eg <a href=",$script_name,"?scroll=all&thru=120>",$script_name,"?scroll=all&thru=120</a>).  This also works for family trees.<br>\n";

      print "<br>\n";
      print "Please send any questions, comments, or corrections to Frank Campagna\n";

      print "</blockquote><br><br><br>\n";

   }
   else {

      #Error handling
      #print "<center><b><font color=ff0000 size=+1>Jugdish's Scroll-o-matic!</font></b></center><br>\n";
      #print "<center><b>Error</b><br><br>\n";
      #print "<center>I don't understand your request.</center><br>\n";
      #Request was not understood, or is blank; do a default scroll
      &show_all_scroll;

   }
#}
#else {

#   #No parameters were passed, so we do a default scroll...
#   &show_all_scroll;

#}

#Print the Footer
&print_ftr;

##########################################################
#Subroutines

sub make_scroll_array {
  open(SCROLL_DB,"$scroll_file") || do {&no_open;};
  #@recline = <SCROLL_DB>;
  while ($recline = <SCROLL_DB>)
  {
    #print $recline, "<BR>\n";
    $num_recs++;

    $scroll_num = substr $recline, 0, 3;
    $tmp_frater_nom = substr $recline, 4, 28;
    $bbro_num = substr $recline, 33, 3;
    $act_stat = substr $recline, 37, 2;
    $tmp_nick = substr $recline, 40, 25;
    $tra_cha = substr $recline, 66, 2;
    $tra_num = substr $recline, 69, 3;
    $demit_flag = substr $recline, 73, 1;

    #Trim trailing blanks off Frater Name
    #for ($i = 27; $i >=0; $i--) {
    #   if (substr($tmp_frater_nom,$i,1) ne " ") {$tmp_frater_nom = substr($tmp_frater_nom,0,$i+1); $i=-1}
    #}
    for ($i = 27; $i >=0; $i--) {
      if (substr($tmp_frater_nom,$i,1) eq " ") {
        $tmp_frater_nom = substr($tmp_frater_nom,0,$i-1+1);
      }
	  else {
        $i = -1;
	  }
    }

    #Trim trailing blanks off Nickname
    for ($i = 24; $i >=0; $i--) {
      if (substr($tmp_nick,$i,1) eq " ") {
        $tmp_nick = substr($tmp_nick,0,$i-1+1);
      }
	  else {
        $i = -1;
	  }
    }
   
    $frater_nom = $tmp_frater_nom;
    $nick = $tmp_nick;

    $scroll_arry[$num_recs][1] = $scroll_num;
    $scroll_arry[$num_recs][2] = $frater_nom;           
    $scroll_arry[$num_recs][3] = $bbro_num;           
    $scroll_arry[$num_recs][4] = $act_stat;
    $scroll_arry[$num_recs][5] = $nick; 
    $scroll_arry[$num_recs][8] = $tra_cha; 
    $scroll_arry[$num_recs][9] = $tra_num; 
    $scroll_arry[$num_recs][10] = $demit_flag; 

  }
  close(SCROLL_DB);
}

sub change_blank_nicks {
  for ($i = 1; $i <= $num_recs; $i++) {
    if ($scroll_arry[$i][5] eq "") {
      $scroll_arry[$i][5] = "(none)";
    }
  }
}

sub hide_demit_names {
  for ($i = 1; $i <= $num_recs; $i++) {
    if ($scroll_arry[$i][10] eq "Y") {
      $scroll_arry[$i][2] = "Xxx Xxxxx";
      $scroll_arry[$i][5] = "Xxxx";
    }
  }
}

sub shorten_array {
  $hi_scroll = $_[0];
  $tmp_num_recs = $num_recs;
  for ($i = 1; $i <= $tmp_num_recs; $i++){
    #print $i,":",int($scroll_arry[$i][1]),":",$tmp_num_recs,":",$num_recs,"<br>\n";
    if (int($scroll_arry[$i][1]) eq $hi_scroll ) {
      $num_recs = $i;
    }
  }
}

sub add_bbro_to_array {
  for ($i = 1; $i <= $num_recs; $i++) {
    for ($j = 1; $j <= $num_recs; $j++) {
      if ($scroll_arry[$i][3] eq $scroll_arry[$j][1]) {
        $scroll_arry[$i][6] = $scroll_arry[$j][2];
        $scroll_arry[$i][7] = $scroll_arry[$j][4];
      }
    }
  }
}

sub print_hdr {
  print "Content-type: text/html\n\n";
  print "<html>\n";
  print "<head><title>Online ",$title,"</title></head>\n";

  print "<body BGCOLOR='#000000' TEXT='#FF0000' LINK='#DDDDDD' VLINK='#999999'>\n\n";
  print "<!-- Perl code version date: ",$ver,". Refer code questions to Jugdish, the Forensic Analyst -->\n\n";
}

sub show_all_scroll {
   print "<center><b><font color=ff0000 size=+1>",$title,"</font></b></center><br><br>\n";
   &print_scroll;
}

sub print_scroll {
    print "<center><table border='1'>\n";
    print "<tr><td align=center valign=bottom><b><font color=ff0000>Scroll<br>Number</font></b></td><td align=center valign=bottom><b><font color=ff0000>Frater</font></b></td><td align=center valign=bottom><b><font color=ff0000>Nickname</font></b></td><td align=center valign=bottom><b><font color=ff0000>Big<br>Brother</font></b></td><td align=center valign=bottom><b><font color=ff0000>Lineage</font></b></td><td align=center valign=bottom><b><font color=ff0000>Family Tree</font></b></td></tr>\n";
    for ($i = 1; $i <= $num_recs; $i++)
    {
      print "<tr><td align=right>";
      #print scroll number
      if ($scroll_arry[$i][3] eq "TRA") {
        if ($scroll_arry[$i][4] eq "AC") {
          print "<font color=ffffff face=symbol>",$scroll_arry[$i][8],"&nbsp;</font>";
          print "<font color=ffffff>";
          printf "%d", $scroll_arry[$i][9];
          print "</font>";
        }
        else {
          print "<font face=symbol>",$scroll_arry[$i][8],"&nbsp;</font>";
          printf "%d", $scroll_arry[$i][9];
        }
      }
      else {
        if ($scroll_arry[$i][4] eq "AC") {
          print "<font color=ffffff>";
          printf "%d", $scroll_arry[$i][1];
          print "</font>";
        }
        else {
          printf "%d", $scroll_arry[$i][1];
        }
      }
      print "</td><td>";

      #print name
      if ($scroll_arry[$i][4] eq "AC") {
        print "<font color=ffffff>",$scroll_arry[$i][2],"</font>";
      }
      else {
        print $scroll_arry[$i][2];
      }

      print "</td><td>";

      #print nickname
      if ($scroll_arry[$i][4] eq "AC") {
        print "<font color=ffffff>",$scroll_arry[$i][5],"</font>";
      }
      else {
        print $scroll_arry[$i][5];
      }
      print "</td><td>";

      if ($scroll_arry[$i][3] eq "FOU")
        {print "Founder";}
      elsif ($scroll_arry[$i][3] eq "HON")
        {print "Honorary";}
      elsif ($scroll_arry[$i][3] eq "TRA")
        {
          if ($scroll_arry[$i][4] eq "AC") {
            print "<font color=ffffff>Transfer</font>";
          }
          else {
            print "Transfer";
          }
        }
      else
        {
          if ($scroll_arry[$i][7] eq "AC") {
            print "<font color=ffffff>",$scroll_arry[$i][6],"</font>";
          }
          else {
            print $scroll_arry[$i][6];
          }
        }
      print "</td><td>";
      #fecfec print "<a href=",$script_name,"?bbro=",$scroll_arry[$i][1],">Lineage</a>";
      print "<a href=",$script_name,"?bbro=",int $scroll_arry[$i][1],">Lineage</a>";
      print "</td><td>";
      #fecfec print "<a href=",$script_name,"?tree=",$scroll_arry[$i][1],">Family Tree</a>";
      print "<a href=",$script_name,"?tree=",int $scroll_arry[$i][1],">Family Tree</a>";
      print "</td></tr>\n";
    }
    print "</table></center><br>\n";
}

sub print_ftr {
  print "<center>Names in <font color=ffffff>white</font> are Active fraters.</center><br>\n";
  print "<center><a href=",$script_name,"?scroll=all>View Chapter Scroll</a>&nbsp;&nbsp;\n";
  print "<a href=",$script_name,"?scroll=actives>View Actives Scroll</a>&nbsp;&nbsp;\n";
  print "<a href=",$script_name,"?tree=all>View Chapter Tree</a>&nbsp;&nbsp;\n";
  print "<a href=",$script_name,"?type=info>View Info</a></center>\n";
  print "</body>\n";
  print "</html>\n";
}

sub no_open {
  print "Error! The database could not be opened.  Contact Frank.<br><br>\n";
  &print_ftr;
  exit;
}

sub print_name_and_bbro {
  $scroll_num = $_[0];
  $name_out = "";
  $bbro_num_out = "";
  &find_name_and_bbro ($scroll_num);
  $bbro_name_out = "";
  &find_bbro_info ($bbro_num_out);
  if ($bbro_num_out eq "FOU"){
    print $name_out," was a founder of Pi Epsilon and has no Big Brother.<br>\n";  
  }
  elsif ($bbro_num_out eq "HON"){
    print $name_out;
    print " is an Honorary and has no Big Brother.<br>\n";
  }

  elsif ($bbro_num_out eq "TRA"){

    if ($status_out eq "AC"){print "<font color=ffffff>";}

    print $name_out;

    if ($status_out eq "AC"){print "</font>";}

    print " is a Transfer and has a Big Brother in another chapter.<br>\n";

  }
  else {
    if ($status_out eq "AC"){print "<font color=ffffff>";}
    print $name_out;
    if ($status_out eq "AC"){print "</font>";}
    print "'s Big Brother is ";
    if ($bbro_status_out eq "AC"){print "<font color=ffffff>";}

    if ($bbro_bbro_num_out eq "TRA") {
      print $bbro_name_out, " (&quot;",$bbro_nick_out,"&quot;&nbsp;";

      print "<font face=symbol>",$bbro_tra_cha_out,"</font>&nbsp;#";

      printf "%d",$bbro_tra_num_out;

      print ")";

    }

    else {

      print $bbro_name_out, " (&quot;",$bbro_nick_out,"&quot;&nbsp;#";

      printf "%d",$bbro_num_out;

      print ")";
    }

    if ($bbro_status_out eq "AC"){print "</font>";}
    print "<br>\n";
  }
}

sub find_name_and_bbro {
  $scroll_num_passed = $_[0];
  $found = "False";
  for ($i = 1; $i <= $num_recs; $i++)
  {
    #fecfec if ($scroll_arry[$i][1] eq $scroll_num_passed){
    #fecfec if (int $scroll_arry[$i][1] == int $scroll_num_passed ){
    #if ((int $scroll_arry[$i][1] == int $scroll_num_passed ) || ($scroll_arry[$i][1] eq $scroll_num_passed)){
    if (((int $scroll_arry[$i][1] == int $scroll_num_passed) && (int $scroll_arry[$i][1] <=> 0)) || ($scroll_arry[$i][1] eq $scroll_num_passed)){
      $name_out = $scroll_arry[$i][2];
      $bbro_num_out = $scroll_arry[$i][3];
      $status_out = $scroll_arry[$i][4];
      $nick_out = $scroll_arry[$i][5];
      $tra_cha_out = $scroll_arry[$i][8];
      $tra_num_out = $scroll_arry[$i][9];
      $found = "True";
    }
  }
  if ($found eq "False") {
    print "Sorry, that Scroll Number was not found!<br><br>\n";
    &print_ftr;
    exit;
  }
  return $name_out;
  return $bbro_num_out;
  return $status_out;
  return $nick_out;
  return $tra_cha_out;
  return $tra_num_out;
}

sub find_bbro_info {
  $scroll_num_passed = $_[0];
  for ($i = 1; $i <= $num_recs; $i++)
  {
    if ($scroll_arry[$i][1] eq $scroll_num_passed){
      $bbro_name_out = $scroll_arry[$i][2];
      $bbro_bbro_num_out = $scroll_arry[$i][3];
      $bbro_nick_out = $scroll_arry[$i][5];
      $bbro_status_out = $scroll_arry[$i][4];
      $bbro_tra_cha_out = $scroll_arry[$i][8];
      $bbro_tra_num_out = $scroll_arry[$i][9];
    }
  }
  return $bbro_name_out;
  return $bbro_bbro_num_out;
  return $bbro_nick_out;
  return $bbro_status_out;
  return $bbro_tra_cha_out;
  return $bbro_tra_num_out;
}

sub find_little_bros {
  local ($scroll_num_passed) = $_[0];
  local ($level_passed) = $_[1];
  local ($i,$lbro_name_out,$lbro_num_out,$sp);
  for ($i = 1; $i <= $num_recs; $i++) {
    #print $scroll_arry[$i][3]," ",int $scroll_arry[$i][3]," ",int $scroll_num_passed," ",$scroll_num_passed,"<br>\n";
    #if ($scroll_arry[$i][3] eq $scroll_num_passed){
    #if (int $scroll_arry[$i][3] == int $scroll_num_passed){
    if (((int $scroll_arry[$i][3] == int $scroll_num_passed) && (int $scroll_arry[$i][3] <=> 0)) || ($scroll_arry[$i][3] eq $scroll_num_passed)){
      $lbro_num_out = $scroll_arry[$i][1];
      $lbro_name_out = $scroll_arry[$i][2];
      
      $num_branches++;
      $tree_arry[$num_branches][1] = $lbro_name_out;
      $tree_arry[$num_branches][2] = $level_passed;
      $tree_arry[$num_branches][3] = $scroll_arry[$i][5];
      $tree_arry[$num_branches][4] = $scroll_arry[$i][4];
      $tree_arry[$num_branches][5] = $lbro_num_out;
      
      if ($scroll_arry[$i][4] eq "AC") {print "</font>";}
      &find_little_bros($lbro_num_out,$level_passed+1);
    }
  }
}

sub print_ftree {
      print "<table border='0' cellpadding='0' cellspacing='0'>\n";
 
      if ($rtype eq 'all') {
        print "<tr><td><nobr><font face=Arial size=-1><img src='clr.gif' align='left' border='0' vspace='0' hspace='0' width='1' height='18'>";
        print "Pi Epsilon Chapter of Tau Kappa Epsilon";
        print "</font></td></tr>\n";
      }
      else {
        print "<tr><td><nobr><font face=Arial size=-1><img src='clr.gif' align='left' border='0' vspace='0' hspace='0' width='1' height='18'>";
        if ($status_out eq "AC"){print "<font color=ffffff>";}

        if ($bbro_num_out eq "TRA") {
          print $name_out," (&quot;",$nick_out,"&quot;&nbsp;";

          print "<font face=symbol>",$tra_cha_out,"</font>&nbsp;#";

          printf "%d",$tra_num_out;
          print ")";

        }

        else {        

          print $name_out," (&quot;",$nick_out,"&quot;&nbsp;#";

          printf "%d",$scroll_num;

          print ")";
        }

        if ($status_out eq "AC"){print "</font>";}
        print "</font></td></tr>\n";
      }
 
      for ($i = 1; $i <= $num_branches; $i++) {
         print "<tr><td><nobr><font face=Arial size=-1>";
         
         #ok, lets first print the bars or the spaces...
         for ($j = 1; $j <= $tree_arry[$i][2] - 1; $j++) {
            if ($lvl[$j] eq 'no') {
               print "<img src='clr.gif' align='left' border='0' vspace='0' hspace='0' width='18' height='18'>";
            }
            else {
               print "<img src='bar.gif' align='left' border='0' vspace='0' hspace='0' width='18' height='18'>";
            }
         }
         
         #we've printed all but the last graphic right next to the name - print either a tee or corner....
         if ($tree_arry[$i][2] == $tree_arry[$i+1][2]) {
            #print a tee - a twin brother is next
            print "<img src='tee.gif' align='left' border='0' vspace='0' hspace='0' width='18' height='18'>";
            $lvl[$tree_arry[$i][2]] = 'yes';
         }
         elsif ($tree_arry[$i][2] < $tree_arry[$i+1][2]) {
            #no more descendents; but first check for a twin somewhere below
            $eoa_flag = "False";
            for ($k = $i+1; $k <= $num_branches; $k++) {
               #print $k;
               if ($tree_arry[$k][2] == $tree_arry[$i][2]) {
                 $eoa_flag = "True";
                 #found a twin...print a tee
                 print "<img src='tee.gif' align='left' border='0' vspace='0' hspace='0' width='18' height='18'>";
                 $lvl[$tree_arry[$i][2]] = 'yes';
                 $k = $num_branches;
               }
               elsif ($tree_arry[$k][2] < $tree_arry[$i][2]) {
                 $eoa_flag = "True";
                 #didn't find a twin...print a corner (there may be further descendents)
                 print "<img src='cornr.gif' align='left' border='0' vspace='0' hspace='0' width='18' height='18'>";
                 $lvl[$tree_arry[$i][2]] = 'no';
                 $k = $num_branches;
               }
            }
            if ($eoa_flag eq "False"){
              #we got to the end of the array, and found no more descendents or twins...print a corner
              print "<img src='cornr.gif' align='left' border='0' vspace='0' hspace='0' width='18' height='18'>";
              $lvl[$tree_arry[$i][2]] = 'no';
            }           
         }
         else {  #therefore $tree_arry[$i][2] > $tree_arry[$i+1][2]
            #no more descendents or twins...print a corner
            print "<img src='cornr.gif' align='left' border='0' vspace='0' hspace='0' width='18' height='18'>";
            $lvl[$tree_arry[$i][2]] = 'no';
         }
         #print name, etc
         if ($tree_arry[$i][4] eq "AC") {$num_act_branches++; print "<font color=ffffff>";}

   #fec formatting

         if ($tree_arry[$i][6] eq "TRA") {
           print $tree_arry[$i][1]," (&quot;",$tree_arry[$i][3],"&quot;&nbsp;";

           print "<font face=symbol>",$tree_arry[$i][7],"</font>&nbsp;";
           printf "%d", $tree_arry[$i][8];
           print ")";

         }
         else {

           print $tree_arry[$i][1]," (&quot;",$tree_arry[$i][3],"&quot;&nbsp;#";

           printf "%d", $tree_arry[$i][5];

           print ")";     

         }

         if ($tree_arry[$i][4] eq "AC") {print "</font>";}
         print "</font></nobr></td></tr>\n";
      }
      print "</table><br><br>\n";
}

sub ftree_summary {
      print "<center>";
      #if there are no little brothers at all found...
      if ($num_branches eq 0){
        print "This frater has no little brothers.<br>\n";
      }
      else {
        print "This frater has ",$num_branches," descendent";
        if ($num_branches > 1) {print "s";}
        print " in his family tree, and ";
        if ($num_act_branches == 0)
          {print "none";}
        else
          {print $num_act_branches;}
        print " ";
        if ($num_act_branches == 1)
          {print "is";}
        else
          {print "are";}
        print " still active.<br>\n";
      }
      print "</center>\n";
}

sub filter_array {
   $new_num_recs = 0;
   for ($i = 1; $i <= $num_recs; $i++)
   {
     if ($scroll_arry[$i][4] eq "AC") {
       $new_num_recs++;
       $tmp_arry[$new_num_recs][1] = $scroll_arry[$i][1];
       $tmp_arry[$new_num_recs][2] = $scroll_arry[$i][2];
       $tmp_arry[$new_num_recs][3] = $scroll_arry[$i][3];
       $tmp_arry[$new_num_recs][4] = $scroll_arry[$i][4];
       $tmp_arry[$new_num_recs][5] = $scroll_arry[$i][5];
       $tmp_arry[$new_num_recs][6] = $scroll_arry[$i][6];
       $tmp_arry[$new_num_recs][7] = $scroll_arry[$i][7];
       $tmp_arry[$new_num_recs][8] = $scroll_arry[$i][8];
       $tmp_arry[$new_num_recs][9] = $scroll_arry[$i][9];
     }
   }
   for ($i = 1; $i <= $new_num_recs; $i++)
   {
      $scroll_arry[$i][1] = $tmp_arry[$i][1];
      $scroll_arry[$i][2] = $tmp_arry[$i][2];
      $scroll_arry[$i][3] = $tmp_arry[$i][3];
      $scroll_arry[$i][4] = $tmp_arry[$i][4];
      $scroll_arry[$i][5] = $tmp_arry[$i][5];
      $scroll_arry[$i][6] = $tmp_arry[$i][6];
      $scroll_arry[$i][7] = $tmp_arry[$i][7];
      $scroll_arry[$i][8] = $tmp_arry[$i][8];
      $scroll_arry[$i][9] = $tmp_arry[$i][9];
   }
   $num_recs = $new_num_recs;
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
