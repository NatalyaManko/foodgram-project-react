<<<<<<< HEAD
<<<<<<< HEAD
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import IngredientListRetrieve, RecipeViewSet, TagListRetrieve
=======
=======
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

from .views import (RecipeViewSet,
#                   RecipeRetrieve,
                    TagListRetrieve,
                    IngredientListRetrieve)
<<<<<<< HEAD
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
=======
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3

app_name = 'api'

router = DefaultRouter()

router.register(r'recipes', RecipeViewSet, basename='recipes')
router.register(r'tags', TagListRetrieve, basename='tags')
router.register(
    r'ingredients',
    IngredientListRetrieve,
    basename='ingredient'
<<<<<<< HEAD
<<<<<<< HEAD
)
=======
    )
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
=======
    )
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3

urlpatterns = [
    path('', include(router.urls)),
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
