<?php
session_start();

if ($_SERVER["REQUEST_METHOD"] === "POST") {
    $productId = $_POST["product_id"];
    $productName = $_POST["product_name"];
    $productPrice = $_POST["product_price"];

    if (!isset($_SESSION["cart"])) {
        $_SESSION["cart"] = [];
    }

    // Add the product to the cart
    $_SESSION["cart"][] = [
        "id" => $productId,
        "name" => $productName,
        "price" => $productPrice
    ];

    // Redirect back to the products page with a success message
    header("Location: products.html?added_to_cart=true");
    exit;
}
?>
