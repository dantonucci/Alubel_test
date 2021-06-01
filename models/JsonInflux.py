#
def FromJson_to_Database(data,Client):
    ''' 
    Get Json file and post file in the database.
    data = json file
    Client = Influxdb Client 
    '''
    # element of the file to be uploaded in the influxDB
    data_body = {}
    tags_body = {}
    fields = {}
    input_Json = []
    
    # get list of Json Keys    
    for item in data.items():
        input_Json.append(item[0])

    # Definition of tags to be used in the json file 
    tags_body['session'] = data['session']
    tags_body["configuration"] = data['configuration']   
        
    # creation fo the file to be uploaded
    for indice in range(4, len(input_Json)): # range 4 because  from 0 to 3 there are tags and time information
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