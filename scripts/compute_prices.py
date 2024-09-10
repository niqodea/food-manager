from weekly_meal_plan import WEEKLY_MEAL_PLAN
from weekly_meal_plan_utils import price_calculator

from food_manager.schema import Nutrient, Money
from food_manager.utils import get_calories, get_nutrient_grams, sum_money

CARB_BUDGET_GRAMS = 20.0

GREEN = "\033[32m"
YELLOW = "\033[33m"

RESET = "\033[0m"

week_price = Money(0, 0)
for day, daily_meal_plan in WEEKLY_MEAL_PLAN.dailies.items():
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
                f"{price.units:3}.{price.cents:<2} EUR  "
                f"{GREEN}{ration.category.name}{RESET}"
            )
    week_price = sum_money(week_price, day_price)
    print()
    print(f"Day total: {day_price.units}.{day_price.cents} EUR")
    print()

print("-" * 20)
print(f"Week total: {week_price.units}.{week_price.cents} EUR")
