from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from users.views import LoginView, LogoutView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('api/v1/', include('users.urls')),
                  path('api/v1/', include('clients.urls')),
                  path('auth/', include('djoser.urls')),
                  path('auth/', include('djoser.urls.jwt')),
                  path('', include('users.urls')),
                  path('', include('clients.urls')),
                  path('', include('products.urls')),
                  path('', include('orders.urls')),
                  path('', include('reviews.urls')),
                  path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
                  path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
                  path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
                  path('login/', LoginView.as_view()),
                  path('logout/', LogoutView.as_view()),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
