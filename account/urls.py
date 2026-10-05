from django.urls import path
from .views import SignUpView, VerifyView, ProfileView

urlpatterns = [
    path('signip/', SignUpView.as_view()),
    path('verify/', VerifyView.as_view()),
    path('profile/', ProfileView.as_view()),

]




