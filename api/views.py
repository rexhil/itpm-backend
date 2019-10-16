from .models import UserInfo, InsuranceType, InsurancePlan, Insurance, Claim
from .serializers import UserInfoSerializer, InsurancePlanSerializer, ClaimsSerializer, UserInsurancesSerializer
from .serializers import InsuranceTypeSerializer, InsurancesSerializer, ClaimUpdateSerialier
from django.contrib.auth.views import LoginView as dLoginView, LogoutView as dLogoutView
from rest_framework_jwt.settings import api_settings
from rest_framework import generics, permissions
from .serializers import TokenSerializer
from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import SessionAuthentication, BasicAuthentication


class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


class UserInfoView(generics.ListCreateAPIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserInfoSerializer

    def get_queryset(self):
        current_user = self.request.user
        return UserInfo.objects.filter(user=current_user)


class InsuranceTypeView(generics.ListCreateAPIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    permission_classes = (permissions.AllowAny,)
    queryset = InsuranceType.objects.all().order_by('id')
    serializer_class = InsuranceTypeSerializer


class InsurancePlanView(generics.ListCreateAPIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    permission_classes = (permissions.AllowAny,)
    queryset = InsurancePlan.objects.all().order_by('id')
    serializer_class = InsurancePlanSerializer


class InsurancesView(generics.ListCreateAPIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    permission_classes = (permissions.AllowAny,)
    queryset = Insurance.objects.all().order_by('id')
    serializer_class = InsurancesSerializer

    def get_queryset(self):
        current_user = self.request.user
        return Insurance.objects.filter(user=current_user)


class ClaimsView(generics.ListCreateAPIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    permission_classes = (permissions.AllowAny,)
    serializer_class = ClaimsSerializer
    lookup_url_kwarg = 'user_id'
    lookup_field = 'insurance__user__id'

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        queryset = Claim.objects.filter(is_active=True).order_by('id')
        if user_id:
            queryset = queryset.filter(insurance__user__id=user_id)
        return queryset


class UpdateClaims(generics.RetrieveUpdateAPIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    permission_classes = (permissions.AllowAny,)
    queryset = Claim.objects.filter(is_active=True)
    lookup_field = 'id'
    serializer_class = ClaimUpdateSerialier
    lookup_url_kwarg = 'claim_id'


class LoginView(generics.CreateAPIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    permission_classes = (permissions.AllowAny,)

    """
    POST auth/login/
    """
    # This permission class will override the global permission
    # class setting

    def post(self, request, *args, **kwargs):
        username = request.data.get("username", "")
        password = request.data.get("password", "")

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response(status=status.HTTP_202_ACCEPTED, data={'username': user.username, 'user_id': user.id})
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(dLogoutView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
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
