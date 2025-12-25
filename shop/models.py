from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Category(models.Model):
    name = models.CharField(max_length=255)
    icon = models.ImageField(upload_to='categories/', null=True, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='children')
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Seller(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class ProductCharacteristicType(models.Model):
    name = models.CharField(max_length=255)
    FILTER_TYPES = [
        ('select', 'Select'),
        ('multiselect', 'Multi-select'),
        ('checkbox', 'Checkbox'),
        ('text', 'Text'),
    ]
    filter_type = models.CharField(max_length=20, choices=FILTER_TYPES, default='text')

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    image = models.ImageField(upload_to='products/')
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    sort_index = models.IntegerField(default=0)
    limited_edition = models.BooleanField(default=False)

    class Meta:
        ordering = ['-sort_index']

    def __str__(self):
        return self.name

    @property
    def price(self):
        price = self.prices.filter(active=True).first()
        return price.value if price else 0

    @property
    def sales_count(self):
        return self.order_items.filter(order__paid=True).aggregate(total=models.Sum('quantity'))['total'] or 0

    @property
    def review_count(self):
        return self.reviews.filter(active=True).count()


class ProductPrice(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='prices')
    value = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.value}"


class ProductCharacteristic(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='characteristics')
    characteristic_type = models.ForeignKey(ProductCharacteristicType, on_delete=models.CASCADE)
    value = models.CharField(max_length=1000)

    def __str__(self):
        return f"{self.product.name} - {self.characteristic_type.name}"


class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Review for {self.product.name}"


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    paid = models.BooleanField(default=False)
    delivery_address = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.id}"

    @property
    def total_price(self):
        return self.items.aggregate(total=models.Sum(models.F('quantity') * models.F('price'), output_field=models.DecimalField()))['total'] or 0


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} in Order #{self.order.id}"


class Banner(models.Model):
    TYPES = [
        ('category', 'Category'),
        ('sale', 'Sale'),
    ]
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='banners/')
    banner_type = models.CharField(max_length=20, choices=TYPES, default='category')
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title
