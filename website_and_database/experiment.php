<?php

\*
# This code is a compliment to "Covert lie detection using keyboard dynamics".
# Copyright (C) 2017  QianQian Li
# See GNU General Public Licence v.3 for more details.
*\


    session_start();
    require_once ('config.php');
    //check whether the participant has the permission
    if(empty($_SESSION['subject'])){
        echo "<script>alert('Please Login or Register');location='index.php';</script>";
    }
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <!-- for phone-->
        <meta content="yes" name="apple-mobile-web-app-capable">
        <meta name="viewport" content="width=device-width,height=device-height,inital-scale=1.0,maximum-scale=1.0,user-scalable=no;">
        <title>Domande per i partecipanti</title>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap.min.css">
        <link href="margins.css" rel="stylesheet" type="text/css" />
        <link rel="Shortcut Icon" href="favicon.ico"/>
        <!--    progress bar style-->
        <style type="text/CSS">
            .outter{
                height:18px;
                width:50px;
                border:solid 1px #000;
                text-align:center;
            }
        .inner{
            height:18px;
            width:<?php echo $percent ?>%;
            border-right:solid 1px #000;
            background: #f8ffe8;
            background: -moz-linear-gradient(top, #f8ffe8 0%, #e3f5ab 33%, #b7df2d 100%);
            background: -webkit-gradient(linear, left top, left bottom, color-stop(0%,#f8ffe8), color-stop(33%,#e3f5ab), color-stop(100%,#b7df2d));
            background: -webkit-linear-gradient(top, #f8ffe8 0%,#e3f5ab 33%,#b7df2d 100%);
            background: -o-linear-gradient(top, #f8ffe8 0%,#e3f5ab 33%,#b7df2d 100%);
            background: -ms-linear-gradient(top, #f8ffe8 0%,#e3f5ab 33%,#b7df2d 100%);
            background: linear-gradient(to bottom, #f8ffe8 0%,#e3f5ab 33%,#b7df2d 100%);
            filter: progid:DXImageTransform.Microsoft.gradient( startColorstr='#f8ffe8', endColorstr='#b7df2d',GradientType=0 );
        }
        </style>
        <script>
        function FocusOnInput(){
            document.getElementById("answerContent").focus();
        }
        </script>
        <script src="js/jquery-1.11.3.js"></script>
        <script src="js/gyro.min.js"></script>
    </head>
    <body>
        <div class="container-fluid">
            <div class="row-xs">
                <div class="col-xs-3 pull-left"><img alt="Unipd" src="images/unipd_1.jpg" class="img-responsive">
                </div>
                <div class="col-xs-3 pull-right"><img alt="HIT" src="images/HIT_logo_1.png" class="img-responsive"/>
                </div>
            </div>
        </div>
        <?php
        // the action of click Next button
        if($_POST["ques_submit"]){
            $session_ID_Post = $_POST['sessionID'];
            $question_Index_Post = $_POST['questionINDEX'];
            $question_ID_Post = $_POST['questionID'];
            //get the content of input
            $text_Answer=$_POST['answerContent1'];
            $text_Answer= str_replace("'", "!", $text_Answer);
            $letters_number = $_POST['lettersNumber'];
            //keystorkes,accellerometer
            $keystrokes = $_POST['keyStrokes'];
	    $keystrokes= str_replace("'", "!",$keystrokes);
            $accellerometerbefore = $_POST['accellerometerBefore'];
            $accellerometertyping = $_POST['accellerometerTyping'];
            $gyroscopetyping = $_POST['gyroscopeTyping'];
            $timestampfirstdigit = $_POST['timestampFirstDigit'];
            //$timestampfirstdigit="1";
            $timestampprompted = $_POST['timestampPrompted'];
            //$timestampprompted="1";
            $timestampenter = $_POST['timestampEnter'];
            //$timestampenter="1";
            $gyroscopebefore = $_POST['gyroscopeBefore'];
	    $timestamptap=$_POST['timestampTap'];
            if(trim($text_Answer)==null){
                echo "<script>alert('La risposta non può essere nulla');location='experiment.php';</script>";
                mysql_close();
                }elseif (trim(is_numeric($text_Answer))&&$letters_number==0) {
                         echo "<script>alert('the answer can not be writen in numbers');location='experiment.php';</script>";
                         mysql_close();
            }
            else{
                //which block the participant take in
                if($question_Index_Post<3){
                    $current_Blocknumber = 0;
                }
                else{
                    $current_Blocknumber = 1;                        
                }                   
            //insert into answers Tables
            $sql_answer_insert="insert into answers_long(session_id,question_id,text_answer,keystroke,accellerometer_typing,accellerometer_before,gyroscope_before,gyroscope_typing,timestamp_first_digit,eyetracking,bci,timestamp_prompted,timestamp_enter,timestamp_tap) values('".$session_ID_Post."','".$question_ID_Post."','".$text_Answer."','".$keystrokes."','".$accellerometertyping."','".$accellerometerbefore."','".$gyroscopebefore."','".$gyroscopetyping."','".$timestampfirstdigit."','','','".$timestampprompted."','".$timestampenter."','".$timestamptap."')";
            $result_answer_insert=mysql_query($sql_answer_insert) or die('Error, insert query failed  '.$sql_answer_insert);
	    if($question_Index_Post==20){
                //update session
                $sql_finish_Question = mysql_query("update sessions_long set completed = 1 where session_id = ".$session_ID_Post."");
                mysql_close();
                echo "<script>location='thanks.php';</script>";
            }  
            else {
                $question_Index_Post++;
                //update session table
                $string = "update sessions_long set current_question_index = '".$question_Index_Post."',current_block_number = '".$current_Blocknumber."' where session_id =".$session_ID_Post."";
                $sql_update_session=mysql_query("update sessions_long set current_question_index = '".$question_Index_Post."',current_block_number = '".$current_Blocknumber."' where session_id =".$session_ID_Post."");
                //jump to which page
                if($question_Index_Post==3){
                    echo "<script>location='Inf_realtest.php';</script>";
                }
                else {
                    echo "<script>location='experiment.php';</script>";
                }
                mysql_close();
            }  
        }

    }
        
        //load the content of the table
        else{
            //check if this participant has a session
            $subject_number =$_SESSION['subject'];
            //get question_index and question_ids_sequence of this participant
            $string = "select * from sessions_long where completed=0 and subject_id=$subject_number ORDER BY start_time DESC LIMIT 1";
            $sql_search_Session = mysql_query($string);
            $rs_search_Session=  mysql_fetch_array($sql_search_Session);
            $question_Index_Table = $rs_search_Session['current_question_index'];
            $question_Sequence_Table=$rs_search_Session['question_ids_sequence'];
            $session_ID = $rs_search_Session['session_id'];
            //convert a String to an Array
            $question_Array = explode(',', $question_Sequence_Table);
            $question_ID=$question_Array[$question_Index_Table];
            //get the question content from Table questions
            $sql_find_Question= mysql_query("select * from questions_long where question_id= $question_ID");
            $rs_find_Question = mysql_fetch_array($sql_find_Question);
            if($rs_find_Question){
            ?>
                <div class="col-xs-offset-1 col-xs-10 panel panel-default">
                <div class="pannel-body">
                <form action="" method="post" name="ques_form" id="ques_form"  style="margin-bottom:0px;" autocomplete="off" class="form-horizontal">
                    <div class="text-center" >
                            <?php
                            //green is true
                            if($question_Index_Table>2){
                                 ?>
                            <h3><?php echo htmlspecialchars($rs_find_Question['text_short']); ?></h3>
                            <?php
                                $percent = ($question_Index_Table-3)/18*100; 
                                $percent = round($percent);
                            }                           
                            else{ 
                                $percent = (int)($question_Index_Table/3*100);
                                $percent = round($percent);
                                ?>
                                <h3><?php echo htmlspecialchars($rs_find_Question['text_short']); ?></h3>
                            <?php }                             
                                }
                            ?>
                    </div>
                    <div class="col-xs-offset-0 col-xs-12 form-group top-margins bottom-margins">
                        <label class="control-label col-xs-2"  for="answerContent">Risposta </label>
                        <div class="col-xs-10">
                            <input class="form-control col-xs-10"  type="text" id="answerContent" name="answerContent" onclick="set_timestamp_tap()" autofocus="autofocus"/>
                        </div>
                    
                    <input id="sessionID" name="sessionID" value="<?php echo $session_ID;?>" type="hidden"/>
                    <input id="questionID" name="questionID" value="<?php echo $question_ID;?>" type="hidden"/>
                    <input id="questionINDEX" name="questionINDEX" value="<?php echo $question_Index_Table;?>" type="hidden"/>
                    <input id="lettersNumber" name="lettersNumber" value="<?php echo $rs_find_Question['lettersnumber'];?>" type="hidden"/>
                    <input id="keyStrokes" name="keyStrokes" value="0" type="hidden"/>
                    <input id="accellerometerBefore" name="accellerometerBefore" value="0" type="hidden"/>
                    <input id="accellerometerTyping" name="accellerometerTyping" value="0" type="hidden"/>
                    <input id="gyroscopeTyping" name="gyroscopeTyping" value="0" type="hidden"/>
                    <input id="timestampFirstDigit" name="timestampFirstDigit" value="0" type="hidden"/>
                    <input id="timestampPrompted" name="timestampPrompted" value="0" type="hidden"/>
                    <input id="timestampEnter" name="timestampEnter" value="0" type="hidden"/>
		    <input id="timestampTap" name="timestampTap" value="0" type="hidden"/>
                    <input id="gyroscopeBefore" name="gyroscopeBefore" value="0" type="hidden"/>
                    <input id="answerContent1" name="answerContent1" value="" type="hidden"/>
                    
                    </div>
                   <div class="col-xs-offset-1 col-xs-10">
			 <div class="progress center-block">
                        	<div class="progress-bar" role="progressbar" aria-valuenow="100" aria-valuemin="0" aria-valuemax="100"  style="width: <?php echo $percent ?>%;">
                            	<?php echo $percent ?>%
                        	</div>
                    	</div>
		   </div>
                    
                    <input type="submit" style="visibility:hidden" id="ques_submit" name="ques_submit" value="Next" onclick="answer_submission()"/>
                </form>
            </div>
        
        
        <?php
            mysql_close();
        }
        ?>
        <table width="100" border="0" align="center" cellpadding="0" cellspacing="0">
            <tr>
                <td height="3"></td>
            </tr>
        </table>
       
    <div class="col-xs-offset-1 col-xs-10">
     <hr>
            <div id="footer">
                <div id="footnote">
                    <div id="footNote1"class="sectiona">@ 2015 TruthOrLie Test. All rights reserved. 
                    </div>
                    <div class="sectionb"></div>
                </div>
            </div>
            </div>
    </div>
        <script>
            //initializing the keyDOWN listener
            
            
            
            var console_debugging= 0;
            
            
            function set_debug(value){
                if(value==0 || value==1){
                    console_debugging= value;
                }
                else {
                    console.log("error on setting console_debugging to "+value);
                }
            }
        
        var keydyn  =[];
        var gyros_before	=[];
        var accel_before	=[];
        var gyros_typing	=[];
        var accel_typing	=[];
        
        var browser_features=gyro.getFeatures()
        
        //var devicemotion_able		= gyro.hasFeature("devicemotion");//"devicemotion" in gyro.getFeatures(); //gyro.hasFeature('devicemotion');
        //var deviceorientation_able	= gyro.hasFeature("deviceorientation");//"deviceorientation" in gyro.getFeatures(); //gyro.hasFeature('deviceorientation');
        
        //I set the frequency of the sampling to X milliseconds
        gyro.frequency = 50; //ms
        
        buffersize=5*(1000/gyro.frequency);
        bufferAnswer=15*(1000/gyro.frequency);//sec
        
        function get_timestamp_now(){
            return new Date().getTime();
        }
        
        //var is_monitoring=0;
        var typing_started=0;
        var timestamp_page_loaded		=get_timestamp_now();		//0
        var timestamp_first_keytap		=0;		//2
        var timestamp_enter_answer		=0;		//3
        var timestamp_tap			=0;
        //global variable for acc and gyro sampling
        var timestamp_sample_glb=0;
        
        //boolean to decect typing errors
        var typing_errors	=0;
        
        
        function console_log(string_){
            if(!console_debugging){
                console.log(""+string_+"");
            }
            return;
        }
        
        
        function set_timestamp(type){
            ts=""+new Date().getTime()+""; //conversion in string (millisec from epoch)
            if(type==0){timestamp_page_loaded=ts;}
            //if(type==1){timestamp_start_monitoring=ts;}
            if(type==2){timestamp_first_keytap=ts;}
            if(type==3){timestamp_enter_answer=ts;}
            console_log("set timestamp for "+type+ " = "+ts);
            return ts;
        }
        
        
        
        
        //function that performs the operations to submit the answer to the database
        function answer_submission(){
            document.getElementById("answerContent").disabled = true;
            gyro.stopTracking();
            set_timestamp(3);//timestamp_enter_answer
            //insert into the database
            //insert values (user,...,keydyn.toString(),gyros_before.toString(),accel_before.toString(),gyros_typing.toString(),accel_typing.toString()) into answer(..,..,..)
            //gyro_before_answer=JSON.stringify(gyros_before);
            //accel_before_answer=JSON.stringify(accel_before);
            //gyro_after_answer=JSON.stringify(gyros_typing);
            //accel_after_answer=JSON.stringify(accel_typing);
            //keystrokes_answer=JSON.stringify(keydyn);
            
            document.ques_form.keyStrokes.value=JSON.stringify(keydyn);
            console_log("document.ques_form.keyStrokes.value="+document.ques_form.keyStrokes.value+"")
            document.ques_form.gyroscopeTyping.value=JSON.stringify(gyros_typing);
            document.ques_form.gyroscopeBefore.value=JSON.stringify(gyros_before);
            document.ques_form.accellerometerTyping.value=JSON.stringify(accel_typing);
            document.ques_form.accellerometerBefore.value=JSON.stringify(accel_before);
            
            document.ques_form.timestampEnter.value=timestamp_enter_answer;
            document.ques_form.timestampPrompted.value=timestamp_page_loaded;
            document.ques_form.timestampFirstDigit.value=timestamp_first_keytap;
            document.ques_form.timestampTap.value=""+timestamp_tap+"";

	    document.ques_form.answerContent1.value=document.getElementById("answerContent").value
	    console_log(""+"timestamp_tap "+document.ques_form.timestampTap.value+" "+document.getElementById("answerContent1").value);	
            console_log(""+document.ques_form.accellerometerBefore.value+"document.ques_form.accelerometerBefore.value")
            //document.quest_form.submit();
            
        };
        
	function set_timestamp_tap() {
		
		if (!timestamp_tap){
			timestamp_tap=get_timestamp_now();			
			//document.ques_form.timestampTap.value=""+timestamp_tap+"";
			
			console_log(""+"timestamp_tap_set "+timestamp_tap+"");
			
		}

	};

        $('#answerContent').keydown(function(evt) {
                                    time_now=get_timestamp_now();
                                    if(!typing_started) {
                                    typing_started=1;
                                    //set_timestamp(1);
                                    timestamp_first_keytap=get_timestamp_now();
                                    console_log("KEYBOARD: first key pressed: DOWN at "+get_timestamp_now());
                                    }		
                                    
                                    if(evt.keyCode == 13) { // ignore enter
                                    //console.log("ENTER ignored");
                                    console_log("KEYBOARD: ENTER DOWN at "+get_timestamp_now());
                                    }
                                    character_typed=String.fromCharCode(evt.which);		
                                    keydyn.push({"t":evt.timeStamp,"tn":time_now, "character":character_typed ,"cod":evt.which, "k":'DOWN'});
                                    console_log("KEYBOARD: Key code: "+evt.which+" character "+character_typed+" DOWN "+" on time: "+evt.timeStamp);
                                    });
                                    
                                    //initializing the keyDOWN listener	
                                    $('#answerContent').keyup(function(evt) {
                                                              time_now=get_timestamp_now(); 
								
							      if(!typing_started) {
                                                              typing_started=1;
                                                              timestamp_first_keytap=get_timestamp_now();//set_timestamp(1);
                                                              console_log("KEYBOARD: first key pressed: UP on time: "+evt.timeStamp);
                                                              }	
                                                              if(evt.keyCode == 13) { // enter answer submission
                                                              //showDynamic();
                                                              set_timestamp(3);
                                                              //answer_submission();
                                                              console_log("KEYBOARD: ENTER UP at "+get_timestamp_now());
                                                              return;
                                                              }
                                                              if( event.keyCode == 8 ) {//backspace
                                                              typing_errors++;
                                                              }
                                                              character_typed=String.fromCharCode(evt.which);
                                                              keydyn.push({"t":evt.timeStamp,"tn":time_now,
                                                                          "cod":evt.which, "character":character_typed,
                                                                          "k":'UP'});
                                                              console_log("KEYBOARD: Key code: "+evt.which+" character "+character_typed+" UP "+" on time: "+evt.timeStamp);
                                                              });
                                                              
                                                              
                                                              
                                                              //document.getElementById('answerContent').focus();
                                                              
                                                              gyro.startTracking(function(o){
                                                                                 
                                                                                 if (o.x || o.y || o.z || o.alpha || o.beta || o.gamma){	
                                                                                 ts=get_timestamp_now();	
                                                                                 
                                                                                 //the typing is not started yet			
                                                                                 if (!typing_started){
                                                                                 accel_before.push({"t": ts, "x": o.x, "y": o.y, "z": o.z});
                                                                                 gyros_before.push({"t": ts, "a": o.alpha, "b": o.beta, "c": o.gamma});
                                                                                 
                                                                                 //checking if the buffer is full
                                                                                 if (buffersize>=0 && (buffersize < accel_before.length || buffersize < gyros_before.length)){
                                                                                 accel_before.shift(); //removing the first element
                                                                                 gyros_before.shift(); //removing the first element
                                                                                 }
                                                                                 }
                                                                                 //the typing is already started
                                                                                 
                                                                                 if (typing_started && (bufferAnswer>accel_typing.length || bufferAnswer>gyros_typing.length)){
                                                                                 accel_typing.push({"t": ts, "x": o.x, "y": o.y, "z": o.z});
                                                                                 gyros_typing.push({"t": ts, "a": o.alpha, "b": o.beta, "c": o.gamma});
                                                                                 }
                                                                                 
                                                                                 }
                                                                                 }	
                                                                                 );
                                                                                 
                                                                                 
        </script>
        
        <script src="js/jquery-1.11.3.js"></script>
        <!-- Latest compiled and minified JavaScript -->
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/js/bootstrap.min.js"></script>
        
    </body>
</html>
