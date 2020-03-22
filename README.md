# Goldendict Web Translation

This project aims to provide web translations for Goldendict.

## Requirements

- flask
- requests
- BeautifulSoup (with html5lib)
- googletrans

## Usage

The query url is

    http://172.0.0.1:5000/translate?q=<word>[&s=server]

where `<word>` is the word (or sentence) to query. `[server]` (optional) is now chosen from `auto` (default), `youdao` or `google`. If `auto` is chosen, then it will first try `youdao` from its dictionaries and then `google` for machine translation.

You can add the url `http://127.0.0.1:5000/translate?q=%GDWORD%` into `Edit -> Dictionaries -> Websites` in goldendict.

## API Interface

You can create your own api and put the file into `api` folder. The file must have the function `get_trans(word)` with exactly one positional argument for the word to be query, and return a list with all available translation. And the api could be called by changing `[server]` to the name of that file (without .py extension)

## Bugs

- Goldendict cannot correctly handle page height according to [this issue](https://github.com/goldendict/goldendict/issues/614). As a workaround, the page have to be loaded twice (see [templates/index.html](templates/index.html)).

- googletrans has an outdated translation api in pypi repository (which has been solved [upstream](https://github.com/ssut/py-googletrans/pull/102)). Please apply this upstream patch to attain better translation quality.
