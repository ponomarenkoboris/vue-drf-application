from django.urls import path
from .views import (
    GetCSRFTokenView,
    RegistartionView,
    LoginView,
    LogoutView,
    DeleteAccountView,
    UpdateUserProfileView,
    UserProfileView,
    CheckUserAuth,
    SearchUser
)

urlpatterns =[
    path('csrf-token/', GetCSRFTokenView.as_view()),
    path('registration/', RegistartionView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('delete-account/', DeleteAccountView.as_view()),
    path('update-account/', UpdateUserProfileView.as_view()),
    path('user-info/', UserProfileView.as_view()),
    path('check-auth/', CheckUserAuth.as_view()),
    path('search-user/', SearchUser.as_view())
]