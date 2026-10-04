from django.urls import path
from .views import SignUpView

urlpatterns = [
    path('signip/', SignUpView.as_view())

]