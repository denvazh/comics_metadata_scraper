Scraper for comics metadata

This is a very simple scraper based on Scrapy (http://scrapy.org).
Intended purpose is to collect metadata for research and data analysis only,
thus no image or any other files gets downloaded.

At the moment the following comics providers were configured:

* Dilbert strips ([dilbert.com](http://dilbert.com/))
* Xkcd ([xkcd.com](http://xkcd.com/))

To run crawler, run the following:

* create virtual environment (I usually do it with `pyenv` + `pyenv-virtualenv`)

```bash
$ pyenv virtualenv 2.7.10 scrapy-venv27
$ pyenv activate scrapy-venv27
```

* install necessary dependencies

```bash
$ pip install -r requirements.txt
$ pyenv rehash
```

* run crawler and save results to `xkcd.json`

```bash
$ scrapy crawl xkcd -o xkcd.json
```