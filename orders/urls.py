from django.urls import include, path

from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers


from orders.views import CartViewSet, OrderViewSet, OrderItemViewSet

router = DefaultRouter()
router.register('carts', CartViewSet, base_name="carts")
router.register('orders', OrderViewSet, base_name='orders')

cart_router = routers.NestedSimpleRouter(router, r'carts', lookup='cart')
cart_router.register(r'items', OrderItemViewSet, base_name='cart-order_items')

order_router = routers.NestedSimpleRouter(router, r'orders', lookup='order')
order_router.register(r'items', OrderItemViewSet, base_name='order-order_items')


urlpatterns = [
    path('', include(router.urls)),
    path('', include(cart_router.urls)),
    path('', include(order_router.urls)),
]
