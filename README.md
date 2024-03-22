# Dataset-Search-Tool

The Dataset Search Tool is a set of two python scripts that can search for a dataset in a web repository and gather basic information, such as:
- Description
- Authors
- Citation Policy
- Web URL

The web repositories that can be considered for the search are [Kaggle](https://www.kaggle.com/) and [UCI](https://archive.ics.uci.edu/).

## Installation

In order to successfully install the tool it is necessary to have installed the ```selenium``` python library:

```bash
pip install selenium
```

After that, you may clone this repository:

```bash
git clone https://github.com/andresafira/Dataset-Search-Tool
```


## Usage

```python
from UCI_search_tool import get_UCI_description_and_link, get_UCI_possible_errors
from Kaggle_search_tool import get_kaggle_description_and_link, get_kaggle_possible_errors

# search for a dataset 'brazil' in the UCI repository
uci_result = get_UCI_description_and_link(link = None, name = 'brazil', minimize = False)
print(uci_result)
print(get_UCI_possible_errors())

# search for the dataset contained in the given link of the Kaggle repository
kaggle_result = get_kaggle_description_and_link(link = 'https://www.kaggle.com/datasets/thesnak/stock-market-analysis', name = None, search_competitions = False, minimize = False)
print(kaggle_result)
print(get_kaggle_possible_errors())
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
