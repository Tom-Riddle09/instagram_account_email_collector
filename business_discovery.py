import csv
import time
from defines import getCreds, makeApiCall
import re

def getAccountInfo( params,ig_username ) :
    endpointParams = dict() # parameter to send to the endpoint
    endpointParams['fields'] = 'business_discovery.username(' + ig_username + '){id,name,follows_count,followers_count,media_count,website,profile_picture_url,biography}' # string of fields to get back with the request for the account
    endpointParams['access_token'] = params['access_token'] # access token

    url = params['endpoint_base'] + params['instagram_account_id'] # endpoint url

    return makeApiCall( url, endpointParams, params['debug'] ) # make the api call

def extract_emails(text):
    # Regular expression pattern for matching email addresses
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    # Find all email addresses in the text using the pattern
    emails = re.findall(email_pattern, text)

    return emails

def sort_acc(follower_min,follower_max):
        filename = 'ig_emails.csv'
        open(filename, 'w').close() #create a new file to store emails
        input = open('ig_username.csv', 'r')
        content  = input.readlines()
        for line in content: #functions confirms  $  revieved by developer or not. if not working then $ not recieved
                if line: 
                    ig_username = line.strip() #store all username into this one

                params = getCreds() # get creds
                params['debug'] = 'no' # set debug
                response = getAccountInfo( params,ig_username ) # hit the api for some data!

                try:               
                    #Data From JSON
                    #user_id = response['json_data']['business_discovery']['id']
                    name = response['json_data']['business_discovery']['name']
                    #follows_count = response['json_data']['business_discovery']['follows_count']
                    follower_count = response['json_data']['business_discovery']['followers_count']
                    #website = response['json_data']['business_discovery']['website']
                    #profile_pic = response['json_data']['business_discovery']['profile_picture_url']
                    biography = response['json_data']['business_discovery']['biography']
                    bio = str(biography.encode("utf-8"))
                    #Data to CSV
                    if int(follower_count) >= follower_min and int(follower_count) <= follower_max:
                        email = extract_emails(bio)
                        if email:
                            with open(filename, 'a', encoding='utf-8') as csvfile:
                                employee_writer = csv.writer(csvfile, delimiter='\t', lineterminator='\r', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                                employee_writer.writerow(['Username:',ig_username,', Name: ', name,', Followers: ', follower_count,', Email : ', email])

                    print(ig_username + ' --- Done')
                except Exception as e:
                    print(ig_username + " --- Username Doesn't have email")
                    print('exception',e)
                #time.sleep(1)  #Delay between every API CALL 

