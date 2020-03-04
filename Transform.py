from TransformMaps import meatToVeg, vegToMeat, toIndian, changeCookMethod
from StepParser import Phrase, Sentence
from RecipeX import Recipe
from ingredients import Ingredient
from random import randint
import spacy
from RecipeGrabber import GrabFromRemote

class FakePrep(object):
    def __init__(self,text,pos,idx):
        self.text = text
        self.pos_ = pos
        self.idx = idx
    
    def __eq__(self,other):
        return self.text == other.text and self.pos_ == other.pos_ and self.idx == other.idx

    def __str__(self):
        return self.text

def TransformIngredient(recipe,ingr,ingrnew):
    for action in recipe.steps:
        for oldingr in action.ingrs:
            if oldingr in ingr.ingredient:
                action.ingrs[action.ingrs.index(oldingr)] = ingrnew.ingredient
                for oldobj in action.objects:
                    if oldobj.text in ingr.ingredient:
                        oldobj = ingrnew.ingredient
                newpreps = []
                for prepphrase in action.preps:
                    newpreps.append([FakePrep(x.text,x.pos_,x.idx) for x in prepphrase])
                for prepphrase in newpreps:
                    for prep in prepphrase:
                            if prep.text in ingr.ingredient and prep.pos_ == "NOUN": 
                                prep.text = ingrnew.ingredient
                action.preps = newpreps
                break
    recipe.ingredients[recipe.ingredients.index(ingr)] = ingrnew

def AddIngredient(recipe, ingr, when):
    recipe.ingredients.append(ingr)
    if when == "with":
        for action in recipe.steps:
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
        recipe.steps.append(action)

def ReplaceCookMethod(recipe,action):
    for actionold in recipe.steps:
        if actionold.typ == "Cook":
            actionold = action
      
def ToVegetarian(recipe):
    for ingredient in recipe.ingredients:
        for meat in meatToVeg:
            if meat in ingredient.ingredient:
                ingrnew = Ingredient(ingredient.quantity,ingredient.measurement,meatToVeg[meat])
                TransformIngredient(recipe,ingredient,ingrnew)
    
    return recipe

def FromVegetarian(recipe):
    addedMeat = False
    for ingredient in recipe.ingredients:
        for veggieRepl in vegToMeat:
            if veggieRepl in ingredient.ingredient:
                ingrnew = Ingredient(ingredient.quantity,ingredient.measurement,vegToMeat[veggieRepl])
                TransformIngredient(recipe,ingredient,ingrnew)
                addedMeat = True
    if not addedMeat:
        meat = list(meatToVeg)[randint(0,len(meatToVeg))]
        AddIngredient(recipe,Ingredient(4,"ounces",meat),"with")
    
    return recipe

def ToHealthy(recipe):
    ph = Phrase("trim")
    ph.type = "Prepare"
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

    return recipe

def FromHealthy(recipe):
    ingrnew = [Ingredient(1,"tablespoon","salt"),Ingredient(1/4,"cup","butter")]
    for ingrx in ingrnew:
        AddIngredient(recipe,ingrx,"with")

    unhealthy = ["bacon","tater tots","vegetable oil","marshmellow","hot dog bits","corn syrup","margarine","mayonnaise"]
    i = 0
    for ingr in recipe.ingredients:
        if any(word in ingr.ingredient for word in ["carrot","fruit","bean","apple","lettuce","spinach","arugula","tomato","pea","kale","beet","cucumber","pear","banana"]):
            TransformIngredient(recipe,ingr,Ingredient(ingr.quantity,"ounce",unhealthy[randint(0,7)]))

    if not any(word in recipe.title for word in ["salad","sandwich"]):
        AddIngredient(recipe,Ingredient(1,'cup','breading'),"none")
        phone = Phrase("bread")
        phone.typ = "Combine"
        phone.preps.append([FakePrep("in a large bowl","NOUN",415)])
        phone.tools.append("bowl")
        phone.ingrs.append("breading")
        AddAction(recipe,"end",phone)
        ph = Phrase("deep fry")
        ph.typ = "Cook"
        ph.objects.append("everything")
        AddAction(recipe,"end",ph)
    
    AddIngredient(recipe,Ingredient(50,None,'french fries'),"none")
    ph = Phrase("serve")
    ph.typ = "Wait"
    ph.preps.append([FakePrep("with side of french fries","NOUN",43500)])
    ph.ingrs.append("french fries")
    AddAction(recipe,"end",ph)

    return recipe
    
def ToAmerican(recipe): 
    recipe = FromHealthy(recipe)
    americanAdd = [
        (Ingredient(1, "ounce", "freedom"), "with"),
        (Ingredient(100, "gallons", "liberty"), "with"),
        (Ingredient(1, 'pair', 'of guns'), "with"),
        (Ingredient(10, "kg" "butter"), "with"),
    ]
    for ingredient, timing in americanAdd:
        AddIngredient(recipe, ingredient, timing)
    return recipe


def DoNothing(recipe):
    return

def ToLethal(recipe):
    print("\nSPONSORED: This transformation is brought to you by Clorox® Liquid Bleach.")
    ingrnew = Ingredient(2,"gallon","bleach")
    AddIngredient(recipe, ingrnew, "end")
    
    return recipe

def DoubleIt(recipe):
    recipe.change_servings(2)
    return recipe

def HalfIt(recipe):
    recipe.change_servings(1/2)
    return recipe


def ToThai(recipe):
    thaiAdd = [
        (Ingredient(1, "ounce", "peanut"), "with"),
        (Ingredient(1, "tablespoon", "chicken broth"), "with"),
        (Ingredient(2, "teaspoons", "soy sauce"), "with"),
        (Ingredient(1, "teaspoon", "fish sauce"), "with"),
        (Ingredient(1, "teaspoon", "white sugar"), "with"),
        (Ingredient(.25, "cup", "very thinly sliced fresh basil leaves"), "end"),

    ]
    for ingredient, timing in thaiAdd:
        AddIngredient(recipe, ingredient, timing)
    return recipe

def ToIndian(recipe): 
    beef = False
    for ingredient in recipe.ingredients:
        for meatReplacement in toIndian:
            if meatReplacement in ingredient.ingredient:
                ingrnew = Ingredient(
                    ingredient.quantity, ingredient.measurement, toIndian[meatReplacement])
                TransformIngredient(recipe, ingredient, ingrnew)
                beef = True
    if not beef:
        meat = list(toIndian)[randint(0, len(toIndian))]
        AddIngredient(recipe, Ingredient(4, "ounces", meat), "with")
    AddIngredient(recipe, Ingredient(1/2, "tablespoon", "curry"))
    AddIngredient(recipe, Ingredient(1, "teaspoon", "coriander"))
    AddIngredient(recipe, Ingredient(1, "teaspoon", "cumin"))
    AddIngredient(recipe, Ingredient(1, "teaspoon", "cayenne"))
    AddIngredient(recipe, Ingredient(1, "teaspoon", "turmeric"))
    return recipe
    
def randomizeCookMethod(recipe): 
    for actionold in recipe.steps:
        if actionold.typ == "Cook":
            for newCook in changeCookMethod:
                if newCook == actionold.verb:
                    actionold.verb = changeCookMethod[newCook]
    return recipe
    
def ToAsianFusion(recipe):
    pass

def ToBBQ(recipe):
    pass

def ToSandwich(recipe):
    pass


# rec = GrabFromRemote("https://www.allrecipes.com/recipe/278271/")
# ToThai(rec)
# print(rec)
