#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
#
# merges all the json files into one

import json

domain_list = ['abcnews_go_com',
                'breitbart_com',
                'cnn_com',
                'dailymail_co_uk',
                'nationalenquirer_com',
                'news_bbc_co_uk',
                'rt_com',
                'telegraph_co_uk',
                'theguardian_com',
                'thesun_co_uk',
                'washingtonpost_com']

list_folders = ['20170215',
                '20170216',
                '20170217',
                '20170219']

for each_domain in domain_list:

    domain_output = []

    for each_folder in list_folders:

        str_path = 'data/%s/%s_data_%s.json' % (each_folder, each_domain, each_folder)

        with open(str_path) as fr:
            json_data = json.loads(fr.read())

        for each_entry in json_data:
            domain_output.append(each_entry)

    with open('merged/%s_20170215-17.json' % each_domain, 'w') as fw:
        fw.write(json.dumps(domain_output, indent=2))

    print('%s DONE' % each_domain)
