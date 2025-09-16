from django.db import models

# Create your models here.

class Zprava(models.Model):
    nazev = models.CharField(max_length=200, verbose_name="Název zprávy", null=True, default="Zpráva")
    obsah = models.TextField(verbose_name="Obsah zprávy")
    datum_vytvoreni = models.DateTimeField(auto_now_add=True, verbose_name="Datum vytvoření")
    autor = models.ForeignKey(
        'auth.User', on_delete=models.CASCADE, verbose_name="Autor zprávy"
    )

    def __str__(self):
        return self.nazev

    class Meta:
        verbose_name = "Zpráva"
        verbose_name_plural = "Zprávy"
        # Ordering by creation date (oldest first)
        ordering = ['-datum_vytvoreni']

class Diskuze(models.Model):
    nazev = models.CharField(max_length=200, verbose_name="Název diskuze")
    
    popis = models.TextField(verbose_name="Popis diskuze", blank=True, null=True)
    datum_zahajeni = models.DateTimeField(verbose_name="Datum zahájení diskuze", auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, verbose_name="Datum aktualizace diskuze")

    zpravy = models.ManyToManyField(
        Zprava, 
        related_name='diskuze', 
        verbose_name="Zprávy v diskuzi"
    )

    def __str__(self):
        return self.nazev
    
    class Meta:
        verbose_name = "Diskuze"
        verbose_name_plural = "Diskuze"
        ordering = ['-datum_zahajeni']