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


class Contact(models.Model):
    EMAIL = 'E'
    PHONE = 'P'

    KINDS = (
        (EMAIL, 'Email'),
        (PHONE, 'Telefone'),
    )

    speaker = models.ForeignKey('Speaker', verbose_name='palestrante', on_delete=models.CASCADE)
    kind = models.CharField('tipo do contato', max_length=1, choices=KINDS)
    value = models.CharField('valor', max_length=255)

    class Meta:
        verbose_name_plural = 'contatos'
        verbose_name = 'contato'

    def __str__(self):
        return self.value
