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

You will be asked to provide instance URL and oAuth access-token.

Instance URL will be of the form:

- https://mastodon.social
- https://mastodon.sharma.io

Create an access-token for your account by visiting:

- https://INSTANCE-DOMAIN/settings/applications
- Click on "New Application"
- Provide a name (example: "mastodon-filter")
- Check `read:filters`
- Check `write:filters`
- Copy value of "Your access token" to clipboard

```
$ mastodon-filter config
Instance URL [https://example.social]: https://mastodon.sharma.io
Access token []: PASTE-YOUR-ACCESS-TOKEN-HERE
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

#### Sync filter keywords from a wordlist

```
$ mastodon-filter sync TITLE WORDLIST-FILE
```

#### Delete a filter

```
$ mastodon-filter delete TITLE
```
