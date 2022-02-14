import tkinter
import subprocess
from tkinter import *
from tkinter import filedialog
import os
import sys
import pickle
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as ExpectedConditions
from selenium.webdriver.support.ui import Select
from os.path import isfile, join
from os import listdir
import pandas as pd
from selenium.webdriver.common.keys import Keys
import os
import shutil

selling = True

root = Tk()
root.geometry('500x400')
root.title("NFTs Upload to OpenSea  ")
input_save_list = ["NFTs folder :", 0, 0, 0, 0, 0, 0, 0, 0]
main_directory = os.path.join(sys.path[0])
is_polygon = BooleanVar()
is_polygon.set(False)

hybridex_filename = "hybridex.csv"
HybriDex = pd.read_csv(hybridex_filename)

def open_chrome_profile():
    subprocess.Popen(
        [
            "start",
            "chrome",
            "--remote-debugging-port=8989",
            "--user-data-dir=" + main_directory + "/chrome_profile",
        ],
        shell=True,
    )

def save_file_path():
    return os.path.join(sys.path[0], "Save_file.cloud") 

# ask for directory on clicking button, changes button name.
def upload_folder_input():
    global upload_path
    upload_path = filedialog.askdirectory()
    Name_change_img_folder_button(upload_path)

def Name_change_img_folder_button(upload_folder_input):
    upload_folder_input_button["text"] = upload_folder_input

class InputField:
    def __init__(self, label, row_io, column_io, pos, master=root):
        self.master = master
        self.input_field = Entry(self.master)
        self.input_field.label = Label(master, text=label)
        self.input_field.label.grid(row=row_io, column=column_io)
        self.input_field.grid(row=row_io, column=column_io + 1)
        try:
            with open(save_file_path(), "rb") as infile:
                new_dict = pickle.load(infile)
                self.insert_text(new_dict[pos])
        except FileNotFoundError:
            pass

    def insert_text(self, text):
        self.input_field.delete(0, "end")
        self.input_field.insert(0, text)

    def save_inputs(self, pos):
        input_save_list.insert(pos, self.input_field.get())
        with open(save_file_path(), "wb") as outfile:
            pickle.dump(input_save_list, outfile)

###input objects###
collection_link_input = InputField("OpenSea Collection Link:", 2, 0, 1)
start_num_input = InputField("Start Number:", 3, 0, 2)
end_num_input = InputField("End Number:", 4, 0, 3)
price = InputField("Price:", 5, 0, 4)
title = InputField("Title:", 6, 0, 5)
description = InputField("Description:", 7, 0, 6)
file_format = InputField("NFT Image Format:", 8, 0, 7)
external_link = InputField("External link:", 9, 0, 8)


###save inputs###
def save():
    input_save_list.insert(0, upload_path)
    collection_link_input.save_inputs(1)
    start_num_input.save_inputs(2)
    end_num_input.save_inputs(3)
    price.save_inputs(4)
    title.save_inputs(5)
    description.save_inputs(6)
    file_format.save_inputs(7)
    external_link.save_inputs(8)
   


def fileExists(mon,path):
    partialName = mon[0:mon.find('-')]
    file = [fn for fn in listdir(path) if partialName in fn]

    return len(file)>0

def verifyFolder(path):
    isExist = os.path.exists(path)

    if not isExist:    
        # Create a new directory because it does not exist 
        os.makedirs(path)
        print("The new directory is created!")

    return path


# _____MAIN_CODE_____
def main_program_loop():
    ###START###
    project_path = main_directory
    file_path = upload_path
    collection_link = collection_link_input.input_field.get()
    completedFolder = verifyFolder(project_path + "/images/Output/Uploaded/")
    #start_num = int(start_num_input.input_field.get())
    #end_num = int(end_num_input.input_field.get())
    #loop_price = float(price.input_field.get())
    loop_title = title.input_field.get()
   # loop_file_format = file_format.input_field.get()
    loop_external_link = str(external_link.input_field.get())
    loop_description = description.input_field.get()

    ##chromeoptions
    opt = Options()
    opt.add_experimental_option("debuggerAddress", "localhost:8989")
    driver = webdriver.Chrome(
        executable_path=project_path + "/chromedriver.exe",
        chrome_options=opt,
    )
    wait = WebDriverWait(driver, 60)

    ###wait for methods
    def wait_css_selector(code):
        wait.until(
            ExpectedConditions.presence_of_element_located((By.CSS_SELECTOR, code))
        )
        
    def wait_css_selectorTest(code):
        wait.until(
            ExpectedConditions.elementToBeClickable((By.CSS_SELECTOR, code))
        )    

    def wait_xpath(code):
        wait.until(ExpectedConditions.presence_of_element_located((By.XPATH, code)))

    cards = [f for f in listdir(file_path) if isfile(join(file_path, f))]    
    #while end_num >= start_num:
    for card in cards:

        if fileExists(card,completedFolder):
                print(card + " has already been uploaded...")
                continue   

        id = card[0:card.find('.')]
        name = card[card.find('.')+1:card.find('-')]
        rarity = card[card.find('-')+1:card.find('_')]
        Type = card[card.find('_')+1:card.find('.png')]
        code = HybriDex.loc[HybriDex['id']==int(id), 'code'].item()
        alphaGene = code[0:code.find('.')]
        betaGene = code[code.find('.')+1:len(code)]

        match rarity:
            case "Common":
                price = .002
            case "Uncommon":
                price = .004
            case "Rare":
                price = .008
            case "Legendary":
                price = .03

        price = .0007
        
            

        #print(collection_link)
        print("Start creating NFT " +  loop_title + " " + card)
        driver.get(collection_link)
        # time.sleep(3)

        wait_xpath('//*[@id="__next"]/div[1]/main/div/div/div[1]/span/a')
        additem = driver.find_element_by_xpath('//*[@id="__next"]/div[1]/main/div/div/div[1]/span/a')
        additem.click()
        time.sleep(1)

        wait_xpath('//*[@id="media"]')
        imageUpload = driver.find_element_by_xpath('//*[@id="media"]')
        imagePath = os.path.abspath(file_path + "\\" + card)  # change folder here
        imageUpload.send_keys(imagePath)

        name_field = driver.find_element_by_xpath('//*[@id="name"]')
        name_field.send_keys(name)  # +1000 for other folders #change name before "#"
        time.sleep(0.5)

        ext_link = driver.find_element_by_xpath('//*[@id="external_link"]')
        ext_link.send_keys(loop_external_link)
        time.sleep(0.5)

        desc = driver.find_element_by_xpath('//*[@id="description"]')
        desc.send_keys(loop_description)
        time.sleep(0.5)

        properties = driver.find_element_by_xpath('//*[@id="main"]/div/div/section/div[2]/form/section/div[1]/div/div[2]/button/div/i')
        properties.click()

        addMore = driver.find_element_by_xpath('/html/body/div[5]/div/div/div/section/button')
        addMore.click()
        addMore.click()
        addMore.click()

        propType = driver.find_element_by_xpath('/html/body/div[5]/div/div/div/section/table/tbody/tr[1]/td[1]/div/div/input')
        propType.send_keys("Type")
        propTypeVal = driver.find_element_by_xpath('/html/body/div[5]/div/div/div/section/table/tbody/tr[1]/td[2]/div/div/input')        
        propTypeVal.send_keys(Type)

        propRarity = driver.find_element_by_xpath('/html/body/div[5]/div/div/div/section/table/tbody/tr[2]/td[1]/div/div/input')
        propRarity.send_keys("Rarity")
        propRarityVal = driver.find_element_by_xpath('/html/body/div[5]/div/div/div/section/table/tbody/tr[2]/td[2]/div/div/input')
        propRarityVal.send_keys(rarity)

        propAlphaGene = driver.find_element_by_xpath('/html/body/div[5]/div/div/div/section/table/tbody/tr[3]/td[1]/div/div/input')
        propAlphaGene.send_keys("Alpha Gene")
        propAlphaGeneVal = driver.find_element_by_xpath('/html/body/div[5]/div/div/div/section/table/tbody/tr[3]/td[2]/div/div/input')
        propAlphaGeneVal.send_keys(alphaGene)

        propBetaGene = driver.find_element_by_xpath('/html/body/div[5]/div/div/div/section/table/tbody/tr[4]/td[1]/div/div/input')
        propBetaGene.send_keys("Beta Gene")
        propBetaGeneVal = driver.find_element_by_xpath('/html/body/div[5]/div/div/div/section/table/tbody/tr[4]/td[2]/div/div/input')
        propBetaGeneVal.send_keys(betaGene)

        saveBtn = driver.find_element_by_xpath('/html/body/div[5]/div/div/div/footer/button')
        saveBtn.click()


        stats = driver.find_element_by_xpath('//*[@id="main"]/div/div/section/div[2]/form/section/div[3]/div/div[2]/button')
        stats.click()


        statId = driver.find_element_by_xpath('/html/body/div[7]/div/div/div/section/table/tbody/tr/td[1]/div/div/input')
        statId.send_keys("ID")
        statIdVal2 = driver.find_element_by_xpath('/html/body/div[7]/div/div/div/section/table/tbody/tr/td[3]/div/div/input')
        statIdVal2.send_keys(Keys.CONTROL + 'a')
        statIdVal2.send_keys("22650")
        statIdVal1 = driver.find_element_by_xpath('/html/body/div[7]/div/div/div/section/table/tbody/tr/td[2]/div/div/input')
        statIdVal1.send_keys(Keys.CONTROL + 'a')
        statIdVal1.send_keys(int(id))  

        saveBtn2 = driver.find_element_by_xpath('/html/body/div[7]/div/div/div/footer/button')
        saveBtn2.click()
       
        # Select Polygon blockchain if applicable
        if is_polygon.get():
            blockchain_button = driver.find_element(By.XPATH, '//*[@id="__next"]/div[1]/main/div/div/section/div/form/div[7]/div/div[2]')
            blockchain_button.click()
            polygon_button_location = '/html/body/div[1]/div/main/div/div/section/div[2]/form/div[7]/div/div[3]'
            wait.until(ExpectedConditions.presence_of_element_located(
                (By.XPATH, polygon_button_location)))            
            polygon_button = driver.find_element(
                By.XPATH, polygon_button_location)            
            polygon_button.click()
                
        create = driver.find_element_by_xpath('//*[@id="__next"]/div[1]/main/div/div/section/div[2]/form/div/div[1]/span/button')
        driver.execute_script("arguments[0].click();", create)
        time.sleep(1)

        wait_css_selector("i[aria-label='Close']")
        cross = driver.find_element_by_css_selector("i[aria-label='Close']")
        cross.click()
        time.sleep(1)

        #move card to output folder    
        os.rename(file_path + "\\" + card, completedFolder + card)

        if selling:
            main_page = driver.current_window_handle
            wait_xpath('//*[@id="__next"]/div[1]/main/div/div/div[1]/div/span[2]/a')
            sell = driver.find_element_by_xpath('//*[@id="__next"]/div[1]/main/div/div/div[1]/div/span[2]/a')
            sell.click()

            wait_css_selector("input[placeholder='Amount']")
            amount = driver.find_element_by_css_selector("input[placeholder='Amount']")
            amount.send_keys(str(price))

            wait_css_selector("button[type='submit']")
            listing = driver.find_element_by_css_selector("button[type='submit']")
            listing.click()                        
    
        
            wait_xpath("/html/body/div[4]/div/div/div/section/div/div/section/div/div/div/div/div/div/div/button")
            sign = driver.find_element_by_xpath("/html/body/div[4]/div/div/div/section/div/div/section/div/div/div/div/div/div/div/button")
            sign.click()
            time.sleep(2)
        
        #for handle in driver.window_handles:
        #    if handle != main_page:
        #        login_page = handle
        # change the control to signin page
        #driver.switch_to.window(login_page)
        #wait_css_selector("button[data-testid='request-signature__sign']")
        #sign = driver.find_element_by_css_selector("button[data-testid='request-signature__sign']")
        #sign.click()
        #time.sleep(1)
        
        # change control to main page
        #driver.switch_to.window(main_page)
        #time.sleep(1)        

        #start_num = start_num + 1
        print('NFT creation completed!')

#####BUTTON ZONE#######
button_save = tkinter.Button(root, width=20, text="Save Form", command=save) 
button_save.grid(row=23, column=1)
button_start = tkinter.Button(root, width=20, bg="green", fg="white", text="Start", command=main_program_loop)
button_start.grid(row=25, column=1)
isPolygon = tkinter.Checkbutton(root, text='Polygon Blockchain', var=is_polygon)
isPolygon.grid(row=20, column=0)
open_browser = tkinter.Button(root, width=20,  text="Open Chrome Browser", command=open_chrome_profile)
open_browser.grid(row=22, column=1)
upload_folder_input_button = tkinter.Button(root, width=20, text="Add NFTs Upload Folder", command=upload_folder_input)
upload_folder_input_button.grid(row=21, column=1)
try:
    with open(save_file_path(), "rb") as infile:
        new_dict = pickle.load(infile)
        global upload_path
        Name_change_img_folder_button(new_dict[0])
        upload_path = new_dict[0]
except FileNotFoundError:
    pass
#####BUTTON ZONE END#######
root.mainloop()
