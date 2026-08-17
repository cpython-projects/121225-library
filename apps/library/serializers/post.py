from rest_framework import serializers
from apps.library.models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'author', 'moderated')
        read_only_fields = ('id',)