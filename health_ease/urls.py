"""
URL configuration for health_ease project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views. Home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from health_ease.settings import settings
from  health_ease.settings import dev

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('users/', include('users.urls')),
    path('doctors/', include('doctors.urls')),
    path('vitals/', include('vitals.urls')),
    path('patients/', include('patients.urls')),
    path('appointments/', include('appointment.urls')),
    path('pharmacies/', include('pharmacies.urls')),
    path('wallet/', include('wallet.urls')),
    path('labs/', include('labs.urls')),
    path('documentation/', include('clinical_documentation.urls')),
]


if dev.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)