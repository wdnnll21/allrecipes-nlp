
def get_ingredient(ingredient_text):
    quantity = get_quantity(ingredient_text)
    ingredient = ingredient_text[len(str(quantity))-1:] if quantity > 0 else ingredient_text
    return quantity, ingredient


def get_quantity(ingredient_text):
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
