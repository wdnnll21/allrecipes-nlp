from RecipeGrabber import GrabFromRemote
from StepParser import ActionMachine
from Transform import *

inputanother = True

while inputanother:
    address = input("Please input URL:")

    recipe = GrabFromRemote(address)

    ActionMachine(recipe)

    print(recipe)
    option = recipe
    conTransform = True
    
    while conTransform:
        print("\nDo you want to transform this recipe?\n0)No.\n1)To Vegetarian\n2) From Vegetarian\n3)To Healthy\n4) From Healthy\n5)To American\n6)To Thai\n7)To Indian\n8)Double It\n9)Half It\n10)Alternate Cook Method\n11)To Sandwich\n13)To Lethal")

        transform = input("Input the number of your selection:")
        while transform not in ["0","1","2","3","4","5","6","7","8","9","10","11","13"]:
            transform = input("Input not recognized. Please input a number between 0 and 13:")
        
        if transform == "0":
            conTransform = False
        else:
            option = {"1":ToVegetarian,"2":FromVegetarian,"3":ToHealthy,"4":FromHealthy,
            "5":ToAmerican,"6":ToThai,"7":ToIndian,"8":DoubleIt,"9":HalfIt,"13":ToLethal,"10":randomizeCookMethod,"11":ToSandwich}[transform](option)

            print(option)

    iA = input("Try another recipe? Y/N")
    while iA not in ["Y","N","y","n","yes","no"]:
        iA = input("Input not recognized. Please input Y or N")

    inputanother = "y" in iA.lower()

