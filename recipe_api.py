from RecipeGrabber import GrabFromRemote
from StepParser import ActionMachine
from Transform import *

inputanother = True

while inputanother:
    address = input("Please input URL:")

    recipe = GrabFromRemote(address)

    ActionMachine(recipe)

    print(recipe)

    print("\nDo you want to transform this recipe?\n0)No.\n1)To Vegetarian\n2) From Vegetarian\n3)To Healthy\n4) From Healthy\n5)To American\n6)To Thai\n7)To Indian\n8)Double It\n9)Half It\n10)To Lethal")

    transform = input("Input the number of your selection:")
    while transform not in "1023456789":
        transform = input("Input not recognized. Please input a number between 0 and 10:")
    
    option = {"0":DoNothing,"1":ToVegetarian,"2":FromVegetarian,"3":ToHealthy,"4":FromHealthy,
    "5":"ToAmerican","6":ToThai,"7":"ToIndian","8":DoubleIt,"9":HalfIt,"10":ToLethal}[transform](recipe)

    print(option)

    iA = input("Try another recipe? Y/N")
    while iA not in ["Y","N","y","n","yes","no"]:
        iA = input("Input not recognized. Please input Y or N")

    inputanother = "y" in iA.lower()

