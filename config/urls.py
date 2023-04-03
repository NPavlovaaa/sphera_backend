from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from clients.views import ClientView
from users.views import LoginAPIView, UserView, LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('users.urls')),
    path('api/v1/', include('clients.urls')),
    path('', include('users.urls')),
    path('', include('clients.urls')),
    path('', include('products.urls')),
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('login/', LoginAPIView.as_view()),
    path('authUser/', UserView.as_view()),
    path('account/', ClientView.as_view()),
    path('logout/', LogoutView.as_view()),
]
