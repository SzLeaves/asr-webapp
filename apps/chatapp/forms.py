from django import forms


class SessionNameForm(forms.Form):
    sessionName = forms.CharField(max_length=10)
