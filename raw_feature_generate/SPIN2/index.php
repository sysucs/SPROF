<?php
    // Load some functions
    include "misc.php";

    // Let James delete all the temporary files
    // system("chmod -R a+rw ./results/*");

    // Print HTML header
    print_header();

    // Data submitted?
    if (empty($_POST["METHOD"])) {
        // No
        print_main();
        print_footer();
    } else { //Yes
        // Check that upload worked
        if (!empty($_FILES["upfile"]["tmp_name"]) && filter_var($_POST["email"], FILTER_VALIDATE_EMAIL)) {

            // Generate a query ID
        	$qid = chop(shell_exec("bin/mkdir_uniq"));

            // Print some progress
            print_progress($qid, $_POST["email"]);
            print_footer();
            ob_flush();
            flush2();

            // Run the predictor
            $qfname = $_FILES['upfile']['tmp_name'];
            $ufname = $_FILES['upfile']['name'];
            system("./process_pdb.sh $qfname $qid");

            // Email the results
            if (file_exists("./results/$qid/results.txt")) {
                // Generate email header
                $header  = "From:no-reply@sparks-lab.org\r\n";
                $header .= "MIME-Version: 1.0\r\n";
                $header .= "Content-type: text/html\r\n";
                $header .= "Content-Disposition: inline\r\n";

                $message  = "<html><body><pre style='font:monospace'>\n";
                $message .= file_get_contents("./results/$qid/results.txt");
                $message .= "</pre></body></html>\n";

                // Email predictions
                mail($_POST["email"], "SPIN2 Results $qid", $message, $header);

                // Clean up files
                system("rm -r ./results/$qid");
            } else {
                // Copy file to failed folder
                copy($qfname, "./results/failed_pdb/$qid");
                system("chmod a+w ./results/failed_pdb/$qid");

                // Clean up files
                system("rm -r ./results/$qid");

                // Generate email header
                $header   = "From:no-reply@sparks-lab.org\r\n";
                $header  .= "Reply-To:james.oconnell@griffithuni.edu.au\r\n";
                $header  .= "MIME-Version: 1.0\r\n";
                $header  .= "Content-type: text/plain\r\n";

                $message  = "Processing failed for your file:\n\n";
                $message .= "    $ufname\n\n";
                $message .= "Please contact james.oconnell@griffithuni.edu.au\n";
                $message .= "by replying to this message with the relevant\n";
                $message .= "PDB file attached.\n";

                // Send an error message
                mail($_POST["email"], "SPIN2 ERROR $qid", $message, $header);
            }
        } else {
            print_error();
            print_footer();
        }
    }
?>
