Quick start
-----------

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
