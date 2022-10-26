from django.contrib import admin
from django.urls import path, include
# from core.views import register
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('products/', products),
    path('users/', include('users.urls')), # users/check-user
    path('', include('core.urls')),
    # path('register', register), # localhost:8000/register -> localhost:8000/register/
    # path('core/bye', bye)
    # path('')
]

# if not settings.DEBUG:
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
