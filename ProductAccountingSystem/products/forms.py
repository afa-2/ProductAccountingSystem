from django import forms
from products.models import Product, Category
from django.contrib.auth.models import User


class FilterForm(forms.Form):
    CHOICES_LOCATION = [
        ('', 'Все'),
        ('warehouse', 'Склад'),
        ('office_gorgasali', 'Офис на ул. Горгасали 9'),
        ('house', 'Дом'),
        ('office_gorizont', 'Офис Горизонт'),
    ]

    PLACE_OF_APPLICATION = [
        ('', 'Все'),
        ('kitchen', 'Кухня'),
        ('Toilet', 'Туалет'),
        ('bar', 'Бар'),
        ('lower_hall', 'Нижний зал'),
        ('upper_hall', 'Верхний зал'),
        ('smart_office', 'Смарт офис'),
        ('reception', 'Ресепшн'),
    ]

    STATUS = [
        ('', 'Все'),
        ('serviceable', 'Исправен'),
        ('requires_repair', 'Требует ремонта'),
        ('write-downs', 'Списание'),
        ('missing', 'Пропажа'),
        ('Requires an extension', 'Требует дополнение'),
        ('on_the_hands', 'На руках')
        ]

    category = forms.ModelChoiceField(queryset=Category.objects.all(),
                                      label='Категория',
                                      empty_label='Все',
                                      required=False,
                                      widget=forms.Select(attrs={'class': 'form-control'}))
    location = forms.ChoiceField(label='Локация:',
                                 required=False,
                                    widget=forms.Select(attrs={'class': 'form-control'}),
                                    choices=CHOICES_LOCATION)
    place_of_application = forms.ChoiceField(label='Мето применения:',
                                    required=False,
                                    widget=forms.Select(attrs={'class': 'form-control'}),
                                    choices=PLACE_OF_APPLICATION)
    status = forms.ChoiceField(label='Статус:',
                               required=False,
                                    widget=forms.Select(attrs={'class': 'form-control'}),
                                    choices=STATUS)
    responsible = forms.ModelChoiceField(queryset=User.objects.all(),
                                        label='Ответственный',
                                        required=False,
                                        empty_label='Все',
                                        widget=forms.Select(attrs={'class': 'form-control'}))