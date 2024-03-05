from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

from .views import (RecipeViewSet,
#                   RecipeRetrieve,
                    TagListRetrieve,
                    IngredientListRetrieve)

app_name = 'api'

router = DefaultRouter()

router.register(r'recipes', RecipeViewSet, basename='recipes')
router.register(r'tags', TagListRetrieve, basename='tags')
router.register(
    r'ingredients',
    IngredientListRetrieve,
    basename='ingredient'
    )

urlpatterns = [
    path('', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)