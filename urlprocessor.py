"""
Generates a Caption for Figures for each Image which stands alone in a paragraph,
similar to pandoc#s handling of images/figures

--------------------------------------------

Licensed under the GPL 2 (see LICENSE.md)

Copyright 2015 - Jan Dittrich by
building upon the markdown-figures Plugin by
Copyright 2013 - [Helder Correia](http://heldercorreia.com) (GPL2)

--------------------------------------------

Examples:
    Bla bla bla

    ![this is the caption](http://lorempixel.com/400/200/)

    Next paragraph starts here

would generate a figure like this:

    <figure>
        <img src="http://lorempixel.com/400/200/">
        <figcaption>this is the caption</figcaption>
    </figure>
"""


from __future__ import unicode_literals
import sys
from markdown import Extension
from markdown.treeprocessors import Treeprocessor

PY3 = sys.version_info >= (3, 0)
PY34 = sys.version_info >= (3, 4)

if PY3:
    uchr = chr  # noqa
    from urllib.request import pathname2url, url2pathname  # noqa
    from urllib.parse import urlparse, urlunparse, quote  # noqa
    from html.parser import HTMLParser  # noqa
    if PY34:
        import html  # noqa
        html_unescape = html.unescape  # noqa
    else:  # pragma: no cover
        html_unescape = HTMLParser().unescape  # noqa
else:
    uchr = unichr  # noqa
    from urllib import pathname2url, url2pathname, quote  # noqa
    from urlparse import urlparse, urlunparse  # noqa
    from HTMLParser import HTMLParser  # noqa
    html_unescape = HTMLParser().unescape  # noqa


class RepoPathTreeprocessor(Treeprocessor):
    def run(self, root):
        """
        Update urls on anchors and images to make them relative
        Iterates through the full document tree looking for specific
        tags and then makes them relative based on the site navigation
        """
        variables = self.config['variables']

        for element in root.iter():
            if element.tag == 'a':
                key = 'href'
            elif element.tag == 'img':
                key = 'src'
            else:
                continue

            url = element.get(key)
            element.set(key, self.update_url(url, variables))

        return root

    def update_url(self, url, variables):
        scheme, netloc, path, params, query, fragment = urlparse(url)

        for key, val in variables.items():
            path = path.replace('{{ %s }}' % key, val)

        components = (scheme, netloc, path, params, query, fragment)
        return urlunparse(components)


class RepoPathExtension(Extension):
    """
    The Extension class is what we pass to markdown, it then
    registers the Treeprocessor.
    """

    def __init__(self, *args, **kwargs):
        """Initialize."""

        self.config = {
            'variables': [{}, "Dict of variables to replace"],
        }

        super(RepoPathExtension, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md, md_globals):
        """Add post processor to Markdown instance."""

        rel_path = RepoPathTreeprocessor(md)
        rel_path.config = self.getConfigs()
        md.treeprocessors.register(rel_path, "urlprocessor", 20)
        md.registerExtension(self)


def makeExtension(**kwargs):
    return RepoPathExtension(**kwargs)
