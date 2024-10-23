<?php
    // Path to the JSON file
    $file = 'ticketData.json';

    // Get the incoming JSON data
    $json = file_get_contents('php://input');
    $newTicket = json_decode($json, true);  // Decode the new ticket to a PHP array

    // Check if the file already exists
    if(file_exists($file)){
        // Read existing data from the file
        $existingData = file_get_contents($file);
        $tickets = json_decode($existingData, true);  // Decode the existing JSON data to a PHP array

        if (!is_array($tickets)) {
            // If the file is empty or corrupt, reset to an empty array
            $tickets = [];
        }
    } else {
        // If the file doesn't exist, start with an empty array
        $tickets = [];
    }

    // Append the ticket to the array
    $tickets[] = $newTicket;

    // Encode the array back to JSON
    $jsonData = json_encode($tickets, JSON_PRETTY_PRINT);  // Pretty print for readability

    // Save the updated JSON array back to the file
    if(file_put_contents($file, $jsonData)){
        echo "Ticket saved successfully!";
    } else {
        echo "Error saving ticket.";
    }
?>