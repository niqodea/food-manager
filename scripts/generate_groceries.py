from weekly_meal_plan import WEEKLY_MEAL_PLAN

from food_manager.utils import get_ingredient_grams

ingredient_grams: dict[str, float] = {}
for daily_meal_plan in WEEKLY_MEAL_PLAN.dailies.values():
    for meal in daily_meal_plan.meals.values():
        for food in meal.foods.values():
            for ingredient, grams in get_ingredient_grams(food).items():
                ingredient_name = ingredient.as_named().name
                ingredient_grams[ingredient_name] = (
                    ingredient_grams.get(ingredient_name, 0.0) + grams
                )

print("Grocery list:")
for ingredient_name, grams in sorted(ingredient_grams.items(), key=lambda item: item[0]):
    print(f"{grams:6.0f}g {ingredient_name}")
