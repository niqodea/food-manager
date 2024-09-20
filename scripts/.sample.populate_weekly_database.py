from __future__ import annotations

from dataclasses import dataclass

from food_manager.path import WORLD_PATH, CURRENT_WEEK_WORLD_PATH
from food_manager.schema import (
    Category,
    CompositeSubstance,
    Day,
    Meal,
    MealSlot,
    Nutrient,
    Product,
    Ration,
    SimpleSubstance,
    Substance,
    create_base_world,
)
from food_manager.utils import PriceCalculator

world = create_base_world().populate(WORLD_PATH).to_open(CURRENT_WEEK_WORLD_PATH)

category_manager = world.get_manager(Category)
substance_manager = world.get_manager(Substance)
ration_manager = world.get_manager(Ration)
meal_slot_manager = world.get_manager(MealSlot)
product_manager = world.get_manager(Product)

# --------------------------------------------------------------------------------------
# Helper methods to easily create weekly objects with minimal boilerplate
def create_category(name: str) -> Category:
    return Category(name=name)


def create_simple_substance(
    category: Category | str,
    carb: float | None = None,
    fat: float | None = None,
    protein: float | None = None,
    ethanol: float | None = None,
) -> SimpleSubstance:
    if isinstance(category, Category):
        category_balloon = category
    elif isinstance(category, str):
        category_balloon = category_manager.get(category)

    nutrient_ratios: dict[Nutrient, float] = {}
    if carb is not None:
        nutrient_ratios[Nutrient.CARB] = carb
    if fat is not None:
        nutrient_ratios[Nutrient.FAT] = fat
    if protein is not None:
        nutrient_ratios[Nutrient.PROTEIN] = protein
    if ethanol is not None:
        nutrient_ratios[Nutrient.ETHANOL] = ethanol

    return SimpleSubstance(
        category=category_balloon,
        nutrient_ratios=nutrient_ratios,
    )


def create_composite_substance(
    category: Category | str, substance_proportions: list[tuple[Substance | str, float]]
) -> CompositeSubstance:
    if isinstance(category, Category):
        category_balloon = category
    elif isinstance(category, str):
        category_balloon = category_manager.get(category)

    substance_balloon_proportions: list[tuple[Substance, float]] = []
    for substance, proportion in substance_proportions:
        if isinstance(substance, Substance):
            substance_balloon = substance
        elif isinstance(substance, str):
            substance_balloon = substance_manager.get(substance)
        substance_balloon_proportions.append((substance_balloon, proportion))

    return CompositeSubstance(
        category=category_balloon,
        components={
            substance_balloon.category: CompositeSubstance.Component(
                substance=substance_balloon, proportion=proportion
            )
            for substance_balloon, proportion in substance_balloon_proportions
        },
    )


def create_ration_from_substance(substance: Substance | str, grams: float) -> Ration:
    if isinstance(substance, Substance):
        substance_balloon = substance
    elif isinstance(substance, str):
        substance_balloon = substance_manager.get(substance)

    return Ration(
        category=substance_balloon.category, substance=substance_balloon, grams=grams
    )


def create_ration_from_substances(
    category: Category | str, substance_grams: list[tuple[Substance | str, float]]
) -> Ration:
    if isinstance(category, Category):
        category_balloon = category
    elif isinstance(category, str):
        category_balloon = category_manager.get(category)

    substance_balloon_grams: list[tuple[Substance, float]] = []
    for substance, grams in substance_grams:
        if isinstance(substance, Substance):
            substance_balloon = substance
        elif isinstance(substance, str):
            substance_balloon = substance_manager.get(substance)
        substance_balloon_grams.append((substance_balloon, grams))

    return Ration(
        category=category_balloon,
        substance=CompositeSubstance(
            category=category_balloon,
            components={
                substance_balloon.category: CompositeSubstance.Component(
                    substance=substance_balloon, proportion=grams
                )
                for substance_balloon, grams in substance_balloon_grams
            },
        ),
        grams=sum(grams for _, grams in substance_balloon_grams),
    )


def create_meal_slot(name: str) -> MealSlot:
    return MealSlot(name=name)


# --------------------------------------------------------------------------------------
# Weekly object creation

ration_balloonist.track(
    create_ration_from_substance(
        substance="eggplant-parmesan", grams=250.0
    ).to_named("prepped-eggplant-parmesan")
)
