from __future__ import annotations

from dataclasses import dataclass

from food_manager.path import JSON_DATABASE_PATH
from food_manager.schema import (
    CompositeFoodMixture,
    Food,
    FoodMixture,
    FoodType,
    create_balloonist_factory,
)

balloonist_factory = create_balloonist_factory(JSON_DATABASE_PATH)

food_types = balloonist_factory.instantiate(FoodType)
food_mixtures = balloonist_factory.instantiate(FoodMixture)
foods = balloonist_factory.instantiate(Food)


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
    foods: dict[FoodType, Food]


def make_daily_meal_plan(
    breakfast: dict[FoodType, Food] | None = None,
    lunch: dict[FoodType, Food] | None = None,
    dinner: dict[FoodType, Food] | None = None,
) -> DailyMealPlan:
    meals = {}
    if breakfast is not None:
        meals["breakfast"] = Meal(foods=breakfast)
    if lunch is not None:
        meals["lunch"] = Meal(foods=lunch)
    if dinner is not None:
        meals["dinner"] = Meal(foods=dinner)
    return DailyMealPlan(meals=meals)


def index_foods(*foods: Food) -> dict[FoodType, Food]:
    indexed_foods = {food.type_: food for food in foods}
    if len(indexed_foods) < len(foods):
        raise ValueError("Duplicate food types")
    return indexed_foods


def portion_food(food_mixture: FoodMixture, grams: float) -> Food:
    return Food(type_=food_mixture.type_, mixture=food_mixture, grams=grams)


def blend_food(type_: FoodType, food_mixture_grams: dict[FoodMixture, float]) -> Food:
    return Food(
        type_=type_,
        mixture=CompositeFoodMixture(
            type_=type_,
            components={
                food_mixture.type_: CompositeFoodMixture.Component(
                    mixture=food_mixture,
                    proportion=grams,
                )
                for food_mixture, grams in food_mixture_grams.items()
            },
        ),
        grams=sum(food_mixture_grams.values()),
    )


WEEKLY_MEAL_PLAN = make_weekly_meal_plan(
    monday=make_daily_meal_plan(
        breakfast=index_foods(
            foods.get("greek-yogurt"),
            foods.get("coffee"),
        ),
        lunch=index_foods(
            portion_food(
                food_mixtures.get("sauteed-chicken"),
                grams=260.0,
            ),
        ),
        dinner=index_foods(
            portion_food(
                food_mixtures.get("sauteed-tuna"),
                grams=200.0,
            ),
        ),
    ),
    tuesday=make_daily_meal_plan(
        breakfast=index_foods(
            foods.get("banana"),
        ),
        lunch=index_foods(
            portion_food(
                food_mixtures.get("salad"),
                grams=200.0,
            ),
        ),
        dinner=index_foods(
            portion_food(
                food_mixtures.get("eggplant-parmesan"),
                grams=250.0,
            ),
            foods.get("coffee"),
        ),
    ),
    wednesday=make_daily_meal_plan(
        # breakfast=index_foods(),
        # lunch=index_foods(),
        # dinner=index_foods(),
    ),
    thursday=make_daily_meal_plan(
        # breakfast=index_foods(),
        # lunch=index_foods(),
        # dinner=index_foods(),
    ),
    friday=make_daily_meal_plan(
        # breakfast=index_foods(),
        # lunch=index_foods(),
        # dinner=index_foods(),
    ),
    saturday=make_daily_meal_plan(
        # breakfast=index_foods(),
        # lunch=index_foods(),
        # dinner=index_foods(),
    ),
    sunday=make_daily_meal_plan(
        # breakfast=index_foods(),
        # lunch=index_foods(),
        # dinner=index_foods(),
    ),
)
