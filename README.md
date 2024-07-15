Files Included
Program Files
1. Main_File.py
2. Buisness_discovery.py
3. Debug_access_token.py
4. Defines.py
5. Get_long_lived_access_token.py
6. Hashtag_search.py
7. media_discovery.py
Data Files
1. database.pickle
CHECK IF ALL THE ABOVE FILES ARE PRESENT IN THE FOLDER
DO NOT DELETE ANY FILES CREATED BY THE SCRIPT DURING EXECUTION


INSTALLATION
IDE Installation (For Windows OS)
● Visit https://www.python.org/downloads/
● Download Python Exe file.
● Install it. (During Installation remember to tick the box “Add Python to PATH”)
Python Library Installation
● Navigate to the folder where the script is stored.
● Right click and click on the “Open in Terminal” option.
● Now run the command [ pip install -r requirements.txt ] on the Command
Prompt.
● Wait for the Installation to be completed.
RUNNING THE SCRIPT
Steps
● Navigate to the folder where the script is stored.
● Right click and click on the “Open in Terminal” option.
● Now run command [ python Main.py]
● Now the script will start execution.




Miscellaneous
IG_MEDIA.CSV File Saving Format
[ username, dict_values([ username , media id , Number of likes , Number
of comments , Media Type, Time Stamp ]) ]
Access Token Expiry
● When Running the script, run the option “Update Access Token” first.
● Note the Expiry Date for you access token.
● When the Token Expires, Visit https://developers.facebook.com/
● Click on “My Apps” option
● Login Using FaceBook Credentials mentioned in the Credential heading.
● Hover over the top header options “Tools” and click on option “Graph API Explorer”
on the drop down menu
● Now on the right side you’ll see option “Generate Access Token”, click on it to
generate access token.
● Copy the new Access Token.
● The newly generated Access Token is only valid for 1 hour.
Extend Access Token Expiry Period to 2 Months
● Open file “defines.py”
● On line number 15 you can see the previous Access Token, replace it with the new
one.
● Save the file.
● Now run the Main.py Script
● Select option “Update Access Token”
● Follow the Steps on the Screen to extend the expiry period.



------------------------------------------------EOF!-----------------------------------------------------------
