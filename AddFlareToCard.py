from multiprocessing.connection import wait
from os import listdir
import os
from os.path import isfile, join
import random
from sre_parse import State
import pandas as pd
from os.path import exists





def isLegendary(code):
    legendaries= ['0x3','0x6','0x9','0x90','0x91','0x92','0x95','0x96','0x97']
    parentA = code[0:code.find('.')]
    parentB = code[code.find('.')+1:len(code)]
    if(parentA in legendaries and parentB in legendaries):
        print("A Legendary has been found!")
        return 2
    if(parentA in legendaries or parentB in legendaries):        
        return 1
    else:
        return 0


Types = ["Colorless",]

print("Starting batch process!")

HybriDex = pd.read_csv('hybridex.csv')

project_path = os.getcwd()
for Type in Types:
    print("Starting " + Type)
    
    card_path = project_path + "\\images\\CardTemplates\\" + Type + "\\"
    flare_path =project_path + "/images/CardTemplates/Flare/"

    cards = [f for f in listdir(card_path) if isfile(join(card_path, f))]    
    

    os.chdir('C:\\Program Files\\ImageMagick-7.1.0-Q16-HDRI\\')

    outputFolder = card_path + 'output\\'

    output_cards = [f for f in listdir(outputFolder) if isfile(join(outputFolder, f))]


    

    i=0
    for card in cards:
        
        id = card[0:card.find('.')]
        name = HybriDex.loc[HybriDex['id']==int(id), 'name'].item()       

        needsVerifying=False
        exists=False
        if needsVerifying:
            for e in output_cards:
                count = e.find(id+"."+name)
                if count > 0:
                    exists=True
                    break
        
        if(exists):
            i+=1
            continue
        else:
            needsVerifying=False
        
         
        HP = HybriDex.loc[HybriDex['id']==int(id), 'HP'].item()
        lengthInches = int(HybriDex.loc[HybriDex['id']==int(id), 'Length'].item())
        lengthFt = int(int(lengthInches)/12)
        lengthInches = lengthInches - (lengthFt*12)        
        weight =HybriDex.loc[HybriDex['id']==int(id), 'weight'].item()
        code = HybriDex.loc[HybriDex['id']==int(id), 'code'].item()        

        evolvedFrom = ""
        evolvedFromId = ""
        evolvedFromCode = ""
        #evolvesInto = ""
        #evolvesIntoCode = ""
        hasEvolved = False
        canEvolve = False

        thirdGen = False
        secondGen = False
        firstGen = False        
        if(not pd.isna(HybriDex.loc[HybriDex['id']==int(id), 'EvolvesFromID'].item())):
            hasEvolved = True
            try:
                evolvedFrom = HybriDex.loc[HybriDex['id']==int(id), 'EvolvesFromName'].item()           
                evolvedFromCode = str(HybriDex.loc[HybriDex['id']==int(id), 'EvolvesFromID'].item())            
                evolvedFromId = str(HybriDex.loc[HybriDex['code']==evolvedFromCode, 'id'].item())
            except:
                print("ERROR! " + code + " " + id + " " + evolvedFromCode)
            
            if(not pd.isna(HybriDex.loc[HybriDex['code']==evolvedFromCode, 'EvolvesFromID'].item())):
                thirdGen = True
            else:
                secondGen = True


        if(not HybriDex.loc[HybriDex['EvolvesFromID']==code, 'name'].empty):
            canEvolve=True
           # try:
            #    evolvesInto = HybriDex.loc[HybriDex['EvolvesFromID']==code, 'name'].item()
            #    evolvesIntoCode = HybriDex.loc[HybriDex['EvolvesFromID']==code, 'code'].item()
            #except:
            #    print("ERROR! " + code + " " + id)
        if(not hasEvolved):
            firstGen = True
        
        if(firstGen):
            priorStage = "N/A"
        elif(secondGen):
            priorStage = "basic"
        elif(thirdGen):
            priorStage = "Stage 1"
        else:
            priorStage = "ERROR"

        randomRoll = random.randint(0,100)
        
        Legendary=isLegendary(code)
        if(Legendary==2):
            rarity="Ultra-Rare"
        elif(Legendary==1):
            rarity = "Rare"
        elif(canEvolve):
            if(firstGen):
                if(randomRoll<80):
                    rarity="Common"
                elif(randomRoll<95):
                    rarity = "Uncommon"
                else:
                    rarity = "Rare"                                            
            elif(secondGen):
                if(randomRoll<10):
                    rarity="Common"
                elif(randomRoll<90):
                    rarity = "Uncommon"
                elif(randomRoll<=100):
                    rarity = "Rare"
                else:
                    rarity = "Ultra-Rare"
            elif(thirdGen):                    
                rarity = "Ultra-Rare"
        else:
            if(firstGen):
                if(randomRoll<10):
                    rarity="Common"
                elif(randomRoll<50):
                    rarity = "Uncommon"
                elif(randomRoll<=100):
                    rarity = "Rare"
                else:
                    rarity = "Ultra-Rare"                        
            elif(secondGen):
                if(randomRoll<10):
                    rarity="Common"
                elif(randomRoll<60):
                    rarity = "Uncommon"
                elif(randomRoll<=100):
                    rarity = "Rare"
                else:
                    rarity = "Ultra-Rare"
            elif(thirdGen):
                if(randomRoll<=1):
                    rarity="Common"
                elif(randomRoll<20):
                    rarity = "Uncommon"
                elif(randomRoll<=100):
                    rarity = "Rare"
                else:
                    rarity = "Ultra-Rare"

        mogrify = "image over 203,295 10,10 \'" + flare_path + rarity + ".png\'\
            image over -190,37 31,23 \'" + flare_path + "1st.png\'"         

        if(firstGen):
            os.system('magick convert -font ' + project_path + '\\fonts\gill-rb.TTF -fill Black -pointsize 20 -gravity west -draw "text 50,-270 ' + name + '" ' + card_path + card + ' ' + outputFolder + card)
            os.system('magick convert -font ' + project_path + '\\fonts\gill-rp.TTF -fill Black -pointsize 10 -gravity west -draw "text 50,-290 \'Basic Splicémon\'" ' + outputFolder + card + ' ' + outputFolder + card)
        else:
            mogrify += "image over -170,-280 75,75 \'" + project_path + "/images/" + Type + "/" + str(evolvedFromId) + "." + evolvedFrom + ".png\'"
            os.system('magick convert -font ' + project_path + '\\fonts\gill-rb.TTF -fill Black -pointsize 20 -gravity west -draw "text 100,-270 ' + name + '" ' + card_path + card + ' ' + outputFolder + card)
            os.system('magick convert -font ' + project_path + '\\fonts\gill-rbi.TTF -fill Black -pointsize 10 -gravity west -draw "text 85,-297 \'Evolves from ' + evolvedFrom + '\'" ' + outputFolder + card + ' ' + outputFolder + card)
            os.system('magick convert -font ' + project_path + '\\fonts\gill-ri.TTF -fill Black -pointsize 10 -gravity east -draw "text 40,-297 \'Put ' + name + ' on the ' + priorStage + ' Splicémon\'" ' + outputFolder + card + ' ' + outputFolder + card)


        os.system('magick convert -font ' + project_path + '\\fonts\gill-rbi.TTF -fill Black -pointsize 12 -gravity center -draw "text 0,32 \'' + Type + ' Splicemon. Length: ' + str(lengthFt) + '` ' + str(lengthInches) + '``, Weight: ' + str(weight) + ' lbs.\'" ' + outputFolder + card + ' ' + outputFolder + card)                    
        os.system('magick convert -font ' + project_path + '\\fonts\gill-rp.TTF -fill Black -pointsize 10 -gravity east -draw "text 42, 299 \'' + str(id) + '/22500\'" ' + outputFolder + card + ' ' + outputFolder + card)
        #os.system('magick convert -font ' + project_path + '\\fonts\gill-rp.TTF -fill Red -pointsize 20 -gravity east -draw "text 80,-270 \''+ str(HP) + ' HP\'" ' + outputFolder + card + ' ' + outputFolder + card)    


        os.system('magick mogrify -format png -path ' + outputFolder + ' -gravity center -draw "'+mogrify+'" ' + outputFolder + card)            
        os.system('magick convert -font ' + project_path + '\\fonts\gill-rbi.TTF -fill Black -pointsize 12 -gravity west -draw \
            "text 50,265 \'This creature has a strange tattoo that reads ' + code + '.\' \
                text 50,280 \'I wonder what that means...\'" ' + outputFolder + card + ' ' + outputFolder + card)                    
        os.system('rename ' + outputFolder + card + ' ' + id + '.' + name + '-' + rarity + '.png')        
        
                        
        i=i+1
        if(i%10==0):
            print(str(i) + " of " + str(len(cards)))
    print("Done with " + str(Type))
    print()
    

