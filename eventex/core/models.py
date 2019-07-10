from django.db import models
from django.shortcuts import resolve_url as r

from eventex.core.managers import KindQuerySet, PeriodManager


class Speaker(models.Model):
    name = models.CharField('nome', max_length=255)
    slug = models.SlugField('slug')
    photo = models.URLField('foto')
    website = models.URLField('website', blank=True)
    description = models.TextField('descrição', blank=True)

    class Meta:
        verbose_name = 'palestrante'
        verbose_name_plural = 'palestrantes'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return r('speaker_detail', slug=self.slug)


class Contact(models.Model):
    EMAIL = 'e'
    PHONE = 'p'
    KINDS = (
        (EMAIL, 'email'),
        (PHONE, 'telefone')
    )
    speaker = models.ForeignKey(
        'Speaker',
        on_delete=models.CASCADE,
        verbose_name='palestrante'
    )
    kind = models.CharField('tipo', max_length=1, choices=KINDS)
    value = models.CharField('valor', max_length=255)
    objects = KindQuerySet.as_manager()

    class Meta:
        verbose_name = 'contato'
        verbose_name_plural = 'contatos'

    def __str__(self):
        return self.value


class Activitiy(models.Model):
    title = models.CharField('título', max_length=200)
    start = models.TimeField('início', blank=True, null=True)
    description = models.TextField('descrição', blank=True)
    speakers = models.ManyToManyField(
        'Speaker',
        verbose_name='palestrantes',
        blank=True
    )
    objects = PeriodManager()

    class Meta:
        abstract = True
        verbose_name = 'palestra'
        verbose_name_plural = 'palestras'

    def __str__(self):
        return self.title


class Talk(Activitiy):
    pass


class Course(Activitiy):
    slots = models.IntegerField('participantes')

    class Meta:
        verbose_name = 'curso'
        verbose_name_plural = 'cursos'
