from rest_framework import serializers

from ingredients.models import Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор Ингредиентов"""

    measurement_unit = serializers.StringRelatedField(read_only=True,
                                                      many=False)

    class Meta:
        model = Ingredient
        fields = '__all__'
