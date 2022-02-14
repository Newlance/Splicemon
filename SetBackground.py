from multiprocessing.connection import wait
from os import listdir
import os
from os.path import isfile, join
import random


Types = ["Colorless"]
project_path = os.getcwd()
for Type in Types:
    
    mon_path = project_path + "\images\\" + Type + "\\"
    backgrounds_path = project_path + "\images\\backgrounds\\" + Type + "\\"

    mons = [f for f in listdir(mon_path) if isfile(join(mon_path, f))]
    backgrounds = [f for f in listdir(backgrounds_path) if isfile(join(backgrounds_path, f))]

    os.chdir('C:\\Program Files\\ImageMagick-7.1.0-Q16-HDRI\\')

    outputFolder = project_path + '\\images\\' + Type + '\\output\\'


    i=0
    for mon in mons:
                
        while True:
            backgroundIndex = random.randint(0, len(backgrounds)-1)
            print(backgrounds[backgroundIndex])
            os.system('magick convert "' + backgrounds_path + backgrounds[backgroundIndex] + '" -gravity center -crop 3:2 -resize 500x333  "' + outputFolder + mon + '"')  
            if(os.system('magick mogrify -format png -path ' + outputFolder + ' -gravity center -draw "image over 0,0 350,350 \'' + mon_path  + mon + '\'" \'' + outputFolder + mon ) == 0):
                break
            else:
                print('Another Error!')
        print(str(i) + " of " + str(len(mons)))
        i=i+1
    print("DOne!")
    #print(backgrounds[backgroundIndex])
    