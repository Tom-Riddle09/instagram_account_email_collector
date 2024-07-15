from bs4 import BeautifulSoup
import requests
import re
import pickle
import time
import random



def search_web(hashtag,city,proxy,header,proxies):
    url = f'https://www.google.com/search?q=site:instagram.com "{hashtag}" "{city}" "@gmail.com"&num=100'
    cr_pr = 0
    while True:
        page = requests.get(url, headers=header, proxies={'socks4': proxy}, timeout=5)
        print(f'API response status: {page.status_code}')
        if page.status_code == 429:
            print('Search has been rate limited. Swapping proxy and trying again...')
            prx = proxies.pop(0)  # Get the first proxy from the list
            proxies.append(prx)  # Move the used proxy to the end of the list for rotation
            proxy = proxies[0]  # Getting the new first proxy
            print(f'Using Combination: City- {city} Proxy - {proxy}' )
            cr_pr+=1
            if cr_pr == len(proxies): #checks if all the proxies have been used or not
                print("Proxy Swapping Blocked for 45 minutes.")
                time.sleep(2700)
                break
        else:
            break  # If response is 200, exit the loop
    
    soup = BeautifulSoup(page.text,'html')
    descrptn = soup.find_all('div', class_ = "BNeawe UPmit AP7Wnd lRVwie")
    usernames = []
    for item in descrptn:
        pattern = r'www\.instagram\.com\s›\s([\w\.]+)'
        match = re.search(pattern, str(item))
        if match:
            usernames.append(match.group(1))
    return usernames,proxies


def proxy_rotation(hashtag):
    print("Randomized time delays between API calls are set to avoid rate limits\n")
    usr_lst = []
    db = open('database.pickle','rb')
    database = pickle.load(db)
    cities = database['cities']
    proxies = database['proxies']
    headers = database['headers']
    db.close()
    for city in cities:
        delay = random.uniform(3, 5)  # Random delay between 20-40 seconds
        proxy = proxies[0] #cyclic selection of proxies
        header = random.choice(headers) #random selection of headers
        print(f'Using Combination: City- {city} Proxy - {proxy}' )
        names,proxies = search_web(hashtag, city, proxy,header,proxies)
        time.sleep(delay)
        print(f"Downloaded {len(names)} UserNames.")
        if len(names)>0:
            usr_lst.extend(names)
            #print(usr_lst)
    usr_lst = list(set(usr_lst))
    return usr_lst

