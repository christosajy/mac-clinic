from django.urls import path
from .views import SignupView, LoginView, GroupListView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('groups/', GroupListView.as_view(), name='group-list'),
]
