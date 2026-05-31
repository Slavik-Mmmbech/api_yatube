from rest_framework import serializers
from posts.models import Post, Comment, Group

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description')
        read_only_fields = fields  # Группы только читаем (по ТЗ)


class PostSerializer(serializers.ModelSerializer):
    # Автор подтягивается автоматически, но в ответе должен быть username
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Post
        fields = ('id', 'text', 'author', 'image', 'group', 'pub_date')
        read_only_fields = ('author', 'pub_date')  # Автор и дата создаются системой


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    # Ссылка на пост будет подставляться автоматически через URL, но отдавать будем ID
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'author', 'post', 'text', 'created')
        read_only_fields = ('author', 'post', 'created')