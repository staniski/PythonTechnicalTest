from . import views
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('register/',views.RegisterUser.as_view()),
    path('bonds/', views.BondView.as_view()),
    path('api-token-auth/', obtain_auth_token),

]