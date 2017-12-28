#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
This is an demo file to collect cve infomation
'''
__author__ = "John Wen"

import requests
from bs4 import BeautifulSoup
import logging
import re
import time
logging.basicConfig(level=logging.INFO)

url = 'https://cassandra.cerias.purdue.edu/CVE_changes/CVE.2017.12.25.html'
#url = 'https://cassandra.cerias.purdue.edu/CVE_changes/today.html'
header = {
    "User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Mobile Safari/537.36",
}

css="""
 * {
    margin: 0;
    padding: 0;
}

body {
    width: 80%;
    margin: 0 auto;
}

.summary {
    font-family: 'sans-serif';
    margin: 20px 0 20px 0;
    padding: 20px;
}

.content {
    border: 1px solid black;
    border-radius: 9px;
    margin: 20px;
    padding: 20px;
}

.id {
    font-family: 'sans-serif';
    font-size: 16px;
    font-weight: bold;
}

.des {
    font-family: 'sans-serif';
    font-size: 14px;
    padding: 15px;
    padding-left: 0;
}

.date {
    font-family: 'sans-serif';
    font-size: 14px;
    padding-bottom: 10px;
}

ul {
    list-style: none;
}
"""

js="""

"""

def get_todays_cve():
    try:
        response = requests.get(url)
        html = get_middle_content(response.text,'New entries:','Graduations')
        if html == None:
            return None
        else:
            html = BeautifulSoup(html,"html.parser")
            # logging.info(html)
            links = html.find_all('a')
            return links
    except Exception as e:
        logging.info(e)
        return None

def get_middle_content(content,startStr,endStr):
    start = content.index(startStr)
    if start > 0:
        start+=len(startStr)
        end = content.index(endStr)
        return content[start:end]
    return None


def get_detail_cve(url):
    cve_reference=[]
    try:
        res = requests.get(url,headers=header,timeout=60)
        if res.status_code!=200:
            logging.info(res.status_code)
            return
        html = BeautifulSoup(res.text,'html.parser')
        table = html.find(id='GeneratedTable').find('table')
        cve_id = html.find(nowrap='nowrap').find('h2').string
        cve_description = table.find_all('tr')[3].find('td').string
        for a in table.find_all('tr')[6].find_all('a'):
            cve_reference.append(a['href'])
        cve_create_date = table.find_all('tr')[10].find('b').string
        return cve_id,cve_description,cve_reference,cve_create_date
    except Exception as e:
        logging.info(e)

def message(cve_id,cve_des,cve_date,cve_ref,cve_url):
    refer_links = ''
    for a in cve_ref:
        refer_links += "<li><a href='"+a+"'>"+a+"</a></li>"
    return "<div class='content'>"+\
    "<div class='id'>CVE ID: <a href='"+cve_url+"'>"+cve_id+"</a></div>"+\
    "<div class='des'><b>CVE Description:</b>"+cve_des+"</div>"+\
    "<div class='date'><b>CVE Create Date:</b>"+cve_date+"</div>"+\
    "<div class='refer'><ul><li class='title'><b>Reference Links:</b></li>"+refer_links+"</ul></div>"+\
    "</div>"

def generate_report():
    links = get_todays_cve()
    html = "<html><head><title>CVE infomation</title><style>"+css+"</style></head><body><div class='summary'><h1>The CVE infomation total is: "+str(len(links))+"</h1></div>"

    if links == None or links ==[]:
        html+="<div class='notice'><h1>There are no CVE infomation today. Please try again later</h1></div></body></html>"
    for a in links:
        time.sleep(0.1)
        cve_id,cve_des,cve_ref,cve_date = get_detail_cve(a['href'])
        #if filter_items(cve_des):
            #html+=message(cve_id,cve_des,cve_date,cve_ref,a['href'])
        #else:
            #pass
        html+=message(cve_id,cve_des,cve_date,cve_ref,a['href'])
    html+="<script>"+js+"</script></body></html>"
    return html

def send_email():
    pass

def search_cve():
    pass

def add_to_db():
    pass

def filter_items(text):
    for keyword in keywords:
        if re.match(keyword,text.lower()):
            return True
        else:
            return False

if __name__ == "__main__":
    #links = get_todays_cve()
    #logging.info(links)
    #cve_id = get_detail_cve('http://cve.mitre.org/cgi-bin/cvename.cgi?name=2017-12736')
    #print(cve_id)
    #url = 'https://cassandra.cerias.purdue.edu/CVE_changes/CVE.2017.12.25.html'
    html = generate_report()
    with open('test.html','w')as f:
        f.write(html)
