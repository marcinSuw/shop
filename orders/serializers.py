from django.conf import settings
from django.db import transaction
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from orders.models import Cart, Order, OrderItem


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'email', 'promotion_code', 'total')


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.SlugRelatedField(source='product', slug_field='name', read_only=True)
    price = serializers.SlugRelatedField(source='product', slug_field='price', read_only=True)

    class Meta:
        model = OrderItem
        fields = ('id', 'product', 'product_name', 'quantity', 'price')

    def create(self, validated_data):
        cart_id = validated_data.get('cart_id', None)
        if cart_id:
            with transaction.atomic():
                item, c = OrderItem.objects.get_or_create(cart_id=cart_id, product=validated_data['product'], defaults={'quantity':0})
                item.quantity += 1
                item.save()
        return item


class CartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = ('id', 'promo_code', 'total')
        read_only_fields = ('total',)

    def validate_promo_code(self, value):
        if value in settings.PROMO_CODES or value == '':
            return value
        raise serializers.ValidationError('Promo Code invalid')


class CartCheckOutSerializer(serializers.Serializer):
    email = serializers.EmailField(validators=[UniqueValidator(queryset=Order.objects.all())])
