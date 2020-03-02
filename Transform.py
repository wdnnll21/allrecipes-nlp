from TransformMaps import meatToVeg
from StepParser import Phrase, Sentence
from RecipeX import Recipe
from ingredients import Ingredient

def TransformIngredient(recipe,ingr,ingrnew):
    for action in recipe.steps:
        for oldingr in action.ingrs:
            if oldingr in ingr.ingredient:
                oldingr = ingrnew.ingredient
                for oldobj in action.objects:
                    if oldobj.text in  ingr.ingredient:
                        oldobj = ingrnew.ingredient
                for prepphrase in action.preps:
                    if any(prep in ingr.ingredient for prep in prepphrase):
                        action.preps.remove(prepphrase)
                break
    for ingrold in recipe.ingredients:
        if ingr.ingredient == ingrold.ingredient:
            ingrold = ingrnew
            break

def AddIngredient(recipe, ingr, when):
    recipe.ingredients.append(ingr)
    if when == "with":
        for action in recipe:
            if action.typ == "Combine":
                action.ingrs.append(ingr.ingredient)
                action.objects.append(ingr.ingredient)
                break
    else:
        newph = Phrase("add")
        newph.typ = "Combine"
        newph.objects.append(ingr.ingredient)
        newph.ingrs.append(ingr.ingredient)
        AddAction(recipe,when,newph)

def AddAction(recipe, when, action):
    if when == "begin":
        recipe.steps.insert(0,action)
    if when == "before":
        i = 0
        for action in recipe.steps:
            if action.typ == "Cook":
                recipe.steps.insert(i,action)
                break
            i+=1
    if when == "after":
        i = 0
        for action in recipe.steps:
            if action.typ == "Cook":
                recipe.steps.insert(i+1,action)
                break
            i+=1
    if when == "end":
        action.steps.append(action)

def ReplaceCookMethod(recipe,action):
    for actionold in recipe.steps:
        if actionold.typ == "Cook":
            actionold = action
      
def ToVegetarian(recipe):
    for ingredient in recipe.ingredients:
        for meat in meatToVeg:
            if meat in ingredient.ingredient:
                ingrnew = Ingredient(ingredient.quantity,ingredient.measurement,meatToVeg[meat][0])
                TransformIngredient(recipe,ingredient,ingrnew)

def FromVegetarian(recipe):
    addedMeat = False
    for ingredient in recipe.ingredients:
        for veggieRepl in vegToMeat:
            if veggieRepl in ingredient.ingredient:
                ingrnew = Ingredient(ingredient.quantity,ingredient.measurement,vegToMeat[veggieRepl][0])
                TransformIngredient(recipe,ingredient,ingrnew)
                addedMeat = True
    if not addedMeat:
        AddIngredient()#add random meat
    

def ToHealthy(recipe):
    pass

def FromHealthy(recipe):
    ingrnew = [Ingredient(1,"tablespoon","salt"),Ingredient(1/4,"cup","butter")]

def ToLethal(recipe):
    ingrnew = Ingredient(2,"gallon","bleach")
    AddIngredient(recipe, ingrnew, "end")


def ToAsianFusion(recipe):
    pass

def ToBBQ(recipe):
    pass

def ToSandwich(recipe):
    pass

