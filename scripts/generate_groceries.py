from weekly_meal_plan import WEEKLY_MEAL_PLAN

from food_manager.utils import get_food_type_grams

food_type_grams: dict[str, float] = {}
for daily_meal_plan in WEEKLY_MEAL_PLAN.dailies.values():
    for meal in daily_meal_plan.meals.values():
        for food in meal.foods.values():
            for food_type, grams in get_food_type_grams(food).items():
                food_type_name = food_type.as_named().name
                food_type_grams[food_type_name] = (
                    food_type_grams.get(food_type_name, 0.0) + grams
                )

print("Grocery list:")
for food_type_name, grams in sorted(food_type_grams.items(), key=lambda item: item[0]):
    print(f"{grams:6.0f}g {food_type_name}")
