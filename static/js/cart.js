var cartItemNumber           = document.getElementById("cart-item-number");
var cartTotalPrice           = document.getElementById("cart-total-price");
var increaseQuantityButtons  = document.getElementsByClassName("quantity-increase");
var decreaseQuantityButtons  = document.getElementsByClassName("quantity-decrease");
var quantityValues           = document.getElementsByClassName("quantity-value");
var rowTotalPrices           = document.getElementsByClassName("row-total");


for(i = 0; i < increaseQuantityButtons.length; i++){
   
    // Set click listener
    increaseQuantityButtons[i].addEventListener('click', function(){

        var productPrice = parseFloat(this.dataset.productPrice);

        //updating quantity in the database
        updateDatabaseQuantity.call(this);

        //updating row quantity and cart item number on the UI
        quantityValues[this.id].innerHTML = parseInt(quantityValues[this.id].innerHTML) + 1;
        cartItemNumber.innerHTML = parseInt(cartItemNumber.innerHTML) + 1;

        //updating row total price on the UI 
        newPrice = parseFloat(rowTotalPrices[this.id].innerHTML) + productPrice;
        rowTotalPrices[this.id].innerHTML = formatPrice(newPrice)  + ' €';

        //updating cart total price on the UI
        cartTotalPrice.innerHTML = formatPrice(parseFloat(cartTotalPrice.innerHTML) + parseFloat(productPrice));
    })  

    decreaseQuantityButtons[i].addEventListener("click", function(){
       
        var quantity = parseInt(quantityValues[this.id].innerHTML);
        var productPrice = parseFloat(this.dataset.productPrice);

        if(quantity > 0){

            //updating quantity in the database
            updateDatabaseQuantity.call(this);

            //updating row quantity and cart item number on the UI
            quantityValues[this.id].innerHTML = quantity - 1;
            cartItemNumber.innerHTML = parseInt(cartItemNumber.innerHTML) - 1;

            //updating row total price on the UI 
            newPrice = parseFloat(rowTotalPrices[this.id].innerHTML) - parseFloat(productPrice);
            rowTotalPrices[this.id].innerHTML = formatPrice(newPrice) + ' €';

            //updating cart total price on the UI
            var totalPrice = formatPrice(parseFloat(cartTotalPrice.innerHTML) - parseFloat(productPrice));
            if(totalPrice < 0) cartTotalPrice.innerHTML = 0;
            else cartTotalPrice.innerHTML = totalPrice;
        } 
    })
    
}

function formatPrice(price){
    var remainder = price.toString().split('.');
    if(parseInt(remainder[1]) == 0) 
    return parseInt(price);
    return price = parseFloat(price.toFixed(2));
}

function updateDatabaseQuantity(){
    console.log('dataset:', this.dataset);
    var productId    = this.dataset.productId;
    var productName  = this.dataset.productName;
    var action       = this.dataset.action;

    orderUpdate(productId, productName, action);
}
