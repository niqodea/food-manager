from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass

from food_manager.schema import (
    DehydratedSubstance,
    CompositeSubstance,
    Ration,
    Money,
    Nutrient,
    Product,
    RationProduct,
    SubstanceProduct,
    Substance,
    Category,
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


def get_nutrient_ratios(substance: Substance) -> dict[Nutrient, float]:
    if isinstance(substance, SimpleSubstance):
        return substance.nutrient_ratios
    if isinstance(substance, CompositeSubstance):
        nutrient_ratios: dict[Nutrient, float] = defaultdict(float)
        total_proportion = 0.0
        for component in substance.components.values():
            component_nutrient_ratios = get_nutrient_ratios(component.substance)
            for nutrient, ratio in component_nutrient_ratios.items():
                nutrient_ratios[nutrient] += ratio * component.proportion
            total_proportion += component.proportion
        nutrient_ratios = {n: r / total_proportion for n, r in nutrient_ratios.items()}
        return nutrient_ratios
    if isinstance(substance, DehydratedSubstance):
        original_nutrient_ratios = get_nutrient_ratios(substance.original_substance)
        return {
            nutrient: original_ratio / substance.dehydration_ratio
            for nutrient, original_ratio in original_nutrient_ratios.items()
        }
    raise ValueError(f"Unknown substance type: {substance}")


def get_nutrient_grams(ration: Ration) -> dict[Nutrient, float]:
    nutrient_ratios = get_nutrient_ratios(ration.substance)
    return {nutrient: ration.grams * ratio for nutrient, ratio in nutrient_ratios.items()}


def get_calories(nutrient_grams: dict[Nutrient, float]) -> float:
    return (
        4 * nutrient_grams.get(Nutrient.CARB, 0.0)
        + 9 * nutrient_grams.get(Nutrient.FAT, 0.0)
        + 4 * nutrient_grams.get(Nutrient.PROTEIN, 0.0)
        + 7 * nutrient_grams.get(Nutrient.ETHANOL, 0.0)
    )


# --------------------------------------------------------------------------------------


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


# --------------------------------------------------------------------------------------


def sum_money(*money: Money) -> Money:
    unit_sum = sum(m.units for m in money)
    cent_sum = sum(m.cents for m in money)
    units = unit_sum + cent_sum // 100
    cents = cent_sum % 100
    return Money(units=units, cents=cents)


def multiply(money: Money, factor: float) -> Money:
    original_total_cents = money.units * 100 + money.cents
    total_cents = round(original_total_cents * factor)
    units = total_cents // 100
    cents = total_cents % 100
    return Money(units=units, cents=cents)


class PriceCalculator:

    def __init__(self, substance_products: list[SubstanceProduct]):
        self._substance_products = substance_products

    def get_kg_price(self, substance: Substance) -> Money:
        for product in self._substance_products:
            if product.item is substance:
                return product.kg_price

        if isinstance(substance, SimpleSubstance):
            raise ValueError(f"Missing price for substance: {substance}")

        if isinstance(substance, DehydratedSubstance):
            original_kg_price = self.get_kg_price(substance.original_substance)
            kg_price = multiply(original_kg_price, 1 / substance.dehydration_ratio)
            return kg_price

        if isinstance(substance, CompositeSubstance):
            total_kg_price = Money(0, 0)
            total_proportion = 0.0
            for component in substance.components.values():
                kg_price = self.get_kg_price(component.substance)
                proportional_kg_price = multiply(kg_price, component.proportion)
                total_kg_price = sum_money(total_kg_price, proportional_kg_price)
                total_proportion += component.proportion
            total_kg_price = multiply(total_kg_price, 1 / total_proportion)
            return total_kg_price

        raise ValueError(f"Unknown substance type: {substance}")

    def get_price(self, ration: Ration) -> Money:
        kg_price = self.get_kg_price(ration.substance)
        kg = ration.grams / 1000
        price = multiply(kg_price, kg)
        return price


    @staticmethod
    def create(products: list[Product]) -> PriceCalculator:
        substance_products = []
        for product in products:
            if isinstance(product, SubstanceProduct):
                substance_products.append(product)
            elif isinstance(product, RationProduct):
                substance = product.item.substance
                kgs = product.item.grams / 1000
                kg_price = multiply(product.price, 1 / kgs)
                substance_products.append(SubstanceProduct(item=substance, kg_price=kg_price))
            else:
                raise ValueError(f"Unknown product type: {product}")

        return PriceCalculator(substance_products)
