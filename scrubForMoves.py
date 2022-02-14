from asyncio.windows_events import NULL
from email.policy import default
from xml.etree.ElementInclude import include
from bs4 import BeautifulSoup as bs
from numpy import mod
import pandas as pd
import requests # to get image from the web
import shutil # to save it locally
import os
import csv
import random
from os import listdir, stat
import os
from os.path import isfile, join
from ast import literal_eval
import re
import time
from PIL import Image, ImageDraw, ImageFont
import textwrap

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
# US english
LANGUAGE = "en-US,en;q=0.5"
perfMode = True

PokeDex = pd.read_csv('pokedex.csv')
project_path = os.getcwd()
Types = ["Water","Ground","Lightning","Bug","Colorless","Psychic"]#"Ice","Ghost","Fighting","Poison","Grass","Rock","Fire",
domain = "https://www.pokemon.com"
chosen_card_url=""
query = ""


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
    #weaknessUL = soup.find_all('ul',{'class':'card-energies'})
    try:
        return resistBlock.find('li')['title']
    except:
        return NULL

def get_retreat_cost(retreatBlock):    
    return len(retreatBlock.find_all('li'))

def get_description(ability, parentPokemon, HybridPokemon):
        try:
            s = ability.find('pre').text.strip().replace(parentPokemon,HybridPokemon).replace('Pokemon','Splicémon').replace('Pokémon','Splicémon')        
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
    

def build_description(moveName, description, output_path,wrap):
    description = moveName + description
    para = textwrap.wrap(description, width=wrap)

    MAX_W, MAX_H = 340,100
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

    im.save(output_path + '\\ability.png')    


def get_next(soup):
    nextBlock = soup.find("div",{"id":"cards-load-more"})
    links = nextBlock.find_all('a')
    try:
        return links[1]['href']
    except:
        return ""

def main():    
    url = domain + "/us/pokemon-tcg/pokemon-cards/"    
    HybriDex = pd.read_csv('hybridex.csv')    
        
    for Type in Types:
        print("Starting " + Type)
        card_path = project_path + "\\images\\CardsNoAbilities\\" + Type + "\\"
        output_path = card_path + "output"
        cards = [f for f in listdir(card_path) if isfile(join(card_path, f))]
        
        i=0
        for card in cards:            
            success=False
            if i<0:
                i+=1
                continue

            while(not success):
                try:

                    id = card[0:card.find('.')]
                    name = HybriDex.loc[HybriDex['id']==int(id), 'name'].item()        
                    code = HybriDex.loc[HybriDex['id']==int(id), 'code'].item()
                    rarity = card[card.find('-')+1:len(card)-4]

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



                    if(rarity=="Common"):        
                        numAbilities=1
                    else:
                        numAbilities=2            
                    os.system('magick convert ' + card_path + "\\" + card + ' ' + output_path + '\\' + card)
                    for ability in range(0,numAbilities):                
                        if(len(possibleAbilities)>0):
                            randomIndex = random.randint(0,len(possibleAbilities)-1)                                                
                            #os.system('magick convert -background transparent -fill "#001" pango:"<span size=\'small\'><b>' + possibleAbilities[randomIndex]['name'].replace("'","\'").replace('"','\"') + '</b> ' +  possibleAbilities[randomIndex]['description'].replace("'","\'").replace('$','\\n') + '</span>" ' + output_path + '\\ability.png')
                            #os.system('magick convert ' + output_path + '\\ability.png -gravity west -background none -extent 340x100 ' + output_path + '\\ability.png')
                            if len(possibleAbilities[randomIndex]['damage'])<1:
                                width = 50
                            else:
                                width = 40
                            build_description(possibleAbilities[randomIndex]['name'].replace("'","\'"), possibleAbilities[randomIndex]['description'].replace("'","\'").replace('$',' '), output_path,width)
                            os.system('magick convert -font C:/Users/Newlance/Documents/python/python/PokeMixer/fonts/gill-rp.ttf -fill Black -pointsize 32 -gravity east -draw "text 0,0 \'' + str(possibleAbilities[randomIndex]['damage']) + '\'" ' + output_path + '\\ability.png ' + output_path + '\\ability.png')                
                            os.system('magick convert ' + output_path + '\\ability.png -gravity center -background none -extent 474x100 ' + output_path + '\\ability.png')                    
                            match len(possibleAbilities[randomIndex]['cost']):
                                    case 1:
                                        size = "100%"
                                    case 2: 
                                        size = "220x110"
                                    case 3: size = "200%"
                                    case 4: size = "200%"
                                    case _:
                                        size = "200%"
                                        #print("something weird happened:" + str(len(possibleAbilities[randomIndex]['cost'])))
                            while len(possibleAbilities[randomIndex]['cost'])<1 or possibleAbilities[randomIndex]['cost'][0] == "Free":                                
                                possibleAbilities.pop(randomIndex)
                            cost = possibleAbilities[randomIndex]['cost'][0]
                            os.system('magick convert ' + project_path + '\\images\\CardsNoAbilities\\elements\\' + cost + '.png -gravity northwest -background none -extent ' + size + ' ' + output_path + '\\cost.png')
                            for costIndex in range(1,len(possibleAbilities[randomIndex]['cost'])):
                                match costIndex:
                                    case 1:
                                        os.system('magick mogrify -format png -path ' + output_path + ' -gravity northeast -draw "image over 0,0 0,0 \'' + project_path + '\\images\\CardsNoAbilities\\elements\\' + possibleAbilities[randomIndex]['cost'][costIndex] + '.png\'" ' + output_path + '\\cost.png')
                                    case 2:
                                        os.system('magick mogrify -format png -path ' + output_path + ' -gravity southwest -draw "image over 0,0 0,0 \'' + project_path + '\\images\\CardsNoAbilities\\elements\\' + possibleAbilities[randomIndex]['cost'][costIndex] + '.png\'" ' + output_path + '\\cost.png')
                                    case 3:                
                                        os.system('magick mogrify -format png -path ' + output_path + ' -gravity southeast -draw "image over 0,0 0,0 \'' + project_path + '\\images\\CardsNoAbilities\\elements\\' + possibleAbilities[randomIndex]['cost'][costIndex] + '.png\'" ' + output_path + '\\cost.png')
                            
                            mod=75*(ability)                
                            os.system('magick convert ' + output_path + '\\cost.png -resize 28% ' + output_path + '\\cost.png')
                            os.system('magick mogrify -format png -path ' + output_path + ' -gravity west -draw "image over 0,0 0,0 \''+ output_path + '\\cost.png\'" ' + output_path + '\\ability.png')

                            os.system('magick mogrify -format png -path ' + output_path + ' -gravity center -draw "image over 25,' + str(90+mod) + ' 474,100 \'' + output_path + '\\ability.png\'" ' + output_path + '\\' + card)
                            #time.sleep(1)
                            #if os.path.exists(output_path + '\\cost.png'):
                            #    os.remove(output_path + '\\cost.png')
        #                    if os.path.exists(output_path + '\\ability.png'):
                            try:
                                os.remove(output_path + '\\ability.png')                    
                            except:
                                print('magick convert -background transparent -fill "#001" pango:"<span size=\'small\'><b>' + possibleAbilities[randomIndex]['name'].replace("'","\'").replace('"','\"') + '</b> ' +  possibleAbilities[randomIndex]['description'].replace("'","\'") + '</span>" ' + output_path + '\\ability.png')
                                print()
                                print(possibleAbilities[randomIndex])  
                                print()
                                print(output_path + '\\ability.png')
                                raise ValueError('A very specific bad thing happened.')
                            possibleAbilities.pop(randomIndex)
                            #time.sleep(1)
                            
                    
                    hitpoints=0
                    for HP in HPs:
                        hitpoints+=int(HP)
                    hitpoints=hitpoints/len(HPs)
                    os.system('magick convert -font ' + project_path + '\\fonts\gill-rp.TTF -fill Black -pointsize 20 -gravity east -draw "text 80,-270 \''+ str(HP) + ' HP\'" ' + output_path + '\\' + card + ' ' + output_path + '\\' + card)    


                    for weakness in weaknesses:
                        for resist in resistances:
                            if weakness == resist:
                                weaknesses.pop(weaknesses.index(weakness))
                                resistances.pop(resistances.index(resist))
                    
                    k=0
                    for weakness in weaknesses:                
                        os.system('magick mogrify -format png -path ' + output_path + ' -gravity southwest -draw "image over ' + str(63-((len(weaknesses)-1)*15)+(30*k)) + ',75 30,30 \'' + project_path + '\\images\\CardsNoAbilities\\elements\\' + weakness + '.png\'" ' + output_path + '\\' + card)
                        k+=1
                    k=0
                    for resist in resistances:
                        os.system('magick mogrify -format png -path ' + output_path + ' -gravity southwest -draw "image over ' + str(225-((len(resistances)-1)*15)+(30*k)) + ',75 30,30 \'' + project_path + '\\images\\CardsNoAbilities\\elements\\' + resist + '.png\'" ' + output_path + '\\' + card)
                        k+=1
                        
                    for rc in range(0,retreatCost):
                        os.system('magick mogrify -format png -path ' + output_path + ' -gravity southeast -draw "image over ' + str(65-((retreatCost-1)*15)+(rc*30)) + ',75 30,30 \'' + project_path + '\\images\\CardsNoAbilities\\elements\\Colorless.png\'" ' + output_path + '\\' + card)                    
                    i+=1
                    if(i%10==0):
                        print(str(i) + " of " + str(len(cards)))
                    success = True
                except:
                    print("retrying...")
                    success=False
        print(Type + " Done!")
        print()
        print()


if __name__ == "__main__":
    import sys
    #try:              
        #county = sys.argv[1]
    #except IndexError:
        #county = ["orangefl","sarasotafl","duvalfl"]
        #print("Please specify a URL.\nUsage: python html_table_extractor.py [URL]")
       # exit(1)
    main()
