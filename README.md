# Mastodon Filter

Manage keyword filters on Mastodon from command-line (and a simple GUI).

![Screenshot of Mastodon Filter app](https://github.com/hiway/mastodon-filter/assets/23116/d5706956-aab2-45c6-99f5-99171c657c21?raw=true "Mastodon Filter")

## Installation

### Requirements

macOS
```
$ brew install python@3.9
$ brew install python-tk
```

FreeBSD
```
$ pkg install python39
$ pkg install py39-tkinter
```

#### Instance URL and Access Token

Instance URL will be of the form:

- https://mastodon.social
- https://mastodon.sharma.io

Create an access-token for your account by visiting:

- https://INSTANCE-DOMAIN/settings/applications
- Click on "New Application"
- Provide a name (example: "mastodon-filter")
- Check `read:filters`
- Check `write:filters`
- Copy value of "Your access token"

If running CLI, see *Configure* section

If running GUI, use *Instance* Menu to configure instance URL and Access Token.


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

### Graphical User Interface

```
$ mastodon-filter
```

### Command Line Interface

#### Show CLI Commands
```
$ mastodon-filter --help
```

#### Configure

```
$ mastodon-filter config
Instance URL [https://example.social]: https://mastodon.sharma.io
Access token []: PASTE-YOUR-ACCESS-TOKEN-HERE
```

#### List filter titles and keyword counts

View all configured filters. 

```
$ mastodon-filter list
```

#### Show filter keywords

Output each keyword in a filter on a separate line.
Pipe output to `grep` to filter words.

```
$ mastodon-filter show TITLE
```

#### Share / backup filter keywords

Backup your existing filter to a file by redirecting output.
Share the file with friends or strangers if you like.
They can then use it to create their own filters.

```
$ mastodon-filter show TITLE > WORDLIST-FILE
```

#### Create a filter from a wordlist

Have a list of words you want to filter?
Someone shared their wordlist?
Import it into your account and create a new filter.
Filter titles must be unique.
Use the `list` command to see your existing filters.

```
$ mastodon-filter create TITLE WORDLIST-FILE
```

#### Create a filter from terminal input

Quickly get started with a new filter list 
by typing out the words or phrases,
each on a new line.
Finally press Ctrl+D to exit text-entry mode and save the filter.

```
$ mastodon-filter create TITLE -
```

#### Sync filter keywords from a wordlist

Once you have a few filters set up, edit the text file locally
and update the server to add new words or remove deleted words.

```
$ mastodon-filter sync TITLE WORDLIST-FILE
```

#### Delete a filter

Delete a filter and discard all words in it.
Use `show` to backup the words to a text file before deleting.

```
$ mastodon-filter delete TITLE
```

#### List Filter Templates

List names of available templates.

```
$ mastodon-filter template list
```

#### Show Filter Template

Show the words in a template.

```
$ mastodon-filter template show NAME
```

#### Use Template to Create Filter

Create a new filter from a template.

```
$ mastodon-filter template use NAME TITLE
```