from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Cliente)
admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(Pedido)
admin.site.register(DetallePedido)
admin.site.register(Direccion)
admin.site.register(Contactanos)
admin.site.register(Reservacion)