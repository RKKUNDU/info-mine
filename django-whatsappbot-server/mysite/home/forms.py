from django import forms


from usersapi.models import users


class PostForm(forms.ModelForm):
    class Meta:
        model=users
        fields='__all__'