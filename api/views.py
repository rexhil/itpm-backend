from .models import UserInfo, InsuranceType, InsurancePlan, Insurance, Claim
from .serializers import UserInfoSerializer, InsurancePlanSerializer, ClaimsSerializer, InsurancesSerializer
from .serializers import InsuranceTypeSerializer
from django.contrib.auth.views import LoginView as dLoginView, LogoutView as dLogoutView
from rest_framework_jwt.settings import api_settings
from rest_framework import generics, permissions
from .serializers import TokenSerializer
from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import render, redirect
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView


class UserInfoView(generics.ListCreateAPIView):
    serializer_class = UserInfoSerializer

    def get_queryset(self):
        current_user = self.request.user
        return UserInfo.objects.filter(user=current_user)


class InsuranceTypeView(generics.ListCreateAPIView):
    queryset = InsuranceType.objects.all().order_by('id')
    serializer_class = InsuranceTypeSerializer


class InsurancePlanView(generics.ListCreateAPIView):
    queryset = InsurancePlan.objects.all().order_by('id')
    serializer_class = InsurancePlanSerializer


class InsurancesView(generics.ListCreateAPIView):
    queryset = Insurance.objects.all().order_by('id')
    serializer_class = InsurancesSerializer

    def get_queryset(self):
        current_user = self.request.user
        return Insurance.objects.filter(user=current_user)


class ClaimsView(generics.ListCreateAPIView):
    queryset = Claim.objects.filter(is_active=True).order_by('id')
    serializer_class = ClaimsSerializer


def dashboard(request):
    if request.user.is_authenticated:
        return render(request, template_name='dashboard/home.html', context={'title': 'Dashboard'})
    return redirect('/login/')


class UserLoginView(dLoginView):
    permission_classes = (permissions.AllowAny,)
    redirect_authenticated_user = True
    template_name = 'dashboard/login.html'


class LoginView(generics.CreateAPIView):
    """
    POST auth/login/
    """
    # This permission class will override the global permission
    # class setting
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        username = request.data.get("username", "")
        password = request.data.get("password", "")

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        user = authenticate(request, username=username, password=password)
        if user is not None:
            # login saves the user’s ID in the session,
            # using Django’s session framework.
            login(request, user)
            serializer = TokenSerializer(data={
                # using drf jwt utility functions to generate a token
                "token": jwt_encode_handler(
                    jwt_payload_handler(user)
                )})
            serializer.is_valid()
            return Response(serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(dLogoutView):
    permission_classes = (permissions.AllowAny,)
    next_page = '/login/'

    def post(self, request, *args, **kwargs):
        logout(request)


# class UploadInputSheetView(APIView):
#     renderer_classes = [TemplateHTMLRenderer]
#     template_name = 'dashboard/upload-input-sheet.html'
#     queryset = Menu.objects.all()
#
#     def get(self, request):
#         queryset = Menu.objects.all()
#         return Response({'menus': queryset})


