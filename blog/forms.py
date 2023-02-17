from .models import Comment, MainTextt
from django import forms
from django_summernote.admin import SummernoteWidget, SummernoteInplaceWidget

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')


class TextForm(forms.ModelForm):
    class Meta:
        model = MainTextt
        fields = ('text_field',)



