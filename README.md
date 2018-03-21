# Rango Advisor
Rango Advisor is the new way to discover gorgeous places around the world. You can add your experiences as well and let others gaze upon the beauty. Upload photos, add ratings and comments, and build up your profile.

## How to install
1. Change into the django_adviser directory
2. Activate the virtual environment (python 3.6)
3. In the command line, run
```bash
$ pip install -r requirements.txt
```

## Sources used for photos
* [Unsplash](https://unsplash.com/)

## External libraries/services used
* [Google Maps JavaScript API](https://developers.google.com/maps/documentation/javascript/)
* [jQuery](https://jquery.com/)
* [Bootstrap 3](https://getbootstrap.com/docs/3.3/)
* [SweetAlert2](https://sweetalert2.github.io/)
* [Bootstrap Star Rating](http://plugins.krajee.com/star-rating)
* [Django Compressor](https://django-compressor.readthedocs.io/en/latest/)
* [lxml](http://lxml.de/)

## How to run tests
```bash
$ python manage.py test
```

## How to populate database initially
```bash
$ python population_script.py
```