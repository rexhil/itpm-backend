from rest_framework import serializers
from .models import User, UserInfo, InsuranceType, InsurancePlan, Insurance, Claim


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
    insurance_plan = InsurancePlanSerializer(many=False, read_only=True)
    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Insurance
        fields = ['insurance_plan', 'user']


class ClaimsSerializer(serializers.ModelSerializer):
    insurance = InsurancePlanSerializer(many=False, read_only=True)

    class Meta:
        model = Claim
        fields = ['insurance', 'amount']



# class UserSerializer(serializers.ModelSerializer):
#     location = serializers.SlugRelatedField(queryset=Location.objects.all(), slug_field='location_name')
#     attribute = serializers.SlugRelatedField(queryset=Attribute.objects.all(), slug_field='attribute_name')
#     rule_type = serializers.SlugRelatedField(queryset=RuleType.objects.all(), slug_field='rule_type_name')
#
#     class Meta:
#         model = U
#         fields = '__all__'
#
#
# class ReportSerializer(serializers.ModelSerializer):
#     location = serializers.SlugRelatedField(queryset=Location.objects.all(), slug_field='location_name')
#     attribute = serializers.SlugRelatedField(queryset=Attribute.objects.all(), slug_field='attribute_name')
#     rule_type = serializers.SlugRelatedField(queryset=RuleType.objects.all(), slug_field='rule_type_name')
#
#     class Meta:
#         model = ReportTable
#         fields = '__all__'
#
#
# class TokenSerializer(serializers.Serializer):
#     token = serializers.CharField(max_length=255)
#
#
# class SummaryReportSerializer(serializers.ModelSerializer):
#     location = serializers.SlugRelatedField(queryset=Location.objects.all(), slug_field='location_name')
#     attribute = serializers.SlugRelatedField(queryset=Attribute.objects.all(), slug_field='attribute_name')
#     rule_type = serializers.SlugRelatedField(queryset=RuleType.objects.all(), slug_field='rule_type_name')
#
#     class Meta:
#         model = SummaryReport
#         fields = '__all__'
