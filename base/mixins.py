from django.core.exceptions import FieldDoesNotExist

from rest_framework.serializers import ModelSerializer
from rest_framework.generics import get_object_or_404


class NastedViewSetMixin(object):
    """
    Mixin which allows to create nested objects by default.
    """
    direct_parent = None

    def _get_param_with_parent_pk(self):
        """
        Metod return dict() with  parent key and value
        """
        parents = [(key.replace('_pk', ''), v) for key, v in self.kwargs.items() if key.endswith('_pk')]
        serializer_class = self.get_serializer_class()
        if issubclass(serializer_class, ModelSerializer):
            return_dict = {}
            for name, pk in parents:
                try:
                    model = serializer_class.Meta.model._meta.get_field(name)
                    get_object_or_404(model.related_model, pk=pk)
                    return_dict[name] = pk
                except FieldDoesNotExist:
                    pass
            return dict([('{}_id'.format(key), v) for key, v in return_dict.items()])
        return dict([('{}_id'.format(key), v) for key, v in parents])

    def get_queryset(self):
        queryset = super().get_queryset()
        filter_params = self._get_param_with_parent_pk()
        return queryset.filter(**filter_params)

    def perform_create(self, serializer):
        serializer.save(**self._get_param_with_parent_pk())
