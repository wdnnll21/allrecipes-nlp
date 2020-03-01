class Recipe(object):
    def __init__(self,titl,ing,step,note,nutr,tim,tools):
        super(Recipe,self)
        #List of Ingredients, Including Quantities
        self.ingredients = ing
        #Title of Recipe
        self.title = titl
        #List of List of Direction Sentences. Each list is a single step. Each list in that list is a sub-step.
        self.directions = step
        #Cook's suggestions, if they exist
        self.notes = note
        #Nutritional Information
        self.nutrition = nutr
        #How long the recipe takes
        self.timing = tim
<<<<<<< HEAD
        #Tools used in making the recipe
        self.tools = tools

    def change_servings(self, multiplier):
        for i in range(len(self.ingredients)):
            self.ingredients[i] = (self.ingredients[i][0]*multiplier, self.ingredients[i][1])
=======
    
    def __repr__(self):
        return f""" 
        ** Title: {self.title} **\n
        ** Ingredients: {self.ingredients} **\n
        ** Directions: {self.directions} **\n
        ** Notes: {self.notes} **\n
        ** Nutrition: {self.nutrition} **\n
        ** Timing: {self.timing} **\n\n"""

class Action(object):
    def __init__(self,typ,verb,doc):
        self.act = typ 
        self.verb = verb
        self.doc = doc
        self.subj = None
        self.ingr = None
        self.tool = None
        self.until = None
        self.properties = None

    def happen(self):
        return 0


class Mixture(object):
    def __init__(self,ingr):
        self.ingr = [ingr]
        self.state = "at rest"

    
>>>>>>> 77c14d2d73ac83a900b0a407374ae0d2b84e6a3e

