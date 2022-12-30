from django.contrib import admin
from products.models import *
from django.utils.safestring import mark_safe


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', )
    list_display_links = ('title',)
    search_fields = ('title',)
    fields = ('title', 'slug')


class ImageGalleryInline(admin.TabularInline):
    model = ImageGallery
    extra = 3
    fields = ('additional_picture', 'created_at', 'get_photo')
    readonly_fields = ('get_photo', 'created_at')

    def get_photo(self, obj):
        if obj.additional_picture:
            res = mark_safe(f'<img src="{obj.additional_picture.url}" width="75">')
        else:
            res = "нет картинки"
        return res

    get_photo.short_description = 'Доп. картинка'


class ProductAdmin(admin.ModelAdmin):
    inlines = [ImageGalleryInline, ]
    list_display = ('get_photo', 'id', 'title', 'category', 'quantity', 'location', 'status')
    list_display_links = ('title',)
    search_fields = ('title', )
    list_filter = ('category', 'location', 'place_of_application', 'responsible',)
    list_editable = ('status', )
    fields = ('get_photo', 'main_image', 'title', 'category', 'description', 'quantity',
              'price', 'serial_number', 'location', 'place_of_application',
              'responsible', 'equipment', 'warranty', 'warranty_period', 'additional_information',
              'status', 'created_at', 'update_at')
    readonly_fields = ('get_photo', 'created_at', 'update_at')
    ordering = ('-created_at',)

    def get_photo(self, obj):
        if obj.main_image_miniature:
            res = mark_safe(f'<img src="{obj.main_image.url}" width="75">')
        else:
            res = "нет картинки"
        return res

    get_photo.short_description = 'Фото'


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)