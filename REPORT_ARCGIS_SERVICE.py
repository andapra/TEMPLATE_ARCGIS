from arcgis.gis import GIS
import arcgis.gis.admin

from datetime import datetime
import os
import pandas as pd
import json

portal = '' ## input portal url example: https://gis.portal.com/webadaptor
username = '' ## username portal that can access username
password = '' ## password of the username
gis = GIS(portal, username, password)

reportingPath = os.getcwd() # change this path if you want to save other address

# will connect to arcgis server index 0, usually the arcgis server base deployment, you can change the other index 
gis_server = gis.admin.servers.list()[0]
service_folder = gis_server.services.folders

def main():
    df = pd.DataFrame(columns=[])
    list_dict = []
    for index, folder in enumerate(service_folder):
        print('=========== {} ==========='.format(folder))
        get_list_service = gis_server.services.list(folder= folder)
        length_service = len(get_list_service)
        for subindex, service_in_folder in enumerate(get_list_service):
            property_service = '{}'.format(service_in_folder.properties)
            load_data = json.loads(property_service)
            dict_frame = {}
            if index == 0 and subindex == 0:
                print('creating the dataframe columns')
                for key in load_data.keys():
                    get_value = load_data['{}'.format(key)]
                    df['{}'.format(key)] = [get_value]
            else:
                print('appending data to dataframe')
                for key in load_data.keys():
                    get_value = load_data['{}'.format(key)]
                    dict_frame['{}'.format(key)] = get_value
                list_dict.append(dict_frame)
            print('Complete in {} of {}'.format(subindex, length_service-1))
        print('=========== {} ==========='.format(folder))

    df_2 = pd.DataFrame(list_dict)

    print('Compiling dataframe')
    compiling = df.append(df_2, ignore_index=True)

    print('Generate Report')
    compiling.to_csv((os.path.join(os.getcwd(), 'report'+'.csv')), sep=';')

if __name__ == '__main__':
    startTime = datetime.today()
    
    try:
        print('Starting to process')
        main()
        print('End of the process')
        endTime = datetime.today()
        deltaTime = endTime - startTime
        print('Completed Time is {}'.format(deltaTime))

    except Exception as e:
        endTime = datetime.today()
        deltaTime = endTime - startTime
        print('Completed Time is {}'.format(deltaTime))
        raise(e)