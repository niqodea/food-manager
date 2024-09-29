from collections import defaultdict
import json

from food_manager.path import (
    WORLD_PATH,
    CURRENT_WEEK_WORLD_PATH,
    CURRENT_WEEK_DATA_PATH,
)
from food_manager.schema import Day, Nutrient, WeeklyMealPlan, create_base_world
from food_manager.utils import get_kcal, get_nutrient_grams

world = create_base_world().populate(WORLD_PATH).populate(CURRENT_WEEK_WORLD_PATH)
weekly_meal_plan_balloonist = world.get_balloonist(WeeklyMealPlan)
deflated_weekly_meal_plan = json.loads(
    (CURRENT_WEEK_DATA_PATH / "meal-plan.json").read_text()
)
weekly_meal_plan = weekly_meal_plan_balloonist.inflate(deflated_weekly_meal_plan)

GREEN = "\033[32m"
YELLOW = "\033[33m"

RESET = "\033[0m"


def main(nutrient_budgets: dict[Nutrient, float]) -> None:
    nutrient_daily_total_grams: dict[Nutrient, dict[Day, float]] = defaultdict(
        lambda: defaultdict(float)
    )
    total_kcals: dict[Day, float] = defaultdict(float)
    for day, daily_meal_plan in weekly_meal_plan.dailies.items():
        if len(daily_meal_plan.meals) == 0:
            continue

        print(YELLOW, end="")
        print(f"{'-' * len(day.name)}")
        print(f"{day.name.upper()}")
        print(f"{'-' * len(day.name)}")
        print(RESET, end="")
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

                    if (nutrient_budget := nutrient_budgets.get(nutrient)) is not None:
                        print(f" ({grams / nutrient_budget * 100:3.0f}%)")
                    else:
                        print()

                for nutrient, grams in nutrient_grams.items():
                    nutrient_daily_total_grams[nutrient][day] += grams
                total_kcals[day] += kcal

        print()
        print(f"Daily total: {total_kcals[day]:.0f} kcal")
        for nutrient in Nutrient:
            if (daily_total_grams := nutrient_daily_total_grams.get(nutrient)) is None:
                continue
            if (total_grams := daily_total_grams.get(day)) is None:
                continue

            print(f"  {total_grams:6.1f}g {nutrient.name.lower()}", end="")

            if (nutrient_budget := nutrient_budgets.get(nutrient)) is not None:
                print(f" ({total_grams / nutrient_budget * 100:3.0f}%)")
            else:
                print()

        print()

    print(YELLOW, end="")
    print("---------------")
    print("WEEKLY AVERAGES")
    print("---------------")
    print(RESET, end="")
    average_daily_total_kcals = sum(total_kcals.values()) / len(
        weekly_meal_plan.dailies
    )
    print(f"Daily total: {average_daily_total_kcals:.0f} kcal")
    for nutrient in Nutrient:
        if (daily_total_grams := nutrient_daily_total_grams.get(nutrient)) is None:
            continue
        weekly_total_grams = sum(daily_total_grams.values())
        average_total_grams = weekly_total_grams / len(weekly_meal_plan.dailies)
        print(f"  {average_total_grams:6.1f}g {nutrient.name.lower()}", end="")

        if (nutrient_budget := nutrient_budgets.get(nutrient)) is not None:
            print(f" ({average_total_grams / nutrient_budget * 100:3.0f}%)")
        else:
            print()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--nutrient-budgets",
        type=lambda s: {
            Nutrient[n.upper()]: float(v)
            for n, v in (item.split(":") for item in s.split(","))
        },
        required=False,
        default={},
    )
    args = parser.parse_args()

    main(args.nutrient_budgets)
