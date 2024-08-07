from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.db.models import Count
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from online_shop.models import Product, Category, Comment

# Register your models here.

admin.site.register(Comment)
admin.site.unregister(User)
admin.site.unregister(Group)

class IsVeryExpensiveFilter(admin.SimpleListFilter):
    title = 'Is Very Expensive Product'
    parameter_name = 'is_very_expensive_product'

    def lookups(self, request, model_admin):
        return (
            ('Yes', 'Yes'),
            ('No', 'No'),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'Yes':
            return queryset.filter(price__gt=20_000_000)
        elif value == 'No':
            return queryset.exclude(price__gt=20_000_000)
        return queryset

@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'product_count')
    search_fields = ['title', 'id']
    prepopulated_fields = {'slug': ('title',)}

    def product_count(self, obj):
        return obj.products.count()

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'category', 'discount', 'image_preview', 'order_count', 'is_very_expensive_product', 'comments_count', 'created_at')
    search_fields = ['name']
    list_filter = ['category', IsVeryExpensiveFilter]

    def is_very_expensive_product(self, obj):
        return obj.price > 20_000_000

    is_very_expensive_product.boolean = True

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            comments_count=Count('comments'),
            orders_count=Count('order')
        )
        return queryset

    def comments_count(self, obj):
        return obj.comments_count

    comments_count.short_description = 'Comments Count'

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="100" />', obj.image.url)
        return 'No Image'

    image_preview.short_description = 'Image Preview'

    def order_count(self, obj):
        return obj.orders_count

    order_count.short_description = 'Quantity of Orders'

