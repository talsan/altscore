
import subprocess
import os
import json
import re
import pandas as pd

provider_info_dir = './provider_info/data/'
run_date = '2021-02-01'
end_month_date = '2021-01-01'
start_month_date = '2017-01-01'

monthly_start_dates = pd.date_range(start_month_date, end_month_date, freq='MS')

out_dir = f'./traffic/raw/run_date={run_date}'
if not os.path.exists(out_dir):
    os.mkdir(out_dir)

full_list = os.listdir(provider_info_dir)
processed_list = os.listdir(out_dir)
new_list = set(full_list) - set(processed_list)

for provider_info_file in new_list:
    with open(os.path.join(provider_info_dir,provider_info_file)) as pif:
        p_info = json.load(pif)

    comp_id = provider_info_file.replace('.json','')
    url = p_info.get('website_link')

    if url is not None:
        out_dict = {'comp_id': comp_id,
                    'run_date': run_date,
                    'url':url,
                    'start_date':start_month_date,
                    'end_date': end_month_date,
                    'responses': []}
        for start_date in monthly_start_dates:
            print(f'{comp_id}: {start_date}')
            out_f = open(os.path.join(out_dir, provider_info_file), "w")

            args = ['python',
                    'awis.py',
                    '-u tsansani@gmail.com',
                    '--key=dRRwfhB6SN1FsYZpgKXW44G8L46Um5vG50Qw8PJL',
                    '--action=TrafficHistory',
                    f'--options="&ResponseGroup=History&Output=json&Start={start_date.strftime("%Y%m%d")}&Url={url}"']

            proc = subprocess.run(args, shell=True, stdout=subprocess.PIPE)
            out_str = proc.stdout.decode('utf-8')
            out_dict['responses'].append(json.loads(re.search('{(.|\n)*}', out_str).group()))

        with open(os.path.join(out_dir, provider_info_file),'w') as pof:
            json.dump(out_dict, pof, indent=2)

    else:
        print('------- MISSSING URL -------')
        print(p_info)