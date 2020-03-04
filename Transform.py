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
                    if str(oldobj) in ingr.ingredient:
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
        combined = False
        for action in recipe.steps:
            if action.typ == "Combine":
                action.ingrs.append(ingr.ingredient)
                action.objects.append(ingr.ingredient)
                combined = True
                break
        if not combined:
            AddIngredient(recipe,ingr,"before")
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
        inserted = False
        for actionz in recipe.steps:
            if actionz.typ == "Cook":
                recipe.steps.insert(i,action)
                inserted = True
                break
            i+=1
        if not inserted:
            AddAction(recipe,"begin",action)
    if when == "after":
        i = 0
        insert = False
        for actionz in recipe.steps:
            if actionz.typ == "Cook":
                recipe.steps.insert(i+1,action)
                insert = True
                break
            i+=1
        if not insert:
            AddAction(recipe,"end",action)
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
    unhealthy = ["bacon","tater tots","marshmellow","hot dog","corn syrup","margarine","mayonnaise","freedom","guns","butter","liberty"]

    ph = Phrase("trim")
    ph.type = "Prepare"
    for ingr in recipe.ingredients:
        if any(unhealth in ingr.ingredient for unhealth in unhealthy):
            recipe.ingredients.remove(ingr)
            continue
        if any(meat in ingr.ingredient for meat in meatToVeg):
            ph.objects.append(ingr.ingredient)
            ph.ingrs.append(ingr.ingredient)
        if any(sugaroil in ingr.ingredient for sugaroil in ["sugar","syrup","glaze","honey","oil","spray","lard","butter","fat","grease"]):
            ingr.quantity /= 3
        if "salt" in ingr.ingredient and "salted" not in ingr.ingredient:
            TransformIngredient(recipe,ingr,Ingredient(ingr.quantity,ingr.measurement,"onion powder"))
        
    if len(ph.objects) > 0:
        AddAction(recipe,"begin",ph)

    healthy = ["spinach","onion","zucchini","kale","oats","quinoa","green beans","whole cucumber","arugula head"]
    AddIngredient(recipe,Ingredient(0,"",healthy[randint(0,8)] + " to taste"),"before")

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
        recipe.pm = "deep fry"
    
    AddIngredient(recipe,Ingredient(50,None,'french fries'),"none")
    ph = Phrase("serve")
    ph.typ = "Wait"
    ph.preps.append([FakePrep("with side of french fries","NOUN",43500)])
    ph.ingrs.append("french fries")
    AddAction(recipe,"end",ph)

    return recipe
    
def ToAmerican(recipe): 
    recipe = FromHealthy(recipe)
    recipe.pm = "artery-clog"
    americanAdd = [
        (Ingredient(1, "ounce", "freedom"), "with"),
        (Ingredient(100, "gallons", "liberty"), "with"),
        (Ingredient(1, 'pair of', 'guns'), "with"),
        (Ingredient(10, "kg", "butter"), "with"),
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
    recipe.pm = "poison"
    
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
      (Ingredient(1, "tablespoon", "Serrano chili dust"),"with"),
      (Ingredient(.25, "cup", "very thinly sliced fresh basil leaves"), "end"),
      (Ingredient(1,'cup','rice noodles'),'none')
    ]
    for ingredient, timing in thaiAdd:
        AddIngredient(recipe, ingredient, timing)
    recipe.pm = "stir fry"
    phb = Phrase("boil")
    phb.typ = "Cook"
    phb.ingrs.append("rice noodles")
    phb.preps.extend([FakePrep("in saucepan over medium heat","NOUN",499)])
    phb.tools.append("saucepan")
    phb.objects.append("rice noodles")
    ph = Phrase("serve")
    ph.typ = "Wait"
    ph.ingrs.append("rice noodles")
    ph.preps.append(FakePrep("over noodles","NOUN",513))
    return recipe

def ToIndian(recipe): 
    for ingredient in recipe.ingredients:
        for meatReplacement in toIndian:
            if meatReplacement in ingredient.ingredient:
                ingrnew = Ingredient(
                    ingredient.quantity, ingredient.measurement, toIndian[meatReplacement])
                TransformIngredient(recipe, ingredient, ingrnew)
    AddIngredient(recipe, Ingredient(1/2, "tablespoon", "curry"),"with")
    AddIngredient(recipe, Ingredient(1, "teaspoon", "coriander"),"with")
    AddIngredient(recipe, Ingredient(1, "teaspoon", "cumin"),"with")
    AddIngredient(recipe, Ingredient(1, "teaspoon", "cayenne"),"with")
    AddIngredient(recipe, Ingredient(1, "teaspoon", "turmeric"),"with")
    recipe.pm = "curry"
    return recipe
    
def randomizeCookMethod(recipe): 
    for actionold in recipe.steps:
        if actionold.typ == "Cook":
            for newCook in changeCookMethod:
                if newCook == str(actionold.verb):
                    actionold.verb = changeCookMethod[newCook]
                    recipe.pm = changeCookMethod[newCook]
    return recipe

def ToSandwich(recipe):
    AddIngredient(recipe,Ingredient(2,"slices","white bread"),"none")
    ph = Phrase("Place")
    ph.preps.append([FakePrep("from this meal between white bread","NOUN",980)])
    ph.objects.append("leftovers")
    ph.ingrs.append("white bread")

    AddAction(recipe,"end",ph)
    recipe.pm = "sandwich"
    return recipe


# rec = GrabFromRemote("https://www.allrecipes.com/recipe/278271/")
# ToThai(rec)
# print(rec)
