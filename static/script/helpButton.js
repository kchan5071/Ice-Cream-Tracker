// Help button javascript for the ice track order entry page

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
document.getElementById("help-flavor").onclick = function() {
    showModal("myModal-flavor");
};
document.getElementById("help-size").onclick = function() {
    showModal("myModal-size");
};
document.getElementById("help-size").onclick = function() {
    showModal("myModal-size");
};
document.getElementById("help-quantity").onclick = function() {
    showModal("myModal-quantity");
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

