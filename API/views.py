from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.views.generic import TemplateView
from rest_framework.authtoken.models import Token
from rest_framework import generics, renderers, filters
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from .serializers import GreenPointSerializer, UserProfileSerializer, BadgeSerializer, StatsSerializer, UserSerializer, \
    AuthCustomTokenSerializer, GameReportSerializer, RedPointSerializer, ReportSerializer, CityStatsSerializer, \
    ResetPasswordSerializer
from .models import GreenPoint, UserProfile, Stats, Badge, User, GameReport
from rest_framework.response import Response
from rest_framework.views import APIView
from django.template.loader import get_template

class CreateViewUser(generics.ListCreateAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        serializer.save()

class DetailsViewUser(generics.RetrieveUpdateDestroyAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer

class CreateViewUserProfile(generics.ListCreateAPIView):

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def perform_create(self, serializer):
        serializer.save()

class DetailsViewUserProfile(generics.RetrieveUpdateAPIView):

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class CreateViewGreenPoint(generics.ListCreateAPIView):

    queryset = GreenPoint.objects.all()
    serializer_class = GreenPointSerializer

    def perform_create(self, serializer):
        serializer.save()

class DetailsViewGreenPoint(generics.RetrieveUpdateAPIView):

    queryset = GreenPoint.objects.all()
    serializer_class = GreenPointSerializer


class CreateViewBadge(generics.ListCreateAPIView):

    queryset = Badge.objects.all()
    serializer_class = BadgeSerializer

    def perform_create(self, serializer):
        serializer.save()

class DetailsViewBadge(generics.RetrieveUpdateDestroyAPIView):

    queryset = Badge.objects.all()
    serializer_class = BadgeSerializer

class CreateViewStats(generics.ListCreateAPIView):

    queryset = Stats.objects.all()
    serializer_class = StatsSerializer

    def perform_create(self, serializer):
        serializer.save()

class DetailsViewStats(generics.RetrieveUpdateDestroyAPIView):

    queryset = Stats.objects.all()
    serializer_class = StatsSerializer

class GameReportView(generics.ListAPIView):

    queryset = GameReport.objects.all()
    serializer_class = GameReportSerializer

class UserGameReportView(generics.ListAPIView):

    serializer_class = GameReportSerializer

    def get_queryset(self):
        """
        This view should return a list of all the game reports for
        the user as determined by the user portion of the URL.
        """
        user = self.kwargs['user']
        return GameReport.objects.filter(user=user)

class UserReport(generics.ListAPIView):

    serializer_class = ReportSerializer

    def get_queryset(self):
        """
        This view should return a list of all the game reports for
        the user as determined by the user portion of the URL.
        """
        user = self.kwargs['user']
        return GreenPoint.objects.filter(user=user)

class RedPointView(generics.UpdateAPIView):

    queryset = GreenPoint.objects.filter(status=-1)
    serializer_class = RedPointSerializer

    def perform_update(self, serializer):
        serializer.save()

""" Login Class """

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
        token, created = Token.objects.get_or_create(user=user)

        user_profile = UserProfile.objects.get(fk_user=user.pk)

        """
            Content of the Response after successful login
        """
        content = {
            'id': user.pk,
            'token': token.key,
            'username': user.username,
            'email': user.email,
            'fullname': user_profile.fullname,
            'country':user_profile.country,
            'city':user_profile.city,
            'points': user_profile.game_points,
            'badge': user_profile.badge,
        }
        return Response(content)

class CityStatsView(generics.ListAPIView):

    serializer_class = CityStatsSerializer
    queryset = Stats.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('city', 'green_index', 'population_density', 'reported_trees')

class ResetPasswordView(APIView):

    def post(self, request):
        print (request)
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        user_exist = User.objects.filter(email=email).exists()
        if user_exist:
            user = User.objects.get(email=email)
            token = Token.objects.get(user=user)
            print(token)
            content = {
                'token': token.key,
                'status': 200
            }

            email_subject = 'Analiticom - Recuperación de Contraseña'
            message_template = 'password-reset-email.html'
            email = [email]
            context = {'username': str(user),
                       'key':token,
                       'host': request.META['HTTP_HOST']}
            send_email(email_subject, message_template,context ,email)

        else:
            content = {'status': 404}
        print(content)
        return Response(content)

        #{"email": "sreyes@idbcgroup.com"}


class Password_Reset_Confirm(TemplateView):
    template_name = 'password-reset-confirm.html'

    def post(self, request, *args, **kwargs):
        print("post reset")
        content = {'status': 200 }
        return Response(content)


def send_email(subject, message_template, context, email):

    from_email = 'canopyverde.analiticom@idbcgroup.com'
    email_subject = subject
    message = get_template(message_template).render(context)
    msg = EmailMessage(email_subject, message, to=email, from_email=from_email)
    msg.content_subtype = 'html'
    msg.send()