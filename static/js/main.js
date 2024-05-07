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
  

  document.querySelectorAll('.button-plus').forEach(function(button) {
    button.addEventListener('click', incrementValue);
});

document.querySelectorAll('.button-minus').forEach(function(button) {
    button.addEventListener('click', decrementValue);
});

document.querySelectorAll('.quantity').forEach(function(input) {
    input.addEventListener('change', validateQuantity);
});

function incrementValue(event) {
    var input = event.target.previousElementSibling;
    var value = parseInt(input.value, 10);
    value = isNaN(value) ? 0 : value;
    if(value < 15) {
        value++;
        input.value = value;
    }
}

function decrementValue(event) {
    var input = event.target.nextElementSibling;
    var value = parseInt(input.value, 10);
    value = isNaN(value) ? 0 : value;
    if(value > 1) {
        value--;
        input.value = value;
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