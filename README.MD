# Readme teleinformatycznej wiki
[![CircleCI](https://circleci.com/gh/nekeal/passit.svg?style=svg&circle-token=982ca38352b4da2c8b8f47ecf96e2bd77b77c268)](https://circleci.com/gh/nekeal/passit)

Aby uruchomić projekt lokalnie należy użyć komendy `docker-compose up`. Wymagana jest do tego instalacja
narzędzi docker i docker-compose.
Uruchomi to instancje aplikacji razem z bazą danych.
Interfejs webowy domyślnie działa na porcie 8000.  
Aby utworzyć konto administratora należy wykonać komendę `docker-compose run web python manage.py createsuperuser`.
Kontem tym można zalogować się pod `/admin/`

Można tworzyć nowe przedmioty/wykładowców itp. ale najlepiej jest załadować bazę z pliku fixture.sql
za pomocą komendy `psql -h localhost -U teleagh -d teleagh -p 5433 < fixture.sql`

Dane są podobne do tych na [https://passit.beyondthe.dev](https://passit.beyondthe.dev)

Konto studenta to testerowyj:Plokij123
Konto admina admin:admin

Ważniejsze ścieżki:
- `/admin/accounts/userprofile/` - profile użytkowników
- `/admin/accounts/customuser/` - konta użytkowników
- `/admin/news/news/` - ogłoszenia
- `/admin/subject/subject/` - przedmioty
- `/api/` - nie wszystkie funkcjonalności są obecne w interfejsie użytkownika,
jednak api do nich znajduje się pod tą ścieżką

Struktura projektu wraz z opisem ważniejszych elementów:
`projekt`  
├── conftest.py - konfiguracja pytesta   
├── deployment - folder przechowujący konfigurację do deploymentu     
├── docker-compose-production.yml  - docker compose przeznaczony na serwer  
├── docker-compose.yml  - docker compose przeznaczony do uruchamiania lokalnego  
├── Dockerfile  - konfiguracja obrazu dockera  
├── entrypoint.sh  - skrypt startowy dla obrazu dockera  
├── heroku.yml  - plik konfiguracyjny dla chmury heroku
├── LICENSE  - plik licencji  
├── manage.py  
├── mypy.ini  - plik konfiguracyjny mypy  
├── package-lock.json  
├── pytest.ini  - konfiguracja pytesta  
├── README.MD  
├── requirements.txt - lista wymaganych pakietów python    
├── requirements-ci.txt   
├── requirements-dev.txt     
├── teleagh  - folder zawierający moduły aplikacji 
│   ├── accounts  - odpowiedzialny za autoryzację  
│   ├── common  - przydatne funkcje i klasy  
│   ├── events  - odpowiedzialny za wydarzenia  
│   ├── frontend  
│   ├── \_\_init__.py    
│   ├── lecturers  - odpowiedzialny za wykładowców  
│   ├── news  - odpowiedzialny za ogłoszenia   
│   ├── settings  - ustawienia projektu   
│   ├── subject  - odpowiedzialny za przedmioty  
│   ├── syllabus  - odpowiedzialny za integrację z syllabusem  
│   ├── urls.py  - konfiguracja urli  
│   ├── views.py - główny widok  
│   └── wsgi.py
└── fixture.sql - przykładowa baza danych   

Struktura modułu na przykładzie aplikacji  
`subject`
├── admin.py - konfiguracja panelu admina  
├── apps.py  
├── factories.py - fabryki do tworzenia danych testowych  
├── filters.py - klasy filtrujące dane  
├── \_\_init__.py   
├── managers.py  - niestandardowe managery odpowiedzialne za komunikację z bazą danych  
├── querysets.py - niestanadardowe klasy reprezentujące dane otrzymane z bazy  
├── migrations - pliki migracji  
├── models.py - modele danych w postaci klas pythona  
├── serializers.py  - klasy konwertujące typy danych pythona na jsona i odwrotnie  
├── tests - testy  
├── urls.py - konfiguracja urli danej aplikacji  
└── views.py - widoki danej aplikacji  

Import z syllabusa znajduje się w pliku `teleagh/syllabus/scripts/start_new_year.py`
Skrypt uruchamia się z lini poleceń komendą: `docker-compose run web python manage.py runscript start_new_year`

Domyślnie brane są argumenty odpowiadające mojemu obecnemu kierunkowi.

Przykład importu z podaniem argumentów:
`docker-compose run web python manage.py runscript start_new_year --script-args '--age-group 2019-2020 --field-of-study stacjonarne-teleinformatyka'`
