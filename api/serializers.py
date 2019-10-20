from rest_framework import serializers
from .models import User, UserInfo, InsuranceType, InsurancePlan, Insurance, Claim
from django.contrib.auth.models import Group


class TokenSerializer(serializers.Serializer):
    """
    This serializer serializes the token data
    """
    token = serializers.CharField(max_length=255)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'groups']


class UserInfoSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = UserInfo
        fields = ['user', 'dob', 'gender', 'mobile']


class InsuranceTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = InsuranceType
        fields = '__all__'


class InsurancePlanSerializer(serializers.ModelSerializer):
    insurance_type = InsuranceTypeSerializer(many=False, read_only=True)

    class Meta:
        model = InsurancePlan
        fields = ['name', 'premium', 'total', 'duration', 'insurance_type']


class InsurancesSerializer(serializers.ModelSerializer):
    # insurance_plan = InsurancePlanSerializer(many=False, read_only=True)
    # user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Insurance
        fields = ['insurance_plan', 'user']


class UserInsurancesSerializer(serializers.ModelSerializer):
    insurance_plan = InsurancePlanSerializer(many=False, read_only=True)
    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Insurance
        fields = ['insurance_plan', 'user']

    def to_representation(self, instance):
        insurance_types = []
        added_insurance_type = []
        print(instance)
        # for insurance in instance:
        if instance.insurance_plan.insurance_type.name not in added_insurance_type:
            insurance_types.append({'id': instance.insurance_plan.insurance_type.id,
                                    'name': instance.insurance_plan.insurance_type.name,
                                    'insurance': []})
            added_insurance_type.append(instance.insurance_plan.insurance_type.name)

        for _types in insurance_types:
            if instance.insurance_plan.insurance_type.name == _types['name']:
                _types['insurance'].append(
                    {
                        'id': instance.insurance_plan.id,
                        'name': instance.insurance_plan.name,
                        'premium': instance.insurance_plan.premium,
                        'total': instance.insurance_plan.total,
                        'duration': instance.insurance_plan.duration,

                    }
                )
        return insurance_types


class ClaimsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Claim
        fields = ['id', 'insurance', 'amount']


class ClaimUpdateSerialier(serializers.ModelSerializer):
    class Meta:
        model = Claim
        fields = ['amount', 'is_active', 'approval_state']


class UserTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']