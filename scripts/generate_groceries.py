from weekly_meal_plan import WEEKLY_MEAL_PLAN

from food_manager.utils import get_category_grams

category_grams: dict[str, float] = {}
for daily_meal_plan in WEEKLY_MEAL_PLAN.dailies.values():
    for meal in daily_meal_plan.meals.values():
        for food in meal.rations.values():
            for category, grams in get_category_grams(food).items():
                category_name = category.name
                category_grams[category_name] = (
                    category_grams.get(category_name, 0.0) + grams
                )

print("Grocery list:")
for category_name, grams in sorted(category_grams.items(), key=lambda item: item[0]):
    print(f"{grams:6.0f}g {category_name}")
