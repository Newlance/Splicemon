from multiprocessing.connection import wait
from os import listdir
import os
from os.path import isfile, join
import random


Types = ["Rock"]
project_path = os.getcwd()
for Type in Types:
    
    img_path = project_path + "\images\\" + Type + "\\output\\"
    card_template_path = project_path + "\images\\CardTemplates\\"

    mons = [f for f in listdir(img_path) if isfile(join(img_path, f))]
    #backgrounds = [f for f in listdir(card_template_path) if isfile(join(backgrounds_path, f))]

    os.chdir('C:\\Program Files\\ImageMagick-7.1.0-Q16-HDRI\\')

    outputFolder = project_path + '\\images\\CardTemplates\\' + Type + '\\'
    
    i=0
    for mon in mons:                
        os.system('magick mogrify -format png -path ' + card_template_path + Type + ' -gravity center -draw "image over 0,-118 360,255 \'' + img_path + mon + '\'" ' + card_template_path + Type + '.png')        
        os.system('rename ' + card_template_path + Type + '\\' + Type + '.png ' + mon)
        print(str(i) + " of " + str(len(mons)))
        i=i+1
    print("DOne!")
    #print(backgrounds[backgroundIndex])
    