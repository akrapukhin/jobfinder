import requests
import codecs
import urllib.request
import webbrowser
version = "29012020a"
new_version = False
for line in urllib.request.urlopen('https://raw.githubusercontent.com/akrapukhin/jobfinder/master/jobfinder.py'):
	line = line.decode('utf-8').rstrip()
	if line[0:7] == "version":
		if line[11:-1] != version:
			new_version = True

# read query from file
file_query = codecs.open('query.txt', 'r', 'utf-8')
query = file_query.readlines()
query_string = ""
for w in query:
	query_string += w.strip() + " "
query_string = query_string.strip()

# read included areas
file_areas = codecs.open('include_areas.txt', 'r', 'utf-8')
areas = file_areas.readlines()
areas_list = []
for area in areas:
	area = area.strip().lower()
	if area != '':
		areas_list.append(area)

russia_areas = []
all_areas = requests.get('https://api.hh.ru/areas')
all_areas = all_areas.json()
for area in all_areas:
	if area['name'].lower() == 'россия':
		russia_id = area['id']
		russia_areas = area['areas']
			
# read excluded areas
file_excl_areas = codecs.open('exclude_areas.txt', 'r', 'utf-8')
excluded_areas = file_excl_areas.readlines()
excluded_areas_noendls = []
for area in excluded_areas:
	area = area.strip().lower()
	if area != '':
		excluded_areas_noendls.append(area)	

# load list of companies
companies = []

for line in urllib.request.urlopen('https://raw.githubusercontent.com/akrapukhin/jobfinder/master/companies.txt'):
	companies.append(line.decode('utf-8').strip())
companies = set(companies)
companies = list(companies)
companies_nums = []
for s in companies:
    companies_nums.append(s[23:])
	
# find corresponding areas IDs
areas_ids = []
if (len(areas_list) == 0):
	areas_ids.append(russia_id)
	areas_list.append("Россия")
else:
	for area in areas_list:
		area_found = False
		for region in russia_areas:
			if region['name'].lower() == area.lower():
				areas_ids.append(region['id'])
				area_found = True
			for city in region['areas']:
				if city['name'].lower() == area.lower():
					areas_ids.append(region['id'])
					area_found = True
		if not area_found:
			print('территория не найдена: ' + area)
			areas_list.remove(area)

print("areas_ids: ")
print(areas_ids)
if len(areas_ids) == 0:
	areas_ids.append(russia_id)
	areas_list.append("Россия")
print("areas_ids: ")
print(areas_ids)
# parameters of query to hh
date_from = None
par = {'text': query_string,
	   'area': areas_ids,
       'per_page': '100',
       'employer_id' : companies_nums,
       'order_by' : 'publication_time',
	   'date_from' : date_from,
       'page': 0}
       
# request to hh to get all vacancies
all_pages = []
first_page_vacancies = requests.get('https://api.hh.ru/vacancies', params=par)
print(first_page_vacancies)
first_page_vacancies = first_page_vacancies.json()
all_pages.append(first_page_vacancies)

num_of_vacancies = first_page_vacancies['found']
num_of_pages = first_page_vacancies['pages']
print("num_of_pages: " + str(num_of_pages))
print("num_of_vacancies: " + str(num_of_vacancies))

for pagenum in range(num_of_pages-1):
    par['page'] = pagenum+1
    page_vacancies = requests.get('https://api.hh.ru/vacancies', params=par)
    page_vacancies = page_vacancies.json()
    all_pages.append(page_vacancies)

#print(e['alternate_url'])
html = ""

counter = 1
for page in all_pages:
	vacancies = page['items']
	for vac in vacancies:
		excluded = False
		for excluded_area in excluded_areas_noendls:
			if excluded_area.lower() == vac['area']['name'].lower():
				excluded = True;
		if (not excluded):	
			# get salary
			salary = vac['salary']
			salary_str = ""
			if salary == None:
				salary_str = "не указана"
			else:
				if salary['from'] != None:
					salary_str = "от " + str(salary['from']) + " "
				if salary['to'] != None:
					salary_str += "до " + str(salary['to'])
				if salary['gross']:
					salary_str += " до вычета"
				else:
					salary_str += " на руки"
			# get logo
			logo_str = ""
			if vac['employer']['logo_urls'] != None:
				if vac['employer']['logo_urls']['90'] != None:
					logo_str = vac['employer']['logo_urls']['90']
			
			# generate one line in HTML file with vacancy info
			html_line = "<tr><td>" + str(counter) #number
			html_line += "</td><td>" + vac['name'] #vacancy title
			html_line += "</td><td>" + vac['employer']['name'] #employer name
			html_line += "</td><td align=\"center\">" + "<img src=\"" + logo_str + "\"" + ">" #employer logo
			html_line += "</td><td>" + vac['area']['name'] #vacancy area
			html_line += "</td><td>" + salary_str #salary
			html_line += "</td><td style=\"white-space:nowrap;\">"+ vac['published_at'][8:10]\
			                                                      + vac['published_at'][7]\
			                                                      + vac['published_at'][5:7]\
			                                                      + vac['published_at'][4]\
			                                                      + vac['published_at'][0:4] + " "\
						 										  + vac['published_at'][11:16] #time of publication
			html_line += "</td><td><a href = \"" + vac['alternate_url'] + "\" target=\"_blank\">" + vac['alternate_url'] + "</a></td></tr>" #link to vacancy
			#print(vac['name'] + " " + vac['employer']['name'] + " " + vac['published_at'] + " " + vac['alternate_url'])
			html += html_line
			counter += 1
		else:
			num_of_vacancies -= 1

print('num of vacancies: ' + str(num_of_vacancies))
html += "</body></html>"
html_start = """<!DOCTYPE html><html><head><style>table, th, td {border: 1px solid black;}</style><meta http-equiv="Content-Type" content="text/html; charset=utf-8" /></head><body>"""
if new_version:
	html_start += "<t>" + "Доступна новая версия скрипта. Эта версия может работать неправильно. \
	Перейдите по ссылке " + "<a href = \"" + "https://github.com/akrapukhin/jobfinder/blob/master/jobfinder.py" + "\" target=\"_blank\">" + "https://github.com/akrapukhin/jobfinder/blob/master/jobfinder.py" + "</a>" + \
				  ", наведите курсор на кнопку \"Raw\", нажмите \"сохранить объект как...\" (или что-то подобное в зависимости от браузера)\
				   и положите скачанный файл в папку со скриптом, согласившись на замену." + "</t><br/><br/>"
html_start += "<t>" + "<b>" +"Вакансий найдено: "+ "</b>"  + str(num_of_vacancies) + "</t><br/>"
html_start += "<t>" + "<b>" +"Область поиска: "+ "</b>"  + str(areas_list) + "</t><br/>"
html_start += "<t>" + "<b>" +"Исключения: "+ "</b>"  + str(excluded_areas_noendls) + "</t><br/>"
html_start += "<t>" + "<b>" + "Запрос: "+ "</b>" + query_string + "</t><br/>"
html_start += "<t>" + "<b>" + "Кол-во компаний из списка на hh: " + "</b>" + str(len(companies_nums)) + "</t><br/>"
html_start += "<table style=\"width:100%\"><tr><th>#</th><th>Должность</th><th>Компания</th><th>Лого</th><th>Город</th><th>Зарплата</th><th>Дата и время (мск)</th><th>Ссылка</th></tr>"
html = html_start + html

file_results = codecs.open('results_test_table.html', 'w', 'utf-8')
file_results.write(html)
file_results.close()


webbrowser.open('results_test_table.html', new=2)  # open in new tab
