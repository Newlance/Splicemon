from fileinput import filename
from logging import basicConfig
from xml.etree.ElementInclude import include
from bs4 import BeautifulSoup as bs
from numpy import mod
import pandas as pd
import requests # to get image from the web
import shutil # to save it locally
import os
import csv
import random
import errno
from os import listdir
from os.path import isfile, join, exists
from asyncio.windows_events import NULL
from email.policy import default
from xml.etree.ElementInclude import include
from ast import literal_eval
from PIL import Image, ImageDraw, ImageFont
import textwrap

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
# US english
LANGUAGE = "en-US,en;q=0.5"

Types = []#Done and verified:"Lightning","Colorless","Psychic","Bug","Ground","Water","Dragon","Fire","Poison","Rock","Grass","Ice","Ghost","Fighting", need to redo: XXX Need to verify:,
project_path = os.getcwd()
PokeDex = pd.read_csv('pokedex.csv')
hybridex_filename = "hybridex.csv"
HybriDex = pd.read_csv(hybridex_filename)
domain = "https://www.pokemon.com"
chosen_card_url=""
query = ""


flare_path=project_path + "/images/CardTemplates/Flare/"
card_template_path = project_path + "/images/CardTemplates/"


def post_soup(url,body):
    """Constructs and returns a soup using the HTML content of `url` passed"""
    
    # initialize a session
    session = requests.Session()
    # set the User-Agent as a regular browser
    session.headers['User-Agent'] = USER_AGENT
    # request for english content (optional)
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    # make the request
    html = requests.post(url, data = body)
    # return the soup
    return bs(html.content, "html.parser")

def get_soup(url):
    """Constructs and returns a soup using the HTML content of `url` passed"""
    # initialize a session
    session = requests.Session()
    # set the User-Agent as a regular browser
    session.headers['User-Agent'] = USER_AGENT
    # request for english content (optional)
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    # make the request
    html = requests.get(url)
    # return the soup
    return bs(html.content, "html.parser")

def get_evolves_from(prefix,suffix):    
    #get ID of mon parent correlating to splicemon's ID
    ParentA=PokeDex.loc[PokeDex['Number']==int(prefix), 'EvolvesFromNum'].item()
    ParentB=PokeDex.loc[PokeDex['Number']==int(suffix), 'EvolvesFromNum'].item()
    #if no value found
    if(pd.isna(ParentA)):
        #parent is self
        ParentA=prefix
        #if no value is found
    if(pd.isna(ParentB)):
        #parent is self
        ParentB=suffix    
    return [ParentA, ParentB]
   


def get_all_selects(soup):
    return soup.find_all("select")

def get_all_options(select):
    return select.find_all('option')


def download_image(splicemon):
    ## Set up the image URL and filename

    prefix = int(splicemon[5][0:splicemon[5].find('.')],16)
    suffix = int(splicemon[5][splicemon[5].find('.')+1:len(splicemon[5])],16)    
        
    image_url = "https://images.alexonsager.net/pokemon/fused/" + prefix['value'] +"/"+ prefix['value'] + "." + suffix['value'] + ".png"

    directory = verifyFolder("./images/" + splicemon[2] + "/")
    filename = directory + splicemon[0] + "." + splicemon[1] + ".png"

    # Open the url image, set stream to True, this will return the stream content.
    r = requests.get(image_url, stream = True)

    # Check if the image was retrieved successfully
    if r.status_code == 200:
        # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
        r.raw.decode_content = True
        

        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise


        # Open a local file with wb ( write binary ) permission.
        with open(filename,'wb') as f:
            shutil.copyfileobj(r.raw, f)
            
        print('Image sucessfully Downloaded: ',filename)
    else:
        print('Image Couldn\'t be retreived')

def get_type(suffix):
    return PokeDex.loc[PokeDex['Number']==int(suffix['value']), 'Type'].item()

def get_inches(feet, inches):
    return int(inches) + (int(feet)*12)

def get_length(prefix,suffix,mod):
    LengthAstr = str(PokeDex.loc[PokeDex['Number']==int(prefix['value']), 'Length'].item())    
    feetA = LengthAstr[0:LengthAstr.find('′')]    
    InchesA = LengthAstr[LengthAstr.find('′')+1:LengthAstr.find('″')]
    lengthA = get_inches(feetA, InchesA)

    LengthBstr = str(PokeDex.loc[PokeDex['Number']==int(suffix['value']), 'Length'].item())    
    feetB = LengthBstr[0:LengthBstr.find('′')]    
    InchesB = LengthBstr[LengthBstr.find('′')+1:LengthBstr.find('″')]
    lengthB = get_inches(feetB, InchesB)
    
    ab= lengthA + lengthB
    return (ab/2)*mod

def get_lbs(prefix,suffix,mod):
    a=PokeDex.loc[PokeDex['Number']==int(prefix['value']), 'lbs'].item()
    b=PokeDex.loc[PokeDex['Number']==int(suffix['value']), 'lbs'].item()
    return int((a+b)/2)*mod

def get_HP(prefix,suffix,mod):    
    a=PokeDex.loc[PokeDex['Number']==int(prefix['value']), 'HP'].item()
    b=PokeDex.loc[PokeDex['Number']==int(suffix['value']), 'HP'].item()
    return int((a+b)/2)*mod

def get_id(j):
    if(j<10):
        return "0000" + str(j)
    elif(j<100):
        return "000" + str(j)
    elif(j<1000):
        return "00" + str(j)
    elif(j<10000):
        return "0" + str(j)
    else:
        return str(j)


def write_hybridex(splicemon,csvwriter):    
    csvwriter.writerow(splicemon)

def getPokestats(prefix,suffix,prefixes,suffixes,i):
    randomModifier = (random.randint(0,40) + 80) / 100
    if(random.randint(0,100) > 95):
        #small chance for a small chance at something unique
        randomModifier*= ((random.randint(0,100) + 50) / 100)
    EvolvesFrom = get_evolves_from(prefix['value'], suffix['value'])                
    #changed from origional to mix things up
    Type = get_type(prefix)                
    Length = int(get_length(prefix, suffix, randomModifier))
    weight = int(get_lbs(prefix,suffix, randomModifier))
    name = prefix.text.strip() + suffix.text.strip()

    code = hex(int(prefix['value'])) + "." + hex(int(suffix['value']))

    #if neither mon's parents are evolved forms
    if((EvolvesFrom[0]==prefix['value'] and EvolvesFrom[1] == suffix['value']) or int(EvolvesFrom[0]) == int(EvolvesFrom[1])):
        EvolvesFromID = ""
        EvolvesFromName = ""
    else:                    
        EvolvesFromID = hex(int(EvolvesFrom[0])) + "." + hex(int(EvolvesFrom[1]))
        EvolvesFromName = prefixes[int(EvolvesFrom[0])-1].text + suffixes[int(EvolvesFrom[1])-1].text

    return [str(i),name,Type, Length, weight, code, EvolvesFromID, EvolvesFromName ]

def verifyFolder(path):
    isExist = os.path.exists(path)

    if not isExist:    
        # Create a new directory because it does not exist 
        os.makedirs(path)
        print("The new directory is created!")

    return path

def get_mon_options():
# get the soup
    
    mixer_url = "https://pokemon.alexonsager.net/"    
    soup = get_soup(mixer_url)  
    
    selects = get_all_selects(soup)
    prefixes = get_all_options(selects[2])
    suffixes = get_all_options(selects[3])

    return prefixes, suffixes
def get_mon_images_and_populate_hybridex():
    prefixes, suffixes = get_mon_options()

    i=1         
    with open(hybridex_filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile) 
        csvwriter.writerow(['id','name','type','Length','weight','code','EvolvesFromID', 'EvolvesFromName']) 
        for prefix in prefixes:     
            for suffix in suffixes:  
                ### if parents arent from the same mon. Splices only!                     
                if(prefix['value'] != suffix['value']):                
                    ### get all important mon stats from the pokedex
                    splicemon = getPokestats(prefix,suffix,prefixes,suffixes,i) 
                    ### Write mon data to hybridex (starts a new file each time this is run)         
                    write_hybridex(splicemon,csvwriter)                                   
                    ### filter and download by type only, or make == into != to download all
                    if(splicemon[2]=="DELETE"):                        
                        download_image(splicemon)
                    i=i+1
                    #print(str(i))     
def addRandomBackground(mon_path, mon, backgrounds_path, backgrounds, outputFolder,Type):
    backgroundIndex = random.randint(0, len(backgrounds)-1)    
    if exists('Temp.png'):
        os.remove('Temp.png')
    os.system('magick convert "' + backgrounds_path + backgrounds[backgroundIndex] + '" -gravity center -crop 3:2 -resize 500x333  "' + outputFolder + backgrounds[backgroundIndex] + '"')  
    os.system('magick mogrify -format png -path ' + outputFolder + ' -gravity center -draw "image over 0,-118 360,255 \'' + outputFolder + backgrounds[backgroundIndex] + '\' image over 0,-118 0,0 \'' + mon_path + mon + '\'" ' + card_template_path + Type + '.png')        
    os.system('rename ' + outputFolder + Type + '.png Temp.png')    
    os.remove(outputFolder + backgrounds[backgroundIndex])  


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

def get_stats(mon):
    id = mon[0:mon.find('.')]
    name = HybriDex.loc[HybriDex['id']==int(id), 'name'].item()
    lengthInches = int(HybriDex.loc[HybriDex['id']==int(id), 'Length'].item())
    lengthFt = int(int(lengthInches)/12)
    lengthInches = lengthInches - (lengthFt*12)        
    weight =HybriDex.loc[HybriDex['id']==int(id), 'weight'].item()
    code = HybriDex.loc[HybriDex['id']==int(id), 'code'].item()
    Type = HybriDex.loc[HybriDex['id']==int(id), 'type'].item()

    return id, name, lengthFt, lengthInches, weight, code, Type
def getStringID(id):
    strId = id
    if len(id) < 5:                
        for x in range(0,5-len(id)):
            strId = "0" + strId
    return strId


def addFlare(mon,outputFolder):
    id,name,lengthFt,lengthInches,weight,code,Type = get_stats(mon)
    hasEvolved = False
    canEvolve=False
    if(not pd.isna(HybriDex.loc[HybriDex['id']==int(id), 'EvolvesFromID'].item())):
        hasEvolved = True
        evolvedFrom = HybriDex.loc[HybriDex['id']==int(id), 'EvolvesFromName'].item()           
        evolvedFromCode = str(HybriDex.loc[HybriDex['id']==int(id), 'EvolvesFromID'].item())            
        evolvedFromId = str(HybriDex.loc[HybriDex['code']==evolvedFromCode, 'id'].item())
        if(not pd.isna(HybriDex.loc[HybriDex['code']==evolvedFromCode, 'EvolvesFromID'].item())):
            gen = 3
        else:
            gen = 2
    else:
        gen = 1

    match gen:
        case 2:
            priorStage = "basic"
        case 3:
            priorStage = "Stage 1"
        case _:
            priorStage = "N/A"

    if(not HybriDex.loc[HybriDex['EvolvesFromID']==code, 'name'].empty):
        canEvolve=True
        if not hasEvolved:
            gen=1

    randomRoll = random.randint(0,100)
        
    Legendary=isLegendary(code)

    if Legendary == 2:
        rarity = "Legendary"
    elif Legendary == 1:
        rarity = "Rare"
    elif canEvolve:
        if(gen==1):
            if(randomRoll<80):
                rarity = "Common"
            elif(randomRoll<95):
                rarity = "Uncommon"
            else:
                rarity = "Rare"                                            
        elif(gen==2):
            if(randomRoll<10):
                rarity = "Common"
            elif(randomRoll<90):
                rarity = "Uncommon"
            elif(randomRoll<=100):
                rarity = "Rare"
            else:
                rarity = "Legendary"
        elif(gen==3):                    
            rarity = "Legendary"
    else:
        if(gen==1):
            if(randomRoll<10):
                rarity = "Common"
            elif(randomRoll<50):
                rarity = "Uncommon"
            elif(randomRoll<=100):
                rarity = "Rare"
            else:
                rarity = "Legendary"                        
        elif(gen==2):
            if(randomRoll<10):
                rarity = "Common"
            elif(randomRoll<60):
                rarity = "Uncommon"
            elif(randomRoll<=100):
                rarity = "Rare"
            else:
                rarity = "Legendary"
        elif(gen==3):
            if(randomRoll<=1):
                rarity = "Common"
            elif(randomRoll<20):
                rarity = "Uncommon"
            elif(randomRoll<=100):
                rarity = "Rare"
            else:
                rarity = "Legendary"
            
    mogrify = "image over 203,295 10,10 \'" + flare_path + rarity + ".png\'\
            image over -190,37 31,23 \'" + flare_path + "1st.png\'"         
    rp=""
    rbi=""    
    if(priorStage=="N/A"):
        rp+='text 40,-297 \'Basic Splicémon\' '
        magickText("gill-rb.TTF",20,"Black","west",'Temp.png','Temp.png','text 50,-270 ' + name)              
    else:
        if Type == "Normal" or "vee" in evolvedFrom:
            Type = "Colorless"
        elif Type == "Electric":
            Type = "Lightning"
        mogrify += "image over -170,-280 75,75 \'" + project_path + "/images/" + Type + "/" + str(evolvedFromId) + "." + evolvedFrom + ".png\'"
        rbi+='text 95,-297 \'Evolves from ' + evolvedFrom + '\' '
        magickText("gill-rb.TTF",20,"Black","west",'Temp.png','Temp.png','text 100,-270 ' + name)             
        rp+='text 40,-297 \'Put ' + name + ' on the ' + priorStage + ' Splicémon\' '
        
    rbi+='text 120,32 \'' + Type + ' Splicemon. Length: ' + str(lengthFt) + '` ' + str(lengthInches) + '``, Weight: ' + str(weight) + ' lbs.\' '
    rbi+='text 50,265 \'This creature has a strange tattoo that reads ' + code + '.\' \
            text 50,280 \'I wonder what that means...\''
    magickText("gill-rbi.TTF",12,"Black","west",outputFolder + 'Temp.png',outputFolder + 'Temp.png', rbi)
    rp+='text 50, 300 \'' + str(id) + '/22650\''
    magickText("gill-ri.TTF",10,"Black","east",outputFolder + 'Temp.png',outputFolder + 'Temp.png',rp)                
    
    os.system('magick mogrify -format png -path ' + outputFolder + ' -gravity center -draw "'+mogrify+'" ' + outputFolder + 'Temp.png')

    return rarity

def magickText(font, size, color, gravity, srcFile, dstFile,string):
    string.replace("'","\'").replace('"','\"').replace('Poké','Splicé')
    os.system('magick convert -font ' + project_path + '\\fonts\\' + font +' -fill ' + color + ' -pointsize ' + str(size) + ' -gravity ' + str(gravity) + ' -draw "' + str(string) + '" ' + srcFile + ' ' + dstFile)
def magickImg(outputFolder, gravity, dst,string):    
    #string.replace("'","\'").replace('"','\"')
    os.system('magick mogrify -format png -path ' + outputFolder + ' -gravity ' + gravity + ' -draw "' + string + '" ' + dst)        

def fileExists(mon,path):
    partialName = mon[0:mon.find('.png')]
    file = [fn for fn in listdir(path) if partialName in fn]

    return len(file)>0

def post_soup(url,body):
    """Constructs and returns a soup using the HTML content of `url` passed"""
    
    # initialize a session
    session = requests.Session()
    # set the User-Agent as a regular browser
    session.headers['User-Agent'] = USER_AGENT
    # request for english content (optional)
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    # make the request
    html = requests.post(url, data = body)
    # return the soup
    return bs(html.content, "html.parser")

def get_soup(url):
    """Constructs and returns a soup using the HTML content of `url` passed"""
    # initialize a session
    session = requests.Session()
    # set the User-Agent as a regular browser
    session.headers['User-Agent'] = USER_AGENT
    # request for english content (optional)
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    # make the request
    html = requests.get(url)
    # return the soup
    return bs(html.content, "html.parser")

def get_all_links(soup,hyperlink):
    ul = soup.find('ul', {'class': 'cards-grid clear'})
    #li = list(ul.descendants)
    try:
        return ul.find_all('a',href=True)
    except:
        print()
        print("Hyperlink: " + hyperlink)
    #return ul.find_all('li')

def get_cost(ability):
    list_items = ability.find_all('li')
    cost = []#{'Colorless':0,'Fire':0,'Water':0,'Grass':0,'Lightning':0,'Fighting':0,'Psychic':0,'Darkness':0,'Metal':0,'Fairy':0,'Dragon':0,'Free':0}        
    for li in list_items:
        try:
            if(li['title'] == "Free"):
                #print("A free ability was detected...")
                raise ValueError("Nothing valuable is free")
            else:                
                cost.append(li['title'])
        except:
            #print('There was no cost found. Probably a bad ability')
            raise ValueError('There was no cost found. Probably a bad ability')
    return cost


def get_HP(block):
    try:
        span = block.find('span',{"class":"card-hp"})        
        return span.text.strip()[2:]
    except:
        print(block)
        print(domain + chosen_card_url)    


def get_weakness(weaknessBlock):    
    try:
        return weaknessBlock.find('li')['title']
    except:
        return ""

def get_resistance(resistBlock):
    try:
        return resistBlock.find('li')['title']
    except:
        return NULL

def get_retreat_cost(retreatBlock):    
    return len(retreatBlock.find_all('li'))

def get_description(ability, parentPokemon, HybridPokemon):
        try:
            s = ability.find('pre').text.strip().replace(parentPokemon,HybridPokemon).replace('Pokemon','Splicémon').replace('Poké','Splicé')        
            if(s=="n/a"):
                return ""
            else:
                return s
        except:
            return ""

def get_ability_name(ability):
    try:
        return ability.find('h4').text.strip()
    except:
        return ""

def get_damage(ability):
    try:
        return ability.find('span').text.strip()
    except:
        return ""
    

def get_a(li):
    return li.find_all('a',href=True)


def get_abilities(soup,parentPokemon,HybridPokemon):
    abilities = []
    abilitiesDiv = soup.find_all('div', {'class':'ability'})

    for div in abilitiesDiv:
        costImg = div.find_all('ul')
        if len(costImg)<1:
            abilitiesDiv.pop(abilitiesDiv.index(div))

    
    for ability in abilitiesDiv:        
        name = get_ability_name(ability) 
        damage = get_damage(ability)
        if(len(damage)>4):
            damage = ""
        description = get_description(ability, parentPokemon, HybridPokemon)
        if(len(description)>240):
            print("This description is too long. Try again")
            raise ValueError("This description is too long. Try again")    
        cost = get_cost(ability)       
        abilities.append({"name":name,"description":description,"damage":damage,"cost":cost})

    return abilities
    

def build_description(moveName, description, wrap):
    description = moveName + description
    para = textwrap.wrap(description, width=wrap)

    MAX_W, MAX_H = 400,100
    im = Image.new('RGBA', (MAX_W, MAX_H), (255, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype(
        'C:/Users/Newlance/Documents/python/python/PokeMixer/fonts/gill-cb.ttf', 15)

    smallFont = ImageFont.truetype(
        'C:/Users/Newlance/Documents/python/python/PokeMixer/fonts/gill-rp.TTF',15)

    current_h, pad = 0, 10

    pad=10
    draw.text((pad,(MAX_H/2)-((15/2)*len(para))), moveName, font=font, fill="#001")
    x,y = font.getsize(moveName)

    i=0

    firstline = True
    start = x+5
    for line in para:
        w, h = draw.textsize(line, font=font)    
        if(firstline):
            w=0
            line = line[len(moveName):]
            firstline=False 
            
        draw.text(((pad+start), (MAX_H/2)-((15/2)*len(para))+i), line, font=smallFont, fill="#001")   
        start=0     
        current_h += h + pad
        i+=15

    im.save('ability.png')    


def get_next(soup):
    nextBlock = soup.find("div",{"id":"cards-load-more"})
    links = nextBlock.find_all('a')
    try:
        return links[1]['href']
    except:
        return ""
def addAbilities(mon,rarity):
    try:
        url = domain + "/us/pokemon-tcg/pokemon-cards/" 
        id,name,lengthFt,lengthInches,weight,code,Type = get_stats(mon)
        parentA_id = code[0:code.find('.')]
        parentA_name = PokeDex.loc[PokeDex['Number']==literal_eval(parentA_id), 'Name'].item()  
        parentB_id = code[code.find('.')+1:len(code)]
        parentB_name = PokeDex.loc[PokeDex['Number']==literal_eval(parentB_id), 'Name'].item()          

        pokemonPair = [parentA_name, parentB_name]
        weaknesses = []
        resistances = []
        retreatCosts = []
        possibleAbilities=[]
        HPs=[]

        for pokemon in pokemonPair:
            query ="?basic-pokemon=on&stage-1-pokemon=on&stage-2-pokemon=on&level-up-pokemon=on&special-pokemon=on&pokemon-legend=on&restored-pokemon=on&break=on&pokemon-gx=on&cardName=" + pokemon   
            
            stats =[]
            while(len(stats)<2):
                soup = get_soup(url+query)                  
            
                links = get_all_links(soup,query)
                card_urls=[]
                for link in links:
                    card_urls.append(link['href'])                        
                next = domain + get_next(soup)
                while(next!=domain):
                    soup = get_soup(next)
                    links = get_all_links(soup,next)
                    for link in links:
                        card_urls.append(link['href'])                        
                    next = domain + get_next(soup)

                chosen_card_url = card_urls[random.randint(0,len(card_urls)-1)]        
                chosen_soup = get_soup(domain + chosen_card_url)
                ability = get_abilities(chosen_soup,pokemon,name)
                if(ability is not NULL):
                    possibleAbilities += ability
                stats = chosen_soup.find_all('div', {'class':'stat'})
            HPs.append(get_HP(chosen_soup))
            try:
                w=get_weakness(stats[0])
            except:
                print(stats)
            if(len(w)>0 and w not in weaknesses):
                weaknesses.append(w)
            r=get_resistance(stats[1])
            if(r!=NULL and r not in resistances):
                resistances.append(r)
            retreatCosts.append(get_retreat_cost(stats[2]))
        if(len(resistances)>0):
            resistance = resistances[len(resistances)-1]
        else:
            resistance= ""
        retreatCost=0
        for rc in retreatCosts:
            retreatCost+=rc
        retreatCost=retreatCost//len(retreatCosts)


        if exists('ability.png'):
            os.remove('ability.png')
        if(rarity=="Common"):        
            numAbilities=1
        elif(rarity=="Legendary"):
            numAbilities=3
        else:
            numAbilities=2  
        for ability in range(0,numAbilities):                
            if(len(possibleAbilities)>0):
                randomIndex = random.randint(0,len(possibleAbilities)-1)                                                
                if len(possibleAbilities[randomIndex]['damage'])<1:
                    width = 55
                else:
                    width = 45
                build_description(possibleAbilities[randomIndex]['name'].replace("'","\'"), possibleAbilities[randomIndex]['description'].replace("'","\'").replace('$',' '),width)
                os.system('magick convert -font C:/Users/Newlance/Documents/python/python/PokeMixer/fonts/gill-rp.ttf -fill Black -pointsize 32 -gravity west -draw "text 325,0 \'' + str(possibleAbilities[randomIndex]['damage']) + '\'" ability.png ability.png')                
                os.system('magick convert ability.png -gravity center -background none -extent 474x100 ability.png')                                                 
                while len(possibleAbilities[randomIndex]['cost'])<1 or possibleAbilities[randomIndex]['cost'][0] == "Free":                                
                    possibleAbilities.pop(randomIndex)
                cost = possibleAbilities[randomIndex]['cost'][0]
                if len(possibleAbilities[randomIndex]['cost'])<3:
                    size = "220x110"
                else:
                    size = "200%"
                if(len(possibleAbilities[randomIndex]['cost'])==1):
                    gravity="center"
                else:
                    gravity="northwest"
                os.system('magick convert ' + project_path + '\\images\\CardsNoAbilities\\elements\\' + cost + '.png -gravity ' + gravity + ' -background none -extent ' + size + ' cost.png')

                for costIndex in range(1,len(possibleAbilities[randomIndex]['cost'])):                    
                    match costIndex:
                        case 1:
                            os.system('magick mogrify -format png -gravity northeast -draw "image over 0,0 0,0 \'' + project_path + '\\images\\CardsNoAbilities\\elements\\' + possibleAbilities[randomIndex]['cost'][costIndex] + '.png\'" cost.png')
                        case 2:
                            os.system('magick mogrify -format png -gravity southwest -draw "image over 0,0 0,0 \'' + project_path + '\\images\\CardsNoAbilities\\elements\\' + possibleAbilities[randomIndex]['cost'][costIndex] + '.png\'" cost.png')
                        case 3:                
                            os.system('magick mogrify -format png -gravity southeast -draw "image over 0,0 0,0 \'' + project_path + '\\images\\CardsNoAbilities\\elements\\' + possibleAbilities[randomIndex]['cost'][costIndex] + '.png\'" cost.png')       
                padding = (150/numAbilities)*(ability)                
                os.system('magick convert cost.png -resize 20% cost.png')
                os.system('magick mogrify -format png -gravity west -draw "image over 0,0 0,0 \'cost.png\'" ability.png')

                os.system('magick mogrify -format png -gravity center -draw "image over 25,' + str(120 - (25*(numAbilities-1)) + padding) + ' 474,100 \'ability.png\'" Temp.png')
                try:
                    os.remove('ability.png')                    
                    os.remove('cost.png')                    
                except:
                    print('magick convert -background transparent -fill "#001" pango:"<span size=\'small\'><b>' + possibleAbilities[randomIndex]['name'].replace("'","\'").replace('"','\"') + '</b> ' +  possibleAbilities[randomIndex]['description'].replace("'","\'") + '</span>" ability.png')
                    print()
                    print(possibleAbilities[randomIndex])  
                    print()
                    print('ability.png')
                    raise ValueError('A very specific bad thing happened.')
                possibleAbilities.pop(randomIndex)
                                                
        hitpoints=0
        for HP in HPs:
            hitpoints+=int(HP)
        hitpoints=hitpoints/len(HPs)
        os.system('magick convert -font ' + project_path + '\\fonts\gill-rp.TTF -fill Black -pointsize 20 -gravity east -draw "text 80,-270 \''+ str(HP) + ' HP\'" Temp.png Temp.png')


        for weakness in weaknesses:
            for resist in resistances:
                if weakness == resist:
                    weaknesses.pop(weaknesses.index(weakness))
                    resistances.pop(resistances.index(resist))
        
        k=0
        for weakness in weaknesses:                
            os.system('magick mogrify -format png -gravity southwest -draw "image over ' + str(63-((len(weaknesses)-1)*15)+(30*k)) + ',75 30,30 \'' + project_path + '\\images\\CardsNoAbilities\\elements\\' + weakness + '.png\'" Temp.png Temp.png')
            k+=1
        k=0
        for resist in resistances:
            os.system('magick mogrify -format png -gravity southwest -draw "image over ' + str(225-((len(resistances)-1)*15)+(30*k)) + ',75 30,30 \'' + project_path + '\\images\\CardsNoAbilities\\elements\\' + resist + '.png\'" Temp.png Temp.png')
            k+=1
            
        for rc in range(0,retreatCost):
            os.system('magick mogrify -format png -gravity southeast -draw "image over ' + str(65-((retreatCost-1)*15)+(rc*30)) + ',75 30,30 \'' + project_path + '\\images\\CardsNoAbilities\\elements\\Colorless.png\'" Temp.png Temp.png')

        
        newId= getStringID(id)
        newFileName = newId + "." + name + "-" + rarity + '.png'     
        os.system('rename Temp.png ' + newFileName)
        return True
    except:
        return False

def main():
    
    #get_mon_images_and_populate_hybridex()  #uncomment this!

    for Type in Types:        
        print("Starting " + Type)

        mon_path = verifyFolder(project_path + "/images/" + Type + "/")
        mons = [f for f in listdir(mon_path) if isfile(join(mon_path, f))]

        backgrounds_path = verifyFolder(project_path + "/images/backgrounds/" + Type + "/")
        backgrounds = [f for f in listdir(backgrounds_path) if isfile(join(backgrounds_path, f))]

        outputFolder = verifyFolder(project_path + '\\images\\output\\' + Type + '\\')                
        os.chdir(outputFolder)
        i=1
        for mon in mons:
            if(i%10==0):
                print(str(i) + " of " + str(len(mons)))
            if i<=0:
                i+=1
                break
            if fileExists(mon,outputFolder):
                i+=1
                continue            
            print(mon)
            addRandomBackground(mon_path, mon,backgrounds_path, backgrounds, outputFolder,Type)                            
            rarity = addFlare(mon,outputFolder)
            
            while not addAbilities(mon,rarity):
                print("Ability failed! Retrying...")            
            i+=1
        print("Done with " + Type)
        print()
        print()
    print("Done!")

if __name__ == "__main__":
    import sys
    main()