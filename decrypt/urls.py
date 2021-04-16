"""decrypt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from keyform import views as keyform_views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls
from rest_framework.permissions import IsAuthenticated
from django.conf.urls import include, url


schema_view = get_schema_view(title='bank-api')


urlpatterns = [
    url(r'^docs/', include_docs_urls(title='bank-api', permission_classes=(IsAuthenticated,))),
    path('key/', include('key.urls')),
    path('admin/', admin.site.urls, name='admin'),
    path('',keyform_views.home,name='home'),
    path('keyform/', include('keyform.urls')),
    path('bank/', include('bank.urls')),
    path('core/', include('core.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)