from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Film(models.Model):
    title = models.CharField(max_length=200)
    release_year = models.IntegerField()
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class Film2(models.Model):
    title = models.CharField(max_length=200)
    release_year = models.IntegerField(null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True)
    viewed_by = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class Review(models.Model):
    film = models.ForeignKey(Film2, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.film.title} ({self.rating}/5)"
