import fractions
import spacy

nlp = spacy.load("en_core_web_sm")


class Ingredient:
    def __init__(self, quantity, measurement, ingredient):
        super(Ingredient, self)
        self.quantity = quantity
        self.measurement = measurement
        self.ingredient = ingredient
        self.preparations = ""
        self.descriptions = ""

    def __repr__(self):
        base =  str(self.quantity) + " - " + str(self.measurement) + " - " + str(self.ingredient) if self.measurement else str(self.quantity) + " - " + str(self.ingredient)
        if self.quantity == 0:
            base = self.ingredient
        if self.descriptions != "":
            base += "  (Descriptions: " + self.descriptions + ")"
        if self.preparations != "":
            base += "  (Preparations: " + self.preparations + ")"
        return base

    def multiply_quantity(self, multiplier):
        if self.quantity != 0:
            old_quantity = self.quantity
            self.quantity = round(multiplier*old_quantity,2)
            if self.measurement:
                if old_quantity <= 1 < self.quantity:
                    self.measurement = self.make_plural(self.measurement)
                elif old_quantity > 1 >= self.quantity:
                    self.measurement = self.make_singular(self.measurement)
            else:
                if old_quantity <= 1 < self.quantity:
                    self.ingredient = self.change_plural_singular(self.ingredient, True)
                elif old_quantity > 1 >= self.quantity:
                    self.ingredient = self.change_plural_singular(self.ingredient, False)

    def change_plural_singular(self, phrase, plural):
        doc = nlp(phrase)
        i = 0
        while i < len(doc) and doc[i].pos_ != "NOUN" and doc[i].pos_ != "PROPN":
            print(doc[i].text, doc[i].pos_)
            i += 1

        if i < len(doc):
            if plural:
                new_word = self.make_plural(doc[i].text)
            else:
                new_word = self.make_singular(doc[i].text)
        j = 0
        res = ""
        for token in doc:
            if j == i:
                res += new_word + " "
            else:
                res += token.text + " "
            j += 1
        return res[:-1]

    @staticmethod
    def make_plural(word):
        if word[-1] != "s":
            word += "s"
        return word

    @staticmethod
    def make_singular(word):
        if word[-1] == "s":
            word = word[:-1]
        return word


def get_ingredient(ingredient_text):
    length, quantity = get_quantity(ingredient_text)
    ingredient = ingredient_text[length-1:] if quantity > 0 else ingredient_text
    measurement = get_measurement(ingredient)
    ingredient = ingredient[len(
        str(measurement))+1:] if measurement else ingredient
    ingredient = ingredient[1:] if ingredient[0] == " " else ingredient
    return Ingredient(quantity, measurement, ingredient)


def get_quantity(ingredient_text):
    nums = "0123456789/ "
    i = 0
    while ingredient_text[i] in nums:
        i += 1

    if i > 0:
        fraction_str = ingredient_text[0:i]
        # print(fraction_str)
        fraction_obj = sum(map(fractions.Fraction, fraction_str.split()))
        return i, float(fraction_obj)
    else:
        return 0, 0


def get_quantity_old(ingredient_text):
    nums = "0123456789"
    quantity = 0
    i = 0
    while ingredient_text[i] in nums:
        quantity = quantity*10 + int(ingredient_text[i])
        i += 1

    if ingredient_text[i] == "/":
        i += 1
        divide = 0
        while ingredient_text[i] in nums:
            divide = divide*10 + int(ingredient_text[i])
            i += 1
    else:
        divide = 1

    return quantity/divide


def get_measurement(ingredient_text): 
    params = ["spoon", "pinch", "clove", "cup", "pound", "ounce", "gram", "kg", "lb", "oz"]
    unit = ingredient_text.split()[0]
    for word in params: 
        if word in unit: 
            return unit

    bulk = ["package", "container", "can"]
    if unit[0] == "(":
        i = 0
        while ingredient_text[i] != ")" and i < len(ingredient_text):
            i += 1
        if ingredient_text[i] == ")":
            cropped = ingredient_text[i+1:]
            bulk_unit = cropped.split()[0]
            for word in bulk:
                if word in bulk_unit:
                    return ingredient_text[0:i+1] + " " + bulk_unit
    return None

