from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from shop.models import Product, Category, Order, OrderItem, Banner, ProductReview
from .serializers import (
    ProductListSerializer, ProductDetailSerializer, CategorySerializer,
    OrderSerializer, BannerSerializer, ProductReviewSerializer
)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.filter(active=True)
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {'category': ['exact']}
    search_fields = ['name', 'description']
    ordering_fields = ['sort_index', 'price', 'review_count', 'id']
    ordering = ['-sort_index']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductDetailSerializer
        return ProductListSerializer

    @action(detail=False, methods=['get'])
    def popular(self, request):
        products = Product.objects.all().order_by('-sort_index')[:8]
        serializer = ProductListSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def limited(self, request):
        products = Product.objects.filter(limited_edition=True)[:16]
        serializer = ProductListSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def reviews(self, request, pk=None):
        product = self.get_object()
        reviews = product.reviews.filter(active=True)
        serializer = ProductReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def add_review(self, request, pk=None):
        if not request.user.is_authenticated:
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)

        product = self.get_object()
        text = request.data.get('text', '')
        rating = request.data.get('rating', 5)
        
        ProductReview.objects.create(
            product=product,
            author=request.user,
            text=text,
            rating=rating
        )
        return Response({'message': 'Review added'}, status=status.HTTP_201_CREATED)


class BannerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Banner.objects.filter(active=True)
    serializer_class = BannerSerializer
    permission_classes = [AllowAny]


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def create(self, request):
        user = request.user
        items_data = request.data.get('items', [])

        if not items_data:
            return Response({'error': 'No items provided'}, status=status.HTTP_400_BAD_REQUEST)

        order = Order.objects.create(user=user, delivery_address=request.data.get('delivery_address', ''))

        for item in items_data:
            try:
                product = Product.objects.get(id=item['product_id'])
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=item['quantity'],
                    price=product.price
                )
            except Product.DoesNotExist:
                order.delete()
                return Response({'error': f'Product {item["product_id"]} not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def pay(self, request, pk=None):
        order = self.get_object()
        order.paid = True
        order.status = 'confirmed'
        order.save()
        return Response({'message': 'Payment successful'}, status=status.HTTP_200_OK)
