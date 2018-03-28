# Rango Advisor
Rango Advisor is the new way to discover gorgeous places around the world. You can add your experiences as well and let others gaze upon the beauty. Upload photos, add ratings and comments, and build up your profile.

This was a group project for the 2nd year Web App Development course at the University of Glasgow. It was created by [Daumantas](https://github.com/Daumis102/), [Anguel](https://github.com/modelorona/), and [Louis](https://github.com/2268980C). The contributions of each individual team member can be seen in the [Contributions](https://github.com/Daumis102/RangoAdvisor/graphs/contributors) section of this repository.

## How to install
1. Clone the repo locally
2. Activate or create a virtual environment (python 3.6 required for this)
3. In the command line, run:
```bash
$ pip install -r requirements.txt
```

## Sources used for photos
* [Unsplash](https://unsplash.com/)
  * They are all royalty free photos and were used in the population_script.

## External libraries/services used
* [Google Maps JavaScript API](https://developers.google.com/maps/documentation/javascript/)
  * Used to show users where the location is and also to allow them to mark the place they want to add physically on the map.
* [jQuery](https://jquery.com/)
  * Used to manipulate frontend elements and post data to the server as well as show pretty modal windows.
* [Bootstrap 3](https://getbootstrap.com/docs/3.3/)
  * Used to style the entire site. If we had to do this manually, it would have taken about 5 years and a proper research team.
* [SweetAlert2](https://sweetalert2.github.io/)
  * Used for showing **sweet alerts** to the user. They're just gorgeous compared to the standard alerts. It's very important to show proper feedback to the user about their actions and if they worked or not.
* [Bootstrap Star Rating](http://plugins.krajee.com/star-rating)
  * Used to show the 5 star input field when users add a location.
* [tqdm](https://github.com/noamraph/tqdm)
  * Used to show nice looking loading bars within the population_script so that the user will know how much time they have left and also on what part of the script they are currently at.

## How to run tests
* Go into the django_advisor folder (where the manage.py is located), and within the commmand line, run:
```bash
$ python manage.py test advisor
```

## How to populate database initially
* First you must make the database. Go into the django_advisor folder and within the command line run:
```bash
$ python manage.py makemigrations advisor
```
* Then run:
```bash
$ python manage.py migrate
```
* At this point you will have made the database, which will be present within the root of the django_advisor folder as db.sqlite3 or similar. At this point, within the same directory, within the command line, run:
```bash
$ python population_script.py
```
* Enjoy the sweet progress bars.

## Live deploy
The application is currently deployed on [PythonAnywhere](https://djangoadvisor.pythonanywhere.com).

## Wireframes
The wireframes that we initially created can be found in the wireframes folder. We tried to stick to the designs from there but obviously as we went on, the designs evolved to ultimately create a better end result.
