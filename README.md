# mastodon-filter

Manage keyword filters on Mastodon from command-line.


## Installation

### Try it out

```
$ python3 -m pip install pipx
$ pipx install git+https://github.com/hiway/mastodon-filter.git
$ mastodon-filter --help
```

### Development

```
$ git clone https://github.com/hiway/mastodon-filter.git
$ cd mastodon-filter
$ poetry install
$ poetry shell

$ mastodon-filter --help
```


## Usage

#### Configure authentication

```
$ mastodon-filter config
```

#### List filter titles and keyword counts

```
$ mastodon-filter list
```

#### Show filter keywords

```
$ mastodon-filter show TITLE
```

#### Share / backup filter keywords

```
$ mastodon-filter show TITLE > WORDLIST-FILE
```

#### Create a filter from a wordlist

```
$ mastodon-filter create TITLE WORDLIST-FILE
```

#### Create a filter from terminal input

```
$ mastodon-filter create TITLE -
```

#### Delete a filter

```
$ mastodon-filter delete TITLE
```
