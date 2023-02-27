from django.db import models
from django.conf import settings
import os
from PIL import Image
from django.utils.text import slugify
import utils
# Create your models here.

class Produto(models.Model):
    nome = models.CharField(max_length=255)
    descricao_curta = models.TextField(max_length=255)
    descricao_longa = models.TextField()
    imagem = models.ImageField(null=True,
                               blank=True,
                               upload_to='imagens/%Y/%m/')
    slug = models.SlugField(unique=True, blank=True, null=True)
    preco = models.FloatField(verbose_name='Preço')
    preco_promocional = models.FloatField(default=0, verbose_name='Promo.')
    tipo = models.CharField(
        default='V', 
        max_length=1, 
        choices=(
            ('V', 'Variável'),
            ('S', 'Simples'),
            )
    )
    
    @staticmethod
    def resize_image(img, new_width=800):
        img_full_path = os.path.join(settings.MEDIA_ROOT, img.name)
        img_pil = Image.open(img_full_path)
        original_width, original_height = img_pil.size

        if original_width <= new_width:
            img_pil.close()
            return
        
        new_height = round((new_width * original_height) / original_width)

        print(original_width, original_height)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        max_image_size = 800

        if self.imagem:
            self.resize_image(self.imagem, max_image_size)

    def __str__(self):
        return self.nome