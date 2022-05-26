from django.db import models

import os
from django.contrib.auth.models import User


from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from datetime import datetime, timezone


_MAX_SIZE = 1280
_MINIATURE_MAX_SIZE = 400


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=150, verbose_name='Название категории')
    slug = models.SlugField(max_length=150, unique=True, verbose_name='Слаг на английском')

    def __str__(self):
        return self.title

    def get_absolute_url_ru(self):
        return f'/categories/{self.slug}'

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Product(models.Model):
    CHOICES_LOCATION = [
        ('warehouse', 'Склад'),
        ('office_gorgasali', 'Офис Горкасали 9'),
        ('house', 'Дом'),
        ('office_gorizont', 'Офис Горизонт'),
    ]

    PLACE_OF_APPLICATION = [
        ('kitchen', 'Кухня'),
        ('Toilet', 'Туалет'),
        ('bar', 'Бар'),
        ('lower_hall', 'Нижний зал'),
        ('upper_hall', 'Верхний зал'),
        ('smart_office', 'Смарт офис'),
        ('reception', 'Ресепшн'),
    ]

    STATUS = [
        ('serviceable', 'Исправен'),
        ('requires_repair', 'Требует ремонта'),
        ('write-downs', 'Списание'),
        ('missing', 'Пропажа'),
        ('Requires an extension', 'Требует дополнение'),
        ('on_the_hands', 'На руках'),
    ]

    id = models.AutoField(primary_key=True)

    title = models.CharField(max_length=150, verbose_name='Название')
    main_image = models.ImageField(verbose_name='Главное изображение', upload_to='product_photo/', blank=True)
    main_image_miniature = models.ImageField(verbose_name='Главное изображение миниатюра', blank=True, upload_to='product_photo/')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='Категория')
    description = models.TextField(verbose_name='Описание', blank=True)
    quantity = models.IntegerField(default=1, verbose_name='Количество')
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена')

    serial_number = models.CharField(max_length=150, blank=True, verbose_name='Серийный номер')
    location = models.CharField(max_length=200, choices=CHOICES_LOCATION, default='office_gorgasali', verbose_name='Локация')
    place_of_application = models.CharField(max_length=200, choices=PLACE_OF_APPLICATION, default='reception', verbose_name='Место применения')
    responsible = models.ForeignKey(User, on_delete=models.PROTECT, default=User, verbose_name='Ответственный')
    equipment = models.TextField(verbose_name='Комплектация', blank=True)
    warranty = models.DateField(verbose_name='Дата, с которой исчисляется гарантийный срок', blank=True, null=True)
    additional_information = models.TextField(verbose_name='Дополнительная информация', blank=True)
    status = models.CharField(max_length=200, choices=STATUS, default='serviceable', verbose_name='Статус')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    update_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product_card', kwargs={"id": self.pk})

    def get_all_price(self):
        return self.price * self.quantity

    def save(self, *args, **kwargs):
        # при замене изображения, удалем старое
        try:
            this = Product.objects.get(id=self.id)
            if this.main_image != self.main_image:
                this.main_image.delete(save=False)
                this.main_image_miniature.delete(save=False)

        except:
            pass  # when new photo then we do nothing, normal case
        super(Product, self).save(*args, **kwargs)

        """
        Меняем разрешение картинки на меньшее, если оно больше максимального размера в пикселях.
        """
        super(Product, self).save(*args, **kwargs)
        if self.main_image:
            # изменение размера главного изображения
            filepath = self.main_image.path
            width = self.main_image.width
            height = self.main_image.height

            max_size = max(width, height)

            if max_size > _MAX_SIZE:
                image = Image.open(filepath)
                image = image.resize(
                    (round(width / max_size * _MAX_SIZE),  # Сохраняем пропорции
                     round(height / max_size * _MAX_SIZE)),
                    Image.ANTIALIAS)
                image.save(filepath)

            # создание миниатюры
            upload_to_miniature = 'product_photo/'  # куда после media грузить миниатюру
            filepath = self.main_image.path
            filename = 'miniature_' + str(os.path.basename(filepath))
            path_for_dir = os.path.dirname(filepath)
            new_path = os.path.join(path_for_dir, filename)

            width = self.main_image.width
            height = self.main_image.height

            max_size = max(width, height)

            image = Image.open(filepath)
            if max_size > _MINIATURE_MAX_SIZE:
                image = image.resize(
                    (round(width / max_size * _MINIATURE_MAX_SIZE),  # Сохраняем пропорции
                     round(height / max_size * _MINIATURE_MAX_SIZE)),
                    Image.ANTIALIAS)
            image.save(new_path)

            self.main_image_miniature = upload_to_miniature + filename
            super(Product, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Материальная ценность"
        verbose_name_plural = "Материальные ценности"
        ordering = ['-created_at', ]


class ImageGallery(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Материальная ценность')
    additional_picture = models.ImageField(verbose_name='Дополнительное изображение', upload_to='product_photo/', blank=True)
    additional_picture_miniature = models.ImageField(verbose_name='Дополнительное изображение миниатюра', upload_to='product_photo/')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    def __str__(self):
        return self.product.title

    def save(self, *args, **kwargs):
        # при замене изображения, удалем старое
        try:
            this = ImageGallery.objects.get(id=self.id)
            if this.additional_picture != self.additional_picture:
                this.additional_picture.delete(save=False)
                this.additional_picture_miniature.delete(save=False)
        except:
            pass  # when new photo then we do nothing, normal case

        super(ImageGallery, self).save(*args, **kwargs)
        """
        Меняем разрешение картинки на меньшее, если оно больше максимального размера в пикселях.
        """
        super(ImageGallery, self).save(*args, **kwargs)
        if self.additional_picture:
            filepath = self.additional_picture.path
            width = self.additional_picture.width
            height = self.additional_picture.height

            max_size = max(width, height)

            if max_size > _MAX_SIZE:
                image = Image.open(filepath)
                image = image.resize(
                    (round(width / max_size * _MAX_SIZE),  # Сохраняем пропорции
                     round(height / max_size * _MAX_SIZE)),
                    Image.ANTIALIAS)
                image.save(filepath)

            # создание миниатюры
            upload_to_miniature = 'product_photo/'  # куда после media грузить миниатюру
            filepath = self.additional_picture.path
            filename = 'additional_picture_miniature_' + str(os.path.basename(filepath))
            path_for_dir = os.path.dirname(filepath)
            new_path = os.path.join(path_for_dir, filename)

            width = self.additional_picture.width
            height = self.additional_picture.height

            max_size = max(width, height)

            image = Image.open(filepath)
            if max_size > _MINIATURE_MAX_SIZE:
                image = image.resize(
                    (round(width / max_size * _MINIATURE_MAX_SIZE),  # Сохраняем пропорции
                     round(height / max_size * _MINIATURE_MAX_SIZE)),
                    Image.ANTIALIAS)
            image.save(new_path)

            self.additional_picture_miniature = upload_to_miniature + filename
            super(ImageGallery, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Дополнительное изображение"
        verbose_name_plural = "Дополнительные изображения"
        ordering = ['-created_at']


@receiver(pre_delete, sender=Product)
def photo_delete(sender, instance, **kwargs):
    if instance.main_image.name:
        instance.main_image.delete(False)
    if instance.main_image_miniature.name:
        instance.main_image_miniature.delete(False)


@receiver(pre_delete, sender=ImageGallery)
def additional_photo_delete(sender, instance, **kwargs):
    if instance.additional_picture.name:
        instance.additional_picture.delete(False)
    if instance.additional_picture_miniature.name:
        instance.additional_picture_miniature.delete(False)