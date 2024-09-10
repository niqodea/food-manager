* Having an object with some values that you want to change retroactively affects old usages of that item, which is annoying. How do we address this, perhaps exploiting the fact that we only run the scripts weekly? On the other hand, long-term analyses would also be cool if possible.
* Still not entirely sure indexing stuff by ingredient is desirable/useful.
* Recipes (mixtures) have to be duplicated if we have to switch out ingredients
* Specifying units other than grams (number, ml , spoons) would be nice
* Specifying anonymous recipes for a given week might actually be pretty handy, since recipe variability is a thing. Maybe a local balloons db!?
* Combining global and week-local database seems to be a really good idea. Perhaps we could even refer to other week databases to refer to previous weeks!
* Notion of equality is not trivial, sometimes you want the name to be part of what counts as equality, sometimes you don't (e.g. food categories, product-food matching, the latter is actually difficult to figure out exactly)
* File representation of a weekly meal plan might not exactly match the input the user provided to generate it. For example, information is transformed when going from `create_ration_from_substances` to the json `Ration` representation. We can have an adapter, or just not care.
