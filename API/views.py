from django.shortcuts import render
# Create your views here.
from rest_framework.authtoken.models import Token
from rest_framework import generics, status, renderers
from rest_framework.decorators import api_view
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser

from .serializers import GreenPointSerializer, UserProfileSerializer, BadgeSerializer, StatsSerializer, UserSerializer, AuthCustomTokenSerializer
from .models import GreenPoint, UserProfile, Stats, Badge, User
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

class CreateViewGreenPoint(generics.ListCreateAPIView):
    """This class defines the create behavior of our rest api."""
    queryset = GreenPoint.objects.all()
    serializer_class = GreenPointSerializer

    def perform_create(self, serializer):
        serializer.save()
        #serializer.save(user=self.request.user)
        #               datafile=self.request.data.get('datafile'))

class DetailsViewGreenPoint(generics.RetrieveUpdateDestroyAPIView):
    """This class handles the http GET, PUT and DELETE requests."""
    queryset = GreenPoint.objects.all()
    serializer_class = GreenPointSerializer

class CreateViewUser(generics.ListCreateAPIView):
    """This class defines the create behavior of our rest api."""
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        serializer.save()

class DetailsViewUser(generics.RetrieveUpdateDestroyAPIView):
    """This class handles the http GET, PUT and DELETE requests."""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CreateViewUserProfile(generics.ListCreateAPIView):
    """This class defines the create behavior of our rest api."""
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def perform_create(self, serializer):
        serializer.save()

class DetailsViewUserProfile(generics.RetrieveUpdateDestroyAPIView):
    """This class handles the http GET, PUT and DELETE requests."""
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class CreateViewBadge(generics.ListCreateAPIView):
    """This class defines the create behavior of our rest api."""
    queryset = Badge.objects.all()
    serializer_class = BadgeSerializer

    def perform_create(self, serializer):
        serializer.save()

class DetailsViewBadge(generics.RetrieveUpdateDestroyAPIView):
    """This class handles the http GET, PUT and DELETE requests."""
    queryset = Badge.objects.all()
    serializer_class = BadgeSerializer

class CreateViewStats(generics.ListCreateAPIView):
    """This class defines the create behavior of our rest api."""
    queryset = Stats.objects.all()
    serializer_class = StatsSerializer

    def perform_create(self, serializer):
        serializer.save()

class DetailsViewStats(generics.RetrieveUpdateDestroyAPIView):
    """This class handles the http GET, PUT and DELETE requests."""
    queryset = Stats.objects.all()
    serializer_class = StatsSerializer

class ObtainAuthToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (
        FormParser,
        MultiPartParser,
        JSONParser,
    )

    renderer_classes = (renderers.JSONRenderer,)

    def post(self, request):
        serializer = AuthCustomTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        print(user, user.pk, user.username,user.email)
        token, created = Token.objects.get_or_create(user=user)

        content = {
            'id': user.pk,
            'token': token.key,
            'username': user.username,
            'email': user.email,
        }
        return Response(content)
