from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.companies.views import CompanyViewSet
from apps.users.views import UserViewSet

router = DefaultRouter()
router.register(r'companies', CompanyViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
]
