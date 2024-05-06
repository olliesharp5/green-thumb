function goBack() {
    window.history.back();
  }

  document.getElementById('button-plus').addEventListener('click', incrementValue);
  document.getElementById('button-minus').addEventListener('click', decrementValue);
  document.getElementById('quantity').addEventListener('change', validateQuantity);
  
  function incrementValue() {
      var value = parseInt(document.getElementById('quantity').value, 10);
      value = isNaN(value) ? 0 : value;
      if(value < 15) {
          value++;
          document.getElementById('quantity').value = value;
      }
  }
  
  function decrementValue() {
      var value = parseInt(document.getElementById('quantity').value, 10);
      value = isNaN(value) ? 0 : value;
      if(value > 1) {
          value--;
          document.getElementById('quantity').value = value;
      }
  }
  
  function validateQuantity() {
      var value = parseInt(document.getElementById('quantity').value, 10);
      if(value < 1) {
          document.getElementById('quantity').value = 1;
      } else if(value > 15) {
          document.getElementById('quantity').value = 15;
      }
  }