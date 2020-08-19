Quick start
-----------
This package provides a user interface for [PerfectExtractor](https://github.com/UUDigitalHumanitieslab/perfectextractor) in the form of a Django web application.
It can be used as part of bigger app (such as [TimeAlign](https://github.com/UUDigitalHumanitieslab/timealign)) or stand-alone.


## How to install inside another Django app:

1. Add "perfectextractor_ui" to your INSTALLED_APPS setting like this:

```
    INSTALLED_APPS = [
        ...
        'widget_tweaks',
        'perfectextractor_ui,
    ]
```

2. Include the perfectextractor_ui URLconf in your project urls.py like this:

```
    path('perfectextractor/', include('perfectextractor_ui.urls')),
```

3. Run ``python manage.py migrate`` to create the required models.

4. Run your app and configure your corpora in the admin panel.

## How to run stand-alone:

1. Create a python virtual environment for running perfectextractor-ui:

```
virtualenv -ppython3 /path/to/venv/
source /path/to/venv/bin/activate
```

2. Install package and requirements:

```
cd /path/to/perfectextractor-ui
pip install -r requirements.txt
pip install .
```

3. Run ``python manage.py migrate`` to create the required models.

4. Start the app:

```
python manage.py runserver
```

5. Configure your corpora in the admin panel (e.g. [http://localhost:8000/admin/](http://localhost:8000/admin))
