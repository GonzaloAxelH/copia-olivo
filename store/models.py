from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import SET_NULL
from django import urls

# Create your models here.
# manage.py makemigrations
# manage.py migrate

#CREANDO CLASE CLIENTE
class Cliente(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50, null=True)
    correo = models.CharField(max_length=50)
    def __str__(self):
        return self.nombre

class Categoria(models.Model):
    codigo = models.CharField(max_length=3, primary_key=True)
    nombre = models.CharField(max_length=40)
    def __str__(self):
        return self.nombre

#CREANDO CLASE PRODUCTOS
class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    categoria = models.ForeignKey(Categoria, null=False, blank=False, on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=7, decimal_places=2)
    descripcion = models.CharField(max_length=200)
    digital = models.BooleanField(default=False, null=True, blank=False)
    imagen = models.ImageField(null=True, blank=True)
    def __str__(self):
        return self.nombre
    @property
    def imagenURL(self):
        try:
            url = self.imagen.url
        except:
            url = ' '
        return url
class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, null=True, blank=True, on_delete=models.SET_NULL)
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.BooleanField(default=False, null=True, blank=False)
    id_transaccion = models.CharField(max_length=50, null=True)
    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        detallepedidos = self.detallepedido_set.all()
        for i in detallepedidos:
            if i.producto.digital == False:
                shipping = True
        return shipping

    @property
    def get_carrito_total(self):
        detallepedidos = self.detallepedido_set.all()
        total = sum([articulo.get_total for articulo in detallepedidos])
        return total

    @property
    def get_carrito_articulos(self):
        detallepedidos = self.detallepedido_set.all()
        total = sum([articulo.cantidad for articulo in detallepedidos])
        return total

    @property
    def get_carrito_articulos_name(self):
        detallepedidos = self.detallepedido_set.all()
        total = [articulo for articulo in detallepedidos]
        return total
    

class DetallePedido(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True, blank=True)
    pedido = models.ForeignKey(Pedido, on_delete=SET_NULL, null=True, blank=True)
    cantidad = models.IntegerField(default=0, null=True, blank=True)
    fec_agregado = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.producto)

    @property
    def get_total(self):
        total = self.producto.precio * self.cantidad
        return total


class Direccion(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, blank=True, null=True)
    pedido = models.ForeignKey(Pedido, on_delete=models.SET_NULL, blank=True, null=True)
    direccion = models.CharField(max_length=50, null=True)
    ciudad = models.CharField(max_length=50, null=True)
    departamento = models.CharField(max_length=50, null=True)
    codigoPostal = models.CharField(max_length=50, null=True)
    numIdentificacionFiscal = models.CharField(max_length=50, null=True)
    fec_agregado = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.direccion

#CREANDO CLASE CONTACTANOS
class Contactanos(models.Model):
    id_contactanos =  models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, null=True)
    correo = models.EmailField(max_length=254, null=True)
    numero_cel= models.CharField(max_length=50,null=True)
    
    def __str__(self):
        return ("Contacto: "+str(self.id_contactanos))

#CREANDO CLASE RESERVACIONES
class Reservacion(models.Model):
    id_reservacion =  models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, null=True)
    correo = models.EmailField(max_length=254, null=True)
    numero_cel= models.CharField(max_length=50,null=True)
    num_personas = models.IntegerField()
    fecha = models.CharField(max_length=50, null=True)
    hora = models.CharField(max_length=50, null=True)
    comida_pref = models.CharField(max_length=50, null=True)
    ocasion = models.CharField(max_length=50, null=True)

    def __str__(self):
        return ("Reservacion: "+str( self.id_reservacion))
