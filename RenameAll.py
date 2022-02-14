import os
from os import listdir
from os.path import isfile, join, exists
import shutil

Types = ["Lightning","Colorless","Psychic","Bug","Ground","Water","Dragon","Fire","Poison","Rock","Grass","Ice","Ghost","Fighting"]

project_path = os.getcwd()


def verifyFolder(path):
    isExist = os.path.exists(path)

    if not isExist:    
        # Create a new directory because it does not exist 
        os.makedirs(path)
        print("The new directory is created!")

    return path


def main():   

    outputFolder = verifyFolder(project_path + '\\images\\output\\Unsorted\\')

    for Type in Types:
        inputFolder = verifyFolder(project_path + '\\images\\output\\' + Type + '\\')    
        cards = [f for f in listdir(inputFolder) if isfile(join(inputFolder, f))]

        TypeB = Type
        match Type:
            case "Colorless":
                TypeB = "Normal"
            case "Lightning":
                TypeB = "Electric"
        for card in cards:
            id = card[0:card.find('.')]
            name = card[card.find('.')+1:card.find('-')]
            rarity = card[card.find('-')+1:card.find(".png")]

            shutil.copy(inputFolder + card, outputFolder + id + '.' + name + '-' + rarity + '_' + TypeB + ".png")


if __name__ == "__main__":
    import sys
    main()            