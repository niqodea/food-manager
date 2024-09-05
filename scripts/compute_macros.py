from weekly_meal_plan import WEEKLY_MEAL_PLAN

from food_manager.utils import get_calories, get_macro_grams

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
    total_calories = 0.0
    total_carb = 0.0
    total_fat = 0.0
    total_protein = 0.0
    for meal_type, meal in daily_meal_plan.meals.items():
        print(f"{YELLOW}{meal_type.capitalize()}:{RESET}")
        for ration in meal.rations.values():
            macro_grams = get_macro_grams(ration)
            calories = get_calories(macro_grams)

            category = ration.category.as_named().name
            carb_budget = macro_grams.carb / CARB_BUDGET_GRAMS * 100
            print(f"  {GREEN}{category}{RESET}: {calories:.0f} calories")
            print(f"    {macro_grams.carb:6.1f}g carb ({carb_budget:3.0f}%)")
            print(f"    {macro_grams.fat:6.1f}g fat")
            print(f"    {macro_grams.protein:6.1f}g protein")

            total_calories += calories
            total_carb += macro_grams.carb
            total_fat += macro_grams.fat
            total_protein += macro_grams.protein

    total_carb_budget = total_carb / CARB_BUDGET_GRAMS * 100
    print()
    print(f"Total: {total_calories:.0f} calories")
    print(f"    {total_carb:6.1f}g carb ({total_carb_budget:3.0f}%)")
    print(f"    {total_fat:6.1f}g fat")
    print(f"    {total_protein:6.1f}g protein")
    print()
