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

document.getElementById("help-commit").onclick = function() {
    showModal("myModal-commit");
};
document.getElementById("help-delete").onclick = function() {
    showModal("myModal-delete");
};
document.getElementById("help-add").onclick = function() {
    showModal("myModal-add");
};
document.getElementById("help-defective").onclick = function() {
    showModal("myModal-defective");
};
// document.getElementById("help-timeFrame").onclick = function() {
//     showModal("myModal-timeFrame");
// };


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
