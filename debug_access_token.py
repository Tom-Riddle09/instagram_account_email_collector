from defines import getCreds, makeApiCall
import datetime

def debugAccessToken( params ) :

	endpointParams = dict() # parameter to send to the endpoint
	endpointParams['input_token'] = params['access_token'] # input token is the access token
	endpointParams['access_token'] = params['access_token'] # access token to get debug info on

	url = params['graph_domain'] + '/debug_token' # endpoint url

	return makeApiCall( url, endpointParams, params['debug'] ) # make the api call

def get_expiry(creds):
	params = getCreds() # get creds
	params['debug'] = 'yes' # set debug
	#update params data 
	params['access_token'] = creds['token']
	params['client_id'] = creds['client_id']
	params['client_secret'] = creds['client_secret']
	params['page_id'] = creds['page_id']
	params['instagram_account_id'] = creds['ig_acc_id']
	params['ig_username'] = creds['ig_username']

	response = debugAccessToken( params ) # hit the api for some data!

	print(f'''\nApp Name:{creds['app_name']}
	   \nClient Id:{creds['client_id']}
	   \nClient Secret:{creds['client_secret']}
		\nPage Id:{creds['page_id']}
		\nInstagram Account Id:{creds['ig_acc_id']}
		\nInstagram Username:{creds['ig_username']}\n''')

	print ("\nData Access Expires at: ") # label
	print (datetime.datetime.fromtimestamp( response['json_data']['data']['data_access_expires_at'] )) # display out when the token expires

	print ("\nToken Expires at: ") # label
	print (datetime.datetime.fromtimestamp( response['json_data']['data']['expires_at'] )) # display out when the token expires