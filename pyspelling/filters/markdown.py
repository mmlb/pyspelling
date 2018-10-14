"""Markdown filter."""
from __future__ import unicode_literals
from .. import filters
from .. import util
import codecs
import markdown


class MarkdownFilter(filters.Filter):
    """Spelling Python."""

    def __init__(self, options, default_encoding='utf-8'):
        """Initialization."""

        extensions = []
        extension_configs = {}
        for item in options.get('markdown_extensions', []):
            if isinstance(item, util.ustr):
                extensions.append(item)
            else:
                k, v = list(item.items())[0]
                extensions.append(k)
                if v is not None:
                    extension_configs[k] = v
        self.markdown = markdown.Markdown(extensions=extensions, extension_configs=extension_configs)
        super(MarkdownFilter, self).__init__(options, default_encoding)

    def filter(self, source_file, encoding):  # noqa A001
        """Parse Markdown file."""

        with codecs.open(source_file, 'r', encoding=encoding) as f:
            text = f.read()
        return [filters.SourceText(self._filter(text), source_file, encoding, 'markdown')]

    def _filter(self, text):
        """Filter markdown."""

        self.markdown.reset()
        return self.markdown.convert(text)

    def sfilter(self, source):
        """Filter."""

        return [filters.SourceText(self._filter(source.text), source.context, source.encoding, 'markdown')]


def get_filter():
    """Return the filter."""

    return MarkdownFilter