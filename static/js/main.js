var toastElList = [].slice.call(document.querySelectorAll('.toast'))
var toastList = toastElList.map(function (toastEl) {
  var toast = new bootstrap.Toast(toastEl);
  toast.show();
  return toast;
})


$('.dropdown').hover(function(){ 
    $('.dropdown-toggle', this).trigger('click'); 
  });


function goBack() {
    window.history.back();
  }


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