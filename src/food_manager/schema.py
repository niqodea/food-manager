from __future__ import annotations

from pathlib import Path

from balloons import Balloon, BalloonistFactory, balloon


def create_balloonist_factory(json_database_path: Path) -> BalloonistFactory:
    """
    Create a BalloonistFactory for the Food Manager schema.

    :param json_database_path: The path to the JSON database.
    """
    return BalloonistFactory.create(
        top_namespace_types={
            Food,
            FoodType,
            FoodMixture,
        },
        types_={
            Food,
            FoodType,
            FoodMixture,
            SimpleFoodMixture,
            DetailedFoodMixture,
            DetailedFoodMixture.Ingredient,
            DehydratedFoodMixture,
            MacroRatios,
        },
        json_database_path=json_database_path,
    )


@balloon
class Food(Balloon):
    """
    A food item.
    """

    type_: FoodType
    """
    The type of food.
    """
    mixture: FoodMixture
    """
    The mixture of the food.
    """
    grams: float
    """
    The weight of the food in grams.
    """


@balloon
class FoodType(Balloon):
    """
    A type of food.
    """


@balloon
class FoodMixture(Balloon):
    """
    A mixture making up a food item.
    """

    type_: FoodType
    """
    The type of food mixture.
    """


@balloon
class SimpleFoodMixture(FoodMixture):
    """
    A simple food mixture.
    """

    macros: MacroRatios
    """
    The macronutrient ratios of the food mixture.
    """


@balloon
class DetailedFoodMixture(FoodMixture):
    """
    A detailed food mixture.
    """

    @balloon
    class Ingredient(Balloon):
        """
        An ingredient in a detailed food mixture.
        """

        mixture: FoodMixture
        """
        The mixture of the ingredient.
        """
        proportion: float
        """
        The proportion of the ingredient in the detailed food mixture.
        """

    ingredients: dict[FoodType, Ingredient]
    """
    The ingredients in the detailed food mixture.
    """


@balloon
class DehydratedFoodMixture(FoodMixture):
    """
    A dehydrated food mixture.
    """

    original_mixture: FoodMixture
    """
    The original food mixture before dehydration.
    """
    dehydration_ratio: float
    """
    The dehydration ratio.
    """


@balloon
class MacroRatios(Balloon):
    """
    The ratios of macronutrients in a food.
    """

    carb: float
    """
    The ratio of carbohydrates in the food.
    """

    fat: float
    """
    The ratio of fat in the food.
    """

    protein: float
    """
    The ratio of protein in the food.
    """
