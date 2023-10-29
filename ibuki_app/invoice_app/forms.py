from bootstrap_datepicker_plus.widgets import DatePickerInput
from django import forms
from django.db.models.base import Model
from django.core.validators import RegexValidator
from .models import Client,Actual,Insurer
from django.forms import ModelChoiceField

class InsurerChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.insurer_name

class ClientForm(forms.ModelForm):

    insurer = forms.ModelChoiceField(
        queryset=Insurer.objects.all(),
    )

    insurance_id = forms.CharField(
        min_length=10,
        max_length=10,
        required=False,  # 追加：入力は必須ではない
        validators=[
            RegexValidator(r'^\d{10}$', message="保険IDは半角数字のみ10桁で入力してください。")
        ],
        error_messages={
            'min_length': "受給者番号は10桁で入力してください。",
            'max_length': "受給者番号は10桁で入力してください。",
        }
    )

    max_amount = forms.CharField(
        validators=[
            RegexValidator(r'^\d+$', message="負担上限額は半角数字のみで入力してください。")
        ],
    )

    class Meta:
        model = Client
        fields = ['client_name','client_kana','client_gender','class_obst','class_num','insurer','insurance_id','max_amount']
        widgets = {
            'client_kana':forms.TextInput(
                attrs={'pattern':"(?=.*?[\u3041-\u309F])[\u3041-\u309F\s]*",
                        'placeholder':'ひらがなを入力してください。',
                    },
            ),
            
        }


    
    
class ActualForm(forms.ModelForm):
    class Meta:
        model = Actual
        fields = ['user_name','date','start_time','end_time','ds','transportation1','transportation2','meal','notes']
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

            'transportation1': forms.CheckboxInput(),

            'transportation2': forms.CheckboxInput(),

            'meal': forms.CheckboxInput(),

        }

class InvoiceCreateForm(forms.Form):
    customer = forms.ModelChoiceField(queryset=Client.objects.all())
    month = forms.DateField()
