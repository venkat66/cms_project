from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import User, Post, Like
from .serializers import UserSerializer, PostSerializer, LikeSerializer
from .permissions import IsOwnerOrReadOnly

class UserCreateAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserRetrieveUpdateDeleteAPIView(APIView):
    permission_classes = [IsOwnerOrReadOnly]

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PostCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostRetrieveUpdateDeleteAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404
            # return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        post = self.get_object(pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, pk):
        post = self.get_object(pk)
        if post.owner != request.user:
            return Response({"error": "You are not authorized to update this post"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        post = self.get_object(pk)
        if post.owner != request.user:
            return Response({"error": "You are not authorized to delete this post"}, status=status.HTTP_400_BAD_REQUEST)
        post.delete()
        return Response({"msg": "Post has been deleted"},status=status.HTTP_200_OK)

class LikeCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = LikeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LikeRetrieveUpdateDeleteAPIView(APIView):
    permission_classes = [IsOwnerOrReadOnly, permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return Like.objects.get(pk=pk)
        except Like.DoesNotExist:
            raise Http404
            # return Response({"error": "Like not found"}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        like = self.get_object(pk)
        serializer = LikeSerializer(like)
        return Response(serializer.data)


    def delete(self, request, pk):
        like = self.get_object(pk)
        if like.user != request.user:
             return Response({"error": "You are not authorized to delete this like"}, status=status.HTTP_400_BAD_REQUEST)
        like.delete()
        return Response({"msg": "Like has been deleted"},status=status.HTTP_200_OK)
