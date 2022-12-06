var updateBtns = document.getElementsByClassName('update-cart')

for (i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener('click', function(){
		var productoId = this.dataset.producto
		var action = this.dataset.action
		console.log('productoId:', productoId, 'Action:', action)
		console.log('USER:', user)

		if (user == 'AnonymousUser'){
			addCookieItem(productoId, action)
		}else{
			updateUserPedido(productoId, action)
		}
	})
}

function addCookieItem(productoId, action){
	console.log('User is not authenticated')

	if (action == 'add'){
		if (cart[productoId] == undefined){
		cart[productoId] = {'quantity':1}

		}else{
			cart[productoId]['quantity'] += 1
		}
	}

	if (action == 'remove'){
		cart[productoId]['quantity'] -= 1

		if (cart[productoId]['quantity'] <= 0){
			console.log('Item should be deleted')
			delete cart[productoId];
		}
	}
	console.log('CART:', cart)
	document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
	location.reload()
}

function updateUserPedido(productoId, action){
	console.log('User is authenticated, sending data...')

	var url = '/update_articulo/'

	fetch(url, {
		method:'POST',
		headers:{
			'Content-Type':'application/json',
			'X-CSRFToken':csrftoken,
		}, 
		body:JSON.stringify({'productoId':productoId, 'action':action}),
	})
	.then((response) => {
	   return response.json();
	})
	.then((data) => {
		console.log('Data:', data)
		location.reload()
	});
}