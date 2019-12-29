import json
from typing import Dict, Any
import random
random.choices()
import django
import requests
django.setup()
from subject.models import Subject
fields_of_studies = ['stacjonarne-informatyka',
           'stacjonarne-cyberbezpieczenstwo--2',
           'stacjonarne-elektronika',
           'stacjonarne-elektronika-i-telekomunikacja--3',
           'full-time-studies-electronics-and-telecommunications--2',
           'stacjonarne-teleinformatyka'
                    ]
list_of_subjects_url = 'https://syllabuskrk.agh.edu.pl/2019-2020/magnesite/api/faculties/wieit/study_plans/{}/modules'
detail_of_subject_url = 'https://syllabuskrk.agh.edu.pl/api/current_annual/modules/{}'
list_of_subjects = []
for field in fields_of_studies:
    result = requests.get(list_of_subjects_url.format(field))
    result = result.json()['syllabus']['assignments']
    for syllabus_subject in result:
        subject = {}
        subject['id'] = syllabus_subject['assignment']['module_id']
        subject['code'] = syllabus_subject['assignment']['module_code']
        subject['mode'] = syllabus_subject['assignment']['module']['name']
        module_details_response: Dict[Any, Any] = requests.get(detail_of_subject_url.format(subject['id'])).json()
        subject['semester'] = module_details_response['study_plans'][0]['semester_number']
        subject['field_of_study'] = field
        print(subject)
        list_of_subjects.append(subject)

with open('syllabus-export.json', 'w+') as f:
    f.write(json.dumps(list_of_subjects))
# Subject.objects.exists()
