<?php
if( !isset($__MISC) ) {
    $__MISC = 1;

    function print_header() {
        ?>
        <html>
        <head>
          <title>SPIN2 - Sequence Profiles from Structure</title>
          <META name=keywords content="Sequence Prediction">
          <script type="text/javascript">
            var _gaq = _gaq || [];
            _gaq.push(['_setAccount', 'UA-16402543-2']);
            _gaq.push(['_trackPageview']);
            (function() {
              var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
              ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
              var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
            })();
          </script>
        </head>
        <body bgcolor="cornsilk">
          <center>
            <h1><img src =./movie.gif width=60 height=60><font size=6 color=green>
              SPIN2:</font> predicts <font color=green><b> S</b></font>equence
              <font color=green><b>P</b></font>rofiles by <font color=green>
              <b>I</b></font>ntegrated <font color=green><b>N</b></font>eural
              network </h1>
            <br>
        <?php
    }

    function print_main() {
        ?>
        <form enctype='multipart/form-data' ACTION="index.php" METHOD="post">
          <table border="0" >
            <tr>
              <td colspan=2>Results will be returned via email. Your email address will not be stored. </td>
            </tr>
            <tr>
              <td colspan=2>&nbsp;</td>
            </tr>
            <tr>
	          <td align=left>Email Address: </td>
              <td ><input type="text" width="40" name="email"> </td>          
            </tr>
            <tr>
	          <td align=left>PDB File: </td>
              <td ><input type="file" name="upfile"> </td>
            </tr>
            <tr>
              <td colspan=2>(Input Structure File <font color=red><b>MUST</b></font> be in <a href=http://www.wwpdb.org/documentation/file-format-content/format33/v3.3.html>PDB format</a>) </td>
            </tr>
          </table>
          <br>
          <INPUT TYPE="hidden" NAME="METHOD" VALUE="SPIN">
          <INPUT TYPE="SUBMIT" VALUE="Submit">
          <INPUT TYPE="reset" VALUE="Clear">
        </form>
        <br>
        <b><a href=./data/sample_results.txt>Here</a> are example results for 3a4rA.<br></b>
        <p>
        <font color=red><b>*** The use of this server means that you have read and accepted</b></font><br>
        <a href="/Softwares-Services_files/notices.htm"> Disclaimers, Warranties, Legal Notices</a><br>
        <?php
    }

    function print_footer() {
        ?>
          </center>
          <div style="position:relative; bottom:0;">
            <hr>
            Please address questions or comments to
           <a href="mailto:james.oconnell@griffithuni.edu.au">James O'Connell</a>.
          </div>
        </body>
        </html>
        <?php
    }

    function print_progress($qid, $email) {
        ?>
        <form enctype='multipart/form-data' ACTION="index.php" METHOD="post">
        <?php
        echo "File successfully uploaded. Your results will be sent to $email ";
        echo "with the subject <b>SPIN2 Results $qid</b>. <p> Please allow a ";
        echo "few minutes, or longer, depending on server load. If you do not ";
        echo "receive an email, please check your spam folder and add ";
        echo "no-reply@sparks-lab.org to your allowed list. <p>"
        ?>
          <INPUT TYPE="SUBMIT" VALUE="Go Back">
        </form>
        <?php
    }

    function print_error() {
        // Print an error message
        ?>
        <form enctype='multipart/form-data' ACTION="index.php" METHOD="post">
          ERROR: File upload failed or invalid email address... <p>
          <INPUT TYPE="SUBMIT" VALUE="Try Again">
        </form>
        <?php
    }

    function flush2() {
    	echo(str_repeat(' ',2024));
    	// check that buffer is actually set before flushing
    	if (ob_get_length()) {
    		@ob_flush();
    		@flush();
    		@ob_end_flush();
    	}
    	@ob_start();
    }
}
?>
