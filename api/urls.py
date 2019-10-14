from django.urls import path
from .views import UserInfoView, ClaimsView, InsurancePlanView, InsurancesView, InsuranceTypeView
from .views import LoginView, LogoutView, insurance_view

urlpatterns = [
    path('user_info/', UserInfoView.as_view(), name="user_info"),
    path('claim/', ClaimsView.as_view(), name="claim"),
    path('insurance_plan/', InsurancePlanView.as_view(), name="insurance_plan"),
    path('insurance/<int:user_id>', insurance_view, name="insurance"),
    path('insurance_type/', InsuranceTypeView.as_view(), name="insurance_type"),
    path('login/', LoginView.as_view(), name="post-login"),
    path('logout/', LogoutView.as_view(), name="logout"),
]
