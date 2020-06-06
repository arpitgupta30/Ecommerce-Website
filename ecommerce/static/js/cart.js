var updateBtns = document.getElementsByClassName("update-cart")

for(var i=0;i<updateBtns.length;i++){
    updateBtns[i].addEventListener('click', function(){
        var productId = this.dataset.product
        var action = this.dataset.action

        console.log("Product-id", productId, "Action ", action)

        if (user === "AnonymousUser"){
            addCookieItem(productId, action)
        }
        else{
            updateUserItem(productId, action)
        }
    })

}

function addCookieItem(productId, action){
    console.log("Anonymous User.....")

    if (action == 'add'){
        if(cart[productId] == undefined){
            cart[productId] = {'quantity': 1}
        }
        else{
            cart[productId]['quantity']+=1
        }
    }
    
    if (action == 'remove'){
        cart[productId]['quantity']-=1
        if(cart[productId]['quantity']<=0){
            delete cart[productId]
        }
    }
    console.log("Cart: ", cart)
    document.cookie = 'cart='+JSON.stringify(cart)+";domain=;path=/"
    location.reload()
}



function updateUserItem(productId, action){

    console.log("User Logged In.....Sending data")
    var url = '/update_item/'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type':'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({'productId': productId, 'action': action})
    })
 
    .then((response)=>{
        return response.json()
    })

    .then((data)=>{
        console.log('Data', data)
        location.reload()
    })

}