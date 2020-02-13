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