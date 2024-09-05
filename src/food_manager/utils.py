from dataclasses import dataclass

from food_manager.schema import (
    DehydratedFoodMixture,
    CompositeFoodMixture,
    Food,
    FoodMixture,
    FoodType,
    MacroRatios,
    SimpleFoodMixture,
)


@dataclass(frozen=True)
class MacroGrams:
    """
    The grams of macronutrients in a food.
    """

    carb: float
    """
    The grams of carbohydrates in the food.
    """

    fat: float
    """
    The grams of fat in the food.
    """

    protein: float
    """
    The grams of protein in the food.
    """


def get_macro_ratios(food_mixture: FoodMixture) -> MacroRatios:
    if isinstance(food_mixture, SimpleFoodMixture):
        return food_mixture.macros
    if isinstance(food_mixture, CompositeFoodMixture):
        carb = 0.0
        fat = 0.0
        protein = 0.0
        total_proportion = 0.0
        for component in food_mixture.components.values():
            component_macro_ratios = get_macro_ratios(component.mixture)

            carb += component_macro_ratios.carb * component.proportion
            fat += component_macro_ratios.fat * component.proportion
            protein += component_macro_ratios.protein * component.proportion
            total_proportion += component.proportion
        carb /= total_proportion
        fat /= total_proportion
        protein /= total_proportion
        return MacroRatios(carb=carb, fat=fat, protein=protein)
    if isinstance(food_mixture, DehydratedFoodMixture):
        original_macro_ratios = get_macro_ratios(food_mixture.original_mixture)
        return MacroRatios(
            carb=original_macro_ratios.carb / food_mixture.dehydration_ratio,
            fat=original_macro_ratios.fat / food_mixture.dehydration_ratio,
            protein=original_macro_ratios.protein / food_mixture.dehydration_ratio,
        )
    raise ValueError(f"Unknown food mixture type: {food_mixture}")


def get_macro_grams(food: Food) -> MacroGrams:
    macro_ratios = get_macro_ratios(food.mixture)
    return MacroGrams(
        carb=food.grams * macro_ratios.carb,
        fat=food.grams * macro_ratios.fat,
        protein=food.grams * macro_ratios.protein,
    )


def get_calories(macro_grams: MacroGrams) -> float:
    return 4 * macro_grams.carb + 9 * macro_grams.fat + 4 * macro_grams.protein


def get_food_type_proportions(food_mixture: FoodMixture) -> dict[FoodType, float]:
    if isinstance(food_mixture, SimpleFoodMixture):
        return {food_mixture.type_: 1.0}
    if isinstance(food_mixture, CompositeFoodMixture):
        proportions: dict[FoodType, float] = {}
        total_proportion = 0.0
        for component in food_mixture.components.values():
            component_proportions = get_food_type_proportions(component.mixture)
            for food_type, proportion in component_proportions.items():
                proportions[food_type] = (
                    proportions.get(food_type, 0.0) + proportion * component.proportion
                )
            total_proportion += component.proportion
        for food_type in proportions:
            proportions[food_type] /= total_proportion
        return proportions
    if isinstance(food_mixture, DehydratedFoodMixture):
        original_proportions = get_food_type_proportions(food_mixture.original_mixture)
        return {
            food_type: proportion / food_mixture.dehydration_ratio
            for food_type, proportion in original_proportions.items()
        }
    raise ValueError(f"Unknown food mixture type: {food_mixture}")


def get_food_type_grams(food: Food) -> dict[FoodType, float]:
    food_type_proportions = get_food_type_proportions(food.mixture)
    return {
        food_type: food.grams * proportion
        for food_type, proportion in food_type_proportions.items()
    }
