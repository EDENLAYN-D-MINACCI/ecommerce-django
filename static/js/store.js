var addToCartButtons = document.getElementsByClassName("cart-add");
var removeFromCartButton = document.getElementById('cart-remove');

for(var i = 0; i < addToCartButtons.length; i++){

    addToCartButtons[i].addEventListener('click', function(){
   
        console.log('dataset:', this.dataset);
        var productId    = this.dataset.productid;
        var productName  = this.dataset.productname;
        var action       = this.dataset.action;

    
        orderUpdate(productId, productName, action);
    });
    
}



  