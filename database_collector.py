
import json
import requests
import pandas as pd
import os

authUsername = '' # api username
authPassword = '' #api password

class raveleryutils:

    def __init__(self, authUsername:str, authPassword:str):
        self.authUsername = authUsername
        self.authPassword = authPassword
        
    def get_patterns(self, query = '', page = 1, page_size = 100, craft = 'crochet') -> pd.core.frame.DataFrame:
        url = 'https://api.ravelry.com/patterns/search.json?query={}&page={}&page_size={}&craft={}'.format(query, page, page_size, craft)  
        r1 = requests.get(url, auth=requests.auth.HTTPBasicAuth(self.authUsername, self.authPassword))
        r1.close()

        return pd.DataFrame.from_records(json.loads(r1.text)['patterns'])
    
    def get_photos(self,photo_id):
        url = 'https://api.ravelry.com/photos/{}/sizes.json'.format(photo_id)

        r1 = requests.get(url, auth=requests.auth.HTTPBasicAuth(self.authUsername, self.authPassword))

        r1.close()
        photo_list=r1.json()

        for i in (photo_list['sizes']):
            if 'large' in i.values():
                return(i['url'])

class ImageHandler():
    def __init__(self):
        pass      

    def save_image(self,folder_name,file_name,img_url):
        img_data = requests.get(img_url).content
        with open(folder_name + '/' + file_name +'.jpg', 'wb') as handler:
            handler.write(img_data)


raveleryutils_api = raveleryutils(authUsername, authPassword)
crochet_stitch_names = ['shell' , 'popcorn' , 'crocodile', 'knit', 'jasmine', 'snowball','bobble','flurry','ripple','larksfoot','moss',
                        'bullion','basketweave','mesh','waffle']

page_size=1000

img_handler_obj=ImageHandler()

for query in crochet_stitch_names:
    top_hat_patterns = raveleryutils_api.get_patterns(query = query, page = 1, page_size = page_size) 

    if not os.path.exists(query):
        os.mkdir(query)

    for i in range(page_size):
        if top_hat_patterns.first_photo[i] is not None:
            top_hat_patterns.first_photo[i]['id']

            url = raveleryutils_api.get_photos(top_hat_patterns.first_photo[i]['id'])
            if url is not None:
                img_handler_obj.save_image(query,str(i),url)



