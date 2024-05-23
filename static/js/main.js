var toastElList = [].slice.call(document.querySelectorAll('.toast'))
var toastList = toastElList.map(function (toastEl) {
  var toast = new bootstrap.Toast(toastEl);
  toast.show();
  return toast;
})


$('.dropdown').hover(function(){ 
    $('.dropdown-toggle', this).trigger('click'); 
  });



document.addEventListener('DOMContentLoaded', function() {
    var dropdownMenuButton = document.getElementById('dropdownMenuButton');
    dropdownMenuButton.addEventListener('click', function(e) {
        e.stopPropagation();
        var dropdownMenu = dropdownMenuButton.nextElementSibling;
        dropdownMenu.classList.toggle('show');
    });
    document.addEventListener('click', function() {
        var dropdownMenu = dropdownMenuButton.nextElementSibling;
        dropdownMenu.classList.remove('show');
    });
});



function openUpdateReviewModal(reviewId, rating, title, text) {
    const updateForm = document.getElementById('updateReviewForm');
    updateForm.action = `/products/review/${reviewId}/update/`;

    // Ensure the dropdown is correctly set
    const ratingField = updateForm.querySelector('#id_rating');
    const options = ratingField.options;
    for (let i = 0; i < options.length; i++) {
        if (options[i].value === rating.toString()) {
            options[i].selected = true;
            break;
        }
    }

    updateForm.querySelector('#id_title').value = title;
    updateForm.querySelector('#id_text').value = text;
}

function openDeleteReviewModal(reviewId) {
    const deleteForm = document.getElementById('deleteReviewForm');
    deleteForm.action = `/products/review/${reviewId}/delete/`;
}




// Get all product detail links
let productDetailLinks = document.querySelectorAll('.product-detail-link');

// Add a click event listener to each link
productDetailLinks.forEach(function(link) {
    link.addEventListener('click', function() {
        // Store the current URL in the session storage
        sessionStorage.setItem('searchResultsUrl', window.location.href);
    });
});


// Functionality for plus and minus buttons to increment quantity value
function goBack() {
    let url = sessionStorage.getItem('searchResultsUrl');
    if (url) {
        window.location.href = url;
    } else {
        // Fallback to the history back method
        window.history.back();
    }
}

// Functionality for plus and minus buttons to increment quantity value
document.querySelectorAll('.btn-outline-secondary').forEach(function(button) {
    if(button.id === 'button-plus' || button.classList.contains('button-plus')) {
        button.addEventListener('click', incrementValue);
    } else if(button.id === 'button-minus' || button.classList.contains('button-minus')) {
        button.addEventListener('click', decrementValue);
    }
});

document.querySelectorAll('input[type="number"]').forEach(function(input) {
    if(input.name === 'quantity' || input.classList.contains('quantity')) {
        input.addEventListener('change', validateQuantity);
    }
});

function incrementValue(event) {
    var input = event.target.previousElementSibling;
    while(input && (input.type !== 'number' || (input.name !== 'quantity' && !input.classList.contains('quantity')))) {
        input = input.previousElementSibling;
    }
    if(input) {
        var value = parseInt(input.value, 10);
        value = isNaN(value) ? 0 : value;
        if(value < 15) {
            value++;
            input.value = value;
        }
    }
}

function decrementValue(event) {
    var input = event.target.nextElementSibling;
    while(input && (input.type !== 'number' || (input.name !== 'quantity' && !input.classList.contains('quantity')))) {
        input = input.nextElementSibling;
    }
    if(input) {
        var value = parseInt(input.value, 10);
        value = isNaN(value) ? 0 : value;
        if(value > 1) {
            value--;
            input.value = value;
        }
    }
}

function validateQuantity(event) {
    var value = parseInt(event.target.value, 10);
    if(value < 1) {
        event.target.value = 1;
    } else if(value > 15) {
        event.target.value = 15;
    }
}


// When the gardener checkbox is checked, the gardener fields will be displayed and marked as required.
// When the checkbox is not checked, the gardener fields will be removed from the form.
var gardenerElement = document.getElementById('id_gardener');
if (gardenerElement) {
    gardenerElement.onchange = function() {
        var gardenerFields = document.getElementById('gardenerFields');
        var fields = ['id_display_name', 'id_location', 'id_about'];

        if (this.checked) {
            gardenerFields.style.display = "block";
            fields.forEach(function(field) {
                var element = document.getElementById(field);
                if (element) {
                    element.removeAttribute('disabled');
                    element.setAttribute('required', 'required');
                }
            });
        } else {
            fields.forEach(function(field) {
                var element = document.getElementById(field);
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
