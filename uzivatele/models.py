from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Uzivatel(User):
    class Meta:
        verbose_name = "Uživatel"
        verbose_name_plural = "Uživatelé"
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"