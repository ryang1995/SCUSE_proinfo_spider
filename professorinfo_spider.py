import requests
from bs4 import BeautifulSoup
import csv

def get_one_page(url):
    response = requests.get(url)
    try:
        if response.status_code == 200:
            return response.content
        print(response.status_code)
        return None
    except Exception as e:
        print(e)
        return None

def parse_detail(html):
    soup = BeautifulSoup(html, 'html.parser')
    info_list = soup.find(id='BodyLabel').table.table.find_all('td')[1:]
    zc = info_list[1].text
    xi = info_list[3].text
    p_num = info_list[4].text
    email = info_list[5].text
    return zc, xi, p_num, email
    # print(zc,xi, p_num, email)

def parse_one_page(html):
    list = []
    soup = BeautifulSoup(html, 'html.parser')
    pro_list = soup.find(id='BodyLabel').find_all('a')
    for pro in pro_list:
        url = pro['href']
        name = pro.text
        zc,xi,p_num,email = parse_detail(get_one_page(url))
        list.append([name, zc, xi, p_num, email])
    return list

def writeCSV(file_name, data_list):
    with open(file_name, 'w') as f:
        writer = csv.writer(f)
        for data in data_list:
            writer.writerow(data)

def main():
    url = 'http://www.scu.edu.cn/sw/szdw/zzjs/H970301index_1.htm'
    html = get_one_page(url)
    pro_list = parse_one_page(html)
    writeCSV('test.csv', pro_list)

if __name__ == '__main__':
    main()
