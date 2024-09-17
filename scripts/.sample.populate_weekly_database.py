from __future__ import annotations

from dataclasses import dataclass

from food_manager.path import GLOBAL_DATABASE_PATH, WEEKLY_DATABASES_PATH
from food_manager.schema import (
    Category,
    CompositeSubstance,
    DailyMealPlan,
    Day,
    Meal,
    MealSlot,
    Nutrient,
    Product,
    Ration,
    SimpleSubstance,
    Substance,
    WeeklyMealPlan,
    create_base_world,
)
from food_manager.utils import PriceCalculator

WEEK = "current"

world = create_base_world().populate(GLOBAL_DATABASE_PATH).to_open(WEEKLY_DATABASES_PATH / WEEK)

category_balloonist = world.get_balloonist(Category)
substance_balloonist = world.get_balloonist(Substance)
ration_balloonist = world.get_balloonist(Ration)
meal_slot_balloonist = world.get_balloonist(MealSlot)
product_balloonist = world.get_balloonist(Product)

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
        category_balloon = category_balloonist.get(category)

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
        category_balloon = category_balloonist.get(category)

    substance_balloon_proportions: list[tuple[Substance, float]] = []
    for substance, proportion in substance_proportions:
        if isinstance(substance, Substance):
            substance_balloon = substance
        elif isinstance(substance, str):
            substance_balloon = substance_balloonist.get(substance)
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
        substance_balloon = substance_balloonist.get(substance)

    return Ration(
        category=substance_balloon.category, substance=substance_balloon, grams=grams
    )


def create_ration_from_substances(
    category: Category | str, substance_grams: list[tuple[Substance | str, float]]
) -> Ration:
    if isinstance(category, Category):
        category_balloon = category
    elif isinstance(category, str):
        category_balloon = category_balloonist.get(category)

    substance_balloon_grams: list[tuple[Substance, float]] = []
    for substance, grams in substance_grams:
        if isinstance(substance, Substance):
            substance_balloon = substance
        elif isinstance(substance, str):
            substance_balloon = substance_balloonist.get(substance)
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
        meal_slot_balloon = meal_slot_balloonist.get(meal_slot)

    ration_balloons: list[Ration] = []
    for ration in rations:
        if isinstance(ration, Ration):
            ration_balloons.append(ration)
        elif isinstance(ration, str):
            ration_balloons.append(ration_balloonist.get(ration))

    return Meal(
        slot=meal_slot_balloon,
        rations={ration.category: ration for ration in ration_balloons},
    )


# --------------------------------------------------------------------------------------
# Weekly object creation

ration_balloonist.track(
    create_ration_from_substance(
        substance="eggplant-parmesan", grams=250.0
    ).to_named("prepped-eggplant-parmesan")
)

# --------------------------------------------------------------------------------------
# Weekly meal plan

weekly_meal_plan = create_weekly_meal_plan(
    monday=create_daily_meal_plan(
        create_meal(
            "breakfast",
            rations=[
                "greek-yogurt",
                "coffee",
            ],
        ),
        create_meal(
            "lunch",
            rations=[
                create_ration_from_substance("sauteed-chicken", grams=260.0),
            ],
        ),
        create_meal(
            "dinner",
            rations=[
                create_ration_from_substance("sauteed-tuna", grams=200.0),
            ],
        ),
    ),
    tuesday=create_daily_meal_plan(
        create_meal(
            "breakfast",
            rations=[
                "banana",
            ],
        ),
        create_meal(
            "lunch",
            rations=[
                create_ration_from_substance("salad", grams=200.0),
            ],
        ),
        create_meal(
            "dinner",
            rations=[
                "prepped-eggplant-parmesan",
                "coffee",
            ],
        )
    ),
#     wednesday=create_daily_meal_plan(
#         create_meal(
#             "breakfast",
#             rations=[
#             ],
#         ),
#         create_meal(
#             "lunch",
#             rations=[
#             ],
#         ),
#         create_meal(
#             "dinner",
#             rations=[
#             ],
#         ),
#     ),
#     thursday=create_daily_meal_plan(
#         create_meal(
#             "breakfast",
#             rations=[
#             ],
#         ),
#         create_meal(
#             "lunch",
#             rations=[
#             ],
#         ),
#         create_meal(
#             "dinner",
#             rations=[
#             ],
#         ),
#     ),
#     friday=create_daily_meal_plan(
#         create_meal(
#             "breakfast",
#             rations=[
#             ],
#         ),
#         create_meal(
#             "lunch",
#             rations=[
#             ],
#         ),
#         create_meal(
#             "dinner",
#             rations=[
#             ],
#         ),
#     ),
#     saturday=create_daily_meal_plan(
#         create_meal(
#             "breakfast",
#             rations=[
#             ],
#         ),
#         create_meal(
#             "lunch",
#             rations=[
#             ],
#         ),
#         create_meal(
#             "dinner",
#             rations=[
#             ],
#         ),
#     ),
#     sunday=create_daily_meal_plan(
#         create_meal(
#             "breakfast",
#             rations=[
#             ],
#         ),
#         create_meal(
#             "lunch",
#             rations=[
#             ],
#         ),
#         create_meal(
#             "dinner",
#             rations=[
#             ],
#         ),
#     ),
).to_named("singleton")

weekly_meal_plan_tracker = world.get_tracker(WeeklyMealPlan)
weekly_meal_plan_tracker.track(weekly_meal_plan)
