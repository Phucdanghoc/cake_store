from django.shortcuts import render
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from shop.models import Order, OrderItem
from rest_framework import status
from django.views.generic import TemplateView
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'total_price']
        read_only_fields = ['total_price']

    def validate(self, data):
        product = data.get('product')
        if not product:
            raise serializers.ValidationError({'product': 'This field is required.'})
        data['price'] = product.price
        data['total_price'] = data['price'] * data['quantity']
        return data


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'status', 'saler', 'order_date', 'delivery_date', 'total_price', 'items']
        read_only_fields = ['total_price', 'order_date', 'status', 'saler']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        validated_data['status'] = 'pending'
        validated_data['saler'] = self.context['request'].user
        order = Order.objects.create(**validated_data)
        total_price = 0
        for item_data in items_data:
            item_data['order'] = order
            item_data['price'] = item_data['product'].price
            item_data['total_price'] = item_data['price'] * item_data['quantity']
            OrderItem.objects.create(**item_data)
            total_price += item_data['total_price']
        order.total_price = total_price
        order.save()
        return order
class OrderAPI(APIView):
    def post(self, request):
        serializer = OrderSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            order = serializer.save()
            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class OrderActionAPI(APIView):
    def get(self, request, pk, *args, **kwargs):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({'detail': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
        if 'pay' in request.path:
            if order.status == 'pending':
                order.status = 'paid' 
                order.save()
                return Response({'detail': 'Payment successful'}, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'Order already processed or invalid status'}, status=status.HTTP_400_BAD_REQUEST)
        
        elif 'cancel' in request.path:
            if order.status == 'pending':
                order.status = 'canceled' 
                order.save()
                return Response({'detail': 'Order canceled successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'Cannot cancel a processed order'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'detail': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
class OrderListView(LoginRequiredMixin, TemplateView):
    template_name = 'manager/order/order_list.html'

    def get(self, request, *args, **kwargs):
        orders = self.get_orders(self.request)
        return render(self.request, self.template_name, {'orders': orders})

    def get_orders(self, request):
        order_list = Order.objects.all()
        search_query = request.GET.get('search', '')
        if search_query:
            order_list = order_list.filter(
                Q(order_date__icontains=search_query)       
            )
        paginator = Paginator(order_list, 10) 
        page_number = request.GET.get('page') 
        page_obj = paginator.get_page(page_number)

        return page_obj
class OrderDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'manager/order/order_detail.html'
    def get_context_data(self, **kwargs):
        order = self.get_order(kwargs['pk'])
        if not order:
            return render(self.request, '404.html', {'message': 'Order not found'})
        order_items = order.items.prefetch_related('product')
        context = {
            'order': order,
            'order_items': order_items,
        }
        return context
    def get_order(self, pk):
        try:
            return Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return None