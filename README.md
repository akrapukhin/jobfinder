# jobfinder
Скрипт для поиска вакансий на hh.ru среди компаний из списка программы Глобальное Образование (http://educationglobal.ru/ns/participant/employment/)

## 1. Скачивание
Нажмите на зеленую кнопку "Clone or download" наверху, затем в появившемся окне нажмите "Download ZIP". Разархивируйте ZIP-файл в любую папку.

## 2. Установка Python
Для запуска скрипта нужен установленный Python 3. Самый простой способ установить его - через Microsoft Store или через Mac App Store. Введите в поиск "python 3" и нажмите "установить".

## 3. Установка библиотеки Requests для Python
Чтобы посылать запросы на headhunter.ru, необходимо установить библиотеку Requests для Python. Это делается очень просто, нужно выполнить одну команду в командной строке. Ниже объясняется, как открыть командную строку и как выполнить эту команду.

### 3.1. Запуск командной строки
На windows нажмите пуск и на клавиатуре введите "cmd". Если у вас Mac, то ...

### 3.2. Установка Requests
Введите в командной строке
'''
pip3 install requests
'''

## 4. Запуск скрипта
Запуск скрипта также осуществляется из командной строки. Для этого сначала нужно, чтобы командная строка указывала на папку, в которой находится скрипт. 

## 5. Настройка поисковых параметров
Для настройки используется 4 файла. Ниже представлены инструкции по каждому файлу.

### 5.1. query.txt
Здесь вам нужно ввести ваш поисковый запрос. Сюда вы пишете то, что вы обычно вводите на сайте hh.ru, когда ищете там вакансии.

### 5.2. include_areas.txt
Здесь вы можете указать города или области, в которых хотите найти вакансии. Если не указано ничего, то вакансии ищутся по всей России. Вы можете указать несколько городов, но каждый город должен быть на новой строке. Вы также можете указывать области, например "Московская область", "Ленинградская область" и тд.

### 5.3. exclude_areas.txt
Здесь вы можете указать, какие города исключить из поиска. В основном это используется для того, чтобы исключить Москву и Санкт-Петербург из поиска, так как квоты закончились, но вы можете исключать любые города (области исключать нельзя). Таким образом, если вы ищете работу по всей России, кроме Москвы и Питера, вы можете оставить оставить include_areas.txt пустым, а в exclude_areas.txt внести Москву и Санкт-Петербург. Скрипт вернет все вакансии в любых городах России, кроме Москвы и Питера.

### 5.4. date_from.txt
Здесь можно указать дату публикации вакансий. Если указано, например, 01-02-2020, то будут показаны только вакансии, опубликованный начиная с 1 февраля 2020 года, а более старые вакансии будут игнорироваться. Этот файл по умолчанию пустой, и скрипт возвращает все вакансии, которые имеют активный статус на hh.ru. Это параметр не особо нужен, так как скрипт показывает вакансии в порядке, отсортированном по дате, так что старые вакансии будут внизу. Я лично его не использую.

