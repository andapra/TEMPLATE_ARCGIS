from arcgis.gis import GIS
from datetime import datetime
import os
import pandas as pd
import json

class reporting_server():
    def __init__(self, portal, username, password, reportingPath) -> None:
        self.portal = portal
        self.username = username
        self.password = password
        self.reportingPath = reportingPath

    def main(self):
        print('Sign in to federated portal')
        gis = GIS(self.portal, self.username, self.password)

        # will connect to arcgis server index 0, usually the arcgis server base deployment, you can change the other index 
        print('Connecting to the main server 0, a bit longer, please wait')
        gis_server = gis.admin.servers.list()[0]

        print(f'Retrieve all service folders')
        service_folder = gis_server.services.folders

        list_base_service = list()
        list_ogc_service = list()
        list_wcs_service = list()
        list_wfs_service = list()
        list_version_service = list()
        list_kml_service = list()
        list_fs_service = list()
        list_na_service = list()

        for folder in service_folder:
            print(f'=================== {folder} ===================')
            get_list_service = gis_server.services.list(folder= folder)

            if len(get_list_service) == 0:
                pass
            
            else:
                for service in get_list_service:
                    print(f'Recording service of {service}')
                    property_service = '{}'.format(service.properties)
                    load_data = json.loads(property_service)

                    temp_dict = dict()
                    for key in load_data.items():
                        if key[0] == 'properties':
                            for sub_key in key[1].items():
                                temp_dict.__setitem__(f'{sub_key[0]}_property', sub_key[1]) 

                        elif key[0] == 'portalProperties':
                            for sub_key in key[1].items():
                                if sub_key[0] == 'portalItems':
                                    for sub_data in sub_key[1]:
                                        temp_dict.__setitem__(sub_data['type'], sub_data['itemID'])    

                                else:
                                    temp_dict.__setitem__(f'{sub_key[0]}_portal_property', sub_key[1])
                        
                        elif key[0] == 'datasets':
                            temp_dict.__setitem__(key[0], ' ,'.join(key[1]))
                        
                        elif key[0] == 'frameworkProperties':
                            temp_dict.__setitem__(key[0], ' ,'.join([f'{sub_key[0]} = {sub_key[1]}' for sub_key in key[1].items()]))

                        elif key[0] == 'extensions':
                            temp_dict_na = dict()
                            temp_dict_ogc = dict()
                            temp_dict_wcs = dict()
                            temp_dict_wfs = dict()
                            temp_dict_version = dict()
                            temp_dict_kml = dict()
                            temp_dict_fs = dict()

                            for data in key[1]:
                                if data['typeName'] == 'OGCFeatureServer':
                                    for sub_sub_key in data.items():
                                        if sub_sub_key[0] == 'properties':
                                            for sub_sub_key_property in sub_sub_key[1].items():
                                                temp_dict_ogc.__setitem__(sub_sub_key_property[0], sub_sub_key_property[1])

                                        else:
                                            temp_dict_ogc.__setitem__(sub_sub_key[0], sub_sub_key[1])

                                    list_ogc_service.append(pd.DataFrame.from_dict([temp_dict_ogc]))
                                    
                                elif data['typeName'] == 'WCSServer':
                                    for sub_sub_key in data.items():
                                        if sub_sub_key[0] == 'properties':
                                            for sub_sub_key_property in sub_sub_key[1].items():
                                                temp_dict_wcs.__setitem__(sub_sub_key_property[0], sub_sub_key_property[1])

                                        else:
                                            temp_dict_wcs.__setitem__(sub_sub_key[0], sub_sub_key[1])

                                    list_wcs_service.append(pd.DataFrame.from_dict([temp_dict_wcs]))

                                elif data['typeName'] == 'WFSServer':
                                    for sub_sub_key in data.items():
                                        if sub_sub_key[0] == 'properties':
                                            for sub_sub_key_property in sub_sub_key[1].items():
                                                temp_dict_wfs.__setitem__(sub_sub_key_property[0], sub_sub_key_property[1])

                                        else:
                                            temp_dict_wfs.__setitem__(sub_sub_key[0], sub_sub_key[1])
                                    
                                    list_wfs_service.append(pd.DataFrame.from_dict([temp_dict_wfs]))
                                    
                                elif data['typeName'] == 'VersionManagementServer':
                                    for sub_sub_key in data.items():
                                        if sub_sub_key[0] == 'properties':
                                            for sub_sub_key_property in sub_sub_key[1].items():
                                                temp_dict_version.__setitem__(sub_sub_key_property[0], sub_sub_key_property[1])

                                        else:
                                            temp_dict_version.__setitem__(sub_sub_key[0], sub_sub_key[1])

                                    list_version_service.append(pd.DataFrame.from_dict([temp_dict_version]))

                                elif data['typeName'] == 'KmlServer':
                                    for sub_sub_key in data.items():
                                        if sub_sub_key[0] == 'properties':
                                            for sub_sub_key_property in sub_sub_key[1].items():
                                                temp_dict_kml.__setitem__(sub_sub_key_property[0], sub_sub_key_property[1])

                                        else:
                                            temp_dict_kml.__setitem__(sub_sub_key[0], sub_sub_key[1])
                                    
                                    list_kml_service.append(pd.DataFrame.from_dict([temp_dict_kml]))

                                elif data['typeName'] == 'FeatureServer':
                                    for sub_sub_key in data.items():
                                        if sub_sub_key[0] == 'properties':
                                            for sub_sub_key_property in sub_sub_key[1].items():
                                                temp_dict_fs.__setitem__(sub_sub_key_property[0], sub_sub_key_property[1])

                                        else:
                                            temp_dict_fs.__setitem__(sub_sub_key[0], sub_sub_key[1])

                                    list_fs_service.append(pd.DataFrame.from_dict([temp_dict_fs]))

                                elif data['typeName'] == 'NAServer':
                                    for sub_sub_key in data.items():
                                        if sub_sub_key[0] == 'properties':
                                            for sub_sub_key_property in sub_sub_key[1].items():
                                                temp_dict_na.__setitem__(sub_sub_key_property[0], sub_sub_key_property[1])

                                        else:
                                            temp_dict_na.__setitem__(sub_sub_key[0], sub_sub_key[1])

                                    list_na_service.append(pd.DataFrame.from_dict([temp_dict_na]))
                        else:
                            temp_dict.__setitem__(key[0], key[1])
                        
                    print(f'Recording service of {service} is completed')

                    list_base_service.append(pd.DataFrame.from_dict([temp_dict]))
                    

        print('Compiling dataframe')
        df_base = pd.concat(list_base_service).reset_index().drop(columns=['index'])
        df_fs = pd.concat(list_fs_service).reset_index().drop(columns=['index'])
        df_kml = pd.concat(list_kml_service).reset_index().drop(columns=['index'])
        df_na = pd.concat(list_na_service).reset_index().drop(columns=['index'])
        df_ogc = pd.concat(list_ogc_service).reset_index().drop(columns=['index'])
        df_wcs = pd.concat(list_wcs_service).reset_index().drop(columns=['index'])
        df_wfs = pd.concat(list_wfs_service).reset_index().drop(columns=['index'])
        df_version = pd.concat(list_version_service).reset_index().drop(columns=['index'])

        print('Generate Report')
        with pd.ExcelWriter(os.path.join(self.reportingPath, 'reporting_server'+'.xlsx')) as writer:
            df_base.to_excel(writer, sheet_name='base')
            df_fs.to_excel(writer, sheet_name='Feature Server')
            df_kml.to_excel(writer, sheet_name='KML Server')
            df_na.to_excel(writer, sheet_name='NAServer')
            df_ogc.to_excel(writer, sheet_name='OGC Server')
            df_wcs.to_excel(writer, sheet_name='WCS Server')
            df_wfs.to_excel(writer, sheet_name='WFS Server')
            df_version.to_excel(writer, sheet_name='Version Server')

if __name__ == '__main__':
    startTime = datetime.today()

    portal = input("Input portal url <example: https://gis.portal.com/webadaptor>: ") ## input portal url example: https://gis.portal.com/webadaptor
    username = input("Input portal username: ") ## username portal that can access username
    password = input("Input password: ") ## password of the username
    saving_file = input("Input full path address <press enter if you want to pass it to default in the current folder>: ")

    if saving_file is None or saving_file == '':
        export_path = os.getcwd() 
    else:
        export_path = saving_file
                
    information = reporting_server(portal, username, password, export_path) 

    try:
        print('Starting to process')
        reporting_server.main(information)
        print('End of the process')
        endTime = datetime.today()
        deltaTime = endTime - startTime
        print('Completed Time is {}'.format(deltaTime))

    except Exception as e:
        endTime = datetime.today()
        deltaTime = endTime - startTime
        print('Completed Time is {}'.format(deltaTime))
        raise(e)