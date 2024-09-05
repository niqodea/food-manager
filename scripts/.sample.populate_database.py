from enum import Enum

from food_manager.path import JSON_DATABASE_PATH
from food_manager.schema import (
    CompositeFoodMixture,
    DehydratedFoodMixture,
    Food,
    FoodMixture,
    Ingredient,
    MacroRatios,
    SimpleFoodMixture,
    create_balloonist_factory,
)


class Ingredients(Enum):
    BANANA = Ingredient().to_named("banana")
    CHICKEN = Ingredient().to_named("chicken")
    COFFEE = Ingredient().to_named("coffee")
    DEHYDRATED_EGGPLANT = Ingredient().to_named("dehydrated-eggplant")
    EGGPLANT = Ingredient().to_named("eggplant")
    GREEK_YOGURT = Ingredient().to_named("greek-yogurt")
    MOZZARELLA = Ingredient().to_named("mozzarella")
    OLIVE_OIL = Ingredient().to_named("olive-oil")
    PARMESAN = Ingredient().to_named("parmesan")
    PEANUT_SEED_OIL = Ingredient().to_named("peanut-seed-oil")
    SUGAR = Ingredient().to_named("sugar")
    TOMATO_SAUCE = Ingredient().to_named("tomato-sauce")
    TUNA = Ingredient().to_named("tuna")


class FoodMixtures(Enum):
    SUGAR = SimpleFoodMixture(
        type_=Ingredients.SUGAR.value,
        macros=MacroRatios(carb=100e-2, fat=0e-2, protein=0e-2),
    ).to_named("sugar")

    OLIVE_OIL = SimpleFoodMixture(
        type_=Ingredients.OLIVE_OIL.value,
        macros=MacroRatios(carb=0e-2, fat=100e-2, protein=0e-2),
    ).to_named("olive-oil")

    PEANUT_SEED_OIL = SimpleFoodMixture(
        type_=Ingredients.PEANUT_SEED_OIL.value,
        macros=MacroRatios(carb=0e-2, fat=100e-2, protein=0e-2),
    ).to_named("peanut-seed-oil")

    BRANDED_GREEK_YOGURT = SimpleFoodMixture(
        type_=Ingredients.GREEK_YOGURT.value,
        macros=MacroRatios(carb=3.5e-2, fat=5e-2, protein=9e-2),
    ).to_named("branded-greek-yogurt")

    COFFEE = SimpleFoodMixture(
        type_=Ingredients.COFFEE.value,
        macros=MacroRatios(carb=0e-2, fat=0e-2, protein=0e-2),
    ).to_named("coffee")

    FISH_MARKET_TUNA = SimpleFoodMixture(
        type_=Ingredients.TUNA.value,
        macros=MacroRatios(carb=0e-2, fat=1.0e-2, protein=23e-2),
    ).to_named("fish-market-tuna")

    LOCAL_BUTCHER_CHICKEN = SimpleFoodMixture(
        type_=Ingredients.CHICKEN_BREAST.value,
        macros=MacroRatios(carb=0e-2, fat=3.6e-2, protein=31e-2),
    ).to_named("local-butcher-chicken")

    LOCAL_FARMER_EGGPLANT = SimpleFoodMixture(
        type_=Ingredients.EGGPLANT.value,
        macros=MacroRatios(carb=2.6e-2, fat=0.4e-2, protein=1.1e-2),
    ).to_named("local-farmer-eggplant")

    BRANDED_TOMATO_SAUCE = SimpleFoodMixture(
        type_=Ingredients.TOMATO_SAUCE.value,
        macros=MacroRatios(carb=5.1e-2, fat=0.5e-2, protein=1.6e-2),
    ).to_named("branded-tomato-sauce")

    BRANDED_MOZZARELLA = SimpleFoodMixture(
        type_=Ingredients.MOZZARELLA.value,
        macros=MacroRatios(carb=0.2e-2, fat=17e-2, protein=17e-2),
    ).to_named("branded-mozzarella")

    PARMESAN = SimpleFoodMixture(
        type_=Ingredients.PARMESAN.value,
        macros=MacroRatios(carb=4.1e-2, fat=29e-2, protein=38e-2),
    ).to_named("parmesan")

    BANANA = SimpleFoodMixture(
        type_=Ingredients.BANANA.value,
        macros=MacroRatios(carb=22e-2, fat=0.2e-2, protein=1.1e-2),
    ).to_named("banana")

    # =================================================================================

    SAUTEED_CHICKEN = CompositeFoodMixture(
        type_=Ingredients.SAUTEED_CHICKEN.value,
        components={
            Ingredients.CHICKEN.value: CompositeFoodMixture.Component(
                mixture=LOCAL_BUTCHER_CHICKEN,
                proportion=200.0,
            ),
            Ingredients.OLIVE_OIL.value: CompositeFoodMixture.Component(
                mixture=OLIVE_OIL,
                proportion=1.0,
            ),
        },
    ).to_named("sauteed-chicken")

    SAUTEED_TUNA = CompositeFoodMixture(
        type_=Ingredients.SAUTEED_TUNA.value,
        components={
            Ingredients.TUNA.value: CompositeFoodMixture.Component(
                mixture=FISH_MARKET_TUNA,
                proportion=100.0,
            ),
            Ingredients.OLIVE_OIL.value: CompositeFoodMixture.Component(
                mixture=OLIVE_OIL,
                proportion=1.0,
            ),
        },
    ).to_named("sauteed-tuna")

    EGGPLANT_PARMESAN = CompositeFoodMixture(
        type_=Ingredients.EGGPLANT_PARMESAN.value,
        components={
            Ingredients.DEHYDRATED_EGGPLANT.value: CompositeFoodMixture.Component(
                mixture=DehydratedFoodMixture(
                    type_=Ingredients.DEHYDRATED_EGGPLANT.value,
                    original_mixture=LOCAL_FARMER_EGGPLANT,
                    dehydration_ratio=0.5,
                ),
                proportion=550.0,
            ),
            Ingredients.TOMATO_SAUCE.value: CompositeFoodMixture.Component(
                mixture=BRANDED_TOMATO_SAUCE,
                proportion=700.0,
            ),
            Ingredients.MOZZARELLA.value: CompositeFoodMixture.Component(
                mixture=BRANDED_MOZZARELLA,
                proportion=200.0,
            ),
            Ingredients.PARMESAN.value: CompositeFoodMixture.Component(
                mixture=PARMESAN,
                proportion=125.0,
            ),
            Ingredients.PEANUT_SEED_OIL.value: CompositeFoodMixture.Component(
                mixture=PEANUT_SEED_OIL,
                proportion=50.0,
            ),
            Ingredients.OLIVE_OIL.value: CompositeFoodMixture.Component(
                mixture=OLIVE_OIL,
                proportion=20.0,
            ),
        },
    ).to_named("eggplant-parmesan")


class Foods(Enum):
    BANANA = Food(
        ingredient=Ingredients.BANANA.value,
        mixture=FoodMixtures.BANANA.value,
        grams=100.0,
    ).to_named("banana")

    GREEK_YOGURT = Food(
        ingredient=Ingredients.GREEK_YOGURT.value,
        mixture=CompositeFoodMixture(
            type_=Ingredients.GREEK_YOGURT.value,
            components={
                Ingredients.GREEK_YOGURT.value: CompositeFoodMixture.Component(
                    mixture=FoodMixtures.BRANDED_GREEK_YOGURT.value,
                    proportion=60.0,
                ),
                Ingredients.SUGAR.value: CompositeFoodMixture.Component(
                    mixture=FoodMixtures.SUGAR.value,
                    proportion=7.0,
                ),
            },
        ),
        grams=67.0,
    ).to_named("greek-yogurt")

    COFFEE = Food(
        ingredient=Ingredients.MACCHIATO_COFFEE.value,
        mixture=CompositeFoodMixture(
            type_=Ingredients.MACCHIATO_COFFEE.value,
            components={
                Ingredients.COFFEE.value: CompositeFoodMixture.Component(
                    mixture=FoodMixtures.COFFEE.value,
                    proportion=25.0,
                ),
                Ingredients.SUGAR.value: CompositeFoodMixture.Component(
                    mixture=FoodMixtures.SUGAR.value,
                    proportion=4.0,
                ),
            },
        ),
        grams=29.0,
    ).to_named("macchiato-coffee")


balloonist_factory = create_balloonist_factory(JSON_DATABASE_PATH)

ingredient_balloonist = balloonist_factory.instantiate(Ingredient)
food_mixture_balloonist = balloonist_factory.instantiate(FoodMixture)
food_balloonist = balloonist_factory.instantiate(Food)

for ingredient in Ingredients:
    ingredient_balloonist.track(ingredient.value)
for food_mixture in FoodMixtures:
    food_mixture_balloonist.track(food_mixture.value)
for food in Foods:
    food_balloonist.track(food.value)
