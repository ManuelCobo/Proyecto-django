from django.shortcuts import render, HttpResponse, redirect
from miapp.models import Article, Category
from miapp.forms import FormArticle #Importamos el formulario desde forms.py
from django.contrib import messages #libreria mensajes flash

# Create your views here.
# MVC = Modelo Vista Controlador --> Acciones (metodos)
# MVT = Modelo template Vista --> Acciodnes (metodos)

layout = """
<h1>Sitio web con  Django | ADSO SENA</h1>
<hr/>
<ul>
    <li>
        <a href="/inicio">Inicio</a>
    </li> 
    <li>
            <a href="/hola-mundo">Hola mundo</a>
    </li> 
    <li>
            <a href="/pagina-pruebas">Pagina de pruebas</a>
    </li> 
    <li>
            <a href="/contacto">contacto</a>
    </li> 
</ul>   
<hr/>        
"""

def index(request):
    
    html = """
            <h1>Inicio</h1>
            <p>Años hasta el 2050:</p>
            <ul>          
    """
    year = 2024
    while year <= 2050:
        if year % 2 == 0:
            html += f"<li>{str(year)}</li>"
        year += 1
        
    html += "</ul>"
    
    nombre = "manuel cobo"
    lenguajes = ['python', 'java', 'javascript', 'c#', 'php']
    
    return render(request, "index.html", {
        'title': 'Inicio',
        'mi_variable': 'soy un dato que esta en la vista ',
        'nombre': nombre,
        'lenguajes': lenguajes,
    })      
    
def hola_mundo(request):
    return render(request, "hola_mundo.html")
    
def pagina(request, redirigir = 0):
    if redirigir == 1:
        return redirect('/inicio/')
    
    return render(request, "pagina.html")
    
def contacto(request, nombre="", apellidos=""):
    html = ""
    
    if nombre and apellidos:
        html += "<p>El nombre completo es: </p>"
        html += f"<h3>{nombre} {apellidos}</h3>"
    
    return HttpResponse(layout + f"<h2>Contacto</h2>"+html)

def crear_articulo(request, title, content, public):
    articulo = Article(
        title = title,
        content = content,
        public = public
    )
    articulo.save()
    return HttpResponse(f"articulo creado: <strong>{articulo.title}</strong> - {articulo.content}")

def articulos(request):
    try:
        articulos = Article.objects.get(title= "matrix", public = True)
        response = f"Articulo: <br />{articulos.id}. {articulos.title} "
    except:
        response = "<h1>Articulo no encontrado</h1>"
        
    return HttpResponse(response)

def editar_articulo(request, id):
    articulo = Article.objects.get(pk=id)
    articulo.title = "batman"
    articulo.content = "pelicula del 2015"
    articulo.public = True
    articulo.save()
    
    return HttpResponse(f"Articulo {articulo.id} actualizado: <strong>{articulo.title}</strong> - {articulo.content}")

def articulos(request):
    
    articulos = Article.objects.all()
    
    articulos = Article.objects.filter(title__exact = "articulo")
    
    articulos = Article.objects.filter(
                                title="Articulo", 
                                ).exclude(
                                    public=True
                                    )
                                
    articulos = Article.objects.raw('SELECT * FROM miapp_article WHERE title = "Articulo" and public = 0')
    
    return render(request, "articulos.html", {
        'articulos': articulos
    })
def borrar_articulo(request, id):
    articulo = Article.objects.get(pk=id)
    articulo.delete()
    
    return redirect('articulos')

# Copia de crear_articulo y lo llamamos save_articulo
# Copia de crear_articulo y lo llamamos save_articulo
def save_article(request): # No pasamos parametros por url y lo vamos a pasar por formulario
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        public = request.POST['public']
        articulo = Article(
            title = title, #title(nombre del modelo) = title(nombre de la variable)
            content = content,
            public = public
        )
        #Para guardar este articulo en la BD
        articulo.save()
        return HttpResponse(f"Artículo creado: <strong>{articulo.title}</strong> - {articulo.content}")
    else:
        return HttpResponse(f"<h2> No se ha podido crear el articulo </h2>")


def create_article(request): #soporte para plantilla para visualizar el formulario
    return render(request, 'create_article.html')   
#Mostrar artículos
def create_full_article(request):
    #Realizamos la comprobacion del metodo (POST-GET)
    if request.method == 'POST':
        #si llega datos por POST se debe:
        formulario = FormArticle(request.POST)
        #aqui podemos validar el formulario con un metodo is_valid
        if formulario.is_valid():
            #generamos una variable para recoger los datos del formulario
            data_form = formulario.cleaned_data #que son los datos limpios que nos llegan
            title = data_form.get('title') #lo puedo hacer asi ó
            content = data_form.get('content') # lo puedo hacer asi
            public = data_form.get('public')
            
            articulo = Article(
                title = title, #title(nombre del modelo) = title(nombre de la variable)
                content = content,
                public = public
            )
            #Para guardar este articulo en la BD
            articulo.save()
            
            #Crear mensaje flash(sesión que solo se muestra 1 vez)
            messages.success(request, f'Ha creado correctamente el articulo {articulo.id}')
            
            #rediccionar la pagina a articulos despues de guardado
            return redirect('articulos')
    else:
        #si nos llegan datos por POST debemos generar un formulario vacio
        formulario = FormArticle() #creamos una variable llamada formulario para instanciar el objeto
    
    #se carga la vista en html
    return render(request, 'create_full_article.html', {
        'form' : formulario
    })
def articulos(request): #creacion de la vista articulos
    #Creamos una template para listar varos articulos
    #1. hacemos la peticion a la base de datos
    #Creamos la variable articulos y Llamamos al modelo Article, usamos objects para porder hacer una consulta
    articulos = Article.objects.all().order_by('-id') #En este caso no usamos el metodo get si no el metodo all()
    #para sacar toda la información
    #dentro de articulos tenemos una lista de objetos un array de objetos
    """
    #Consultas con condiciones filter para filtrar por un valor especifico
    articulos = Article.objects.filter(title_contains = "Tiburón")
    
    #Realizar una consulta que muestre solo los esten publicados y excluya bajo una condición
    articulos = Article.objects.filter(title = "Tiburón",).exclude(public=True)
    
    #Consulta ejecutando SQL
    articulos = Article.objects.raw("SELECT * FROM miapp_articulo WHERE title='Tiburón' AND public=1")

    #Consulta utilizando el ORM con Q
    articulos = Article.objects.filter(
        Q(title_contains="John") | Q(title_contains="Señor")
    )
    """
    return render(request, 'articulos.html', {
        'articulos' : articulos #pasamos el request, 'articulos.html' y como tercer parametro 'articulos' : articulos pasamos un diccionario con las variables que deseamos mostrar
    })