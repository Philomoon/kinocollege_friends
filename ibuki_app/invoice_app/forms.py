from bootstrap_datepicker_plus.widgets import DatePickerInput
from django import forms
from .models import Client,Actual


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['client_name','client_kana','client_gender','number','insurer','room_number']
        widgets = {
            'client_gender':forms.RadioSelect,
        }
    
    
class ActualForm(forms.ModelForm):
    class Meta:
        model = Actual
        fields = ['user_name','date','start_time','end_time','bathing','transportation','meal','notes']
        widgets = {
            'date': DatePickerInput(
                attrs={'class':'datepicker'},
                options={
                    'format':'YYYY-MM-DD',
                    'locale':'ja',
                    'dayViewHeaderFormat':'YYYY年 MMMM',
                }
            ),

            'start_time':forms.TimeInput(
                attrs={'type':'time'},
            ),

            'end_time':forms.TimeInput(
                attrs={'type':'time'},
            ),
        }