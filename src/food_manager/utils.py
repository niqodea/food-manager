from dataclasses import dataclass

from food_manager.schema import (
    DehydratedSubstance,
    CompositeSubstance,
    Ration,
    Substance,
    Category,
    MacroRatios,
    SimpleSubstance,
)


@dataclass(frozen=True)
class MacroGrams:
    """
    Grams of macronutrients.
    """

    carb: float
    """
    The grams of carbohydrates.
    """

    fat: float
    """
    The grams of fat.
    """

    protein: float
    """
    The grams of protein.
    """


def get_macro_ratios(substance: Substance) -> MacroRatios:
    if isinstance(substance, SimpleSubstance):
        return substance.macros
    if isinstance(substance, CompositeSubstance):
        carb = 0.0
        fat = 0.0
        protein = 0.0
        total_proportion = 0.0
        for component in substance.components.values():
            component_macro_ratios = get_macro_ratios(component.substance)

            carb += component_macro_ratios.carb * component.proportion
            fat += component_macro_ratios.fat * component.proportion
            protein += component_macro_ratios.protein * component.proportion
            total_proportion += component.proportion
        carb /= total_proportion
        fat /= total_proportion
        protein /= total_proportion
        return MacroRatios(carb=carb, fat=fat, protein=protein)
    if isinstance(substance, DehydratedSubstance):
        original_macro_ratios = get_macro_ratios(substance.original_substance)
        return MacroRatios(
            carb=original_macro_ratios.carb / substance.dehydration_ratio,
            fat=original_macro_ratios.fat / substance.dehydration_ratio,
            protein=original_macro_ratios.protein / substance.dehydration_ratio,
        )
    raise ValueError(f"Unknown substance type: {substance}")


def get_macro_grams(ration: Ration) -> MacroGrams:
    macro_ratios = get_macro_ratios(ration.substance)
    return MacroGrams(
        carb=ration.grams * macro_ratios.carb,
        fat=ration.grams * macro_ratios.fat,
        protein=ration.grams * macro_ratios.protein,
    )


def get_calories(macro_grams: MacroGrams) -> float:
    return 4 * macro_grams.carb + 9 * macro_grams.fat + 4 * macro_grams.protein


def get_category_proportions(substance: Substance) -> dict[Category, float]:
    if isinstance(substance, SimpleSubstance):
        return {substance.category: 1.0}
    if isinstance(substance, CompositeSubstance):
        proportions: dict[Category, float] = {}
        total_proportion = 0.0
        for component in substance.components.values():
            component_proportions = get_category_proportions(component.substance)
            for category, proportion in component_proportions.items():
                proportions[category] = (
                    proportions.get(category, 0.0) + proportion * component.proportion
                )
            total_proportion += component.proportion
        for category in proportions:
            proportions[category] /= total_proportion
        return proportions
    if isinstance(substance, DehydratedSubstance):
        original_proportions = get_category_proportions(substance.original_substance)
        return {
            category: proportion / substance.dehydration_ratio
            for category, proportion in original_proportions.items()
        }
    raise ValueError(f"Unknown substance type: {substance}")


def get_category_grams(ration: Ration) -> dict[Category, float]:
    category_proportions = get_category_proportions(ration.substance)
    return {
        category: ration.grams * proportion
        for category, proportion in category_proportions.items()
    }
