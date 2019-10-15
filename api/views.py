from .models import UserInfo, InsuranceType, InsurancePlan, Insurance, Claim
from .serializers import UserInfoSerializer, InsurancePlanSerializer, ClaimsSerializer, UserInsurancesSerializer
from .serializers import InsuranceTypeSerializer, InsurancesSerializer
from django.contrib.auth.views import LoginView as dLoginView, LogoutView as dLogoutView
from rest_framework_jwt.settings import api_settings
from rest_framework import generics, permissions
from .serializers import TokenSerializer
from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import render, redirect
from django.http import JsonResponse


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


def insurance_view(request, user_id):
    insurance_types = []
    added_insurance_type = []
    insurances = Insurance.objects.filter(user__id=user_id)
    claims = Claim.objects.filter(insurance__user__id=user_id)

    for instance in insurances:
        if instance.insurance_plan.insurance_type.name not in added_insurance_type:
            insurance_types.append({'insurance_type_id': instance.insurance_plan.insurance_type.id,
                                    'insurance_type_name': instance.insurance_plan.insurance_type.name,
                                    'insurance': []})
            added_insurance_type.append(instance.insurance_plan.insurance_type.name)

    for _type in insurance_types:
        for instance in insurances:
            if instance.insurance_plan.insurance_type.name == _type['insurance_type_name']:
                _type['insurance'].append(
                    {
                        'insurance_id': instance.id,
                        'insurance_plan_id': instance.insurance_plan.id,
                        'insurance_plan_name': instance.insurance_plan.name,
                        'premium': instance.insurance_plan.premium,
                        'total': instance.insurance_plan.total,
                        'duration': instance.insurance_plan.duration,
                        'claims': []

                    }
                )
    for _type in insurance_types:
        for insurance in _type['insurance']:
            for claim in claims:
                if insurance['insurance_id'] == claim.insurance.id:
                    insurance['claims'].append({
                        'claim_id': claim.id,
                        'claim_amount': claim.amount,
                        'claim_active_status': claim.is_active,
                        'claim_made_on': claim.creation_time

                    })

    return JsonResponse(insurance_types, safe=False)
