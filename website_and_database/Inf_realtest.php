<!DOCTYPE html>
<!--
# This code is a compliment to "Covert lie detection using keyboard dynamics".
# Copyright (C) 2017  QianQian Li
# See GNU General Public Licence v.3 for more details.
-->
<html>
    <head>
        <meta charset="UTF-8">
        <meta content="yes" name="apple-mobile-web-app-capable">
        <meta name="viewport" content="width=device-width,height=device-height,inital-scale=1.0,maximum-scale=1.0,user-scalable=no;">
        <title>Information Page</title>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap.min.css">
        <link rel="Shortcut Icon" href="favicon.ico"/>
    </head>
    <body>
        <div class="container-fluid">
            <div class="row-xs">
                <div class="col-xs-3 pull-left"><img alt="Unipd" src="images/unipd_1.jpg" class="img-responsive"></div>
                <div class="col-xs-3 pull-right"><img alt="HIT" src="images/HIT_logo_1.png" class="img-responsive"/></div>
            </div>
        </div>
        <table width="100" border="0" align="center" cellpadding="0" cellspacing="0">
          <tr>
            <td height="5"></td>
          </tr>
        </table>

        <?php
        // put your code here
        ?>

        <div class="col-xs-offset-1 col-xs-10">
        <form action="" method="post" name="informForm"  style="margin-bottom:0px;" >
            <table class=" table table-striped">
                <tr>
                    <td class="text-center" bgcolor="#EBEBEB">Ora sei pronto per iniziare l’esperimento.</td>
                </tr>
                <tr >
                    <td  align="left" bgcolor="#FFFFFF" >
                        <p class="text-justified">
                            Ricordati di rispondere in modo accurato a tutte le domande che ti vengono proposte, <b>basandoti sulle informazioni che hai precedentemente inserito all’interno della tua carta d’identità</b>.<br/><br/>
                            <br/>Buon lavoro!</p>                    </td>
                </tr>
                <tr>
                    <td colspan="2" align="center" valign="top" bgcolor="#FFFFFF" >
                        <input id="setup" name="setup" type="button" onclick="javascript:window.open('experiment.php','_self')" value="Continue"/></td>
                </tr>
            </table>
        </form>
        </div>
    <table width="100" border="0" align="center" cellpadding="0" cellspacing="0">
        <tr>
          <td height="5"></td>
        </tr>
    </table>    
    <div class="footer col-xs-offset-1 col-xs-8" id="footer">
                <div id="footnote">
                    <div class="sectiona">@ 2015 TruthOrLie Test. All rights reserved.
                    </div>
                    <div class="sectionb"></div>
                </div>
            </div>
            <script src="js/jquery-1.11.3.js"></script>
            <!-- Latest compiled and minified JavaScript -->
            <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/js/bootstrap.min.js"></script>    
    </body>
</html>
