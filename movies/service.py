from django_filters import rest_framework as filters
from movies.models import Movie


def get_client_ip(request):
    """For receiving IP of user"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class CharFieldInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class MovieFilter(filters.FilterSet):
    genres = CharFieldInFilter(field_name='genres__name', lookup_expr='in')
    year = filters.RangeFilter()

    class Meta:
        model = Movie
        fields = ['genres', 'year']

