import requests
import codecs
import urllib.request
import webbrowser

# check if there is a new version available
version = "2020-02-02b"
new_version = False
for line in urllib.request.urlopen('https://raw.githubusercontent.com/akrapukhin/jobfinder/master/jobfinder.py'):
    line = line.decode('utf-8').strip()
    if line[0:7] == "version":
        if line[11:-1] != version:
            new_version = True

# read query from file
file_query = codecs.open('query.txt', 'r', 'utf-8')
query = file_query.readlines()
query_string = ""
for line in query:
    query_string += line.strip() + " "
query_string = query_string.strip()

# read date from file
file_date_from = codecs.open('date_from.txt', 'r', 'utf-8')
date_from = file_date_from.readline().strip()
date_from_format_day_first = "-"
if len(date_from) > 0:
    if len(date_from) != 10 or date_from[2] != '-' or date_from[5] != '-':
        print("Ошибка: неверно введена дата в файле date_from.txt. Правильный формат: ДД-ММ-ГГГГ. Пример: 01-02-2020")
        print("Можете также убрать ограничение по дате, удалив все из файла date_from.txt")
        exit()
    else:
        date_from_format_day_first = date_from
        date_from = date_from[6:10] + date_from[5] + date_from[3:5] + date_from[2] + date_from[0:2]
else:
    date_from = None

# read included areas
file_areas = codecs.open('include_areas.txt', 'r', 'utf-8')
areas = file_areas.readlines()
areas_list = []
for area in areas:
    area = area.strip().lower()
    if area != '':
        areas_list.append(area)

# load all areas in Russia
russia_areas = []
russia_id = 113
all_areas = requests.get('https://api.hh.ru/areas')
all_areas = all_areas.json()
for area in all_areas:
    if area['name'].lower() == 'россия':
        russia_id = area['id']
        russia_areas = area['areas']

# read excluded areas
file_excl_areas = codecs.open('exclude_areas.txt', 'r', 'utf-8')
excluded_areas = file_excl_areas.readlines()
excluded_areas_list = []
excluded_areas_str = "-"
for area in excluded_areas:
    area = area.strip().lower()
    if area != '':
        excluded_areas_list.append(area)

# check excluded cities
for excl_area in excluded_areas_list:
    area_found = False
    for region in russia_areas:
        if region['name'].lower() == excl_area.lower():
            if excl_area.lower() == "москва" or excl_area.lower() == "санкт-петербург":
                area_found = True
                excluded_areas_str += region['name'] + ", "
        for city in region['areas']:
            if city['name'].lower() == excl_area.lower():
                area_found = True
                excluded_areas_str += city['name'] + ", "
    if not area_found:
        print('Ошибка: город не найден: ' + excl_area)
        print("Исправьте название города в файле exclude_areas.txt")
        exit()

excluded_areas_str = excluded_areas_str.strip()
if excluded_areas_str[-1] == ",":
    excluded_areas_str = excluded_areas_str[1:-1]  # index from 1 to eliminate '-'

# load list of companies
companies = []
for line in urllib.request.urlopen('https://raw.githubusercontent.com/akrapukhin/jobfinder/master/companies.txt'):
    companies.append(line.decode('utf-8').strip())
companies = set(companies)
companies = list(companies)
companies_ids = []
for s in companies:
    companies_ids.append(s[23:])

# find corresponding areas IDs
areas_ids = []
areas_str = ""
if len(areas_list) == 0:
    areas_ids.append(russia_id)
    areas_list.append("Россия")
    areas_str = "Россия"
else:
    for area in areas_list:
        area_found = False
        for region in russia_areas:
            if region['name'].lower() == area.lower():
                areas_ids.append(region['id'])
                area_found = True
                areas_str += region['name'] + ", "
            for city in region['areas']:
                if city['name'].lower() == area.lower():
                    areas_ids.append(city['id'])
                    area_found = True
                    areas_str += city['name'] + ", "
        if not area_found:
            print('Ошибка: территория не найдена: ' + area)
            print("Исправьте название города или области в файле include_areas.txt")
            exit()

areas_str = areas_str.strip()
if areas_str[-1] == ",":
    areas_str = areas_str[:-1]

# parameters of query to hh
par = {'text': query_string,
       'area': areas_ids,
       'per_page': '100',
       'employer_id': companies_ids,
       'order_by': 'publication_time',
       'date_from': date_from,
       'page': 0}

# request to hh to get all vacancies
all_pages = []
first_page_vacancies = requests.get('https://api.hh.ru/vacancies', params=par)
print("Запрос отправлен. Подождите несколько секунд...")
if str(first_page_vacancies)[11:14] != "200":
    print("Ошибка: некорректный запрос. Возможные причины:")
    print("- Неверно указана дата в файле date_from.txt")
    print("- Неверно написан запрос в файле query.txt")
    print("- Неверно указаны включаемые и исключаемые территории в файлах include_areas.txt и exclude_areas.txt")
    exit()
first_page_vacancies = first_page_vacancies.json()
all_pages.append(first_page_vacancies)

num_of_vacancies_total = first_page_vacancies['found']
num_of_vacancies = first_page_vacancies['found']
if num_of_vacancies > 2000:
    num_of_vacancies = 2000
num_of_pages = first_page_vacancies['pages']

for page_num in range(num_of_pages - 1):
    par['page'] = page_num + 1
    page_vacancies = requests.get('https://api.hh.ru/vacancies', params=par)
    page_vacancies = page_vacancies.json()
    all_pages.append(page_vacancies)

# generate HTML with all found vacancies
html = ""
counter = 1
for page in all_pages:
    vacancies = page['items']
    for vac in vacancies:
        excluded = False
        for excluded_area in excluded_areas_list:
            if excluded_area.lower() == vac['area']['name'].lower():
                excluded = True
        if not excluded:
            # get salary
            salary = vac['salary']
            salary_str = ""
            if salary is None:
                salary_str = "не указана"
            else:
                if salary['from'] is not None:
                    salary_str = "от " + str(salary['from']) + " "
                if salary['to'] is not None:
                    salary_str += "до " + str(salary['to'])
                if salary['gross']:
                    salary_str += " до вычета"
                else:
                    salary_str += " на руки"
            # get logo
            logo_str = ""
            if vac['employer']['logo_urls'] is not None:
                if vac['employer']['logo_urls']['90'] is not None:
                    logo_str = vac['employer']['logo_urls']['90']

            # generate one line in HTML file with vacancy info
            html_line = "<tr><td>" + str(counter)  # number
            html_line += "</td><td>" + vac['name']  # vacancy title
            html_line += "</td><td>" + vac['employer']['name']  # employer name
            html_line += "</td><td align=\"center\">" + "<img src=\"" + logo_str + "\"" + ">"  # employer logo
            html_line += "</td><td>" + vac['area']['name']  # vacancy area
            html_line += "</td><td>" + salary_str  # salary
            html_line += "</td><td style=\"white-space:nowrap;\">" + vac['published_at'][8:10] + vac['published_at'][7]
            html_line += vac['published_at'][5:7] + vac['published_at'][4] + vac['published_at'][0:4] + " "
            html_line += vac['published_at'][11:16]  # time of publication
            html_line += "</td><td><a href = \"" + vac['alternate_url'] + "\" target=\"_blank\">" + vac['alternate_url']
            html_line += "</a></td></tr>"  # link to vacancy
            html += html_line
            counter += 1
        else:
            num_of_vacancies -= 1

too_many_vac_warn = "Нашлось больше 2000 вакансий (" + str(num_of_vacancies_total) + " вакансий). "
too_many_vac_warn += "Из-за особенностей работы API HH доступны только самые свежие 2000 \
вакансий. Кроме того, из этих 2000 исключаются вакансии в городах, указанных в файле exclude_areas.txt. \
Итоговое кол-во вакансий указано ниже в поле \"Вакансий найдено\". "
too_many_vac_warn += "Если вы хотите быть уверенными в том, что по вашему запросу вернулись все вакансии, сделайте \
запрос более жестким. Например, ограничив дату в date_from.txt, изменив запрос в query.txt или изменив область поиска \
в include_areas.txt"

print('Вакансий найдено: ' + str(num_of_vacancies))
html += "</body></html>"
html_start = """<!DOCTYPE html><html><head><style>table, th, td {border: 1px solid black;}</style>"""
html_start += """<meta http-equiv="Content-Type" content="text/html; charset=utf-8" /></head><body>"""
if new_version:
    html_start += "<t>" + "Доступна новая версия скрипта. Ваша версия может работать неправильно. Перейдите"
    html_start += " по ссылке " + "<a href = \"" + "https://github.com/akrapukhin/jobfinder/blob/master/jobfinder.py"
    html_start += "\" target=\"_blank\">" + "https://github.com/akrapukhin/jobfinder/blob/master/jobfinder.py" + "</a>"
    html_start += ", наведите курсор на кнопку \"Raw\", нажмите \"сохранить объект как...\" (или что-то подобное в"
    html_start += " зависимости от браузера) и положите скачанный файл в папку со скриптом, согласившись на замену."
    html_start += "</t><br/><br/>"

if num_of_vacancies_total > 2000:
    html_start += "<t>" + too_many_vac_warn + "</t><br/><br/>"
html_start += "<t>" + "<b>" + "Вакансий найдено: " + "</b>" + str(num_of_vacancies) + "</t><br/>"
html_start += "<t>" + "<b>" + "Область поиска: " + "</b>" + areas_str + "</t><br/>"
html_start += "<t>" + "<b>" + "Исключения: " + "</b>" + excluded_areas_str + "</t><br/>"
if query_string == "":
    query_string = "-"
html_start += "<t>" + "<b>" + "Запрос: " + "</b>" + query_string + "</t><br/>"
html_start += "<t>" + "<b>" + "Ограничение по дате: " + "</b>" + date_from_format_day_first + "</t><br/>"
html_start += "<t>" + "<b>" + "Кол-во компаний из списка на hh: " + "</b>" + str(len(companies_ids)) + "</t><br/>"
html_start += "<table style=\"width:100%\"><tr><th>#</th><th>Должность</th><th>Компания</th>"
html_start += "<th>Лого</th><th>Город</th><th>Зарплата</th><th>Дата и время (мск)</th><th>Ссылка</th></tr>"
html = html_start + html

# save HTML file
file_results = codecs.open('results.html', 'w', 'utf-8')
file_results.write(html)
file_results.close()
print("Результаты записаны в файл results.html")

# open in new tab
webbrowser.open('results.html', new=2)
