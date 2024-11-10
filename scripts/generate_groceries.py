import json

from food_manager.path import WORLD_PATH, CURRENT_WEEK_WORLD_PATH, CURRENT_WEEK_DATA_PATH
from food_manager.schema import WeeklyMealPlan, create_base_world
from food_manager.utils import get_category_grams

world = create_base_world().populate(WORLD_PATH).populate(CURRENT_WEEK_WORLD_PATH)
weekly_meal_plan_balloonist = world.get_balloonist(WeeklyMealPlan)
deflated_weekly_meal_plan = json.loads((CURRENT_WEEK_DATA_PATH / "meal-plan.json").read_text())
weekly_meal_plan = weekly_meal_plan_balloonist.inflate(deflated_weekly_meal_plan)

category_grams: dict[str, float] = {}
for daily_meal_plan in weekly_meal_plan.dailies.values():
    for meal in daily_meal_plan.meals.values():
        for food in meal.rations:
            for category, grams in get_category_grams(food).items():
                category_name = category.name
                category_grams[category_name] = (
                    category_grams.get(category_name, 0.0) + grams
                )

print("Grocery list:")
for category_name, grams in sorted(category_grams.items(), key=lambda item: item[0]):
    print(f"{grams:6.0f}g {category_name}")
