from rest_framework import generics, permissions, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .models import Movie, Actor
from .serializers import (
    MovieListSerializer,
    MovieDetailSerializer,
    ReviewCreateSerializer,
    CreateRatingSerializer,
    ActorListSerializer,
    ActorDetailSerializer,
)
from .service import get_client_ip, MovieFilter
from django.db import models


class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    """List of films"""
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MovieFilter

    def get_queryset(self):
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=models.Count("ratings",
                                     filter=models.Q(retings__ip=get_client_ip(self.request)))
        ).annotate(
            middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
        )
        return movies

    def get_serializer_class(self):
        if self.action == 'list':
            return MovieListSerializer
        elif self.action == 'retrieve':
            return MovieDetailSerializer


class ReviewCreateViewSet(viewsets.ModelViewSet):
    """Adding a review to a film"""
    serializer_class = ReviewCreateSerializer


class AddStarRatingViewSet(viewsets.ModelViewSet):
    """adding a rating to a film"""
    serializer_class = CreateRatingSerializer

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))


class ActorsViewSet(viewsets.ReadOnlyModelViewSet):
    """outputing an actors or a directors"""
    queryset = Actor.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ActorListSerializer
        elif self.action == 'retrieve':
            return ActorDetailSerializer
# class MovieListView(generics.ListAPIView):
#     """List of films. Way number1"""
#     serializer_class = MovieListSerializer
#     filter_backends = (DjangoFilterBackend,)
#     filterset_class = MovieFilter
#     permission_classes = [permissions.IsAuthenticated]
#
#     def get_queryset(self):
#         movies = Movie.objects.filter(draft=False).annotate(
#             rating_user=models.Count("rating",
#                                      filter=models.Q(rating__ip=get_client_ip(self.request)))
#         ).annotate(
#             middle_star=models.Sum(models.F('rating__star')) / models.Count(models.F('rating'))
#         )
#         return movies
    # """List of films. Way number2"""
    # def get(self, request):
    #     movies = Movie.objects.filter(draft=False).annotate(
    #         rating_user=models.Case(
    #             models.When(rating__ip=get_client_ip(request), then=True),
    #             default=False,
    #             output_field=models.BooleanField()
    #         ),
    #     )


# class MovieDetailView(generics.RetrieveAPIView):
#     """Movie output"""
#     queryset = e = Movie.objects.filter(draft=False)
#     serializer_class = MovieDetailSerializer
#
#
# class ReviewCreateView(generics.CreateAPIView):
#     """Adding a review to a film"""
#     serializer_class = ReviewCreateSerializer
#
#
# class AddStarRatingView(generics.CreateAPIView):
#     """add rating to a film"""

    # def get_client_ip(self, request):
    #     x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    #     if x_forwarded_for:
    #         ip = x_forwarded_for.split(',')[0]
    #     else:
    #         ip = request.META.get('REMOTE_ADDR')
    #     return ip
#     serializer_class = CreateRatingSerializer
#
#     def perform_create(self, serializer):
#         serializer.save(ip=get_client_ip(self.request))
#
#
# class ActorsListView(generics.ListAPIView):
#     """List pf actors"""
#     queryset = Actor.objects.all()
#     serializer_class = ActorListSerializer
#
#
# class ActorsDetailView(generics.RetrieveAPIView):
#     """detail information about actor or director"""
#     queryset = Actor.objects.all()
#     serializer_class = ActorDetailSerializer
