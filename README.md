# Student-Teacher management system
LMS course project that keeps track on student/teacher data
- created during learning at Hillel IT School


### Supports all the CRUD operations with data:
- create new records (allows uploading images & files as well)
- read full list of students and teachers
- update existing records data
- delete them


## Running
```
git clone git@github.com:NastyaKolodezhnaya/smashing-wallpaper-downloader.git
docker build -t lms .
docker run -it lms
```


## Quick Hint
use `generate_students` command from your console to generate random data for listing:
```
python manage.py generate_students [number_of_generated_objects]
```