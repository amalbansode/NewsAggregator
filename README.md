# NewsAggregator

## Introduction
NewsAggregator is a Python script that fetches and summarises news articles from numerous sources and presents them in an easily readable manner. 

## Installation
NewsAggregator requires Python 3 to be installed on your system, along with the primary dependency package, [newspaper](https://github.com/codelucas/newspaper).

### Setting Up for Usage with Python 3
1. [Install Python 3](https://www.python.org/downloads/) on your system. If you are running on macOS, your system will already have a version of Python 2.x installed. However, NewsAggregator only works with Python 3 and above!
2. Clone/download this repository and place it in a folder. Technically, you will only require `main.py` and `sources.json`.
3. In terminal, navigate to this folder.
	```bash
	$ cd location/of/your/folder
	```
4. Install the latest newspaper using pip.
	```bash
	$ pip3 install newspaper3k
	```

## Usage

### Using NewsAggregator
1. In terminal, navigate to the folder containing `main.py`.
	```bash
	$ cd location/of/your/folder
	```
2. Run the python script using 
	```bash
	$ python3 main.py
	```
3. Select a category you would like to view by typing in the category name.

![Select a source category](/images/cat_select.png)
4. Depending on the number of sources, the number of articles requested, and the status of the Internet connection, fetching and processing may require anything from under a minute to two minutes to finish.
5. A new tab should have now opened in your default web browser with the news articles’ summaries. If this fails, check the folder for a file named `NewsReport.html` and open it.

## Features

### Fully customizable sources and categories
Categories and source URLs can be customized by editing `sources.json`.

![Customize sources.json](/images/sources_json.png)

### JSON Output
The output of NewsAggregator can be exported to a JSON file using in-built functions by setting `ENABLE_JSON_OUTPUT` to `True`

![Output can be exported to a JSON file](/images/json_output.png)

## License
MIT License

© Amal Bansode, 2019