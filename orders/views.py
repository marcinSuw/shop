from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import ListModelMixin, DestroyModelMixin, CreateModelMixin, UpdateModelMixin
from rest_framework.response import Response


from base.mixins import NastedViewSetMixin
from orders.models import Cart, Order, OrderItem
from orders.serializers import CartCheckOutSerializer, CartSerializer, OrderSerializer, OrderItemSerializer


class OrderItemViewSet(NastedViewSetMixin, ListModelMixin, DestroyModelMixin, CreateModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer


class CartViewSet(ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    @action(detail=True, methods=['post'])
    def checkout(self, request, pk=None):
        serializer = CartCheckOutSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            self._check_unique_order_email(serializer.validated_data['email'])
            cart = self.get_object()
            order = Order.objects.create(
                email=serializer.validated_data['email'],
                promotion_code=cart.promo_code,
                total=cart.total
            )
            cart.orderitem_set.all().update(order=order, cart=None)
            cart.delete()
            return Response(data=OrderSerializer(order).data, status=status.HTTP_201_CREATED)

    def _check_unique_order_email(self, email):
        if Order.objects.filter(email=email).first():
            return Response({'Failure': 'Order with given email already exist.'}, status.HTTP_400_BAD_REQUEST)


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
