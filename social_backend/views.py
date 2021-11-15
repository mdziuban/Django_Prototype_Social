from django.shortcuts import render
from rest_framework import generics
from . models import Player, Post, Reply, GameData, User, SiteImages
from . serializers import ImageSerializer, PlayerSerializer, PostSerializer, PostDetailSerializer, ReplySerializer, GameDataSerializer, UserSerializer, RegisterSerializer
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.decorators import action

class PlayerList(generics.ListCreateAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = User.objects.select_related('player')
        user = self.request.user
        queryset = queryset.filter(id = user.id)
        return queryset  
          
class PlayerDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class PlayerInfo(generics.ListAPIView):
    serializer_class = UserSerializer

    def return_data(self):
        queryset = User.objects.all()
        return queryset

class PlayerUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostDetail(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer

class PostLike(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer

    @action(methods=['delete'], detail=True)
    def removeLike(self, request):
        queryset = Post.objects.all()
        print(queryset)
        user_id = self.request.query_params.get('user_likes')
        print(user_id)
        queryset.user_likes.remove(user_id)

    @action(methods=['patch'], detail=True)
    def addLike(self, request):
        queryset = Post.objects.all()
        print(queryset)
        user_id = self.request.query_params.get('user_likes')
        print(user_id)
        queryset.user_likes.add(user_id)

class PostDelete(generics.DestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class ReplyDelete(generics.DestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer

class ReplyList(generics.ListCreateAPIView):
    serializer_class = ReplySerializer

    def get_queryset(self):
        queryset = Reply.objects.all()
        post_number = self.request.query_params.get('post_id')
        queryset = queryset.filter(post_id = post_number)
        return queryset


class ReplyAdd(generics.ListCreateAPIView):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer

class ReplyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer


class GameDataList(generics.ListCreateAPIView):
    queryset = GameData.objects.all()
    serializer_class = GameDataSerializer

class GameDataDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = GameData.objects.all()
    serializer_class = GameDataSerializer

class Register(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

class Images(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = SiteImages.objects.all()
    serializer_class = ImageSerializer


def playGame(request):
    return render(request, 'sanctuary/index.html')



