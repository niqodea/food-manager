from __future__ import annotations

from dataclasses import dataclass

from food_manager.path import JSON_DATABASE_PATH
from food_manager.schema import Food, FoodMixture, FoodType, create_balloonist_factory
from food_manager.utils import get_calories, get_food_type_grams, get_macro_grams

balloonist_factory = create_balloonist_factory(JSON_DATABASE_PATH)

food_mixture_balloonist = balloonist_factory.instantiate(FoodMixture)
food_balloonist = balloonist_factory.instantiate(Food)


def index_foods(*foods: Food) -> dict[FoodType, Food]:
    return {food.type_: food for food in foods}


def make_food(food_mixture: FoodMixture, grams: float) -> Food:
    return Food(type_=food_mixture.type_, mixture=food_mixture, grams=grams)


@dataclass
class WeeklyMealPlan:
    dailies: dict[str, DailyMealPlan]


@dataclass
class DailyMealPlan:
    meals: dict[str, Meal]


@dataclass
class Meal:
    foods: dict[FoodType, Food]


weekly_meal_plan = WeeklyMealPlan(
    dailies={
        "monday": DailyMealPlan(
            meals={
                "breakfast": Meal(
                    foods=index_foods(
                        food_balloonist.get("greek-yogurt"),
                        food_balloonist.get("coffee"),
                    )
                ),
                "lunch": Meal(
                    foods=index_foods(
                        make_food(
                            food_mixture_balloonist.get("sauteed-chicken"),
                            grams=260.0,
                        ),
                    )
                ),
                "dinner": Meal(
                    foods=index_foods(
                        make_food(
                            food_mixture_balloonist.get("sauteed-tuna"),
                            grams=200.0,
                        ),
                    )
                ),
            }
        ),
        "tuesday": DailyMealPlan(
            meals={
                "breakfast": Meal(
                    foods=index_foods(
                        food_balloonist.get("banana"),
                    )
                ),
                "lunch": Meal(
                    foods=index_foods(
                        make_food(
                            food_mixture_balloonist.get("salad"),
                            grams=200.0,
                        ),
                    )
                ),
                "dinner": Meal(
                    foods=index_foods(
                        make_food(
                            food_mixture_balloonist.get("eggplant-parmesan"),
                            grams=250.0,
                        ),
                        food_balloonist.get("coffee"),
                    )
                ),
            }
        ),
    },
)

for day_name, daily_meal_plan in weekly_meal_plan.dailies.items():
    print(f"{day_name.upper()}")
    print("-" * 20)
    total_calories = 0.0
    total_carbs = 0.0
    total_fat = 0.0
    total_protein = 0.0
    for meal_type, meal in daily_meal_plan.meals.items():
        print(f"{meal_type.capitalize()}:")
        for food in meal.foods.values():
            macro_grams = get_macro_grams(food)
            calories = get_calories(macro_grams)

            print(f"  {food.type_.as_named().name}: {calories:.0f} calories")
            print(f"    {macro_grams.carb:6.1f}g carbs")
            print(f"    {macro_grams.fat:6.1f}g fat")
            print(f"    {macro_grams.protein:6.1f}g protein")

            total_calories += calories
            total_carbs += macro_grams.carb
            total_fat += macro_grams.fat
            total_protein += macro_grams.protein

    print("-" * 20)
    print(f"  Total: {total_calories:.0f} calories")
    print(f"    {total_carbs:6.1f}g carbs")
    print(f"    {total_fat:6.1f}g fat")
    print(f"    {total_protein:6.1f}g protein")
    print()

food_type_grams: dict[FoodType, float] = {}
for daily_meal_plan in weekly_meal_plan.dailies.values():
    for meal in daily_meal_plan.meals.values():
        for food in meal.foods.values():
            for food_type, grams in get_food_type_grams(food).items():
                food_type_grams[food_type] = food_type_grams.get(food_type, 0.0) + grams

print("Food type grams:")
for food_type, grams in food_type_grams.items():
    print(f"{grams:6.0f}g {food_type.as_named().name}")
print()
