// Initialize all toast elements on the page and show them using Bootstrap's Toast component
let toastElList = [].slice.call(document.querySelectorAll('.toast'));
let toastList = toastElList.map(function (toastEl) {
  let toast = new bootstrap.Toast(toastEl);
  toast.show();
  return toast;
});

// Add hover functionality to dropdowns to trigger click event on the dropdown toggle
$('.dropdown').hover(function() {
  $('.dropdown-toggle', this).trigger('click');
});

// Event listener for when the document content is fully loaded
document.addEventListener('DOMContentLoaded', function() {
    let dropdownMenuButton = document.getElementById('dropdownMenuButton');
    
    // Toggle the visibility of the dropdown menu on button click
    dropdownMenuButton.addEventListener('click', function(e) {
        e.stopPropagation();
        let dropdownMenu = dropdownMenuButton.nextElementSibling;
        dropdownMenu.classList.toggle('show');
    });
    
    // Hide the dropdown menu when clicking anywhere else on the document
    document.addEventListener('click', function() {
        let dropdownMenu = dropdownMenuButton.nextElementSibling;
        dropdownMenu.classList.remove('show');
    });
});

// Function to open the update review modal with pre-filled form fields
function openUpdateReviewModal(reviewId, rating, title, text) {
    const updateForm = document.getElementById('updateReviewForm');
    updateForm.action = `/products/review/${reviewId}/update/`;

    // Set the rating field correctly
    const ratingField = updateForm.querySelector('#id_rating');
    const options = ratingField.options;
    for (let i = 0; i < options.length; i++) {
        if (options[i].value === rating.toString()) {
            options[i].selected = true;
            break;
        }
    }

    // Set the title and text fields with the provided values
    updateForm.querySelector('#id_title').value = title;
    updateForm.querySelector('#id_text').value = text;
}

// Function to open the delete review modal with the correct action URL
function openDeleteReviewModal(reviewId) {
    const deleteForm = document.getElementById('deleteReviewForm');
    deleteForm.action = `/products/review/${reviewId}/delete/`;
}

// Get all product detail links and add a click event listener to each
let productDetailLinks = document.querySelectorAll('.product-detail-link');
productDetailLinks.forEach(function(link) {
    link.addEventListener('click', function() {
        // Store the current URL in the session storage
        sessionStorage.setItem('searchResultsUrl', window.location.href);
    });
});

// Function to go back to the previous page or to a stored URL
function goBack() {
    let url = sessionStorage.getItem('searchResultsUrl');
    if (url) {
        window.location.href = url;
    } else {
        // Fallback to the history back method
        window.history.back();
    }
}

// Add event listeners to plus and minus buttons to increment/decrement quantity value
document.querySelectorAll('.btn-outline-secondary').forEach(function(button) {
    if (button.id === 'button-plus' || button.classList.contains('button-plus')) {
        button.addEventListener('click', incrementValue);
    } else if (button.id === 'button-minus' || button.classList.contains('button-minus')) {
        button.addEventListener('click', decrementValue);
    }
});

// Add event listener to quantity input fields to validate the quantity
document.querySelectorAll('input[type="number"]').forEach(function(input) {
    if (input.name === 'quantity' || input.classList.contains('quantity')) {
        input.addEventListener('change', validateQuantity);
    }
});

// Increment the quantity value, ensuring it doesn't exceed 15
function incrementValue(event) {
    let input = event.target.previousElementSibling;
    while (input && (input.type !== 'number' || (input.name !== 'quantity' && !input.classList.contains('quantity')))) {
        input = input.previousElementSibling;
    }
    if (input) {
        let value = parseInt(input.value, 10);
        value = isNaN(value) ? 0 : value;
        if (value < 15) {
            value++;
            input.value = value;
        }
    }
}

// Decrement the quantity value, ensuring it doesn't go below 1
function decrementValue(event) {
    let input = event.target.nextElementSibling;
    while (input && (input.type !== 'number' || (input.name !== 'quantity' && !input.classList.contains('quantity')))) {
        input = input.nextElementSibling;
    }
    if (input) {
        let value = parseInt(input.value, 10);
        value = isNaN(value) ? 0 : value;
        if (value > 1) {
            value--;
            input.value = value;
        }
    }
}

// Validate the quantity input value to be within the range of 1 to 15
function validateQuantity(event) {
    let value = parseInt(event.target.value, 10);
    if (value < 1) {
        event.target.value = 1;
    } else if (value > 15) {
        event.target.value = 15;
    }
}

// Manage the display and requirement status of gardener fields based on the gardener checkbox
let gardenerElement = document.getElementById('id_gardener');
if (gardenerElement) {
    gardenerElement.onchange = function() {
        let gardenerFields = document.getElementById('gardenerFields');
        let fields = ['id_display_name', 'id_location', 'id_about'];

        if (this.checked) {
            gardenerFields.style.display = "block";
            fields.forEach(function(field) {
                let element = document.getElementById(field);
                if (element) {
                    element.removeAttribute('disabled');
                    element.setAttribute('required', 'required');
                }
            });
        } else {
            fields.forEach(function(field) {
                let element = document.getElementById(field);
                if (element) {
                    element.setAttribute('disabled', 'disabled');
                    element.removeAttribute('required');
                }
            });
            gardenerFields.style.display = "none";
        }
    };

    // Trigger the change event to set the initial state correctly on page load
    gardenerElement.onchange();
}
