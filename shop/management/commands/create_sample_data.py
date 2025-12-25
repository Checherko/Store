from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from shop.models import Category, Seller, Product, ProductPrice, ProductReview, Banner, ProductCharacteristicType
from decimal import Decimal

class Command(BaseCommand):
    help = 'Create sample data for testing'

    def handle(self, *args, **options):
        # Create sellers
        seller1, _ = Seller.objects.get_or_create(name='TechStore', defaults={'description': 'Best tech products'})
        seller2, _ = Seller.objects.get_or_create(name='ElectroShop', defaults={'description': 'Electronics'})

        # Create categories
        electronics, _ = Category.objects.get_or_create(name='Electronics', defaults={'active': True})
        computers, _ = Category.objects.get_or_create(name='Computers', defaults={'active': True, 'parent': electronics})
        phones, _ = Category.objects.get_or_create(name='Phones', defaults={'active': True, 'parent': electronics})

        # Create test user
        user, _ = User.objects.get_or_create(username='testuser', defaults={'password': '123456'})

        # Create products
        products_data = [
            {'name': 'Laptop Dell', 'desc': 'Powerful laptop', 'category': computers, 'seller': seller1, 'price': 99999, 'sort': 10},
            {'name': 'iPhone 15', 'desc': 'Latest iPhone', 'category': phones, 'seller': seller2, 'price': 79999, 'sort': 9},
            {'name': 'MacBook Pro', 'desc': 'Professional laptop', 'category': computers, 'seller': seller1, 'price': 189999, 'sort': 8, 'limited': True},
            {'name': 'Samsung Galaxy S24', 'desc': 'Android phone', 'category': phones, 'seller': seller2, 'price': 69999, 'sort': 7},
            {'name': 'iPad Air', 'desc': 'Tablet device', 'category': electronics, 'seller': seller1, 'price': 49999, 'sort': 6},
        ]

        for p_data in products_data:
            product, created = Product.objects.get_or_create(
                name=p_data['name'],
                defaults={
                    'description': p_data['desc'],
                    'category': p_data['category'],
                    'seller': p_data['seller'],
                    'sort_index': p_data['sort'],
                    'limited_edition': p_data.get('limited', False),
                    'image': 'products/default.png'
                }
            )
            if created:
                ProductPrice.objects.create(product=product, value=Decimal(p_data['price']), active=True)
                ProductReview.objects.create(product=product, author=user, text='Great product!', rating=5, active=True)

        # Create banners
        Banner.objects.get_or_create(
            title='Electronics Sale',
            defaults={'image': 'banners/default.png', 'banner_type': 'sale', 'active': True, 'order': 1}
        )

        self.stdout.write(self.style.SUCCESS('Sample data created successfully!'))
