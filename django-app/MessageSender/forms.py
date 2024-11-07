from django import forms


class NewMessageForm(forms.Form):
    target_person_id = forms.NumberInput()
    message = forms.TextInput()
