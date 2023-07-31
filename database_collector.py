
import json
import requests
import pandas as pd
import os

authUsername = 'eea85e442134d36c861bc2f46bafdfa0'
authPassword = 'Ts6L8lEbVk90wej2RhVIKq1UQLjvDyKqvM1Rc_sS'

class raveleryutils:

    def __init__(self, authUsername:str, authPassword:str):
        self.authUsername = authUsername
        self.authPassword = authPassword
        
    def get_patterns(self, query = '', page = 1, page_size = 100, craft = 'crochet') -> pd.core.frame.DataFrame:
        #define URL
        url = 'https://api.ravelry.com/patterns/search.json?query={}&page={}&page_size={}&craft={}'.format(query, page, page_size, craft)  
        #make the request
        r1 = requests.get(url, auth=requests.auth.HTTPBasicAuth(self.authUsername, self.authPassword))
        #close the connection
        r1.close()
        return pd.DataFrame.from_records(json.loads(r1.text)['patterns'])
    
 
class ImageHandler():
    def __init__(self):
        pass      

    def save_image(self,folder_name,file_name,img_url):
        img_data = requests.get(img_url).content
        with open(folder_name + '/' + file_name +'.jpg', 'wb') as handler:
            handler.write(img_data)

raveleryutils_api = raveleryutils(authUsername, authPassword)

page_size=100
query= 'shell'
top_hat_patterns = raveleryutils_api.get_patterns(query = query, page = 15, page_size = page_size) 

img_handler_obj=ImageHandler()
if not dir(query):
    os.mkdir(query)
for i in range(page_size):
    image_url=top_hat_patterns.first_photo[i]['medium2_url']
    img_handler_obj.save_image(query,str(i),image_url)



