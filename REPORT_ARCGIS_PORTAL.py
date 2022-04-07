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

        reportingFile = 'reporting'
        itemTypeGIS = ['Feature Layer', 'Geoprocessing Toolbox', 'Map Image Layer', 'Data Store', 'Web Map',
                'Web Experience', 'Dashboard']

        listRAW = []
        listService = []
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
                    if getItemType == 'Web Map' or getItemType == 'Dashboard':
                        for i in range(len(contentGIS)):
                            getData = contentGIS[i]['title']
                            getItem = contentGIS[i].id

                            print(getItemType, getData, getItem)
                            listLayerURL = []
                            try:
                                getLayers = WebMap(contentGIS[i]).layers
                                for layer in getLayers:
                                    layerURL = layer['url']
                                    listLayerURL.append(layerURL)
                            except:
                                listLayerURL = 'FAILED TO GET URL LIST'

                            itemStatus = Item(gis, contentGIS[i].id)
                            shareStatus = itemStatus.shared_with
                            shareStatus_Public = shareStatus['everyone']
                            shareStatus_Org = shareStatus['org']
                            shareStatus_Group = shareStatus['groups']

                            rowDict = {'title': getData, 'type': getItemType, 'owner': getUser,
                                    'url': contentGIS[i].homepage, 'itemid': contentGIS[i].id,
                                    'shared_public': shareStatus_Public,
                                    'shared_org': shareStatus_Org,
                                    'shared_groups': str(shareStatus_Group),
                                    'layers': '{}'.format(str(listLayerURL))}
                            listService.append(rowDict)
                            listRAW.append(contentGIS[i])

                    else:
                        for i in range(len(contentGIS)):
                            getData = contentGIS[i]['title']
                            getItem = contentGIS[i].id

                            print(getData, getItem)
                            itemStatus = Item(gis, contentGIS[i].id)
                            shareStatus = itemStatus.shared_with
                            shareStatus_Public = shareStatus['everyone']
                            shareStatus_Org = shareStatus['org']
                            shareStatus_Group = shareStatus['groups']

                            rowDict = {'title': getData, 'type': getItemType, 'owner': getUser,
                                    'url': contentGIS[i].url, 'itemid': contentGIS[i].id,
                                    'shared_public': shareStatus_Public,
                                    'shared_org': shareStatus_Org,
                                    'shared_groups': str(shareStatus_Group),
                                    'layers': None}
                            listService.append(rowDict)

                            listRAW.append(contentGIS[i])

            print('============= {} ============='.format(getUser))

        df = pd.DataFrame(columns = ['title', 'type', 'owner', 'url', 'itemid', 'shared_public',
                                    'shared_org', 'shared_groups','layers'])
        dfAppend = df.append(listService, ignore_index=True)
        dfAppend.to_csv(os.path.join(reportingPath, reportingFile+ '.csv'))


if __name__ == '__main__':
    startTime = datetime.today()

    portal = input("Input portal url <example: https://gis.portal.com/webadaptor>: ") ## input portal url example: https://gis.portal.com/webadaptor
    username = input("Input portal username: ") ## username portal that can access username
    password = input("Input password: ") ## password of the username
    saving_file = input("Input full path address <press enter if you wan to pass it to default in the current folder>: ")

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
