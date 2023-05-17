from bootstrap_datepicker_plus.widgets import DatePickerInput
from django import forms
from .models import Client,Actual

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['client_name','client_kana','client_gender','number','insurer','room_number']
        widgets = {
            'client_kana':forms.TextInput(
                attrs={'pattern':"(?=.*?[\u3041-\u309F])[\u3041-\u309F\s]*",
                        'placeholder':'ひらがなを入力してください。',
                    },
            ),
            'number':forms.TextInput(
                attrs={'pattern':"\d{2,4}-?\d{2,4}-?\d{3,4}",
                        'placeholder':'半角数字、-(ハイフン)のみ',
                    },
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['room_number'].required = False
    
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

            # 'notes':forms.TextInput(
                
            # ),
        }