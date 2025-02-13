from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .producers.order_created_producer import OrderCreatedProducer
from .models import Order
from .serializers import OrderSerializer

class PlaceOrderView(APIView):
    def post(self, request):
        user_id = request.headers.get("id")
        if not user_id:
            return Response({"error": "UNAUTHORIZED"}, status=status.HTTP_401_UNAUTHORIZED)
        
        product_id = request.data.get("product_id")
        quantity = request.data.get("quantity")

        if not product_id or not quantity:
            return Response({'error': 'Not found product_id & quantity'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product_id = int(product_id)
            quantity = int(quantity)
        except (TypeError, ValueError):
            return Response({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)
        
        order_created_producer = OrderCreatedProducer()
        result = order_created_producer.order_created(product_id, quantity)
        if not result["exists"]:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        if not result["stock_updated"] and result["product"]["stock"] < quantity:
            return Response({"error": "Not enough stock"}, status=status.HTTP_400_BAD_REQUEST)

        order = Order.objects.create(user_id=user_id, product_id=product_id, quantity=quantity)
        order_serializer = OrderSerializer(order).data

        return Response({"message": "Order placed successfully", "order" : order_serializer}, status=status.HTTP_200_OK)