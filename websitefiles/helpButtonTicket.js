// Help button javascript for the ice track shipment page

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

// Event listeners for each help button and close button (in order of appearance)
document.getElementById("help-todaysDate").onclick = function() {
    showModal("myModal-todaysDate");
};
document.getElementById("help-sourceName").onclick = function() {
    showModal("myModal-sourceName");
};
document.getElementById("help-detectionDate").onclick = function() {
    showModal("myModal-detectionDate");
};
document.getElementById("help-problemType").onclick = function() {
    showModal("myModal-problemType");
};
document.getElementById("help-description").onclick = function() {
    showModal("myModal-description");
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