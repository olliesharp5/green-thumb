function goBack() {
    window.history.back();
  }

  function incrementValue() {
    var value = parseInt(document.getElementById('quantity').value, 10);
    value = isNaN(value) ? 0 : value;
    value++;
    document.getElementById('quantity').value = value;
}

function decrementValue() {
    var value = parseInt(document.getElementById('quantity').value, 10);
    value = isNaN(value) ? 0 : value;
    value < 1 ? value = 1 : '';
    value--;
    document.getElementById('quantity').value = value;
}