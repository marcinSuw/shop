from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response


class PromoCodesView(APIView):
    """
    Returns possible endpoints.
    """
    # renderer_classes = (JSONRenderer,)

    def get(self, request, format=None):
        list_of_codes = []
        for code, val in settings.PROMO_CODES.items():
            list_of_codes.append({'code': code, 'discount': val})
        return Response(list_of_codes)
