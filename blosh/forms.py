from .models import Comment
from django import forms


# form class inheriting from forms.ModelForm
class CommentForm(forms.ModelForm):
    class Meta:
        # to base its structure from
        model = Comment
        # tuple of the properties we want
        fields = ('body',)
