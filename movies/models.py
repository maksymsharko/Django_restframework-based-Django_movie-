from django.db import models
from datetime import date

from django.urls import reverse


class Category(models.Model):
    name = models.CharField(
        "Категорія",
        max_length=150,
    )
    description = models.TextField(
        "Опис",
    )
    url = models.SlugField(
        max_length=150,
        unique=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'


class Actor(models.Model):
    name = models.CharField(
        "Ім'я",
        max_length=100,
    )
    age = models.PositiveSmallIntegerField(
        "Вік",
        default=0,
    )
    description = models.TextField(
        "Опис",
    )
    image = models.ImageField(
        "Зображення",
        upload_to="actors/",
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("actor_detail", kwargs={"slug": self.name})

    class Meta:
        verbose_name = 'Актор і режисер'
        verbose_name_plural = 'Актори і режисери'


class Genre(models.Model):
    name = models.CharField(
        "Ім'я",
        max_length=100,
    )
    description = models.TextField(
        "Опис",
    )
    url = models.SlugField(
        max_length=100,
        unique=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанри'


class Movie(models.Model):
    title = models.CharField(
        "Назва",
        max_length=100,
    )
    tagline = models.CharField(
        "Слоган",
        max_length=100,
        default='',
    )
    description = models.TextField(
        "Опис",
    )
    poster = models.ImageField(
        "Постер",
        upload_to="movies/",
    )
    year = models.PositiveSmallIntegerField(
        "Дата виходу",
        default=2020,
    )
    country = models.CharField(
        "Країна",
        max_length=20,
    )
    directors = models.ManyToManyField(
        Actor,
        verbose_name="режисер",
        related_name="film_director",
    )
    actors = models.ManyToManyField(
        Actor,
        verbose_name="актори",
        related_name="film_actor",
    )
    genres = models.ManyToManyField(
        Genre,
        verbose_name="жанри",
    )
    world_premiere = models.DateField(
        "Прем'єра у світі",
        default=date.today,
    )
    budget = models.PositiveIntegerField(
        "Бюджет",
        help_text="вказувати суму у долларах",
    )
    fees_in_usa = models.PositiveIntegerField(
        "Збір у США",
        default=0,
        help_text="вказувати суму у долларах",
    )
    fees_in_world = models.PositiveIntegerField(
        "Збір у світі",
        default=0,
        help_text="вказувати суму у долларах",
    )
    category = models.ForeignKey(
        Category,
        verbose_name="Категорія",
        on_delete=models.SET_NULL,
        null=True,
    )
    url = models.SlugField(
        max_length=130,
        unique=True,
    )
    draft = models.BooleanField(
        "Чорновик",
        default=False,
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("movie_detail", kwargs={"slug": self.url})

    def get_review(self):
        return self.reviews_set.filter(parent__isnull=True)

    class Meta:
        verbose_name = 'Фільм'
        verbose_name_plural = 'Фільми'


class MovieShots(models.Model):
    title = models.CharField(
        "Заголовок",
        max_length=100,
    )
    description = models.TextField(
        "Опис",
    )
    image = models.ImageField(
        "Зображення",
        upload_to="movie_shots/",
    )
    movie = models.ForeignKey(
        Movie,
        verbose_name="Фільм",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Кадр з фільму"
        verbose_name_plural = "Кадри з фільму"


class RatingStar(models.Model):
    value = models.PositiveSmallIntegerField(
        "Значення",
        default=0,
    )

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = 'Зірка рейтингу'
        verbose_name_plural = 'Зірки рейтингу'
        ordering = ["-value"]


class Rating(models.Model):
    ip = models.CharField(
        "ІР адрес",
        max_length=20,
    )
    star = models.ForeignKey(
        RatingStar,
        on_delete=models.CASCADE,
        verbose_name='зірка',
    )
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        verbose_name="фільм",
        related_name="rating",
    )

    def __str__(self):
        return f'{self.star} - {self.movie}'

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'


class Review(models.Model):
    email = models.EmailField()
    name = models.CharField(
        "Ім'я",
        max_length=100,
    )
    text = models.TextField(
        "Сповіщення",
        max_length=10000,
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="children",
    )
    movie = models.ForeignKey(
        Movie,
        verbose_name="фільм",
        on_delete=models.CASCADE,
        related_name="reviews",
    )

    def __str__(self):
        return f'{self.name} - {self.movie}'

    class Meta:
        verbose_name = 'Відгук'
        verbose_name_plural = 'Відгуки'