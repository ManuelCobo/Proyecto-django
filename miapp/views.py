from django.shortcuts import render, HttpResponse, redirect
from miapp.models import Article, Category

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

def crear_articulo(request):
    articulo = Article(
        title = 'primer articulo',
        content = 'contenido del primer articulo',
        public = True
)
    articulo.save()
    return HttpResponse("articulo creado: ")