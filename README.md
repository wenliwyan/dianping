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

**Important:**

When making http requests to acquire the *personal member page* and *specific review page*, `http_headers` in `src/review_summary.py` need to be updated accordingly in order to get a successfull response. It is not clear when `302 Redirect` to verification and `403 Forbidden` will be triggered on the dianping website.

My current approach is to access the personal member page in the actual browser, do the login and verification manually if needed, open browser development tools such as `Inspect Element`, and copy the `Cookie` value.

