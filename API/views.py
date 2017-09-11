from django.core.mail import EmailMessage
from django.views.generic import TemplateView
from rest_framework.authtoken.models import Token
from rest_framework import generics, renderers, filters
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from .serializers import TreePointSerializer, UserProfileSerializer, BadgeSerializer, StatsSerializer, UserSerializer, \
    AuthCustomTokenSerializer, GameReportSerializer, ReportSerializer, CityStatsSerializer, \
    ResetPasswordSerializer, ChangePasswordSerializer
from .models import TreePoint, UserProfile, Stats, Badge, User, GameReport
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

class DetailsViewUserProfile(generics.RetrieveUpdateDestroyAPIView):

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class CreateViewTreePoint(generics.ListCreateAPIView):

    queryset = TreePoint.objects.all()
    serializer_class = TreePointSerializer

    def perform_create(self, serializer):
        serializer.save()

class DetailsViewTreePoint(generics.RetrieveUpdateDestroyAPIView):

    queryset = TreePoint.objects.all()
    serializer_class = TreePointSerializer


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

# Filters the user's game report with the argument of the URL
class UserGameReportView(generics.ListAPIView):

    serializer_class = GameReportSerializer

    def get_queryset(self):
        """
        This view should return a list of all the game reports for
        the user as determined by the user portion of the URL.
        """
        user = self.kwargs['user']
        return GameReport.objects.filter(user=user)


# Filters the user's game report with the argument of the URL
class UserReport(generics.ListAPIView):

    serializer_class = ReportSerializer

    def get_queryset(self):
        """
        This view should return a list of all the game reports for
        the user as determined by the user portion of the URL.
        """
        user = self.kwargs['user']
        return TreePoint.objects.filter(user=user)

# Search view that filters the stats of the city requested in the URL
class CityStatsView(generics.ListAPIView):

    serializer_class = CityStatsSerializer
    queryset = Stats.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('city', 'green_index', 'population_density', 'reported_trees')

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

        # Saves the token of the User
        user_profile = UserProfile.objects.get(fk_user=user.pk)
        user_profile.activation_key = str(token)
        user_profile.save()

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


class ResetPasswordView(APIView):

    # Check if the email has an account associated and sends an email with the link
    # to change the password using the Token of the user
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        user_exist = User.objects.filter(email=email).exists()
        if user_exist:
            user = User.objects.get(email=email)
            token = Token.objects.get(user=user)
            content = {
                'token': token.key,
                'status': 200
            }
            email_subject = 'CanopyVerde - Recuperación de Contraseña'
            # The email is built with a template
            message_template = 'password-reset-email.html'
            email = [email]
            profile = UserProfile.objects.get(fk_user=user.pk)
            #The context of the email
            context = {'username': str(profile),
                       'key':token,
                       'host': request.META['HTTP_HOST']}
            send_email(email_subject, message_template,context ,email)

        else:
            content = {'status': 404}
        return Response(content)

# Sends an email built with a template using the user's token
#
# @param subject the subject of the email
#
# @param message_template the template view
#
# @param context the params that will be used in the template
#
# @param email the user's email
#
def send_email(subject, message_template, context, email):

    from_email = 'canopyverde.analiticom@idbcgroup.com'
    email_subject = subject
    message = get_template(message_template).render(context)
    msg = EmailMessage(email_subject, message, to=email, from_email=from_email)
    msg.content_subtype = 'html'
    msg.send()

class Password_Reset_Confirm(generics.CreateAPIView):

    # Check if the passwords are the same and updates the user's password
    def post(self, request, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data['password']
        confirm_password = serializer.validated_data['confirm_password']
        profile = UserProfile.objects.get(activation_key=kwargs['token'])
        user = profile.fk_user
        if ((password == confirm_password) and (len(password)>=8 or len(confirm_password)>=8)):
            user.set_password(password)
            user.save()
            content = {'status': 200}
        else:
            content = {'status': 400}
        return Response(content)

class HomeView(TemplateView):
    template_name = 'index.html'