from enum import Enum

from food_manager.path import DATA_PATH
from food_manager.schema import (
    CompositeSubstance,
    DehydratedSubstance,
    MealSlot,
    Ration,
    Substance,
    Category,
    MacroRatios,
    SimpleSubstance,
    create_balloonist_factory,
)


class Categories(Enum):
    BANANA = Category("banana")
    CHICKEN = Category("chicken")
    COFFEE = Category("coffee")
    DEHYDRATED_EGGPLANT = Category("dehydrated-eggplant")
    EGGPLANT = Category("eggplant")
    GREEK_YOGURT = Category("greek-yogurt")
    MOZZARELLA = Category("mozzarella")
    OLIVE_OIL = Category("olive-oil")
    PARMESAN = Category("parmesan")
    PEANUT_SEED_OIL = Category("peanut-seed-oil")
    SUGAR = Category("sugar")
    TOMATO_SAUCE = Category("tomato-sauce")
    TUNA = Category("tuna")


class Substances(Enum):
    SUGAR = SimpleSubstance(
        type_=Categories.SUGAR.value,
        macros=MacroRatios(carb=100e-2, fat=0e-2, protein=0e-2),
    ).to_named("sugar")

    OLIVE_OIL = SimpleSubstance(
        type_=Categories.OLIVE_OIL.value,
        macros=MacroRatios(carb=0e-2, fat=100e-2, protein=0e-2),
    ).to_named("olive-oil")

    PEANUT_SEED_OIL = SimpleSubstance(
        type_=Categories.PEANUT_SEED_OIL.value,
        macros=MacroRatios(carb=0e-2, fat=100e-2, protein=0e-2),
    ).to_named("peanut-seed-oil")

    BRANDED_GREEK_YOGURT = SimpleSubstance(
        type_=Categories.GREEK_YOGURT.value,
        macros=MacroRatios(carb=3.5e-2, fat=5e-2, protein=9e-2),
    ).to_named("branded-greek-yogurt")

    COFFEE = SimpleSubstance(
        type_=Categories.COFFEE.value,
        macros=MacroRatios(carb=0e-2, fat=0e-2, protein=0e-2),
    ).to_named("coffee")

    FISH_MARKET_TUNA = SimpleSubstance(
        type_=Categories.TUNA.value,
        macros=MacroRatios(carb=0e-2, fat=1.0e-2, protein=23e-2),
    ).to_named("fish-market-tuna")

    LOCAL_BUTCHER_CHICKEN = SimpleSubstance(
        type_=Categories.CHICKEN_BREAST.value,
        macros=MacroRatios(carb=0e-2, fat=3.6e-2, protein=31e-2),
    ).to_named("local-butcher-chicken")

    LOCAL_FARMER_EGGPLANT = SimpleSubstance(
        type_=Categories.EGGPLANT.value,
        macros=MacroRatios(carb=2.6e-2, fat=0.4e-2, protein=1.1e-2),
    ).to_named("local-farmer-eggplant")

    BRANDED_TOMATO_SAUCE = SimpleSubstance(
        type_=Categories.TOMATO_SAUCE.value,
        macros=MacroRatios(carb=5.1e-2, fat=0.5e-2, protein=1.6e-2),
    ).to_named("branded-tomato-sauce")

    BRANDED_MOZZARELLA = SimpleSubstance(
        type_=Categories.MOZZARELLA.value,
        macros=MacroRatios(carb=0.2e-2, fat=17e-2, protein=17e-2),
    ).to_named("branded-mozzarella")

    PARMESAN = SimpleSubstance(
        type_=Categories.PARMESAN.value,
        macros=MacroRatios(carb=4.1e-2, fat=29e-2, protein=38e-2),
    ).to_named("parmesan")

    BANANA = SimpleSubstance(
        type_=Categories.BANANA.value,
        macros=MacroRatios(carb=22e-2, fat=0.2e-2, protein=1.1e-2),
    ).to_named("banana")

    # =================================================================================

    SAUTEED_CHICKEN = CompositeSubstance(
        type_=Categories.SAUTEED_CHICKEN.value,
        components={
            Categories.CHICKEN.value: CompositeSubstance.Component(
                substance=LOCAL_BUTCHER_CHICKEN,
                proportion=200.0,
            ),
            Categories.OLIVE_OIL.value: CompositeSubstance.Component(
                substance=OLIVE_OIL,
                proportion=1.0,
            ),
        },
    ).to_named("sauteed-chicken")

    SAUTEED_TUNA = CompositeSubstance(
        type_=Categories.SAUTEED_TUNA.value,
        components={
            Categories.TUNA.value: CompositeSubstance.Component(
                substance=FISH_MARKET_TUNA,
                proportion=100.0,
            ),
            Categories.OLIVE_OIL.value: CompositeSubstance.Component(
                substance=OLIVE_OIL,
                proportion=1.0,
            ),
        },
    ).to_named("sauteed-tuna")

    EGGPLANT_PARMESAN = CompositeSubstance(
        type_=Categories.EGGPLANT_PARMESAN.value,
        components={
            Categories.DEHYDRATED_EGGPLANT.value: CompositeSubstance.Component(
                substance=DehydratedSubstance(
                    type_=Categories.DEHYDRATED_EGGPLANT.value,
                    original_substance=LOCAL_FARMER_EGGPLANT,
                    dehydration_ratio=0.5,
                ),
                proportion=550.0,
            ),
            Categories.TOMATO_SAUCE.value: CompositeSubstance.Component(
                substance=BRANDED_TOMATO_SAUCE,
                proportion=700.0,
            ),
            Categories.MOZZARELLA.value: CompositeSubstance.Component(
                substance=BRANDED_MOZZARELLA,
                proportion=200.0,
            ),
            Categories.PARMESAN.value: CompositeSubstance.Component(
                substance=PARMESAN,
                proportion=125.0,
            ),
            Categories.PEANUT_SEED_OIL.value: CompositeSubstance.Component(
                substance=PEANUT_SEED_OIL,
                proportion=50.0,
            ),
            Categories.OLIVE_OIL.value: CompositeSubstance.Component(
                substance=OLIVE_OIL,
                proportion=20.0,
            ),
        },
    ).to_named("eggplant-parmesan")


class Rations(Enum):
    BANANA = Ration(
        category=Categories.BANANA.value,
        substance=Substances.BANANA.value,
        grams=100.0,
    ).to_named("banana")

    GREEK_YOGURT = Ration(
        category=Categories.GREEK_YOGURT.value,
        substance=CompositeSubstance(
            type_=Categories.GREEK_YOGURT.value,
            components={
                Categories.GREEK_YOGURT.value: CompositeSubstance.Component(
                    substance=Substances.BRANDED_GREEK_YOGURT.value,
                    proportion=60.0,
                ),
                Categories.SUGAR.value: CompositeSubstance.Component(
                    substance=Substances.SUGAR.value,
                    proportion=7.0,
                ),
            },
        ),
        grams=67.0,
    ).to_named("greek-yogurt")

    COFFEE = Ration(
        category=Categories.MACCHIATO_COFFEE.value,
        substance=CompositeSubstance(
            type_=Categories.MACCHIATO_COFFEE.value,
            components={
                Categories.COFFEE.value: CompositeSubstance.Component(
                    substance=Substances.COFFEE.value,
                    proportion=25.0,
                ),
                Categories.SUGAR.value: CompositeSubstance.Component(
                    substance=Substances.SUGAR.value,
                    proportion=4.0,
                ),
            },
        ),
        grams=29.0,
    ).to_named("macchiato-coffee")


class MealSlots(Enum):
    BREAKFAST = MealSlot("breakfast")
    LUNCH = MealSlot("lunch")
    DINNER = MealSlot("dinner")


balloonist_factory = create_balloonist_factory(DATA_PATH)

category_balloonist = balloonist_factory.instantiate(Category)
substance_balloonist = balloonist_factory.instantiate(Substance)
ration_balloonist = balloonist_factory.instantiate(Ration)
meal_slot_balloonist = balloonist_factory.instantiate(MealSlot)

for category in Categories:
    category_balloonist.track(category.value)
for substance in Substances:
    substance_balloonist.track(substance.value)
for ration in Rations:
    ration_balloonist.track(ration.value)
for meal_slot in MealSlots:
    meal_slot_balloonist.track(meal_slot.value)
