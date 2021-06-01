#%%
#  ===========================  
import json 
from influxdb import InfluxDBClient, DataFrameClient

# file = "/Users/dantonucci/Alubel/Esempi_json/json with session and project.json"
file = "/Users/dantonucci/Alubel/Esempi_json/json_errato_2.json"
# file = "/Users/dantonucci/Alubel/Esempi_json/json_errato.json"

class Connection_DB:

    def __init__(self,host,port,username,password,database):
        self.host = host
        self.port = port
        self.username =  username
        self.password = password
        self.database = database

    def db_connection(self):
        Client = InfluxDBClient(
            host =  self.host,
            port = self.port,
            username = self.username,
            password= self.password,
            database = self.database,
            ssl = True,
            verify_ssl= True
        )
        return (Client)

       
Project_name = 'Test'       
host_DB =  'ts.eurac.net'
port_DB =  443
username_DB =  'new_air_rw'
password_DB = '#7WT?lZUfB+snr*0b80#'
database_DB = 'new_air_renene'


DB_input = Connection_DB(host = host_DB, 
                        port = port_DB,
                        username = username_DB, 
                        password = password_DB,
                        database= database_DB)  

with open(file) as json_file:
    data = json.load(json_file)


def FromJson_to_Database(data,DB_input):
    ''' 
    Get Json file and post file in the database.
    create a measurement 
    '''
    Client = DB_input.db_connection() 
    
    data_body = {}
    tags_body = {}
    fields = {}
    input_Json = []
    
   
    for item in data.items():
        input_Json.append(item[0])
    
    tags_body['session'] = data['session']
    tags_body["configuration"] = data['configuration']   
        
    for indice in range(4, len(input_Json)):
            value = input_Json[indice]
            room = data[value]
            data_body["measurement"] = f"{data['project']}.{value}"
            data_body['tags'] =tags_body
            data_body["time"] = data['time']

            for element in room:
                    try:
                        if len(room[element]) == 0:
                            return("empty list")
                        else:                         
                            for item in room[element]:                        
                                text = f"{value}.{element}:{item}"
                                valore = data[value][element][item]
                                fields[text] = valore 
                                data_body["fields"] = fields
                                json_body=[data_body]
                                
                                Client.write_points(json_body)                            
                    except:                   
                        return("There is an error on the json data")                             
    return('Data Uploaded')

Result = FromJson_to_Database(data,DB_input)



#%%
#  =========================== TEST or DELETE MEASUREMENT =============================
    
# connessione con il database
Client = DB_input.db_connection()  
Value = Client.get_list_measurements()
json.dumps(Value)

# check data
Measurement_name = '"project1.A"'
field_sens = '"A.ADF:TM02TY"'
field_sens = "*"
Query = f"SELECT {field_sens} FROM {Measurement_name}"
Client.query(Query)

# drop series if wrong
Client.delete_series(database= 'new_air_renene', measurement='project1.AS')



# %%
