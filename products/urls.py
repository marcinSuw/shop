from django.urls import include, path

from rest_framework.routers import DefaultRouter

from products.views import ProductViewSet

router = DefaultRouter()
router.register('products', ProductViewSet, base_name="products")


urlpatterns = router.urls
