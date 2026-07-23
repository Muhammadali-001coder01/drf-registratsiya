from rest_framework import serializers
from .models import Book, Category

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128, write_only=True)

    def create(self, validated_data):
        from django.contrib.auth.models import User

        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"]
        )
        return user


class TranslatedFieldsMixin:
    

    translatable = []  

    def get_lang(self):
        request = self.context.get("request")
        lang = "uz"

        if request is not None:
            lang = request.query_params.get("lang", "uz")

        if lang not in ("uz", "ru"):
            lang = "uz"

        return lang

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
