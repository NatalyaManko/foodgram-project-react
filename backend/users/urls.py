from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from users.views import CustomUserViewSet
#from rest_framework.authtoken import views


app_name = 'users'

router = DefaultRouter()

router.register(r'users', CustomUserViewSet, basename='users')
#router.register(r'users/set_password', PasswordChangeViewSet, basename='passwords')


urlpatterns = [
#    path('v1/auth/signup/', APISignup.as_view(), name='signup'),
#    path('v1/auth/token/', APIGetToken, 'token'), 
    path('', include(router.urls)),
    #path('users/', include('djoser.urls')),
#    path('users/', include('djoser.urls.jwt')),
#    path('auth/token/login/', EmailTokenObtainPairView.as_view()),
    path('auth/', include('djoser.urls.authtoken')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)