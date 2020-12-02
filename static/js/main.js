var SUCCESS = 1;
var FAILURE = -1;

function orderValidationSnackbar(state) {
    // Set snackbar DIV content
    if(state == SUCCESS) showSnackbar("transaction succeed, an email will be sent")
    else if(state == FAILURE) showSnackbar("error: transaction canceled")
}

function showSnackbar(message) {
    // Get the snackbar DIV
    var x = document.getElementById("snackbar");
    
    // Set snackbar DIV content
    x.innerHTML = message;

    // Add the "show" class to DIV
    x.className = "show";
  
    // After 3 seconds, remove the show class from DIV
    setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);

    console.log('showing snackbar');
}

// If the length of the element's string is 0 then display helper message 
function required(inputtx) 
{
  if (inputtx.value.length == 0)
   { 
      alert("message");  	
      return false; 
   }  	
   return true; 
 } 

 
function orderUpdate(productId, productName, action){
    console.log('add to cart: sending data..');
    var message = "";
    if(action == "add") message = productName + " added to cart";
    else message = productName + " removed from cart";

    fetch('/order-update/', 
    {
        method:'POST',
        headers:{'Content-Type':'application/json', 'X-CSRFToken':csrftoken},
        body:JSON.stringify({'productId':productId, 'action':action})
    })
    .then(response =>{
        if (response.ok){
          console.log('Success:', response);
          showSnackbar(message);
          return response.json();
        } 
        else showSnackbar("An error occurs, try again")
        
    })
    .catch((error) => {
        console.log(error)
    });
}