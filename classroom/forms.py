from django import forms


class ContentForm(forms.Form):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'form-control', }), help_text='Выберите файл для загрузки', label='Файл')
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название файла'}),
                            help_text='Обязательное поле', label='Название')
    description = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Комментарий к файлу'}),
                                  help_text='Необязательное поле', label='Комментарий')
