from __future__ import annotations

from dataclasses import dataclass

from food_manager.path import DATA_PATH
from food_manager.schema import (
    Category,
    CompositeSubstance,
    DailyMealPlan,
    Day,
    Meal,
    MealSlot,
    Nutrient,
    Ration,
    SimpleSubstance,
    Substance,
    WeeklyMealPlan,
    create_balloonist_factory,
)

balloonist_factory = create_balloonist_factory(DATA_PATH)


# --------------------------------------------------------------------------------------
# Global and weekly objects
categories = balloonist_factory.instantiate(Category)
substances = balloonist_factory.instantiate(Substance)
rations = balloonist_factory.instantiate(Ration)
meal_slots = balloonist_factory.instantiate(MealSlot)

weekly_categories: dict[str, Category] = {}
weekly_substances: dict[str, Substance] = {}
weekly_rations: dict[str, Ration] = {}
weekly_meal_slots: dict[str, MealSlot] = {}


def get_category(name: str) -> Category:
    if name in weekly_categories:
        return weekly_categories[name]
    else:
        return categories.get(name)


def get_substance(name: str) -> Substance:
    if name in weekly_substances:
        return weekly_substances[name]
    else:
        return substances.get(name)


def get_ration(name: str) -> Ration:
    if name in weekly_rations:
        return weekly_rations[name]
    else:
        return rations.get(name)


def get_meal_slot(name: str) -> MealSlot:
    if name in weekly_meal_slots:
        return weekly_meal_slots[name]
    else:
        return meal_slots.get(name)


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
        category_balloon = get_category(category)

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
        category_balloon = get_category(category)

    substance_balloon_proportions: list[tuple[Substance, float]] = []
    for substance, proportion in substance_proportions:
        if isinstance(substance, Substance):
            substance_balloon = substance
        elif isinstance(substance, str):
            substance_balloon = get_substance(substance)
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
        substance_balloon = get_substance(substance)

    return Ration(
        category=substance_balloon.category, substance=substance_balloon, grams=grams
    )


def create_ration_from_substances(
    category: Category | str, substance_grams: list[tuple[Substance | str, float]]
) -> Ration:
    if isinstance(category, Category):
        category_balloon = category
    elif isinstance(category, str):
        category_balloon = get_category(category)

    substance_balloon_grams: list[tuple[Substance, float]] = []
    for substance, grams in substance_grams:
        if isinstance(substance, Substance):
            substance_balloon = substance
        elif isinstance(substance, str):
            substance_balloon = get_substance(substance)
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
# Weekly meal plan helper creation methods
def create_weekly_meal_plan(
    monday: DailyMealPlan | None = None,
    tuesday: DailyMealPlan | None = None,
    wednesday: DailyMealPlan | None = None,
    thursday: DailyMealPlan | None = None,
    friday: DailyMealPlan | None = None,
    saturday: DailyMealPlan | None = None,
    sunday: DailyMealPlan | None = None,
) -> WeeklyMealPlan:
    dailies = {}
    if monday is not None:
        dailies[Day.MONDAY] = monday
    if tuesday is not None:
        dailies[Day.TUESDAY] = tuesday
    if wednesday is not None:
        dailies[Day.WEDNESDAY] = wednesday
    if thursday is not None:
        dailies[Day.THURSDAY] = thursday
    if friday is not None:
        dailies[Day.FRIDAY] = friday
    if saturday is not None:
        dailies[Day.SATURDAY] = saturday
    if sunday is not None:
        dailies[Day.SUNDAY] = sunday
    return WeeklyMealPlan(dailies=dailies)


def create_daily_meal_plan(*meals: Meal) -> DailyMealPlan:
    return DailyMealPlan(meals={meal.slot: meal for meal in meals})


def create_meal(meal_slot: MealSlot | str, rations: list[Ration | str]) -> Meal:
    if isinstance(meal_slot, MealSlot):
        meal_slot_balloon = meal_slot
    elif isinstance(meal_slot, str):
        meal_slot_balloon = get_meal_slot(meal_slot)

    ration_balloons: list[Ration] = []
    for ration in rations:
        if isinstance(ration, Ration):
            ration_balloons.append(ration)
        elif isinstance(ration, str):
            ration_balloons.append(get_ration(ration))

    return Meal(
        slot=meal_slot_balloon,
        rations={ration.category: ration for ration in ration_balloons},
    )
