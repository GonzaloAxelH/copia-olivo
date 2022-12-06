from django.urls import path
from . import views

urlpatterns = [
    path('', views.store_view, name='Index'),
    path('contact_us/',views.contact_us, name='contact_us'),
    path('menu/', views.menu, name='menu'),
    path('reservation/',views.reservation, name='reservation'),
    path('about_us/',views.about_us, name='about_us'),
    path('carrito/', views.carrito, name="carrito"),
    path('pago/', views.pago, name="pago"),

    path('login/', views.loginForm, name="login"),
	path('logout/', views.logoutUser, name="logout"),
	path('registro/', views.registro, name="registro"),

	path('perfil/', views.perfil, name="perfil"),
    path('ver_pedido/', views.ver_pedido, name="ver_pedido"),

	path('update_articulo/', views.updateArticulo, name="update_articulo"),
	path('proceso_pedido/', views.procesoPedido, name="proceso_pedido"),
]