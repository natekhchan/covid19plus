# Coded by Nathan Chan 
# A Covid19 Stats Analyzer
# Greetz to mdleung a.k.a Darth, cyberalvin, Aaron Race, and pyneapple
# Props to GOD THE FATHER.
# version 1.0

import os
import numpy as np
import pandas as pd
import requests
from datetime import date

responseSummary = requests.get("https://api.covid19api.com/summary")

covid19_basic_info = []
today = date.today()
todays_date = today.strftime("%B%d%Y")
json_response = responseSummary.json()



def list_countries():

    print("Countries Effected By COVID 19")
    print(73 * "-")
    print("Country | Slug")
    print(73 * "-")
    for item in json_response["Countries"]:
        if item['Country'] == "":
            pass
        else:            
            print(item['Country'] + " | " + item['Slug'])
    
def extract_info_per_country(countryname):
    for item in json_response["Countries"]:
        if item['Country'] == countryname or item['Slug'] == countryname:
            print("")
            print(("Newly Confirmed Cases Of COVID-19:  " + str(item['NewConfirmed'])))
            print(("Total Confirmed Cases Of COVID-19:  " + str(item['TotalConfirmed'])))
            print(("New Deaths Today: " + str(item['NewDeaths'])))
            print(("Total Deaths Overall: " + str(item['TotalDeaths'])))
            print(("Newly Recovered: " + str(item['NewRecovered'])))
            print(("Total Recovered: " + str(item['TotalRecovered'])))
            print("")
            print("For more detailed research on the CoronaVirus case, please visit: https://www.worldometers.info/coronavirus/")

def extract_info_per_province(countryname, provincename, responseProvince, json_response2):
    print("Province / State             " +  "Date               " + "Cases")
    for item in json_response2:
        if item['Province'] == provincename:
            print(str(item['Province']) + "    " + str(item['Date']) + "    " + str(item['Cases']))
   
def generate_csv_per_country():
    for item in json_response["Countries"]:
        covid19_basic_info.append([item['Country'], item['NewConfirmed'], item['TotalConfirmed'], item['NewDeaths'], item['TotalDeaths'], item['NewRecovered'], item['TotalRecovered']])
    dataset = pd.DataFrame(covid19_basic_info)
    print("Your .csv file is processed.")

    dataset.columns = ['Country', 'New Confirmed Cases', 'Total Confirmed Cases', 'New Deaths', 'Total Deaths', 'Newly Recovered', 'Total Recovered']
    dataset.to_csv(r'covid19dataSummaryData' + todays_date + '.csv', index=False, header=True)

def generate_csv_per_province(provincename, json_response2):
    covid19_province_info = []
    exportdata = input("Would you like to export CSV? ")
    if exportdata == "Y" or exportdata == "y":
        for item in json_response2:
            if item['Province'] == provincename:
                covid19_province_info.append([item['Province'], item['Date'], item['Cases']])
        dataset = pd.DataFrame(covid19_province_info)
        print("")
        print("Your .csv file is processed.")
        dataset.columns = ['Province', 'Date', 'Total Cases']
        dataset.to_csv(r'covid19data' + provincename + todays_date + '.csv', index=False, header=True)
        
    elif exportdata == "N" or exportdata == "n":
        print("Goodbye!")
    else:
        print("Goodbye!")

def get_menu_choice():
    os.system("cls")
    def print_menu():       # Your menu design here
        
        print("""\

                                    (`-.           _ .-') _                              
                                    _(OO  )_        ( (  OO) )                             
        .-----.  .-'),-----. ,--(_/   ,. \ ,-.-') \     .'_  .---.   .----.      ,-.     
        '  .--./ ( OO'  .-.  '\   \   /(__/ |  |OO),`'--..._)/_   | /  ,.  \     | |     
        |  |('-. /   |  | |  | \   \ /   /  |  |  \|  |  \  ' |   ||  |  \  |,---| |---. 
        /_) |OO  )\_)|  |\|  |  \   '   /,  |  |(_/|  |   ' | |   | '  `-'''  ---| |---' 
        ||  |`-'|   \|  | |  |   \     /__),|  |_.'|  |   / : |   |  `- /  '     | |     
        (_'  '--'\  `'  '-'  '    \   /   (_|  |   |  '--'  / |   |   ,'  /      `-'     
        `-----'       `-----'      `-'      `--'   `-------'  `---'  `---'               


        """)

        print(73 * "-")
        print("   M A I N - M E N U")
        print(73 * "-")
        print("1. List Countries Effected And Slug ID")
        print("2. API Discovery by Country / Slug")
        print("3. API Discovery by Province / State")
        print("4. Export Summary Data To CSV")
        print("5. Exit")   
        print(73 * "-")

    loop = True
    int_choice = -1

    while loop:          # While loop which will keep going until loop = False
        print_menu()    # Displays menu
        choice = input("Enter your choice [1-5]: ")

        if choice == '1':
            int_choice = 1
            list_countries()
            loop = True
        elif choice == '2':
            choice = ''
            countryname = input("Enter your Country Name or Slug ID from Option 1 To Extract Info: ")
            if len(countryname) > 0:
                extract_info_per_country(countryname)
            int_choice = 2
            loop = False
        elif choice == '3':
            choice = ''
            countryname = input("Enter your Country Name or Slug ID from Option 1 To Extract Info: ")
            responseProvince = requests.get("https://api.covid19api.com/dayone/country/" + countryname + "/status/confirmed/live")
            json_response2 = responseProvince.json()
            if len(countryname) > 0:
                provincename = input("Enter your Province / State Name: ")
                extract_info_per_province(countryname, provincename, responseProvince, json_response2)        
                generate_csv_per_province(provincename, json_response2)
            int_choice = 2
            loop = False    
        elif choice == '4':
            choice = ''
            generate_csv_per_country()
            int_choice = 3
            loop = False
        elif choice == '5':
            int_choice = -1
            print("Exiting..")
            loop = False  # This will make the while loop to end
        else:
            # Any inputs other than values 1-4 we print an error message
            input("Wrong menu selection. Enter any key to try again..")
    return [int_choice, choice]


if __name__ == "__main__": 
    get_menu_choice()


