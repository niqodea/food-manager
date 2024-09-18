import json

from food_manager.path import BALLOONS_PATH, CURRENT_WEEK_BALLOONS_PATH, CURRENT_WEEK_DATA_PATH
from food_manager.schema import Nutrient, WeeklyMealPlan, create_base_world
from food_manager.utils import get_kcal, get_nutrient_grams

world = create_base_world().populate(BALLOONS_PATH).populate(CURRENT_WEEK_BALLOONS_PATH)
weekly_meal_plan_balloonist = world.get_balloonist(WeeklyMealPlan)
deflated_weekly_meal_plan = json.loads((CURRENT_WEEK_DATA_PATH / "meal-plan.json").read_text())
weekly_meal_plan = weekly_meal_plan_balloonist.inflate(deflated_weekly_meal_plan)

CARB_BUDGET_GRAMS = 20.0

GREEN = "\033[32m"
YELLOW = "\033[33m"

RESET = "\033[0m"

for day, daily_meal_plan in weekly_meal_plan.dailies.items():
    if len(daily_meal_plan.meals) == 0:
        continue

    print(YELLOW, end="")
    print(f"{'-' * len(day.name)}")
    print(f"{day.name.upper()}")
    print(f"{'-' * len(day.name)}")
    print(RESET, end="")
    total_nutrient_grams: dict[Nutrient, float] = {}
    total_kcal = 0.0
    for meal_slot, meal in daily_meal_plan.meals.items():
        print(f"{YELLOW}{meal_slot.name.capitalize()}:{RESET}")
        for ration in meal.rations.values():
            nutrient_grams = get_nutrient_grams(ration)
            kcal = get_kcal(nutrient_grams)

            print(f"  {GREEN}{ration.category.name}{RESET}: {kcal:.0f} kcal")
            for nutrient in Nutrient:
                if (grams := nutrient_grams.get(nutrient)) is None:
                    continue

                print(f"    {grams:6.1f}g {nutrient.name.lower()}", end="")

                if nutrient == Nutrient.CARB:
                    print(f" ({grams / CARB_BUDGET_GRAMS * 100:3.0f}%)")
                else:
                    print()

            for nutrient, grams in nutrient_grams.items():
                total_nutrient_grams[nutrient] = (
                    total_nutrient_grams.get(nutrient, 0.0) + grams
                )
            total_kcal += kcal

    print()
    print(f"Total: {total_kcal:.0f} kcal")
    for nutrient in Nutrient:
        if (total_grams := total_nutrient_grams.get(nutrient)) is None:
            continue

        print(f"  {total_grams:6.1f}g {nutrient.name.lower()}", end="")

        if nutrient == Nutrient.CARB:
            print(f" ({total_grams / CARB_BUDGET_GRAMS * 100:3.0f}%)")
        else:
            print()

    print()
