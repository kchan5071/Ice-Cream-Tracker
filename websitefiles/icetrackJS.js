
// allows for the expansion of an input domain
const textarea = document.getElementById('orderDescription');
    
    textarea.addEventListener('input', function() {
      // Reset the height to auto to calculate the new height
      this.style.height = 'auto';
      // Set the height based on the scroll height (height of the content)
      this.style.height = (this.scrollHeight) + 'px';
    });

// fixes the types of numbers that can be input for the cost values
    const amountInput = document.getElementById('amount');

    // Event to ensure no more than two decimal places are entered
    amountInput.addEventListener('input', function(e) {
        let value = e.target.value;

        // If the input value has more than two decimal places
        if (value.includes('.') && value.split('.')[1].length > 2) {
        // Truncate to two decimal places
        e.target.value = parseFloat(value).toFixed(2);
        }
    });

    // Ensure value is properly formatted when focus is lost
    amountInput.addEventListener('blur', function() {
        if (this.value !== '' && !isNaN(this.value)) {
        this.value = parseFloat(this.value).toFixed(2); // Format to two decimals
        }
    });

// adds aesthetic to the dropdown menu
  function hideOptions() {
    var select = document.getElementById('fruits');
    select.style.display = 'none';  // Hide the drop-down
    // Optionally, enable the submit button if you want to allow submission after selection
    document.getElementById('submitBtn').disabled = false; 
}

// Function to handle showing modals
function showModal(modalId) {
    var modal = document.getElementById(modalId);
    modal.style.display = "block";
}

// Function to handle closing modals
function closeModal(modalId) {
    var modal = document.getElementById(modalId);
    modal.style.display = "none";
}

// Event listeners for each help button and close button
document.getElementById("help-shipping").onclick = function() {
    showModal("myModal-shipping");
};
document.getElementById("help-billing").onclick = function() {
    showModal("myModal-billing");
};

// Event listeners for closing modals
document.querySelectorAll('.close').forEach(function(element) {
    element.onclick = function() {
        var modalId = this.getAttribute('data-modal');
        closeModal(modalId);
    };
});

// Close modal when clicking outside of it
window.onclick = function(event) {
    var modals = document.querySelectorAll('.modal');
    modals.forEach(function(modal) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    });
};


// // the following controls the help button on-click pop-up
// var modal = document.getElementById("myModal");
// var btn = document.getElementById("myButton");
// var span = document.getElementsByClassName("close")[0];

// btn.onclick = function() {
//     modal.style.display = "block";
// }

// span.onclick = function() {
//     modal.style.display = "none";
// }

// window.onclick = function(event) {
//     if (event.target == modal) {
//         modal.style.display = "none";
//     }
// }