import django_filters
from .models import Visitor

class VisitorFilter(django_filters.FilterSet):
    class Meta:
        model = Visitor
        fields = {
            'first_name': ['startswith', 'icontains'],
            'last_name': ['startswith', 'icontains'],
            'gov_id_no': ['startswith', 'icontains'],
            'phone': ['startswith', 'icontains'],
        }
        # together = ['first_name', 'last_name', 'gov_id_no']
