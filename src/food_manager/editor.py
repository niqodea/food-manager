from dataclasses import replace
from food_manager.schema import WeeklyMealPlan, Day, DailyMealPlan, MealSlot, Meal, Category, Ration, Substance


class WeeklyMealPlanManager:

    def __init__(self, entity: WeeklyMealPlan) -> None:
        self._entity = entity

    def get_daily_meal_plan_manager(self, day: Day) -> DailyMealPlanManager:
        if (daily_meal_plan := self._entity.dailies.get(day)) is not None:
            return DailyMealPlanManager(daily_meal_plan)
        else:
            return DailyMealPlanManager(DailyMealPlan(meals={}))

    def upsert_daily_meal_plan(self, day: Day, daily_meal_plan: DailyMealPlan):
        self._entity = replace(
            self._entity,
            dailies=self._entity.dailies | {day: daily_meal_plan}
        )

    def delete_daily_meal_plan(self, day: Day) -> None:
        if day not in self._entity.dailies:
            raise ValueError(f"Daily meal plan for {day.name} does not exist.")
        
        self._entity = replace(
            self._entity,
            dailies={k: v for k, v in self._entity.dailies.items() if k != day}
        )

    def get_entity(self) -> WeeklyMealPlan:
        return self._entity



class DailyMealPlanManager:

    def __init__(self, entity: DailyMealPlan) -> None:
        self._entity = entity

    def get_meal_manager(self, meal_slot: MealSlot) -> MealManager:
        if (meal := self._entity.meals.get(meal_slot)) is not None:
            return MealManager(meal)
        else:
            return MealManager(Meal(slot=meal_slot, rations={}))

    def upsert_meal(self, meal_slot: MealSlot, meal: Meal) -> None:
        self._entity = replace(
            self._entity,
            meals=self._entity.meals | {meal_slot: meal}
        )

    def delete_meal(self, meal_slot: MealSlot) -> None:
        if meal_slot not in self._entity.meals:
            raise ValueError(f"Meal for {meal_slot.name} does not exist.")
        
        self._entity = replace(
            self._entity,
            meals={k: v for k, v in self._entity.meals.items() if k != meal_slot}
        )

    def get_entity(self) -> DailyMealPlan:
        return self._entity



class MealManager:

    def __init__(self, entity: Meal) -> None:
        self._entity = entity

    def upsert_ration(self, category: Category, ration: Ration) -> None:
        self._entity = replace(
            self._entity,
            rations=self._entity.rations | {category: ration}
        )

    def delete_ration(self, category: Category) -> None:
        if category not in self._entity.rations:
            raise ValueError(f"Ration for {category.name} does not exist.")
        
        self._entity = replace(
            self._entity,
            rations={k: v for k, v in self._entity.rations.items() if k != category}
        )

    def get_entity(self) -> Meal:
        return self._entity


# TODO: Build a ration
