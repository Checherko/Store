from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

class BasketView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Return empty basket for now
        return Response({
            'count': 0,
            'total_price': 0,
            'items': []
        })
    
    def post(self, request):
        # Add item to basket
        return Response({'status': 'success'}, status=status.HTTP_201_CREATED)
    
    def delete(self, request):
        # Remove item from basket
        return Response({'status': 'success'}, status=status.HTTP_200_OK)
