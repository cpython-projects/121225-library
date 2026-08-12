from rest_framework import serializers
from apps.library.models import Book, Author, Category, Library
from .author import AuthorSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class BookSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(), allow_null=True, required=False
    )
    # average_rating = serializers.FloatField(source='rating_db', read_only=True)

    class Meta:
        model = Book
        fields = (
            'id', 'title', 'author', 'published_at', 'genre', 'page_count',
            'category', 'publisher', 'libraries', 'description', 'photo',
            # 'average_rating',
        )
        read_only_fields = ('id', 'average_rating')


class BookCreateSerializer(serializers.ModelSerializer):
    """Используется только для POST, без вычисляемых read-only полей."""
    class Meta:
        model = Book
        fields = (
            'title', 'author', 'published_at', 'genre', 'page_count',
            'category', 'publisher', 'libraries', 'description', 'photo',
        )


# class BookSerializer(serializers.ModelSerializer):
#     author = serializers.PrimaryKeyRelatedField(
#         queryset=Author.objects.all(), required=False, allow_null=True
#     )
#     url = serializers.HyperlinkedIdentityField(view_name='library:book-detail', read_only=True)
#     author_detail = AuthorSerializer(source='author', read_only=True)
#     author_url = serializers.HyperlinkedRelatedField(source='author', view_name='library:author-detail', read_only=True)
#     category = serializers.SlugRelatedField(
#         queryset=Category.objects.all(), slug_field='name', required=True, allow_null=True
#     )
#     libraries = serializers.PrimaryKeyRelatedField(
#         queryset=Library.objects.all(), many=True, required=False, allow_null=True
#     )
#     libraries_count = serializers.SerializerMethodField()
#     rating = serializers.FloatField(source='rating_db', read_only=True)
#
#     class Meta:
#         model = Book
#         fields = ('id', 'url', 'title', 'author', 'author_detail', 'author_url', 'published_at',
#                   'genre', 'page_count', 'category', 'libraries', 'libraries_count', 'publisher', 'description', 'photo', 'rating')
#
#     def get_libraries_count(self, obj):
#         return obj.libraries.count()

