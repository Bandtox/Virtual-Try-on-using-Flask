<?php
if ($_SERVER["REQUEST_METHOD"] === "POST") {
    // Get the submitted form data
    $name = $_POST["name"];
    $email = $_POST["email"];
    $message = $_POST["message"];

    // Validate data (you can add more validation here)
    if (!empty($name) && filter_var($email, FILTER_VALIDATE_EMAIL) && !empty($message)) {
        // Send an email with the contact information (this is just a simple example)
        $to = "your@email.com"; // Replace with the actual email address to receive the messages
        $subject = "New Contact Form Submission";
        $messageBody = "Name: $name\nEmail: $email\nMessage: $message";
        $headers = "From: $email";

        mail($to, $subject, $messageBody, $headers);

        // Redirect the user back to the form page with a success message
        header("Location: contacts.html?success=true");
        exit;
    } else {
        // Redirect the user back to the form page with an error message
        header("Location: contacts.html?success=false");
        exit;
    }
} else {
    // Redirect if the form is accessed directly without submission
    header("Location: contacts.html");
    exit;
}
?>
