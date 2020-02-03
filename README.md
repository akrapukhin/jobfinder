# jobfinder
Скрипт для поиска вакансий на hh.ru среди компаний из списка программы "Глобальное Образование" (http://educationglobal.ru/ns/participant/employment/)

Скрипт генерирует html-файл с вакансиями. Файл можно открыть в браузере, результаты отображаются в виде таблицы. Каждую вакансию из таблицы можно открыть на hh.ru, перейдя по ссылке, указанной в последнем столбце. Поиск настраивается с помощью четырех текстовых файлов. Вакансии отсортированы по дате (самые свежие наверху).


## 1. Скачивание
Нажмите на зеленую кнопку "Clone or download" наверху, затем в появившемся окне нажмите "Download ZIP". Разархивируйте ZIP-файл в любую папку.


## 2. Установка Python
Для запуска скрипта нужен установленный Python 3. Самый простой способ установить его - через Microsoft Store или через Mac App Store. Здесь и далее инструкция описывает процесс работы на Windows, но на Маке все примерно также. 

Нажмите "Пуск" и введите на клавиатуре "store". Поиск покажет приложение Microsoft Store - запустите его.
![Image of store](https://github.com/akrapukhin/jf_images/blob/master/2020-02-03_21-57-52.png)

Введите в поиск "python". Вы должны увидеть результатах python 3.7 и 3.8. Можно установить любой, у меня установлен 3.7. 
![python search](https://github.com/akrapukhin/jf_images/blob/master/2020-02-03_22-02-14.png)

Заходите на страницу программы и нажимаете "Получить". Все должно установиться автоматически.
![python install](https://github.com/akrapukhin/jf_images/blob/master/2020-02-03_22-14-45.png)


## 3. Установка библиотеки Requests для Python
Чтобы скрипт мог посылать запросы на headhunter.ru, необходимо установить библиотеку Requests для Python. Для этого нужно выполнить одну команду в командной строке. Ниже объясняется, как открыть командную строку и как выполнить эту команду.

#### 3.1. Запуск командной строки
Нажмите "Пуск" и введите на клавиатуре "cmd". Вы увидите Command Prompt или Командную строку. Запустите ее.
![terminal](https://github.com/akrapukhin/jf_images/blob/master/2020-02-03_22-18-40.png)

#### 3.2. Установка Requests
Введите команду "pip3 install requests" в командной строке и нажмите Enter:
```
pip3 install requests
```
![terminal](https://github.com/akrapukhin/jf_images/blob/master/2020-02-03_22-25-00.png)


## 4. Запуск скрипта
Запуск скрипта также осуществляется из командной строки. Для этого сначала нужно, чтобы командная строка указывала на папку, в которой находится скрипт. Для этого вы можете сначала зайти в папку со скриптом и скопировать адрес:
![copy](https://github.com/akrapukhin/jf_images/blob/master/2020-02-03_22-25-00.png)

И затем вставить (ctrl+v) этот адрес в командную строку, перед этим написав cd:
```
cd path/to/script
```
![terminal](https://github.com/akrapukhin/jf_images/blob/master/2020-02-03_22-48-19.png)

Нажмите Enter. Командная строка в результате указывает на папку со скриптом. Теперь можно запустить скрипт. Введите команду "python3 jobfinder.py":
```
python3 jobfinder.py
```
![terminal](https://github.com/akrapukhin/jf_images/blob/master/2020-02-03_23-25-07.png)

Если все работает правильно, появится информация о количестве найденных вакансий и тд.
![terminal](https://github.com/akrapukhin/jf_images/blob/master/2020-02-03_23-30-22.png)

Результаты будут записаны в HTML-файл results.html, который должен сразу автоматически открыться в вашем браузере:
![results](https://github.com/akrapukhin/jf_images/blob/master/2020-02-03_23-35-25.png)

Если файл не открылся, то зайдите в папку со скриптом, выберите файл results.html и откройте с помощью любого браузера:
![open_with](https://github.com/akrapukhin/jf_images/blob/master/2020-02-03_23-40-07.png)




## 5. Настройка поисковых параметров
Для настройки используется 4 файла. Ниже представлены инструкции по каждому файлу.

#### 5.1. query.txt
Здесь вам нужно ввести ваш поисковый запрос. Сюда вы пишете то, что вы обычно вводите на сайте hh.ru, когда ищете там вакансии.

#### 5.2. include_areas.txt
Здесь вы можете указать города или области, в которых хотите найти вакансии. Если не указано ничего, то вакансии ищутся по всей России. Вы можете указать несколько городов, но каждый город должен быть на новой строке. Вы также можете указывать области, например "Московская область", "Ленинградская область" и тд. Зеленоград.

#### 5.3. exclude_areas.txt
Здесь вы можете указать, какие города исключить из поиска. В основном это используется для того, чтобы исключить Москву и Санкт-Петербург из поиска, так как квоты закончились, но вы можете исключать любые города (области исключать нельзя). Таким образом, если вы ищете работу по всей России, кроме Москвы и Питера, вы можете оставить оставить include_areas.txt пустым, а в exclude_areas.txt внести Москву и Санкт-Петербург. Скрипт вернет все вакансии в любых городах России, кроме Москвы и Питера.

#### 5.4. date_from.txt
Здесь можно указать дату публикации вакансий. Если указано, например, 01-02-2020, то будут показаны только вакансии, опубликованный начиная с 1 февраля 2020 года, а более старые вакансии будут игнорироваться. Этот файл по умолчанию пустой, и скрипт возвращает все вакансии, которые имеют активный статус на hh.ru. Это параметр не особо нужен, так как скрипт показывает вакансии в порядке, отсортированном по дате, так что старые вакансии будут внизу. Я лично его не использую.

