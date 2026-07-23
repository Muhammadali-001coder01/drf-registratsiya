from django.db import models


class Category(models.Model):
    name_uz = models.CharField(max_length=120)
    name_ru = models.CharField(max_length=120)

    def __str__(self):
        return self.name_uz


class Book(models.Model):
    title_uz = models.CharField(max_length=200)
    title_ru = models.CharField(max_length=200)

    description_uz = models.TextField(blank=True)
    description_ru = models.TextField(blank=True)

    author_uz = models.CharField(max_length=150)
    author_ru = models.CharField(max_length=150)

    price = models.DecimalField(max_digits=8, decimal_places=2)
    published = models.DateField()

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="books"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title_uz