from rest_framework import serializers
from .models import Book, Category


class TranslatedFieldsMixin:
    translatable = []

    def get_lang(self):
        request = self.context.get("request")
        lang = "uz"
        if request is not None:
            lang = request.query_params.get("lang", "uz")
        return lang if lang in ("uz", "ru") else "uz"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        lang = self.get_lang()
        for field in self.translatable:
            data[field] = getattr(instance, f"{field}_{lang}")
            data.pop(f"{field}_uz", None)
            data.pop(f"{field}_ru", None)
        return data


class CategorySerializer(TranslatedFieldsMixin, serializers.ModelSerializer):
    translatable = ["name"]

    class Meta:
        model = Category
        fields = ["id", "name_uz", "name_ru"]


class BookSerializer(TranslatedFieldsMixin, serializers.ModelSerializer):
    translatable = ["title", "description", "author"]
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Book
        fields = [
            "id",
            "title_uz", "title_ru",
            "description_uz", "description_ru",
            "author_uz", "author_ru",
            "price", "published", "category", "created_at",
        ]