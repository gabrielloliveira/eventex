from django.db import models
from django.urls import reverse


class Speaker(models.Model):
    name = models.CharField('nome', max_length=255)
    slug = models.SlugField('slug')
    photo = models.URLField('link da foto')
    website = models.URLField('link do site', blank=True)
    description = models.TextField('descrição', blank=True)

    def get_absolute_url(self):
        return reverse("core:speaker-detail", kwargs={'slug': self.slug})

    class Meta:
        verbose_name_plural = 'palestrantes'
        verbose_name = 'palestrante'

    def __str__(self):
        return self.name
