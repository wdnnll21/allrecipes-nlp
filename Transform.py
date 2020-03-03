from TransformMaps import meatToVeg, vegToMeat
from StepParser import Phrase, Sentence
from RecipeX import Recipe
from ingredients import Ingredient
from random import randint

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
    elif when == "none":
        "Hello"
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
        meat = list(meatToVeg)[randint(0,len(meatToVeg))]
        AddIngredient(recipe,Ingredient(4,"ounces",meat),"with")
    

def ToHealthy(recipe):
    ph = Phrase("trim")
    for ingr in recipe.ingredients:
        if any(meat in ingr.ingredient for meat in meatToVeg):
            ph.objects.append(ingr.ingredient)
            ph.ingrs.append(ingr.ingredient)
        if any(sugaroil in ingr.ingredient for sugaroil in ["sugar","syrup","glaze","honey","oil","spray","lard","butter","fat","grease"]):
            ingr.quantity /= 3
        if "salt" in ingr.ingredient and "salted" not in ingr.ingredient:
            TransformIngredient(recipe,ingr,Ingredient(ingr.quantity,ingr.measurement,"onion powder"))
    if len(ph.objects) > 0:
        AddAction(recipe,"begin",ph)

def FromHealthy(recipe):
    ingrnew = [Ingredient(1,"tablespoon","salt"),Ingredient(1/4,"cup","butter")]
    for ingrx in ingrnew:
        AddIngredient(recipe,ingrx,"with")

    unhealthy = ["bacon","tater tots","vegetable oil","marshmellow","hot dog","corn syrup","margarine","mayonnaise"]
    i = 0
    for ingr in recipe.ingredients:
        if any(word in ingr.ingredient for word in ["carrot","fruit","bean","apple","lettuce","spinach","arugula","tomato","pea","kale","beet","cucumber","pear","banana"]):
            TransformIngredient(recipe,ingr,Ingredient(ingr.quantity,"ounce",unhealthy[i%5]))

    if not any(word in recipe.title for word in ["salad","sandwich"]):
        AddIngredient(recipe,Ingredient(1,'cup','breading'),"none")
        phone = Phrase("bread")
        phone.typ = "Combine"
        phone.preps.append("in a large bowl")
        phone.tools.append("bowl")
        phone.ingrs.append("breading")
        ph = Phrase("deep fry")
        ph.typ = "Cook"
        ph.objects.append("everything")
    
    AddIngredient(recipe,Ingredient(50,None,'french fries'),"none")
    ph = Phrase("serve")
    ph.typ = "Wait"
    ph.preps.append("with side of french fries")
    ph.ingrs.append("french fries")
    AddAction(recipe,ph,"end")

    

def ToLethal(recipe):
    ingrnew = Ingredient(2,"gallon","bleach")
    AddIngredient(recipe, ingrnew, "end")


def ToAsianFusion(recipe):
    pass

def ToBBQ(recipe):
    pass

def ToSandwich(recipe):
    pass

