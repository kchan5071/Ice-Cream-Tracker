
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
