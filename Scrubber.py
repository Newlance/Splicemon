from xml.etree.ElementInclude import include
from bs4 import BeautifulSoup as bs
from numpy import mod
import pandas as pd
import requests # to get image from the web
import shutil # to save it locally
import os
import csv
import random



USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
# US english
LANGUAGE = "en-US,en;q=0.5"
perfMode = True

PokeDex = pd.read_csv('pokedex.csv')


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
    ParentA=PokeDex.loc[PokeDex['Number']==int(prefix), 'EvolvesFromNum'].item()
    ParentB=PokeDex.loc[PokeDex['Number']==int(suffix), 'EvolvesFromNum'].item()
    if(pd.isna(ParentA)):
        ParentA=prefix
    if(pd.isna(ParentB)):
        ParentB=suffix    
    return [ParentA, ParentB]

def get_hybrid_name(prefixNum, suffixNum,prefixOptions,suffixOptions):    
    return (prefixOptions[int(prefixNum)-1].text + suffixOptions[int(suffixNum)-1].text)
    


def get_all_selects(soup):
    return soup.find_all("select")


def get_image(soup):
    return soup(id="pk_img")

def get_all_options(select):
    return select.find_all('option')


def download_image(prefix,suffix,filename):
    ## Set up the image URL and filename
    
    image_url = "https://images.alexonsager.net/pokemon/fused/" + prefix['value'] +"/"+ prefix['value'] + "." + suffix['value'] + ".png"
    filename = "./images/" + filename + ".png"

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

def main():    
    # get the soup
    

    pkmn_a_xpath = '//*[@id="select1"]'
    pkmn_b_xpath = '//*[@id="select2"]'
    pkmn_ab_xpath = '//*[@id="pk_img"]'
    url = "https://pokemon.alexonsager.net/"
    
    
   # details = f"https://{county}.realtaxlien.com/popup/popup-certificates.cfm"        
    soup = get_soup(url)  
    
    selects = get_all_selects(soup)
    img1 = selects[0]
    img2 = selects[1]
    prefixes = get_all_options(selects[2])
    suffixes = get_all_options(selects[3])
    
    
    i=1 
    j=1         
    with open("hybridex.csv", 'w', newline='') as csvfile: 
        #csvwriter = csv.writer(csvfile) 
        #csvwriter.writerow(['id','name','type','HP','Length','weight','code','EvolvesFromID', 'EvolvesFromName']) 
        for prefix in prefixes:     
            for suffix in suffixes:                       
                if(prefix['value'] != suffix['value']):                
                    
                    randomModifier = (random.randint(0,40) + 80) / 100
                    if(random.randint(0,100) > 95):
                        #small chance for a small chance at something unique
                        randomModifier*= ((random.randint(0,100) + 50) / 100)
                    EvolvesFrom = get_evolves_from(prefix['value'], suffix['value'])                
                    Type = get_type(suffix)
                    HP = int(get_HP(prefix,suffix,randomModifier))
                    Length = int(get_length(prefix, suffix, randomModifier))
                    weight = int(get_lbs(prefix,suffix, randomModifier))
                    name = prefix.text.strip() + suffix.text.strip()

                    code = hex(int(prefix['value'])) + "." + hex(int(suffix['value']))


                    if((EvolvesFrom[0]==prefix['value'] and EvolvesFrom[1] == suffix['value']) or int(EvolvesFrom[0]) == int(EvolvesFrom[1])):
                        EvolvesFromID = ""
                        EvolvesFromName = ""
                    else:                    
                        EvolvesFromID = hex(int(EvolvesFrom[0])) + "." + hex(int(EvolvesFrom[1]))
                        EvolvesFromName = get_hybrid_name(EvolvesFrom[0],EvolvesFrom[1],prefixes,suffixes)                    
                        

                    filename = Type + "/" + str(j) + "." + name
                    print(str(j))
                    #csvwriter.writerow([str(j),name,Type, str(HP), Length, weight, code, EvolvesFromID, EvolvesFromName ])
                    if(Type=="Water"):
                        download_image(prefix, suffix, filename)
                    j=j+1
    
    hybridImg = get_image(soup)



if __name__ == "__main__":
    import sys
    #try:              
        #county = sys.argv[1]
    #except IndexError:
        #county = ["orangefl","sarasotafl","duvalfl"]
        #print("Please specify a URL.\nUsage: python html_table_extractor.py [URL]")
       # exit(1)
    main()


