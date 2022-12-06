from django.http import request
from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
import datetime

from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from .models import *
from .utils import cookieCart, cartData, guestOrden
from django.db.models import Q

from django.http import HttpResponse
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
# Create your views here.

def store_view(request):
	data=cartData(request)
	carritoItems=data['carritoItems']
	productos = Producto.objects.all()
	
	
	context ={'productos':productos,'carritoItems':carritoItems}
	return render(request, 'index.html',context)

def contact_us(request):
	data=cartData(request)
	carritoItems=data['carritoItems']
	productos = Producto.objects.all()
	if request.method == "POST":
		nombre = request.POST["nombre"]
		correo = request.POST["correo"]
		celular = request.POST["celular"]

		template = render_to_string('email_template.html',{
			'nombre':nombre,
			'correo':correo,
			'celular':celular
		})
		email=EmailMessage("Mensaje de app Django",
            template, 
            settings.EMAIL_HOST_USER,
            ["contact.restaurantolivo@gmail.com"])
		email.fail_silently = False
		email.send()

		obj = Contactanos(nombre=nombre, correo=correo,numero_cel=celular)
		obj.save()
		
		messages.success(request,'Se ha enviado tu correo.')
		mensaje=("Se ha enviado correctamente al correo")
		context ={'productos':productos,'carritoItems':carritoItems,'mensaje':mensaje}
		return render(request,'contact_us.html',context)
		


	context ={'productos':productos,'carritoItems':carritoItems}
	return render(request, 'contact_us.html',context)

def menu(request):
	data=cartData(request)
	carritoItems=data['carritoItems']
	productos_segundos = Producto.objects.filter(categoria="001")
	productos_caldos = Producto.objects.filter(categoria="004")
	productos_postres = Producto.objects.filter(categoria="003")
	productos_bebidas = Producto.objects.filter(categoria="002")
	context = {'productos':productos_segundos, 'productos2':productos_caldos, 'productos3':productos_postres, 'productos4':productos_bebidas,'carritoItems':carritoItems}
	return render(request, 'menu.html', context)

def about_us(request):
	data=cartData(request)
	carritoItems=data['carritoItems']
	productos = Producto.objects.all()
	
	context ={'productos':productos,'carritoItems':carritoItems}
	return render(request, 'about_us.html', context)

def reservation(request):
	data=cartData(request)
	carritoItems=data['carritoItems']
	productos = Producto.objects.all()
	if request.method == "POST":
		nombre = request.POST["nombre"]
		correo = request.POST["correo"]
		celular = request.POST["celular"]
		num_personas = request.POST["num_personas"]
		fecha = request.POST["fecha"]
		hora = request.POST["hora"]
		comida_pref = request.POST["comida_pref"]
		ocasion = request.POST["ocasion"]

		template = render_to_string('email_template2.html',{
			'nombre':nombre,
			'correo':correo,
			'celular':celular,
			'num_personas':num_personas,
			'fecha':fecha,
			'hora':hora,
			'comida_pref':comida_pref,
			'ocasion':ocasion
		})
		email=EmailMessage("Mensaje de app Django",
            template, 
            settings.EMAIL_HOST_USER,
            ["contact.restaurantolivo@gmail.com"])
		email.fail_silently = False
		email.send()

		obj = Reservacion(nombre=nombre, correo=correo,numero_cel=celular,num_personas=num_personas,fecha=fecha,hora=hora,comida_pref=comida_pref, ocasion= ocasion)
		obj.save()

		messages.success(request,'Se ha enviado tu correo.')
		mensaje=("Se ha enviado correctamente al correo")

		context ={'productos':productos,'carritoItems':carritoItems,'mensaje':mensaje}
		return render(request, 'reservation.html', context)
	
	context ={'productos':productos,'carritoItems':carritoItems}
	return render(request, 'reservation.html', context)


def carrito(request):
	data = cartData(request)
	carritoItems = data['carritoItems']
	pedido = data['pedido']
	articulos = data['articulos']

	context = {'articulos':articulos, 'pedido':pedido, 'carritoItems':carritoItems}
	return render(request, 'carrito2.html', context)

def ver_pedido(request):
	data = cartData(request)
	carritoItems = data['carritoItems']
	pedido = data['pedido']
	articulos = data['articulos']

	context = {'articulos':articulos, 'pedido':pedido, 'carritoItems':carritoItems}
	return render(request, 'ver_pedido.html', context)

@login_required(login_url='login')
def pago(request):
	data = cartData(request)
	carritoItems = data['carritoItems']
	pedido = data['pedido']
	articulos = data['articulos']

	context = {'articulos': articulos, 'pedido': pedido, 'carritoItems':carritoItems}
	return render(request, 'pago.html', context)

def perfil(request):
	data = cartData(request)
	carritoItems = data['carritoItems']
	pedidos = request.user.cliente.pedido_set.all()
	context = {'carritoItems':carritoItems,'pedidos':pedidos}
	return render(request, 'perfil.html', context)

#Funciones de registro y logueo

def loginForm(request):

	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		
		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('Index')
		else:
			messages.info(request, 'Usuario o contraseña son incorrectos')

	context = {}
	return render(request, 'login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('Index')


def registro(request):
	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user=form.save()
			username = form.cleaned_data.get('username')
			group = Group.objects.get(name='clientes')
			user.groups.add(group)
			Cliente.objects.create(
				user=user,
				nombre=username,
			)
			
			messages.success(request, 'La cuenta fue creada para '+ username)
			return redirect('login')

	context = {'form':form}
	return render(request, 'registro.html', context)
	

def updateArticulo(request):
	data = json.loads(request.body)
	productoId = data['productoId']
	action = data['action']

	print('Action:', action)
	print('productoId:', productoId)

	cliente = request.user.cliente
	producto = Producto.objects.get(id_producto=productoId)
	pedido, created = Pedido.objects.get_or_create(cliente= cliente, estado = False)

	detallepedido, created = DetallePedido.objects.get_or_create(pedido=pedido, producto=producto)

	if action == 'add':
		detallepedido.cantidad =(detallepedido.cantidad + 1)
	elif action == 'remove':
		detallepedido.cantidad = (detallepedido.cantidad -1)

	detallepedido.save()

	if detallepedido.cantidad <= 0:
		detallepedido.delete()

	return JsonResponse('Articulo fue agregado', safe=False)

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt

def procesoPedido(request):
	id_transaccion = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		cliente = request.user.cliente
		pedido, created = Pedido.objects.get_or_create(cliente= cliente, estado = False)
	
	else:
		cliente, pedido = guestOrden(request, data)

	total=float(data['form']['total'])
	pedido.id_transaccion = id_transaccion

	if total == float(pedido.get_carrito_total):
		pedido.estado = True
	pedido.save()

	

	return JsonResponse('Payment submitted', safe=False)
