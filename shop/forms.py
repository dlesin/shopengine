from django import forms
from django.utils import timezone


class OrderForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField(required=False)
    phone = forms.CharField()
    buying_type = forms.ChoiceField(widget=forms.Select(), choices=([('self', 'Самовывоз'), ('delivery', 'Доставка')]))
    #date = forms.DateField(widget=forms.SelectDateWidget(), initial=timezone.now())
    address = forms.CharField(required=False)
    comments = forms.CharField(widget=forms.Textarea, required=False)

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].label = 'Имя'
        self.fields['last_name'].label = 'Фамилия'
        self.fields['phone'].label = 'Контактный телефон'
        self.fields['phone'].help_text = 'Пожалуйста, указывайте реальный телефон, по которому можно с Вами связаться'
        self.fields['buying_type'].label = 'Способ получения товара'
        self.fields['address'].label = 'Адрес доставки'
        self.fields['address'].help_text = '*Обязательно укажите город!'
        # self.fields['date'].label = 'Дата доставки'
        # self.fields['date'].help_text = 'Доставка производиться на следующий день после оформления заказа. Менеджер с Вами свяжится'
        # self.fields['date'].widget.attrs['class'] = 'help-text-class help-text-other'

    # date.widget.attrs.update({'style': 'width: 33%; display: inline; margin-right: 1px;', 'class': 'date-widget'})
