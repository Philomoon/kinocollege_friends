from django import forms
from .models import Client,Actual

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['client_name','client_kana','client_gender','number','insurer','room_number']

class ActualForm(forms.ModelForm):
    class Meta:
        model = Actual
        fields = ['user_name','date','start_time','end_time','bathing','transportation','meal','notes']