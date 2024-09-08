from weekly_meal_plan import WEEKLY_MEAL_PLAN

from food_manager.schema import Nutrient
from food_manager.utils import get_calories, get_nutrient_grams

CARB_BUDGET_GRAMS = 20.0

GREEN = "\033[32m"
YELLOW = "\033[33m"

RESET = "\033[0m"

for day_name, daily_meal_plan in WEEKLY_MEAL_PLAN.dailies.items():
    if len(daily_meal_plan.meals) == 0:
        continue

    print(YELLOW, end="")
    print(f"{'-' * len(day_name)}")
    print(f"{day_name.upper()}")
    print(f"{'-' * len(day_name)}")
    print(RESET, end="")
    total_nutrient_grams: dict[Nutrient, float] = {}
    total_calories = 0.0
    for meal_type, meal in daily_meal_plan.meals.items():
        print(f"{YELLOW}{meal_type.capitalize()}:{RESET}")
        for ration in meal.rations.values():
            nutrient_grams = get_nutrient_grams(ration)
            calories = get_calories(nutrient_grams)

            print(f"  {GREEN}{ration.category.name}{RESET}: {calories:.0f} calories")
            for nutrient, grams in nutrient_grams.items():
                print(f"    {grams:6.1f}g {nutrient.name.lower()}", end="")

                if nutrient == Nutrient.CARB:
                    print(f" ({grams / CARB_BUDGET_GRAMS * 100:3.0f}%)")
                else:
                    print()

            for nutrient, grams in nutrient_grams.items():
                total_nutrient_grams[nutrient] = (
                    total_nutrient_grams.get(nutrient, 0.0) + grams
                )
            total_calories += calories

    print()
    print(f"Total: {total_calories:.0f} calories")
    for nutrient, total_grams in total_nutrient_grams.items():
        print(f"  {total_grams:6.1f}g {nutrient.name.lower()}", end="")
        if nutrient == Nutrient.CARB:
            print(f" ({total_grams / CARB_BUDGET_GRAMS * 100:3.0f}%)")
        else:
            print()
    print()
