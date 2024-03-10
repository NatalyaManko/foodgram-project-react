<<<<<<< HEAD
<<<<<<< HEAD
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import CustomUserViewSet
=======
=======
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from users.views import CustomUserViewSet
#from rest_framework.authtoken import views

<<<<<<< HEAD
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
=======
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3

app_name = 'users'

router = DefaultRouter()

router.register(r'users', CustomUserViewSet, basename='users')
<<<<<<< HEAD
<<<<<<< HEAD

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
=======
=======
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
#router.register(r'users/set_password', PasswordChangeViewSet, basename='passwords')


urlpatterns = [
#    path('v1/auth/signup/', APISignup.as_view(), name='signup'),
#    path('v1/auth/token/', APIGetToken, 'token'), 
    path('', include(router.urls)),
    #path('users/', include('djoser.urls')),
#    path('users/', include('djoser.urls.jwt')),
#    path('auth/token/login/', EmailTokenObtainPairView.as_view()),
<<<<<<< HEAD
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
=======
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
    path('auth/', include('djoser.urls.authtoken')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
<<<<<<< HEAD
<<<<<<< HEAD
                          document_root=settings.MEDIA_ROOT)
=======
                          document_root=settings.MEDIA_ROOT)
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
=======
                          document_root=settings.MEDIA_ROOT)
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
