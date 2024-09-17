from __future__ import annotations

from enum import Enum, auto
from pathlib import Path

from balloons import Balloon, ClosedBalloonWorld, NamedBalloon, balloon


# --------------------------------------------------------------------------------------
@balloon
class Category(NamedBalloon):
    """
    A food category.
    """


# --------------------------------------------------------------------------------------
class Nutrient(Enum):
    """
    A nutrient.
    """

    CARB = auto()
    FAT = auto()
    PROTEIN = auto()
    ETHANOL = auto()


# --------------------------------------------------------------------------------------
@balloon
class Substance(Balloon):
    """
    A food substance.
    """

    category: Category
    """
    The category of the food substance.
    """


@balloon
class SimpleSubstance(Substance):
    """
    A simple food substance.
    """

    nutrient_ratios: dict[Nutrient, float]
    """
    The macronutrient ratios of the substance.
    """


@balloon
class CompositeSubstance(Substance):
    """
    A composite food substance.
    """

    @balloon
    class Component(Balloon):
        """
        A component in the composite substance.
        """

        substance: Substance
        """
        The substance of the component.
        """
        proportion: float
        """
        The proportion of the component in the composite substance.
        """

    components: dict[Category, Component]
    """
    The components in the composite substance.
    """


@balloon
class DehydratedSubstance(Substance):
    """
    A dehydrated food substance.
    """

    original_substance: Substance
    """
    The original substance before dehydration.
    """
    dehydration_ratio: float
    """
    The dehydration ratio.
    """


# --------------------------------------------------------------------------------------
@balloon
class Ration(Balloon):
    """
    A food ration.
    """

    category: Category
    """
    The category of the ration.
    """
    substance: Substance
    """
    The substance of the ration.
    """
    grams: float
    """
    The weight of the ration in grams.
    """


# --------------------------------------------------------------------------------------
@balloon
class MealSlot(NamedBalloon):
    """
    A meal slot (e.g. breakfast).
    """


@balloon
class Meal(Balloon):
    """
    A meal.
    """

    slot: MealSlot
    """
    The slot of the meal.
    """

    rations: dict[Category, Ration]
    """
    The rations of the meal
    """


@balloon
class DailyMealPlan(Balloon):
    """
    A daily meal plan.
    """

    meals: dict[MealSlot, Meal]
    """
    The meals of the day.
    """


class Day(Enum):
    """
    A day of the week.
    """

    MONDAY = auto()
    TUESDAY = auto()
    WEDNESDAY = auto()
    THURSDAY = auto()
    FRIDAY = auto()
    SATURDAY = auto()
    SUNDAY = auto()


@balloon
class WeeklyMealPlan(Balloon):
    """
    A weekly meal plan.
    """

    dailies: dict[Day, DailyMealPlan]
    """
    The daily meal plans of the week.
    """




# --------------------------------------------------------------------------------------
@balloon
class Money(Balloon):
    """
    An amount of money.
    """

    units: int
    """
    The amount of money units.
    """
    cents: int
    """
    The amount of money cents.
    """


@balloon
class Product(Balloon):
    """
    A grocery product.
    """


@balloon
class RationProduct(Product):
    """
    A grocery product for a ration.
    """

    item: Ration
    """
    The ration of the product.
    """

    price: Money
    """
    The price of the product.
    """


@balloon
class SubstanceProduct(Product):
    """
    A grocery product for a substance.
    """

    item: Substance
    """
    The substance of the product.
    """

    kg_price: Money
    """
    The price of the product per kilogram.
    """


# --------------------------------------------------------------------------------------
def create_base_world() -> ClosedBalloonWorld:
    """
    Create a base world for the Food Manager schema.
    """
    return ClosedBalloonWorld.create(
        namespace_types={
            Category,
            Substance,
            Ration,
            Product,
            MealSlot,
            WeeklyMealPlan,
        },
        types_={
            Category,
            Substance,
            SimpleSubstance,
            CompositeSubstance,
            CompositeSubstance.Component,
            DehydratedSubstance,
            Ration,
            Meal,
            MealSlot,
            DailyMealPlan,
            WeeklyMealPlan,
            Money,
            Product,
            RationProduct,
            SubstanceProduct,
        },
    )
