import datetime
from rest_framework import serializers
from apps.library.models import Author, AuthorDetail


class AuthorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthorDetail
        fields = ('biography', 'birth_city', 'gender')


class AuthorSerializer(serializers.ModelSerializer):
    details = AuthorDetailSerializer(required=False)
    url = serializers.HyperlinkedIdentityField(view_name='library:author-detail')

    class Meta:
        model = Author
        fields = ('id', 'url', 'first_name', 'last_name', 'date_of_birth', 'profile', 'rating', 'is_deleted', 'details')
        read_only_fields = ('id', 'url', 'is_deleted')

    def validate_date_of_birth(self, value):
        if value >= datetime.date.today():
            raise serializers.ValidationError("Date of birth is in the future")
        return value

    def update(self, instance, validated_data):
        details_data = validated_data.pop('details', None)

        author = super().update(instance, validated_data)
        if details_data:
            AuthorDetail.objects.update_or_create(author=author, **details_data)
        return instance


    def create(self, validated_data):
        details_data = validated_data.pop('details', None)
        author = Author.objects.create(**validated_data)
        if details_data:
            AuthorDetail.objects.create(author=author, **details_data)
        return author











