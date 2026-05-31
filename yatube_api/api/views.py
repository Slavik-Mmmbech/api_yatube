from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated

from posts.models import Post, Comment, Group
from .serializers import PostSerializer, CommentSerializer, GroupSerializer
from .permissions import IsOwnerOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        # Привязываем текущего пользователя к посту при создании
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Только GET. ReadOnlyModelViewSet уже имеет list() и retrieve()"""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        # Фильтруем комментарии только для конкретного поста
        return Comment.objects.filter(post_id=self.kwargs['post_id'])

    def perform_create(self, serializer):
        # Привязываем комментарий к посту и текущему автору
        serializer.save(author=self.request.user, post_id=self.kwargs['post_id'])