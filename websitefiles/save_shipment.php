<?php
    // Path to the JSON file
    $file = 'shipmentData.json';

    // Get the incoming JSON data
    $json = file_get_contents('php://input');
    $newShipment = json_decode($json, true);  // Decode the new shipment to a PHP array

    // Check if the file already exists
    if(file_exists($file)){
        // Read existing data from the file
        $existingData = file_get_contents($file);
        $Shipments = json_decode($existingData, true);  // Decode the existing JSON data to a PHP array

        if (!is_array($shipments)) {
            // If the file is empty or corrupt, reset to an empty array
            $shipments = [];
        }
    } else {
        // If the file doesn't exist, start with an empty array
        $shipments = [];
    }

    // Append the new shipment to the array
    $shipments[] = $newShipment;

    // Encode the array back to JSON
    $jsonData = json_encode($shiments, JSON_PRETTY_PRINT);  // Pretty print for readability

    // Save the updated JSON array back to the file
    if(file_put_contents($file, $jsonData)){
        echo "Shipment saved successfully!";
    } else {
        echo "Error saving shipment.";
    }
?>