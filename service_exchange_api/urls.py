from django.urls import include, path
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

app_name = 'service_exchange_api'

router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet)
router.register(r'providers', views.ProviderViewSet)
router.register(r'services', views.ServiceViewSet)

urlpatterns = [
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='service_exchange_api:schema'), name='swagger-ui'),
    path('', include(router.urls)),
]

