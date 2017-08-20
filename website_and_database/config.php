<?php

\*
# This code is a compliment to "Covert lie detection using keyboard dynamics".
# Copyright (C) 2017  QianQian Li
# See GNU General Public Licence v.3 for more details.
*\


 $hostname="localhost"; //mysql Address
 $basename="???"; //mysql username
 $basepass="?????"; //mysql password
 $database="truth_or_lie"; //mysql database

 $conn=mysql_connect($hostname,$basename,$basepass)or die("Can not connect to the mysql database"); //connect to mysql              
 mysql_select_db($database,$conn); // choose mysql database
 mysql_query("set names 'utf8'");//mysql encoding
?>
