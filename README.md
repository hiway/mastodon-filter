# mastodon-filter

Manage keyword filters on Mastodon from command-line.


## Installation

### Try it out

```
$ python3.10 -m pip install pipx
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

#### Backup filter keywords

```
$ mastodon-filter show TITLE > WORDLIST-FILE
```

#### Create a filter

```
$ mastodon-filter create TITLE WORDLIST-FILE
```

#### Delete a filter

```
$ mastodon-filter delete TITLE
```

