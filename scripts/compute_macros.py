from weekly_meal_plan import WEEKLY_MEAL_PLAN

from food_manager.utils import get_calories, get_macro_grams

CARB_BUDGET_GRAMS = 20.0

for day_name, daily_meal_plan in WEEKLY_MEAL_PLAN.dailies.items():
    if len(daily_meal_plan.meals) == 0:
        continue

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

            carb_budget = macro_grams.carb / CARB_BUDGET_GRAMS * 100
            print(f"  {food.type_.as_named().name}: {calories:.0f} calories")
            print(f"    {macro_grams.carb:6.1f}g carbs ({carb_budget:3.0f}%)")
            print(f"    {macro_grams.fat:6.1f}g fat")
            print(f"    {macro_grams.protein:6.1f}g protein")

            total_calories += calories
            total_carbs += macro_grams.carb
            total_fat += macro_grams.fat
            total_protein += macro_grams.protein

    total_carb_budget = total_carbs / CARB_BUDGET_GRAMS * 100
    print("-" * 20)
    print(f"  Total: {total_calories:.0f} calories")
    print(f"    {total_carbs:6.1f}g carbs ({total_carb_budget:3.0f}%)")
    print(f"    {total_fat:6.1f}g fat")
    print(f"    {total_protein:6.1f}g protein")
    print()
