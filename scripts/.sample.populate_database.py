from enum import Enum

from food_manager.path import JSON_DATABASE_PATH
from food_manager.schema import (
    DehydratedFoodMixture,
    DetailedFoodMixture,
    Food,
    FoodMixture,
    FoodType,
    MacroRatios,
    SimpleFoodMixture,
    create_balloonist_factory,
)


class FoodTypes(Enum):
    BANANA = FoodType().to_named("banana")
    CHICKEN = FoodType().to_named("chicken")
    COFFEE = FoodType().to_named("coffee")
    DEHYDRATED_EGGPLANT = FoodType().to_named("dehydrated-eggplant")
    EGGPLANT = FoodType().to_named("eggplant")
    GREEK_YOGURT = FoodType().to_named("greek-yogurt")
    MOZZARELLA = FoodType().to_named("mozzarella")
    OLIVE_OIL = FoodType().to_named("olive-oil")
    PARMESAN = FoodType().to_named("parmesan")
    PEANUT_SEED_OIL = FoodType().to_named("peanut-seed-oil")
    SUGAR = FoodType().to_named("sugar")
    TOMATO_SAUCE = FoodType().to_named("tomato-sauce")
    TUNA = FoodType().to_named("tuna")


class FoodMixtures(Enum):
    SUGAR = SimpleFoodMixture(
        type_=FoodTypes.SUGAR.value,
        macros=MacroRatios(carb=100e-2, fat=0e-2, protein=0e-2),
    ).to_named("sugar")

    OLIVE_OIL = SimpleFoodMixture(
        type_=FoodTypes.OLIVE_OIL.value,
        macros=MacroRatios(carb=0e-2, fat=100e-2, protein=0e-2),
    ).to_named("olive-oil")

    PEANUT_SEED_OIL = SimpleFoodMixture(
        type_=FoodTypes.PEANUT_SEED_OIL.value,
        macros=MacroRatios(carb=0e-2, fat=100e-2, protein=0e-2),
    ).to_named("peanut-seed-oil")

    BRANDED_GREEK_YOGURT = SimpleFoodMixture(
        type_=FoodTypes.GREEK_YOGURT.value,
        macros=MacroRatios(carb=3.5e-2, fat=5e-2, protein=9e-2),
    ).to_named("branded-greek-yogurt")

    COFFEE = SimpleFoodMixture(
        type_=FoodTypes.COFFEE.value,
        macros=MacroRatios(carb=0e-2, fat=0e-2, protein=0e-2),
    ).to_named("coffee")

    FISH_MARKET_TUNA = SimpleFoodMixture(
        type_=FoodTypes.TUNA.value,
        macros=MacroRatios(carb=0e-2, fat=1.0e-2, protein=23e-2),
    ).to_named("fish-market-tuna")

    LOCAL_BUTCHER_CHICKEN = SimpleFoodMixture(
        type_=FoodTypes.CHICKEN_BREAST.value,
        macros=MacroRatios(carb=0e-2, fat=3.6e-2, protein=31e-2),
    ).to_named("local-butcher-chicken")

    LOCAL_FARMER_EGGPLANT = SimpleFoodMixture(
        type_=FoodTypes.EGGPLANT.value,
        macros=MacroRatios(carb=2.6e-2, fat=0.4e-2, protein=1.1e-2),
    ).to_named("local-farmer-eggplant")

    BRANDED_TOMATO_SAUCE = SimpleFoodMixture(
        type_=FoodTypes.TOMATO_SAUCE.value,
        macros=MacroRatios(carb=5.1e-2, fat=0.5e-2, protein=1.6e-2),
    ).to_named("branded-tomato-sauce")

    BRANDED_MOZZARELLA = SimpleFoodMixture(
        type_=FoodTypes.MOZZARELLA.value,
        macros=MacroRatios(carb=0.2e-2, fat=17e-2, protein=17e-2),
    ).to_named("branded-mozzarella")

    PARMESAN = SimpleFoodMixture(
        type_=FoodTypes.PARMESAN.value,
        macros=MacroRatios(carb=4.1e-2, fat=29e-2, protein=38e-2),
    ).to_named("parmesan")

    BANANA = SimpleFoodMixture(
        type_=FoodTypes.BANANA.value,
        macros=MacroRatios(carb=22e-2, fat=0.2e-2, protein=1.1e-2),
    ).to_named("banana")

    # =================================================================================

    SAUTEED_CHICKEN = DetailedFoodMixture(
        type_=FoodTypes.SAUTEED_CHICKEN.value,
        ingredients={
            FoodTypes.CHICKEN.value: DetailedFoodMixture.Ingredient(
                mixture=LOCAL_BUTCHER_CHICKEN,
                proportion=200.0,
            ),
            FoodTypes.OLIVE_OIL.value: DetailedFoodMixture.Ingredient(
                mixture=OLIVE_OIL,
                proportion=1.0,
            ),
        },
    ).to_named("sauteed-chicken")

    SAUTEED_TUNA = DetailedFoodMixture(
        type_=FoodTypes.SAUTEED_TUNA.value,
        ingredients={
            FoodTypes.TUNA.value: DetailedFoodMixture.Ingredient(
                mixture=FISH_MARKET_TUNA,
                proportion=100.0,
            ),
            FoodTypes.OLIVE_OIL.value: DetailedFoodMixture.Ingredient(
                mixture=OLIVE_OIL,
                proportion=1.0,
            ),
        },
    ).to_named("sauteed-tuna")

    EGGPLANT_PARMESAN = DetailedFoodMixture(
        type_=FoodTypes.EGGPLANT_PARMESAN.value,
        ingredients={
            FoodTypes.DEHYDRATED_EGGPLANT.value: DetailedFoodMixture.Ingredient(
                mixture=DehydratedFoodMixture(
                    type_=FoodTypes.DEHYDRATED_EGGPLANT.value,
                    original_mixture=LOCAL_FARMER_EGGPLANT,
                    dehydration_ratio=0.5,
                ),
                proportion=550.0,
            ),
            FoodTypes.TOMATO_SAUCE.value: DetailedFoodMixture.Ingredient(
                mixture=BRANDED_TOMATO_SAUCE,
                proportion=700.0,
            ),
            FoodTypes.MOZZARELLA.value: DetailedFoodMixture.Ingredient(
                mixture=BRANDED_MOZZARELLA,
                proportion=200.0,
            ),
            FoodTypes.PARMESAN.value: DetailedFoodMixture.Ingredient(
                mixture=PARMESAN,
                proportion=125.0,
            ),
            FoodTypes.PEANUT_SEED_OIL.value: DetailedFoodMixture.Ingredient(
                mixture=PEANUT_SEED_OIL,
                proportion=50.0,
            ),
            FoodTypes.OLIVE_OIL.value: DetailedFoodMixture.Ingredient(
                mixture=OLIVE_OIL,
                proportion=20.0,
            ),
        },
    ).to_named("eggplant-parmesan")


class Foods(Enum):
    
    BANANA = Food(
        type_=FoodTypes.BANANA.value,
        mixture=FoodMixtures.BANANA.value,
        grams=100.0,
    ).to_named("banana")

    GREEK_YOGURT = Food(
        type_=FoodTypes.GREEK_YOGURT.value,
        mixture=DetailedFoodMixture(
            type_=FoodTypes.GREEK_YOGURT.value,
            ingredients={
                FoodTypes.GREEK_YOGURT.value: DetailedFoodMixture.Ingredient(
                    mixture=FoodMixtures.BRANDED_GREEK_YOGURT.value,
                    proportion=60.0,
                ),
                FoodTypes.SUGAR.value: DetailedFoodMixture.Ingredient(
                    mixture=FoodMixtures.SUGAR.value,
                    proportion=7.0,
                ),
            },
        ),
        grams=67.0,
    ).to_named("greek-yogurt")

    COFFEE = Food(
        type_=FoodTypes.MACCHIATO_COFFEE.value,
        mixture=DetailedFoodMixture(
            type_=FoodTypes.MACCHIATO_COFFEE.value,
            ingredients={
                FoodTypes.COFFEE.value: DetailedFoodMixture.Ingredient(
                    mixture=FoodMixtures.COFFEE.value,
                    proportion=25.0,
                ),
                FoodTypes.SUGAR.value: DetailedFoodMixture.Ingredient(
                    mixture=FoodMixtures.SUGAR.value,
                    proportion=4.0,
                ),
            },
        ),
        grams=29.0,
    ).to_named("macchiato-coffee")

balloonist_factory = create_balloonist_factory(JSON_DATABASE_PATH)

food_type_balloonist = balloonist_factory.instantiate(FoodType)
food_mixture_balloonist = balloonist_factory.instantiate(FoodMixture)
food_balloonist = balloonist_factory.instantiate(Food)

for food_type in FoodTypes:
    food_type_balloonist.track(food_type.value)
for food_mixture in FoodMixtures:
    food_mixture_balloonist.track(food_mixture.value)
for food in Foods:
    food_balloonist.track(food.value)
