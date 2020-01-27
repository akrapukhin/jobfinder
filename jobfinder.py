import requests
import codecs
print("test")
x=[]
url = 'https://api.hh.ru/vacancies'

#testtxt = requests.get('https://raw.githubusercontent.com/akrapukhin/jobfinder/master/companies.txt')
#test_test = testtxt.content
#for s in test_test:
#	print(s)

data = []
import urllib.request  # the lib that handles the url stuff
for line in urllib.request.urlopen('https://raw.githubusercontent.com/akrapukhin/jobfinder/master/companies.txt'):
	data.append(line.decode('utf-8'))
    #print(line.decode('utf-8')) #utf-8 or iso8859-1 or whatever the page encoding scheme is

print(data)
file_companies = open("companies.txt", "r")
companies = file_companies.readlines()
#companies = data
companies_set = set(companies)
companies_list = list(companies_set)
companies_nums = []
for s in companies_list:
    companies_nums.append(s[23:-1])

print(companies_nums)
#par = {'text': 'fpga OR плис OR asic OR vhdl OR verilog OR matlab OR embedded OR встраиваемые OR микроконтроллер OR цос OR dsp OR vision OR "компьютерное зрение" OR "computer vision" OR c/c++ OR junior OR СБИС OR vlsi OR quartus OR modelsim OR "deep learning" OR "tensorflow" OR "pytorch" OR synopsys',
#       'area': [1, 2],
#       'per_page': '100',
#       'employer_id' : companies_nums,
#       'order_by' : 'publication_time',
#      'page': 0}
       
par = {'text': 'vhopsdflghj',
       'area': [1, 2],
       'per_page': '100',
       'employer_id' : companies_nums,
       'order_by' : 'publication_time',
       'page': 0}
r = requests.get(url, params=par)
e=r.json()
x.append(e)
#print(e)
print(e['found'])
num_of_pages = e['pages']
print("num_of_pages: " + str(num_of_pages))

for pagenum in range(num_of_pages-1):
    par['page'] = pagenum+1
    r = requests.get(url, params=par)
    e = r.json()
    x.append(e)

#print(e['alternate_url'])
html = """<!DOCTYPE html><html><head><style>table, th, td {border: 1px solid black;}</style><meta http-equiv="Content-Type" content="text/html; charset=utf-8" /></head><body><h1>"""
html+= str(e['found']) + " вакансий найдено:" + "</h1>"

html+= "<table style=\"width:100%\"><tr><th>#</th><th>Должность</th><th>Компания</th><th>Лого</th><th>Город</th><th>Зарплата</th><th>Дата</th><th>Ссылка</th></tr>"

counter = 1
for j in x:
    y = j['items']
    for i in y:
        salary = i['salary']
        salary_str = ""
        if salary == None:
            salary_str = "не указана"
        else:
            if salary['from'] != None:
                salary_str = "от " + str(salary['from']) + " "
            if salary['to'] != None:
                salary_str += "до " + str(salary['to'])
            if salary['gross']:
                salary_str += " до вычета НДФЛ"
            else:
                salary_str += " на руки"
        #'salary': {'from': 40000, 'to': 80000, 'currency': 'RUR', 'gross': False}
        logo_str = ""
        if i['employer']['logo_urls'] != None:
            if i['employer']['logo_urls']['90'] != None:
                logo_str = i['employer']['logo_urls']['90']

        html_line = "<tr><td>"
        html_line += str(counter) + "</td><td>" + i['name'] + "</td><td>" + i['employer']['name'] + "</td> <td align=\"center\">" + "<img src=\"" + logo_str + "\"" + "></td> <td>" + i['area']['name'] + "</td> <td>" + salary_str +"</td> <td style=\"white-space:nowrap;\">"+ i['published_at'][8:10] + i['published_at'][7] + i['published_at'][5:7] + i['published_at'][4] + i['published_at'][0:4] +  "</td> "
        html_line += "<td><a href = \"" + i['alternate_url'] + "\" target=\"_blank\">" + i['alternate_url'] + "</a></td>"
        #html_line += i['published_at'][:10] + " " + i['alternate_url']
        html_line += "</tr>"
        print(i['name'] + " " + i['employer']['name'] + " " + i['published_at'][:10] + " " + i['alternate_url'])
        html += html_line
        counter += 1

html += "</body></html>"
#параметры, которые будут добавлены к запросу
# file_area = open("area.txt","r")
# area = file_area.readline()
# if lower(area) == 'россия':
#     countries_result = requests.get('https://api.hh.ru/areas/countries')
#     countries = countries_result.json()
#     for country in countries:
#         if lower(country['name']) == 'россия':
#             area_id = country['id']

# regions = requests.get('https://api.hh.ru/areas/countries')
# reg=regions.json()
# print(reg)

#file_results = open("results.html", "w+", encoding="utf-8")
file_results = codecs.open('results_test_table.html', 'w', 'utf-8')
file_results.write(html)
file_results.close()

import webbrowser
url = 'results_test_table.html'
webbrowser.open(url, new=2)  # open in new tab
