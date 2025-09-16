from django.db import models
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from diskuze.models import Diskuze

class Page(models.Model):
    title = models.CharField(max_length=200, verbose_name="Název stránky")
    slug = models.SlugField(unique=True, verbose_name="Identifikátor (slug)", auto_created=True, 
                            help_text="Identifikátor pro URL, automaticky generován z názvu stránky", 
                            error_messages={
                                'unique': "Tento identifikátor již existuje.",
                                'blank': "Identifikátor nesmí být prázdný."
                            })
    content = RichTextUploadingField(verbose_name="Obsah")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Datum vytvoření")
    updated = models.DateTimeField(auto_now=True, verbose_name="Datum poslední úpravy")

    # uložení uživatele, který stránku upravil
    updated_by = models.ForeignKey(
        'auth.User', on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return self.title