<?php
if ($_SERVER["REQUEST_METHOD"] === "POST") {
    // Get the submitted email from the form
    $email = $_POST["email"];

    // Validate the email (you can add more robust validation here)
    if (filter_var($email, FILTER_VALIDATE_EMAIL)) {
        // Save the email to a file or database (this is just a simple example)
        $file = "subscribed_emails.txt";
        file_put_contents($file, $email . PHP_EOL, FILE_APPEND);

        // You can also send a confirmation email to the subscriber here

        // Redirect the user back to the form page with a success message
        header("Location: index.html?success=true");
        exit;
    } else {
        // Redirect the user back to the form page with an error message
        header("Location: index.html?success=false");
        exit;
    }
} else {
    // Redirect if the form is accessed directly without submission
    header("Location: index.html");
    exit;
}
?>
