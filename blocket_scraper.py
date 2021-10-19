from bs4 import BeautifulSoup
import urllib3
import pandas as pd
import argparse
from datetime import date

parser = argparse.ArgumentParser()

parser.add_argument('--path', type=str, default=None, help='The directory where the csv file should be saved')
parser.add_argument('--pages_to_scrape', type=int, default=1, help='Number of pages of ads to be parsed. 1 page corresponds to 40 ads.')

args = parser.parse_args()

def blocket_scraper(path=None, pages_to_scrape=1):
    #Separate dictionaries containing lists with the info to be extracted from ads
    data_dict = {'Ad name': [], 'Category': [], 'Price': [], "Location":[],\
                 "Time": [], "Link":[], "ID": []}
        
    http = urllib3.PoolManager()
    
    for page in range(1, int(pages_to_scrape)+1):
        link = http.request('GET', f'https://www.blocket.se/annonser/hela_sverige?page={page}')
        soup = BeautifulSoup(link.data, 'html.parser')
        #Accessing all ads available on the pages
        alla_annonser = soup.find_all("div", class_='gaNDDX')
        #Accessing one ad from the page at a time
        for element in alla_annonser:
            
            #Extracting Ad name and adding it to the dict
            ad_name = element.find("span", class_="bkaUbj")
            data_dict['Ad name'].append(ad_name.text)
            
            #Extracting Category and adding it to the dict
            category = element.find("a", class_="dcKCyh")
            data_dict['Category'].append(category.text)
            
            #Extracting Price and adding it to the dict
            price = element.find("div", class_="fBHqpx")
            data_dict['Price'].append(price.text)
            
            #Extracting Location and adding it to the dict
            category_and_city = element.find("p", class_="lbavoU")
            location = category_and_city.text.split('·')[-1]
            data_dict['Location'].append(location)
            
            #Extracting Time and adding it to the dict
            time = element.find("p", class_="gEFkeH")
            #If the ad was created today
            if str(time.text[:4]) == 'Idag':
                time = time.text.split(' ')[1]
                time_ = f'{date.today()} {time}'
                data_dict['Time'].append(time_)
            else:
                data_dict['Time'].append(time.text)
                
            #Extracting Link and adding it to the dict
            link = element.find("a", class_="dcKCyh" )["href"]
            data_dict['Link'].append(f'https://www.blocket.se{link}')
            
            #Extracting ID and adding it to the dict
            id_ = element.attrs['to']
            id_ = id_.split('/')[-1]
            data_dict['ID'].append(id_)

    #Initializing DataFrame
    df = pd.DataFrame.from_dict(data_dict)
    if path:
        path_with_name = f'{path}blocket_corpus.csv'
        try:
            print('Corpus retrieved successfully')
            #Saving the scraped corpus to a CSV file
            df.to_csv(path_with_name, encoding='utf-8')
        except PermissionError:
            print('''
                  You already have a file under this name in the same directory.
                  Please delete the existing one first.
                  ''')
            
    else:
        try:
            print('Corpus retrieved successfully')
            df.to_csv("blocket_corpus.csv", encoding='utf-8')
        except PermissionError:
            print('''
                  
Please note you already have a file under this name in the same directory.
Please consider deleting the existing file.
''')
print()
if args:
    blocket_scraper(args.path, args.pages_to_scrape)
else:
    blocket_scraper()