from django.db import models

# Create your models here.

class Article(models.Model):
    title = models.CharField(max_length=150, verbose_name='Título')
    content = models.TextField(verbose_name='Contenido')
    image = models.ImageField(default='null', verbose_name='Imagen', upload_to="articles")
    public = models.BooleanField(verbose_name='¿Publicado?')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        #poner nombre en singular
        verbose_name = 'Artículo'
        verbose_name_plural = 'Artículos'
        
        def __str__(self):
            if self.public:
                public = '(publicado)'
            else:
                public = '(privado)'
            return f"{self.title} {public}"

class Category(models.Model): #Entidad
    name = models.CharField(max_length=110)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        #poner nombre en singular
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'