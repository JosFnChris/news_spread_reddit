#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
#
# download the data from reddit using the api into json
# this has to be a domain name, like cnn.com

# v1 - now both things are functions so you can take them off and then hopefully
#      this will lead to a loop that will then do all things needed.

import requests
import json
import re
import time
import os
import datetime
import codecs

# if this doesn't work then delete this and use the other
# str_domain = os.sys.argv[1]

list_all_domains = ['dailymail.co.uk',
	            'thesun.co.uk',
	            'news.bbc.co.uk',
	            'theguardian.com',
	            'telegraph.co.uk',
                    'breitbart.com',
                    'nationalenquirer.com',
                    'cnn.com',
                    'washingtonpost.com',
                    'abcnews.go.com',
                    'rt.com']

# figure our if the folder is there, if not then make it
if os.path.isdir('temp_data')==False:
    os.mkdir('temp_data')
else:
    pass

# this will merge all the json files into one
def _merge_and_delete(str_domain,list_files):

    if os.path.isdir('data/%s' % str_date)==False:
        os.mkdir('data/%s' % str_date)
    else:
        pass


    domain_name = re.sub('\.','_', str_domain)

    json_output = []

    for str_each_file in list_files:
        with open('temp_data/%s' % (str_each_file)) as fr:
            data_json = json.loads(fr.read())

        for each_entry in data_json['data']['children']:
            json_output.append(each_entry)

    with open('data/%s/%s_data_%s.json' %  (str_date,domain_name, str_date), 'w') as fw:
        fw.write(json.dumps(json_output, indent=2))

    for every_file in list_files:
        os.remove('temp_data/%s' % (every_file))

    print('JSON files merged and cleaned')

    return None

def _download_data(str_domain):

    # regular expression to make the domain name more friendly
    domain_name = re.sub('\.','_', str_domain)

    print('start %s' % domain_name)

    # the url
    str_p_url = 'https://www.reddit.com/domain/%s/.json?limit=100&sort=top&t=day' % str_domain

    # a clean url so that it doesn't
    str_p_new = str_p_url

    is_more = True

    # get the date
    str_date = datetime.datetime.today().strftime('%Y%m%d')

    list_json_files = []

    page_count= 1
    while is_more==True:

        # make the request
        r = requests.get(str_p_url, headers={'User-agent':'Mozilla/5.0'})

        # get and format json data
        json_data = r.json()

        str_file_name = '%s_%s_page_%i.json' % (domain_name, str_date, page_count)

        with open('temp_data/%s' % (str_file_name), 'w') as fw:
            fw.write(json.dumps(json_data, indent=2))

        # add name to list so it can be deleted later
        list_json_files.append(str_file_name)

        if json_data['data']['after']!=None:
            str_p_url = '%s&after=%s' % (str_p_new, json_data['data']['after'])
            print('page %i done' % page_count)
            page_count+=1
            time.sleep(6)

        else:
            print('page %i done' % page_count)
            print('ALL DONE')
            is_more = False

    return list_json_files

for str_domain in list_all_domains:

    str_date = datetime.datetime.today().strftime('%Y%m%d')

    # download and create a list of json files to delete
    list_json_files = _download_data(str_domain)

    # merge and delete files
    _merge_and_delete(str_domain,list_json_files)
