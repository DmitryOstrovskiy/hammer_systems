from django.urls import include, path
from rest_framework.routers import DefaultRouter
from api.views import (get_confirmation_code, check_activation_code,
                       UsersViewSet)

router_v1 = DefaultRouter()

router_v1.register(r'users', UsersViewSet, basename='users')

app_name = 'app'

v1_auth_patterns = [
    path('signup/', get_confirmation_code),
    path('code/', check_activation_code)
]

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/', include(v1_auth_patterns)),
]
