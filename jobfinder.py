import requests
import codecs
x=[]
url = 'https://api.hh.ru/vacancies'

file_areas = codecs.open('include_areas.txt', 'r', 'utf-8')
areas = file_areas.readlines()
areas_list = []
for area in areas:
	if len(area) > 1:
		areas_list.append(area)
print(areas_list)
areas_ids = []
russia_areas = []
all_areas = requests.get('https://api.hh.ru/areas')
all_areas = all_areas.json()
for area in all_areas:
	if area['name'].lower() == 'россия':
		russia_id = area['id']
		russia_areas = area['areas']
			
			
file_excl_areas = codecs.open('exclude_areas.txt', 'r', 'utf-8')
excluded_areas = file_excl_areas.readlines()
print(excluded_areas)
excluded_areas_noendls = []
for area in excluded_areas:
	if area[-1] == '\n':
		area = area[:-1]
	excluded_areas_noendls.append(area.lower())
print("excluded_areas_noendls:")
print(excluded_areas_noendls)		
		
#print(russia_areas)
if (len(areas_list) == 0):
	areas_ids.append(russia_id)
else:
	for area in areas_list:
		if area[-1] == '\n':
			area = area[:-1]
		area_found = False
		print('area: ' + area)
		for region in russia_areas:
			print(region['name'].lower())
			print(area.lower())
			print(region['name'].lower() == area.lower())
			if region['name'].lower() == area.lower():
				areas_ids.append(region['id'])
				area_found = True
			for city in region['areas']:
				if city['name'].lower() == area.lower():
					areas_ids.append(region['id'])
					area_found = True
		if not area_found:
			print('территория не найдена: ' + area)
			
print('areas_ids: ' + str(areas_ids))
#testtxt = requests.get('https://raw.githubusercontent.com/akrapukhin/jobfinder/master/companies.txt')
#test_test = testtxt.content
#for s in test_test:
#	print(s)

data = []
import urllib.request  # the lib that handles the url stuff
for line in urllib.request.urlopen('https://raw.githubusercontent.com/akrapukhin/jobfinder/master/companies.txt'):
	data.append(line.decode('utf-8'))
    #print(line.decode('utf-8')) #utf-8 or iso8859-1 or whatever the page encoding scheme is

#print(data)
file_companies = open("companies.txt", "r")
companies = file_companies.readlines()
#companies = data
companies_set = set(companies)
companies_list = list(companies_set)
companies_nums = []
for s in companies_list:
    companies_nums.append(s[23:-1])

#print(companies_nums)
#par = {'text': 'fpga OR плис OR asic OR vhdl OR verilog OR matlab OR embedded OR встраиваемые OR микроконтроллер OR цос OR dsp OR vision OR "компьютерное зрение" OR "computer vision" OR c/c++ OR junior OR СБИС OR vlsi OR quartus OR modelsim OR "deep learning" OR "tensorflow" OR "pytorch" OR synopsys',
#       'area': [1, 2],
#       'per_page': '100',
#       'employer_id' : companies_nums,
#       'order_by' : 'publication_time',
#      'page': 0}
       
par = {'text': 'с++',
       'area': areas_ids,
       'per_page': '100',
       'employer_id' : companies_nums,
       'order_by' : 'publication_time',
       'page': 0}
r = requests.get(url, params=par)
e=r.json()
x.append(e)
#print(e)
num_of_vacancies = e['found']
num_of_pages = e['pages']
print("num_of_pages: " + str(num_of_pages))

for pagenum in range(num_of_pages-1):
    par['page'] = pagenum+1
    r = requests.get(url, params=par)
    e = r.json()
    x.append(e)

#print(e['alternate_url'])
html = ""

counter = 1
for j in x:
	y = j['items']
	for i in y:
		excluded = False
		for excluded_area in excluded_areas_noendls:
			if excluded_area.lower() == i['area']['name'].lower():
				excluded = True;
		if (not excluded):	
			print (i['area']['name'].lower() + " not in " + str(excluded_areas_noendls))
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
		else:
			num_of_vacancies -= 1

print('num of vacancies: ' + str(num_of_vacancies))
html += "</body></html>"

html_start = """<!DOCTYPE html><html><head><style>table, th, td {border: 1px solid black;}</style><meta http-equiv="Content-Type" content="text/html; charset=utf-8" /></head><body><h1>"""
html_start+= str(num_of_vacancies) + " вакансий найдено:" + "</h1>"

html_start+= "<table style=\"width:100%\"><tr><th>#</th><th>Должность</th><th>Компания</th><th>Лого</th><th>Город</th><th>Зарплата</th><th>Дата</th><th>Ссылка</th></tr>"
html = html_start + html
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

test_list = ['москва', 'сочи', 'санкт-петербург']
print(test_list)
test_boo = 'санкт-петербург' not in test_list
print(test_boo)
