from rest_framework import serializers
from shop.models import (
    Category, Product, ProductPrice, ProductReview, Order, OrderItem,
    Banner, ProductCharacteristic, Seller
)


class CategorySerializer(serializers.ModelSerializer):
    icon = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'icon']

    def get_icon(self, obj):
        if obj.icon:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.icon.url) if request else obj.icon.url
        return None


class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = ['id', 'name']


class ProductPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPrice
        fields = ['value']


class ProductCharacteristicSerializer(serializers.ModelSerializer):
    characteristic_name = serializers.CharField(source='characteristic_type.name', read_only=True)

    class Meta:
        model = ProductCharacteristic
        fields = ['characteristic_name', 'value']


class ProductReviewSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.get_full_name', read_only=True)

    class Meta:
        model = ProductReview
        fields = ['id', 'author_name', 'text', 'rating', 'created_at']


class ProductListSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'description', 'images', 'category', 'limited_edition']
        
    def get_images(self, obj):
        request = self.context.get('request')
        if obj.image:
            return [{
                'src': request.build_absolute_uri(obj.image.url) if request else obj.image.url,
                'alt': obj.name
            }]
        return []
        
    def get_price(self, obj):
        try:
            price = obj.prices.latest('created_at')
            return str(price.value)
        except:
            return '0.00'
    price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    review_count = serializers.IntegerField(read_only=True)
    title = serializers.CharField(source='name', read_only=True)
    images = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'title', 'images', 'description', 'price', 'review_count']

    def get_images(self, obj):
        if obj.image:
            request = self.context.get('request')
            image_url = request.build_absolute_uri(obj.image.url) if request else obj.image.url
            return [{'src': image_url, 'alt': obj.name}]
        return []


class ProductDetailSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    review_count = serializers.IntegerField(read_only=True)
    sales_count = serializers.IntegerField(read_only=True)
    title = serializers.CharField(source='name', read_only=True)
    images = serializers.SerializerMethodField()
    reviews = ProductReviewSerializer(many=True, read_only=True)
    characteristics = ProductCharacteristicSerializer(many=True, read_only=True)
    seller = SellerSerializer(read_only=True)
    category = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'title', 'description', 'images', 'price', 'review_count',
            'sales_count', 'limited_edition', 'reviews', 'characteristics',
            'seller', 'category'
        ]

    def get_images(self, obj):
        if obj.image:
            request = self.context.get('request')
            image_url = request.build_absolute_uri(obj.image.url) if request else obj.image.url
            return [{'src': image_url, 'alt': obj.name}]
        return []


class OrderItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(write_only=True, required=True)
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['product_id', 'product_name', 'quantity', 'price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'status', 'paid', 'delivery_address', 'created_at', 'items', 'total_price']


class BannerSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    class Meta:
        model = Banner
        fields = ['id', 'title', 'images', 'banner_type', 'category', 'price']

    def get_images(self, obj):
        if obj.image:
            request = self.context.get('request')
            image_url = request.build_absolute_uri(obj.image.url) if request else obj.image.url
            return [{'src': image_url, 'alt': obj.title}]
        return []
    
    def get_price(self, obj):
        return '0'
