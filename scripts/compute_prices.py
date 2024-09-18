import json

from food_manager.path import BALLOONS_PATH, CURRENT_WEEK_BALLOONS_PATH, CURRENT_WEEK_DATA_PATH
from food_manager.schema import Product, WeeklyMealPlan, create_base_world
from food_manager.utils import Money, PriceCalculator, get_category_grams, sum_money

world = create_base_world().populate(BALLOONS_PATH).populate(CURRENT_WEEK_BALLOONS_PATH)
weekly_meal_plan_balloonist = world.get_balloonist(WeeklyMealPlan)
deflated_weekly_meal_plan = json.loads((CURRENT_WEEK_DATA_PATH / "meal-plan.json").read_text())
weekly_meal_plan = weekly_meal_plan_balloonist.inflate(deflated_weekly_meal_plan)

product_provider = world.get_provider(Product)
price_calculator = PriceCalculator.create(
    products=[product_provider.get(n) for n in product_provider.get_names()]
)

GREEN = "\033[32m"
YELLOW = "\033[33m"

RESET = "\033[0m"

week_price = Money(0, 0)
for day, daily_meal_plan in weekly_meal_plan.dailies.items():
    if len(daily_meal_plan.meals) == 0:
        continue

    day_price = Money(0, 0)
    print(YELLOW, end="")
    print(f"{'-' * len(day.name)}")
    print(f"{day.name.upper()}")
    print(f"{'-' * len(day.name)}")
    print(RESET, end="")
    for meal_slot, meal in daily_meal_plan.meals.items():
        print(f"{YELLOW}{meal_slot.name.capitalize()}:{RESET}")
        for ration in meal.rations.values():
            price = price_calculator.get_price(ration)
            day_price = sum_money(day_price, price)
            print(
                f"{price.units:3}.{price.cents:0>2} EUR  "
                f"{GREEN}{ration.category.name}{RESET}"
            )
    week_price = sum_money(week_price, day_price)
    print()
    print(f"Day total: {day_price.units}.{day_price.cents:0>2} EUR")
    print()

print("-" * 20)
print(f"Week total: {week_price.units}.{week_price.cents:0>2} EUR")
