import pymongo
import requests

def loop(url: str = 'https://swapi.dev/api/starships/?page='):
   
    db = ['test'] 
    col = db['pilots']

    my_list = []

    for page_number in range(1, 5):
        req = requests.get(url + str(page_number))
        starships = req.json()['results']

        for ship in starships:
            pilots = ship['pilots']
            pilot_data = []
            
            for pilot_url in pilots:
                pilot_req = requests.get(f'{pilot_url}')
                pilot_name = pilot_req.json()['name'] 
                each_pilot_id = col.find( {'name': f'{pilot_name}'}, {'_id': 1} ) 

                for identity in each_pilot_id:
                    pilot_data.append(identity['_id'])
            
           
            ship['pilots'] = pilot_data

            my_list.append(ship)

    return my_list

def write_to_mongodb(data: dict, database: str = 'test', collectionName: str = 'starships', server: str = 'mongodb://localhost:27017/'):

    try: 
        client = pymongo.MongoClient(server) 
        print('Connection Successful')
    except:
        print('Connection Unsuccessful')
    
    db = client[database] 
    col = db[collectionName]
    col.insert_many(data)
    return print(f'Data has been written to database: {database}')
    
write_to_mongodb(loop())