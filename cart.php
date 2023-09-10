<?php
session_start();

// Function to calculate the total price of items in the cart
function calculateTotal() {
    $total = 0;
    if (isset($_SESSION['cart'])) {
        foreach ($_SESSION['cart'] as $item) {
            $total += $item['price'];
        }
    }
    return $total;
}

// Add an item to the cart
if (isset($_POST['add_to_cart'])) {
    $productId = $_POST['product_id'];
    $productName = $_POST['product_name'];
    $productPrice = $_POST['product_price'];

    $cartItem = array(
        'id' => $productId,
        'name' => $productName,
        'price' => $productPrice
    );

    if (!isset($_SESSION['cart'])) {
        $_SESSION['cart'] = array();
    }

    $_SESSION['cart'][] = $cartItem;

    header('Location: cart.php');
    exit;
}

// Remove an item from the cart
if (isset($_GET['remove_item'])) {
    $itemId = $_GET['remove_item'];

    if (isset($_SESSION['cart'][$itemId])) {
        unset($_SESSION['cart'][$itemId]);
    }

    header('Location: cart.php');
    exit;
}
?>
