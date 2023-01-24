import os
import json
import pandas as pd

pd.set_option('max_columns',100)
pd.set_option('max_rows',1000)

provider_info_dir = './provider_info/data/'

traffic_run_date = '2021-02-01'
traffic_dir = f'./traffic/raw/run_date={traffic_run_date}'

info_list = os.listdir(provider_info_dir)
processed_list = os.listdir(traffic_dir)

traffic_list = []
for provider_info_file in info_list:

    print(provider_info_file)

    with open(os.path.join(provider_info_dir,provider_info_file)) as pif:
        p_info = json.load(pif)

    p_data = pd.DataFrame.from_dict(p_info, orient='index').transpose()

    if provider_info_file in processed_list:
        with open(os.path.join(traffic_dir, provider_info_file)) as tif:
            t_info = json.load(tif)

        t_data_list = []
        for r in t_info['responses']:
            hd = r['Awis']['Results']['Result']['Alexa']['TrafficHistory']['HistoricalData']
            if hd is not None:
                hd = hd['Data']
                if not isinstance(hd,list):
                    hd = [hd]
                for h in hd:
                    h['PageViews_PerMillion'] = h['PageViews']['PerMillion']
                    h['PageViews_PerUser'] = h['PageViews']['PerUser']
                    h['Reach_PerMillion'] = h['Reach']['PerMillion']
                    del h['PageViews']
                    del h['Reach']

                t_data_list.append(pd.DataFrame(hd))

        if len(t_data_list) > 0:
            t_data = pd.concat(t_data_list)
            t_data.insert(1,'id', t_info['comp_id'])
            t_data.insert(2, 'run_date', t_info['run_date'])
            p_data = p_data.merge(t_data,how='left',on='id')

    traffic_list.append(p_data)

traffic = pd.concat(traffic_list)
traffic.main_data_source.unique()
traffic['Rank'] = traffic['Rank'].astype(float)
traffic['PageViews_PerMillion'] = traffic['PageViews_PerMillion'].astype(float)
traffic['PageViews_PerUser'] = traffic['PageViews_PerUser'].astype(float)
traffic['Reach_PerMillion'] = traffic['Reach_PerMillion'].astype(float)


traffic.to_csv(f'./traffic/clean/rundate={traffic_run_date}.csv',index=False)