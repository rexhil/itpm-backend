from django.urls import path
from django.conf.urls import url
from .views import UserInfoView, ClaimsView, InsurancePlanView, create_claim, InsuranceTypeView
from .views import LoginView, LogoutView, insurance_view, update_claim, claim_view, delete_claim
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('user_info/<int:user_id>', csrf_exempt(UserInfoView.as_view()), name="user_info"),
    path('claim/', csrf_exempt(create_claim), name="claim"),
    path('claim/<int:user_id>', csrf_exempt(claim_view), name="claim"),
    path('insurance_plan/', csrf_exempt(InsurancePlanView.as_view()), name="insurance_plan"),
    path('insurance/<int:user_id>', csrf_exempt(insurance_view), name="user_insurance"),
    # path('insurance/', csrf_exempt(InsurancesView.as_view()), name="insurance"),
    path('claim/update/<int:claim_id>', csrf_exempt(update_claim), name="update_claim"),
    path('insurance_type/', csrf_exempt(InsuranceTypeView.as_view()), name="insurance_type"),
    path('login/', csrf_exempt(LoginView.as_view()), name="post-login"),
    path('logout/', csrf_exempt(LogoutView.as_view()), name="logout"),
    path('claim/delete/<int:claim_id>', csrf_exempt(delete_claim), name='delete_claim'),
]
