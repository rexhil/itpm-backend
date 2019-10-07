from django.urls import path
from .views import dashboard
from .views import UserLoginView
from .views import LoginView
from .views import LogoutView
from .views import UploadInputSheetView

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('login/', UserLoginView.as_view(), name="get-login"),
    path('login/', LoginView.as_view(), name="post-login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('upload-input-sheet/', UploadInputSheetView.as_view(), name="upload_input_sheet")
]
