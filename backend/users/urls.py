from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CustomUserViewSet, FollowViewSet

app_name = 'users'

router = DefaultRouter()

router.register(r'users', CustomUserViewSet, basename='users')
router.register(r'users/(?P<post_pk>\d+)/subscribe',
                FollowViewSet,
                basename='follows')


urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
