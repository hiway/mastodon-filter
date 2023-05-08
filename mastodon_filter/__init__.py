"""
Manage keyword filters on Mastodon from command-line.
"""
try:
    # Eager imports to satisfy py2app
    import charset_normalizer as _cn
    import charset_normalizer.md__mypyc as _cn_md__mypyc
except ImportError:
    pass
