import json
from.models import *

def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
		
    print('Cart:', cart)

    articulos = []
    pedido = {'get_carrito_total':0, 'get_carrito_articulos':0, 'shipping':False}
    carritoItems = pedido['get_carrito_articulos']

    for i in cart:
        try:
            carritoItems += cart[i]['quantity']
            producto = Producto.objects.get(id_producto=i)
            total = (producto.precio*cart[i]['quantity'])
            pedido['get_carrito_total'] += total
            pedido['get_carrito_articulos'] += cart[i]['quantity']

            articulo = {
				'producto':{
				    'id_producto':producto.id_producto,
				    'nombre':producto.nombre,
				    'precio':producto.precio,
				    'imagenURL':producto.imagenURL,
			        },
		        'cantidad':cart[i]['quantity'],
		        'get_total':total,
			    }
            articulos.append(articulo)
            if producto.digital == False:
                pedido['shipping']=True
        except:
                pass

    return {'carritoItems': carritoItems, 'pedido': pedido, 'articulos':articulos}

def cartData(request):
    if request.user.is_authenticated:
        cliente = request.user.cliente
        pedido, created = Pedido.objects.get_or_create(cliente=cliente, estado=False )
        articulos = pedido.detallepedido_set.all()
        carritoItems = pedido.get_carrito_articulos
    else:
        cookieData = cookieCart(request)
        carritoItems = cookieData['carritoItems']
        pedido = cookieData['pedido']
        articulos = cookieData['articulos']
    return{'carritoItems': carritoItems, 'pedido': pedido, 'articulos':articulos}

def guestOrden(request, data):
    print('Usuario no logueado...')
    print('COOKIES:',request.COOKIES)

    nombre = data['form']['nombre']
    correo = data['form']['email']

    cookieData = cookieCart(request)
    articulos = cookieData['articulos']

    cliente, created = Cliente.objects.get_or_create(
		correo=correo,
	)
    cliente.nombre = nombre
    cliente.save()

    pedido = Pedido.objects.create(
		cliente=cliente,
		estado=False
	)
    for articulo in articulos:
        producto = Producto.objects.get(id_producto=articulo['producto']['id_producto'])
        detallePedido = DetallePedido.objects.create(
            producto=producto,
            pedido = pedido,
            cantidad = articulo['cantidad']
		)

    return cliente, pedido
