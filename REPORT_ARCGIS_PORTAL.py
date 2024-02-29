from arcgis.gis import GIS, UserManager, Item
from datetime import datetime
from arcgis.mapping import WebMap
import os
import pandas as pd

class reporting_portal():
    def __init__(self, portal, username, password, reportingPath) -> None:
        self.portal = portal
        self.username = username
        self.password = password
        self.reportingPath = reportingPath

    def main(self):
        gis = GIS(self.portal, self.username, self.password)
        reportingPath = self.reportingPath # change this path if you want to save other address

        reportingFile = 'reporting_portal'
        itemTypeGIS = ['Feature Layer', 'Geoprocessing Toolbox', 'Map Image Layer', 'Data Store', 'Web Map',
                'Web Experience', 'Dashboard']

        listService = list()
        listUsers = gis.users.search(query=None)
        for user in listUsers:
            getUser = user['username']
            print('============= {} ============='.format(getUser))

            for item in itemTypeGIS:
                getItemType = item
                contentGIS = gis.content.search(query="owner:" + getUser, item_type=getItemType, max_items=1000)

                if len(contentGIS) == 0:
                    pass
                else:
                    if getItemType == 'Web Map':
                        for content in contentGIS:
                            getData = content.title
                            getItem = content.id

                            print(getItemType, getData, getItem)
                            listLayerURL = []
                            try:
                                getLayers = WebMap(content).layers
                                for layer in getLayers:
                                    layerURL = layer['url']
                                    listLayerURL.append(layerURL)
                            except:
                                listLayerURL = ['FAILED TO GET URL LIST, PLEASE CHECK MANUAL']

                            itemStatus = Item(gis, content.id)
                            shareStatus = itemStatus.shared_with
                            shareStatus_Public = shareStatus['everyone']
                            shareStatus_Org = shareStatus['org']
                            shareStatus_Group = shareStatus['groups']

                            rowDict = {'title': getData, 'type': getItemType, 'owner': getUser,
                                    'url': content.homepage, 'itemid': content.id,
                                    'shared_public': shareStatus_Public,
                                    'shared_org': shareStatus_Org,
                                    'shared_groups': ', '.join(shareStatus_Group),
                                    'layers': ',\n'.join(listLayerURL)}
                            
                            df = pd.DataFrame.from_dict([rowDict])
                            listService.append(df)
                        
                    else:
                        for content in contentGIS:
                            getData = content['title']
                            getItem = content.id

                            print(getData, getItem)
                            itemStatus = Item(gis, content.id)
                            shareStatus = itemStatus.shared_with
                            shareStatus_Public = shareStatus['everyone']
                            shareStatus_Org = shareStatus['org']
                            shareStatus_Group = shareStatus['groups']

                            rowDict = {'title': getData, 'type': getItemType, 'owner': getUser,
                                    'url': content.url, 'itemid': content.id,
                                    'shared_public': shareStatus_Public,
                                    'shared_org': shareStatus_Org,
                                    'shared_groups': ', '.join(shareStatus_Group),
                                    'layers': None}

                            df = pd.DataFrame.from_dict([rowDict])
                            listService.append(df)

            print('============= {} ============='.format(getUser))

        compile_df = pd.concat(listService).reset_index().drop(columns=['index'])
        with pd.ExcelWriter(os.path.join(reportingPath, reportingFile+'.xlsx')) as writer:
            compile_df.to_excel(writer, sheet_name='list_portal')


if __name__ == '__main__':
    startTime = datetime.today()

    portal = input("Input portal url <example: https://gis.portal.com/webadaptor>: ") ## input portal url example: https://gis.portal.com/webadaptor
    username = input("Input portal username: ") ## username portal that can has same previleges as administrator
    password = input("Input password: ") ## password of the username
    saving_file = input("Input full path address <press enter if you want to pass it to default in the current folder>: ")

    if saving_file is None or saving_file == '':
        export_path = os.getcwd() 
    else:
        export_path = saving_file
        
    information = reporting_portal(portal, username, password, export_path) 

    try:
        print('Starting to process')
        reporting_portal.main(information)

        print('End of the process')
        endTime = datetime.today()
        deltaTime = endTime - startTime
        print('Completed Time is {}'.format(deltaTime))

    except Exception as e:
        endTime = datetime.today()
        deltaTime = endTime - startTime
        print('Completed Time is {}'.format(deltaTime))
        raise(e)
