# Installation Notes

This package requires at least Python 3.6.

To install module locally, go to the `dist/` directory and run.

```
python3 -m pip install uber_clone_pkg_CROWDBOTICS-0.0.1-py3-none-any.whl
```

# Testing

Test files are located in `tests/` folder
```
python3 test_app.py
```

# Module Dependencies:
* Open Street Map (OSM) API (https://github.com/metaodi/osmapi)
* GeoPy (https://geopy.readthedocs.io/en/stable/) - for calculating distance
* PyrouteLib (https://wiki.openstreetmap.org/wiki/PyrouteLib) - identifying route

# Uninstalling Module

run ```pip uninstall -r requirements.txt``` in the parent directory