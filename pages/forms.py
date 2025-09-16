from django import forms
from .models import Page
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget
# rich text editor widget for CKEditor with file upload support


class PageForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget(), label="Obsah", required=True)

    class Meta:
        model = Page
        fields = ['title', 'content']

