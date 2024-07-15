from business_discovery import sort_acc
from hashtag_search import proxy_rotation
import csv
from debug_access_token import get_expiry
from get_long_lived_access_token import generate_token
import time
from media_discovery import get_acc_stats
import pickle
from defines import check_response_code



if __name__ == '__main__':
    while True:
        usr_inp = input('Select One: (Type in the Option Number) >\n1.Collect Usernames From IG Account\n2.Update Access Token\n3.Get Acoount Stats\n4.View Downloaded Data\n5.Exit\n>')
        if usr_inp == '1':
            hashtag = input("Type in Your Hashtag>")
            fol_min = int(input("Type in your Minimum Follower Threshold>"))
            fol_max = int(input("Type in your Maximum Follower Threshold>"))
            usr_nm_lst = proxy_rotation(hashtag) #obtains a list of ig usernames
            check_response_code() #function defined in defines.py
            with open('ig_username.csv', mode='w', newline='') as file:
                writer = csv.writer(file)
                for username in usr_nm_lst:
                    writer.writerow([username])
            print("\n10 Sec Delay activated to  bypass API rate limits")
            time.sleep(10)
            sort_acc(fol_min,fol_max)
            continue
        elif usr_inp == '2': #modify the token expiry program for token rotation.
            print('Loading Access Token Expiry Date..\n')
            dt = open('D:/Work/Neakma-insta-email/Main app/database.pickle',"rb")
            database = pickle.load(dt)
            dt.close()
            print('Displaying all Tokens, check App Name and generate new tokens for expired ones.')
            for params in database['creds']: #iterate through each token file
                get_expiry(params)#prints access token expiry date
            inp = input('Type in "Y" if you want to extend any Access Token Expiry Time.(else "N")>')
            if inp == 'Y' or inp == 'y':
                creds = {}
                creds['token'] = input("Enter the new Access Token:")
                creds['client_id'] = input("Enter the  Client_id:")
                creds['client_secret'] = input("Enter the Client Secret:")
                generate_token(creds)
                continue
        elif usr_inp == '3':
            get_acc_stats()
            print('\n Open file "ig_medias.csv" to View the Account Media Stats for Downloaded usernames \n')

        elif usr_inp == '4':
            print('Displaying UserName Bio Info >\n')
            with open('ig_emails.csv', mode='r', encoding='utf-8') as file:
                reader = csv.reader(file, delimiter='\t', lineterminator='\r', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                for row in reader:
                    print('\n')
                    for ele in row:
                        print(ele, end=' ')
                    time.sleep(0.25)
            print('\nDisplaying UserName Media Info >\n')
            with open('ig_media.csv', mode='r', encoding='utf-8') as file:
                reader = csv.reader(file, delimiter='\t', lineterminator='\r', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                for row in reader:
                    print('\n')
                    for ele in row:
                        print(ele, end=' ')
                    time.sleep(0.25)
        elif usr_inp == '5':
            print('Exiting..')
            exit()
        else:
            print('\nInvalid Input\n')
            continue


        




        
        
