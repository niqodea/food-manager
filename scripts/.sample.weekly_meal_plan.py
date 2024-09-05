from __future__ import annotations

from dataclasses import dataclass

from food_manager.path import DATA_PATH
from food_manager.schema import (
    CompositeSubstance,
    Category,
    Ration,
    Substance,
    create_balloonist_factory,
)

balloonist_factory = create_balloonist_factory(DATA_PATH)

categories = balloonist_factory.instantiate(Category)
substances = balloonist_factory.instantiate(Substance)
rations = balloonist_factory.instantiate(Ration)


def make_weekly_meal_plan(
    monday: DailyMealPlan,
    tuesday: DailyMealPlan,
    wednesday: DailyMealPlan,
    thursday: DailyMealPlan,
    friday: DailyMealPlan,
    saturday: DailyMealPlan,
    sunday: DailyMealPlan,
) -> WeeklyMealPlan:
    return WeeklyMealPlan(
        dailies={
            "monday": monday,
            "tuesday": tuesday,
            "wednesday": wednesday,
            "thursday": thursday,
            "friday": friday,
            "saturday": saturday,
            "sunday": sunday,
        },
    )


@dataclass
class WeeklyMealPlan:
    dailies: dict[str, DailyMealPlan]


@dataclass
class DailyMealPlan:
    meals: dict[str, Meal]


@dataclass
class Meal:
    rations: dict[Category, Ration]


def make_daily_meal_plan(
    breakfast: dict[Category, Ration] | None = None,
    lunch: dict[Category, Ration] | None = None,
    dinner: dict[Category, Ration] | None = None,
) -> DailyMealPlan:
    meals = {}
    if breakfast is not None:
        meals["breakfast"] = Meal(rations=breakfast)
    if lunch is not None:
        meals["lunch"] = Meal(rations=lunch)
    if dinner is not None:
        meals["dinner"] = Meal(rations=dinner)
    return DailyMealPlan(meals=meals)


def index_rations(*rations: Ration) -> dict[Category, Ration]:
    indexed_rations = {ration.category: ration for ration in rations}
    if len(indexed_rations) < len(rations):
        raise ValueError("Found duplicate category")
    return indexed_rations


def get_ration_from_substance(substance: Substance, grams: float) -> Ration:
    return Ration(category=substance.type_, substance=substance, grams=grams)


def get_ration_from_substances(type_: Category, substance_grams: dict[Substance, float]) -> Ration:
    return Ration(
        category=type_,
        substance=CompositeSubstance(
            type_=type_,
            components={
                substance.type_: CompositeSubstance.Component(
                    substance=substance,
                    proportion=grams,
                )
                for substance, grams in substance_grams.items()
            },
        ),
        grams=sum(substance_grams.values()),
    )


WEEKLY_MEAL_PLAN = make_weekly_meal_plan(
    monday=make_daily_meal_plan(
        breakfast=index_rations(
            rations.get("greek-yogurt"),
            rations.get("coffee"),
        ),
        lunch=index_rations(
            get_ration_from_substance(
                substances.get("sauteed-chicken"),
                grams=260.0,
            ),
        ),
        dinner=index_rations(
            get_ration_from_substance(
                substances.get("sauteed-tuna"),
                grams=200.0,
            ),
        ),
    ),
    tuesday=make_daily_meal_plan(
        breakfast=index_rations(
            rations.get("banana"),
        ),
        lunch=index_rations(
            get_ration_from_substance(
                substances.get("salad"),
                grams=200.0,
            ),
        ),
        dinner=index_rations(
            get_ration_from_substance(
                substances.get("eggplant-parmesan"),
                grams=250.0,
            ),
            rations.get("coffee"),
        ),
    ),
    wednesday=make_daily_meal_plan(
        # breakfast=index_rations(),
        # lunch=index_rations(),
        # dinner=index_rations(),
    ),
    thursday=make_daily_meal_plan(
        # breakfast=index_rations(),
        # lunch=index_rations(),
        # dinner=index_rations(),
    ),
    friday=make_daily_meal_plan(
        # breakfast=index_rations(),
        # lunch=index_rations(),
        # dinner=index_rations(),
    ),
    saturday=make_daily_meal_plan(
        # breakfast=index_rations(),
        # lunch=index_rations(),
        # dinner=index_rations(),
    ),
    sunday=make_daily_meal_plan(
        # breakfast=index_rations(),
        # lunch=index_rations(),
        # dinner=index_rations(),
    ),
)
