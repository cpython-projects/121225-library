import datetime
from rest_framework import serializers
from apps.library.models import Author, AuthorDetail


class AuthorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthorDetail
        fields = ('biography', 'birth_city', 'gender')


class AuthorSerializer(serializers.ModelSerializer):
    details = AuthorDetailSerializer(required=False, read_only=True)

    class Meta:
        model = Author
        fields = ('id', 'first_name', 'last_name', 'date_of_birth', 'profile', 'rating', 'is_deleted', 'details')
        read_only_fields = ('id', 'is_deleted')

    def validate_date_of_birth(self, value):
        if value >= datetime.date.today():
            raise serializers.ValidationError("Date of birth is in the future")
        return value

    # def create(self, validated_data):
    #     details_data = validated_data.pop('details', None)
    #     author = Author.objects.create(**validated_data)
    #     if details_data:
    #         AuthorDetail.objects.create(author=author, **details_data)
    #     return author











