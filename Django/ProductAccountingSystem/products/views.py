import os
from django.shortcuts import render, HttpResponse
from products.models import Product
from django.db.models import *
from django.db.models import Sum, Aggregate, F
from products.forms import FilterForm
import qrcode
from ProductAccountingSystem.settings import MEDIA_ROOT


def general_table(request):
    context = {}

    #общее количество объектов
    product_count = Product.objects.all().count()
    context['product_count'] = product_count

    # общее количество товара
    quantity_all_products = Product.objects.aggregate(quantity_all_products = Sum('quantity'))
    context['quantity_all_products'] = quantity_all_products['quantity_all_products']

    # общая стоимость всех товаров
    all_products = Product.objects.all().annotate(total_price=F('quantity') * F('price'))
    price_all_products = 0
    for i in all_products:
        price_all_products += i.total_price
    price_all_products = round(price_all_products, 2)
    context['price_all_products'] = price_all_products

    # количество товара, требующее ремонта
    goods_requiring_repair = Product.objects.filter(status='requires_repair').count()
    context['goods_requiring_repair'] = goods_requiring_repair

    # списание
    goods_write_downs = Product.objects.filter(status='write-downs').count()
    context['goods_write_downs'] = goods_write_downs

    return render(request, 'products/general_table.html', context)


def all_products(request):
    # проверяем есть ли фильтры
    filter_form = FilterForm(request.GET)
    if filter_form.is_valid():
        if filter_form.cleaned_data['category'] != None \
            or filter_form.cleaned_data['location'] != '' \
            or filter_form.cleaned_data['place_of_application'] != ''\
            or filter_form.cleaned_data['status'] != '' \
            or filter_form.cleaned_data['responsible'] != None:

            # если запрос на фильтры есть
            # категории
            if filter_form.cleaned_data['category'] != None:
                text_filter_category = filter_form.cleaned_data['category']
            else:
                text_filter_category = ''
            #локация
            text_filter_location = filter_form.cleaned_data['location']
            #место применения
            text_filter_place_of_application = filter_form.cleaned_data['place_of_application']
            #статус
            text_filter_status = filter_form.cleaned_data['status']
            # ответственный
            if filter_form.cleaned_data['responsible'] != None:
                # text_filter_user = filter_form.cleaned_data['responsible']
                text_filter_user = filter_form.cleaned_data['responsible']
            else:
                text_filter_user = ''

            all_products = Product.objects.filter(category__title__icontains=text_filter_category,
                                                  location__icontains=text_filter_location,
                                                  place_of_application__icontains=text_filter_place_of_application,
                                                  status__icontains=text_filter_status,
                                                  responsible__username__icontains=text_filter_user,
                                                  )
        else:
            # дергаем все ТМЦ
            all_products = Product.objects.all()

    context = {'all_products': all_products,
               'filter_form': filter_form}

    return render(request, 'products/all_products.html', context)


def product_card(request, id):
    product = Product.objects.get(id=id)
    qr_code = qrcode.make(request.build_absolute_uri(product.get_absolute_url()))

    qr_path = os.path.join(MEDIA_ROOT, 'for_qr', 'qr.png')
    qr_code.save(qr_path)
    qr_image = True
    context = {'product': product, 'qr_image': qr_image}
    return render(request, 'products/product_card.html', context)

