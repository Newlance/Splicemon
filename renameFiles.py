import os
from os import listdir, name
from os.path import isfile, join


project_path = os.getcwd()
Types = ["Bug","Colorless","Dragon","Ice","Ghost","Fighting","Poison","Grass","Rock","Fire","Water","Ground","Lightning","Psychic"]

for Type in Types:
    outputFolder = project_path + '\\images\\FinalProduct\\' + Type + '\\'
    os.chdir(outputFolder)
    cards = [f for f in listdir(outputFolder) if isfile(join(outputFolder, f))]
    i=0
    for card in cards:        
        index = card.find('.')                
        id=card[0:index]
        if index < 5:            
            
            for x in range(0,5-index):
                id = "0" + id

        elif 'Ultra-Rare' not in card:            
            continue
                
        os.system('rename ' + card + ' ' + id + card[index:len(card)].replace('Ultra-Rare','Legendary'))

        i+=1


