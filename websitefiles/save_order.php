<?php
    // Path to the JSON file
    $file = 'orderData.json';

    // Get the incoming JSON data
    $json = file_get_contents('php://input');
    $newOrder = json_decode($json, true);  // Decode the new order to a PHP array

    // Check if the file already exists
    if(file_exists($file)){
        // Read existing data from the file
        $existingData = file_get_contents($file);
        $orders = json_decode($existingData, true);  // Decode the existing JSON data to a PHP array

        if (!is_array($orders)) {
            // If the file is empty or corrupt, reset to an empty array
            $orders = [];
        }
    } else {
        // If the file doesn't exist, start with an empty array
        $orders = [];
    }

    // Append the new order to the array
    $orders[] = $newOrder;

    // Encode the array back to JSON
    $jsonData = json_encode($orders, JSON_PRETTY_PRINT);  // Pretty print for readability

    // Save the updated JSON array back to the file
    if(file_put_contents($file, $jsonData)){
        echo "Order saved successfully!";
    } else {
        echo "Error saving order.";
    }
?>

