from django.db import models
from django.urls import reverse

from eventex.core.managers import KindQuerySet, PeriodManager


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

    objects = KindQuerySet.as_manager()

    class Meta:
        verbose_name_plural = 'contatos'
        verbose_name = 'contato'

    def __str__(self):
        return self.value


class Talk(models.Model):
    title = models.CharField('título da palestra', max_length=200)
    start = models.TimeField('hora', blank=True, null=True)
    description = models.TextField('descrição', blank=True)
    speakers = models.ManyToManyField('Speaker', verbose_name='palestrantes', blank=True)

    objects = PeriodManager()

    class Meta:
        verbose_name_plural = 'palestras'
        verbose_name = 'palestra'

    def __str__(self):
        return self.title
