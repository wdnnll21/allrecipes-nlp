class Recipe(object):
    def __init__(self,titl,ing,step,note,nutr,tim):
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
        # #Tools used in making the recipe
        self.tools = []
        self.steps = []
        self.pm = None 

    def change_servings(self, multiplier):
        for ingredient in self.ingredients:
            ingredient.multiply_quantity(multiplier)

    def halve(self):
        self.change_servings(.5)

    def double(self):
        self.change_servings(2)
    
    def __repr__(self):
        ingreds = "\n".join([str(ing) for ing in self.ingredients])
        dirs = "\n".join([str(step) for step in self.steps])

        return f"""
** Title: {self.title} **\n
** Ingredients: **\n {ingreds} \n
** Parsed Steps: **\n {dirs} \n
** Primary Method: {self.pm} **\n
** Tools: {", ".join(list(set(self.tools)))} **\n
** Notes: {self.notes} **\n
** Timing: {", ".join(self.timing)} **\n\n"""


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

