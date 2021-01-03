# dianping
mini-project for scraping personal review comments from dianping

## prepare python environment

### package dependencies

* python3
* requests
* beautifulsoup4

add current project path to `PYTHONPATH` for importing python modules

```
export PYTHONPATH=.
```

## run script

* parse review comments from local html file
```
python src/review_parser.py
```

* parse review comments from personal member page
```
python src/review_summary.py
```

\* Cookie may need to be updated if error occurs...
