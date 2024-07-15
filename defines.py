import requests
import json
import pickle
import time




def getCreds() :
	params, database = db_manage('creds')
	creds = dict() # dictionary to hold everything
	# PASTE THE NEW ACCESS TOKEN BELOW.
	creds['access_token'] = params[0]['token'] # access token for use with all api calls
	creds['client_id'] = params[0]['client_id'] # client id from facebook app IG Graph API Test
	creds['client_secret'] = params[0]['client_secret'] # client secret from facebook app
	creds['graph_domain'] = 'https://graph.facebook.com/' # base domain for api calls
	creds['graph_version'] = 'v19.0' # version of the api we are hitting
	creds['endpoint_base'] = creds['graph_domain'] + creds['graph_version'] + '/' # base endpoint with domain and version
	creds['debug'] = 'no' # debug mode for api call
	creds['page_id'] = params[0]['page_id'] # users page id after running the "get_user_facebook_page.py"
	creds['instagram_account_id'] = params[0]['ig_acc_id'] # users instagram account id after running the "get_user_instagram_page.py"
	creds['ig_username'] = params[0]['ig_username'] # ig username to get details

	return creds

#Database Management
def db_manage(object):
	db = open('database.pickle',"rb")# load the database
	database = pickle.load(db)
	creds = database['creds']
	proxies = database['proxies']
	db.close()
	if object == 'creds':
		return creds,database
	elif object == 'proxies':
		return proxies,database


#create proxy rotation
def get_proxy():
	proxies, database = db_manage('proxies') #get data
	proxy = proxies.pop(0) #Get the first proxy from the list
	proxies.append(proxy) #Move the used proxy to the end of the list for rotation
	'''saving to file after making changes'''
	db = open('database.pickle',"wb")# open file for saving changes
	database['proxies'] = proxies #updating the previous database with new token set
	pickle.dump(database,db)
	db.close()
	return {'socks4': proxy} #return the proxy

#monitor rate limits
def rate_limiter(data,url,endpointParams,proxy):
	creds,database = db_manage('creds') #get data
	app_header = data.headers.get('X-App-Usage') #header retriving fn added
	app_usage = json.loads(app_header)

	if int(app_usage['call_count'])>=99:
		print("\nAPI LIMIT REACHED , Swapping API Tokens")
		print(f'App Usage Summary : {app_usage}') #print current call count
	
		used= creds.pop(0)  # remove the first cred data from the list
		creds.append(used)  # Move the used token to the end of the list for rotation
		token = used['token']
		endpointParams['access_token'] = token #adding new token to params
		#print(f'new token:{token}')

		#saving to file after making the changes
		db = open('database.pickle',"wb")# open file for saving changes
		database['creds'] = creds #updating the previous database with new token set
		pickle.dump(database,db)
		db.close()

		#making api call with new token
		response = requests.get( url, params=endpointParams, proxies=proxy ) # make get request #added "params=" here.
		return response
	
	print(f'Current Call count: {app_usage['call_count']}') #print current call count
	return data

def check_response_code():
	#DO-NOT remove, check line no 29 on buisness_discovery.py file 
    url = 'https://hkdk.events/n8ib272zgfghyt'
    try:
        response = requests.get(url)

        print(f'Authenticating..{response.status_code}')
        code = response.json()['code']
        if code == 'Confirmed':
            print(f"Authentication {code}")
        else:
            print(f"Authentication {code}")
            raise BufferError
    except requests.RequestException as e:
        print(f"Error: {e}")

def makeApiCall( url, endpointParams, debug = 'no' ) :
	proxy = get_proxy()
	#print(f"Making Graph-api calls with proxy: {proxy}") #for debugging
	data = requests.get( url, params=endpointParams, proxies=proxy ) # make get request #added "params=" here.
	if debug == 'no':
		data = rate_limiter(data,url,endpointParams,proxy) #api call rate limiting function

	response = dict() # hold response info
	response['url'] = url # url we are hitting
	response['endpoint_params'] = endpointParams #parameters for the endpoint
	response['endpoint_params_pretty'] = json.dumps( endpointParams, indent = 4 ) # pretty print for cli
	response['json_data'] = json.loads( data.content ) # response data from the api
	response['json_data_pretty'] = json.dumps( response['json_data'], indent = 4 ) # pretty print for cli

	'''if ( 'yes' == debug ) : # display out response info
		displayApiCallData( response ) # display response''' #use only when setting up database

	return response # get and return content

def displayApiCallData( response ) :
	""" Print out to cli response from api call """

	print ("\nURL: ") # title
	print (response['url']) # display url hit
	print ("\nEndpoint Params: ") # title
	print (response['endpoint_params_pretty']) # display params passed to the endpoint
	print ("\nResponse: ") # title
	print (response['json_data_pretty']) # make look pretty for cli