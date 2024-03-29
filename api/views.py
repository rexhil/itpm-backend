from .models import UserInfo, InsuranceType, InsurancePlan, Insurance, Claim
from .serializers import UserInfoSerializer, InsurancePlanSerializer, ClaimsSerializer
from .serializers import InsuranceTypeSerializer, ClaimUpdateSerialier, UserTypeSerializer
from django.contrib.auth.views import LogoutView as dLogoutView
from rest_framework_jwt.settings import api_settings
from rest_framework import generics, permissions
from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
import json


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


class UserInfoView(generics.ListCreateAPIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserInfoSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return UserInfo.objects.filter(user__id=user_id)


class UserType(generics.ListAPIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserTypeSerializer


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


class ClaimsView(generics.ListCreateAPIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    permission_classes = (permissions.AllowAny,)
    serializer_class = ClaimsSerializer
    lookup_url_kwarg = 'user_id'
    lookup_field = 'insurance__user__id'

    def get_queryset(self):
        queryset = Claim.objects.filter(is_active=True).order_by('id')
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
        _type = request.data.get("type", "")

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        user = authenticate(request, username=username, password=password)
        is_staff = False if _type == 'customer' else True
        if user is not None and is_staff == user.is_staff:
            login(request, user)
            return Response(status=status.HTTP_202_ACCEPTED, data={'username': user.username, 'user_id': user.id})
        return Response(False)


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


def claim_view(request, user_id):
    all_claims = []
    if user_id:
        claims = Claim.objects.filter(insurance__user__id=user_id).order_by('-creation_time')
    else:
        claims = Claim.objects.filter().order_by('-creation_time')

    for claim in claims:
        _data = {
            'id': claim.id,
            'insurance_name': claim.insurance.insurance_plan.name,
            'insurance_total': claim.insurance.insurance_plan.total,
            'insurance_plan_id': claim.insurance.insurance_plan.id,
            'premium': claim.insurance.insurance_plan.premium,
            'duration': claim.insurance.insurance_plan.duration,
            'amount': claim.amount,
            'name': claim.insurance.user.first_name,
            'status': claim.approval_state
        }
        all_claims.append(_data)

    return JsonResponse(all_claims, safe=False)


def delete_claim(request, claim_id):
    if request.method == "GET":
        return JsonResponse({'error': "Method Not Allowed"})
    else:
        try:
            Claim.objects.filter(id=claim_id).delete()
        except Exception as E:
            return JsonResponse({'error': E}, status=401)
        else:
            return JsonResponse({'Status': 'Success'})


def update_claim(request, claim_id):
    if request.method == "GET":
        return JsonResponse({'error': "Method Not Allowed"})
    else:
        _request = json.loads(request.body.decode('utf-8'))
        try:
            amount = _request.get("amount", None)
            is_active = _request.get("is_active", None)
            state = _request.get("approval_state", None)
            claim = Claim.objects.filter(id=claim_id)[0]
            if amount:
                claim.amount = amount
            if is_active:
                claim.is_active = is_active
            if state:
                claim.approval_state = state
            claim.save()
        except Exception as E:
            return JsonResponse({'error': str(E)}, status=401)
        else:
            return JsonResponse({'Status': 'Success'})


def create_claim(request):
    if request.method == "GET":
        return JsonResponse({'error': "Method Not Allowed"})
    else:
        _request = json.loads(request.body.decode('utf-8'))
        try:
            amount = _request.get("amount", None)
            insurance_id = _request.get("insurance", None)
            claim = Claim.objects.filter(approval_state='P', insurance__id=insurance_id)
            if not claim:
                new_claim = Claim.objects.create(amount=amount, insurance_id=insurance_id)
                new_claim.save()
            else:
                return JsonResponse({'status': "Claim already in pending"})
        except Exception as E:
            return JsonResponse({'error': str(E)}, status=401)
        else:
            return JsonResponse({'status': 'Success'})