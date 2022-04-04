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
    df_properties = pd.DataFrame(columns=[])
    df_portalproperties = pd.DataFrame(columns=[])
    df_extension = pd.DataFrame(columns=[])
    list_dict = []
    list_dict_property = []
    list_dict_portalproperty = []
    list_dict_extension = []
    sheet_basename = 'base'
    for index, folder in enumerate(service_folder):
        print('=========== {} ==========='.format(folder))
        get_list_service = gis_server.services.list(folder= folder)
        length_service = len(get_list_service)
        print(folder, length_service)
        if length_service == 0:
            pass
        else:
            for subindex, service_in_folder in enumerate(get_list_service):
                property_service = '{}'.format(service_in_folder.properties)
                load_data = json.loads(property_service)
                dict_frame = {}
                sub_dictframe_properties = {}
                sub_dictframe_portalproperties = {}
                sub_dictframe_extensions = {}
                if index == 0 and subindex == 0:
                    print('creating the dataframe columns')
                    for key in load_data.keys():
                        if key == 'properties' or key == 'portalProperties':
                            sheet_name = key
                            get_subvalue = load_data['{}'.format(key)]

                            if sheet_name == 'properties':
                                df_properties['serviceName'] = load_data['serviceName']
                                for subkey in get_subvalue.keys():
                                    df_properties['{}'.format(subkey)] = get_subvalue['{}'.format(subkey)]

                            elif sheet_name == 'portalProperties':
                                df_portalproperties['serviceName'] = load_data['serviceName']
                                for subkey in get_subvalue.keys():
                                    df_portalproperties['{}'.format(subkey)] = get_subvalue['{}'.format(subkey)]

                        elif key == 'extensions':
                            sheet_name = key
                            get_subvalue = load_data['{}'.format(key)]
                            for subkey in get_subvalue[0].keys():
                                df_extension['{}'.format(subkey)] = get_subvalue[0]['{}'.format(subkey)]

                        else:
                            get_value = load_data['{}'.format(key)]
                            df['{}'.format(key)] = [get_value]
                else:
                    print('appending data to dataframe')
                    for key in load_data.keys():
                        if key == 'properties' or key == 'portalProperties':
                            sheet_name = key
                            get_subvalue = load_data['{}'.format(key)]
                            if sheet_name == 'properties':
                                sub_dictframe_properties['serviceName'] = load_data['serviceName']
                                for subkey in get_subvalue.keys():
                                    sub_dictframe_properties['{}'.format(subkey)] = get_subvalue['{}'.format(subkey)]
                                list_dict_property.append(sub_dictframe_properties)

                            elif sheet_name == 'portalProperties':
                                sub_dictframe_portalproperties['serviceName'] = load_data['serviceName']
                                for subkey in get_subvalue.keys():
                                    sub_dictframe_portalproperties['{}'.format(subkey)] = get_subvalue['{}'.format(subkey)]
                                list_dict_portalproperty.append(sub_dictframe_portalproperties)

                        elif key == 'extensions':
                            sheet_name = key
                            get_subvalue = load_data['{}'.format(key)]
                            if len(get_subvalue) == 0:
                                pass
                            else:
                                for subkey in get_subvalue[0].keys():
                                    sub_dictframe_extensions['{}'.format(subkey)] = get_subvalue[0]['{}'.format(subkey)]
                                list_dict_extension.append(sub_dictframe_extensions)

                        else:
                            get_value = load_data['{}'.format(key)]
                            dict_frame['{}'.format(key)] = get_value

                    list_dict.append(dict_frame)
                print('Complete in {} of {}'.format(subindex, length_service-1))
        print('=========== {} ==========='.format(folder))

        df_2 = pd.DataFrame(list_dict)
        df_properties_2 = pd.DataFrame(list_dict_property)
        df_portalproperties_2 = pd.DataFrame(list_dict_portalproperty)
        df_extension_2 = pd.DataFrame(list_dict_extension)

        print('Compiling dataframe')
        compiling_base = df.append(df_2, ignore_index=True)
        compiling_properties = df_properties.append(df_properties_2)
        compiling_portalproperties = df_portalproperties.append(df_portalproperties_2)
        compiling_extension = df_extension.append(df_extension_2)

    print('Generate Report')
    with pd.ExcelWriter(os.path.join(os.getcwd(), 'reporting_server'+'.xlsx')) as writer:
        compiling_base.to_excel(writer, sheet_name=sheet_basename)
        compiling_properties.to_excel(writer, sheet_name='properties')
        compiling_portalproperties.to_excel(writer, sheet_name='portalproperties')
        compiling_extension.to_excel(writer, sheet_name='extension')

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