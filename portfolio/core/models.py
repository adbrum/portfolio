from django.db import models


class Email(models.Model):
    name = models.CharField('nome', max_length=100)
    email = models.EmailField('e-mail', blank=True)
    phone = models.CharField('telefone', max_length=20, blank=True)
    created_at = models.DateTimeField('criado em', auto_now_add=True)
    message = models.TextField('mensagem', max_length=255)

    class Meta:
        verbose_name_plural = 'emails'
        verbose_name = 'email'
        ordering = ('-created_at',)

    def __str__(self):
        return self.name
