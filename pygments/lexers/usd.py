# -*- coding: utf-8 -*-

"""The module that parses Pixar's Universal Scene Description file format."""

from pygments.lexer import RegexLexer, bygroups
from pygments.lexer import words as words_
from pygments.lexers._usd_builtins import COMMON_ATTRIBUTES, KEYWORDS, \
    OPERATORS, SPECIAL_NAMES, TYPES
from pygments.token import Comment, Generic, Keyword, Name, Number, Operator, \
    Punctuation, String, Text, Whitespace

__all__ = ["UsdLexer"]


def _keywords(words, type_):
    """list[tuple[:class:`pygments.lexer.words`, :class:`pygments.token._TokenType`]]."""
    return [(words_(words, prefix=r"\b", suffix=r"\b"), type_)]


_TYPE = r"(\w+(?:\[\])?)"
_BASE_ATTRIBUTE = r"([\w_]+(?:\:[\w_]+)*)(?:(\.)(timeSamples))?"
_WHITESPACE = r"([ \t]+)"


class UsdLexer(RegexLexer):
    """
    A lexer that parses Pixar's Universal Scene Description file format.

    .. versionadded:: 2.6.0
    """

    name = "USD"
    aliases = ["usd", "usda"]
    filenames = ["*.usd", "*.usda"]

    tokens = {
        "root": [
            (
                r"(custom){_WHITESPACE}(uniform)(\s+){}(\s+){}(\s*)(=)".format(
                    _TYPE, _BASE_ATTRIBUTE, _WHITESPACE=_WHITESPACE
                ),
                bygroups(
                    Keyword.Token,
                    Whitespace,
                    Keyword.Token,
                    Whitespace,
                    Keyword.Type,
                    Whitespace,
                    Name.Attribute,
                    Generic,
                    Name.Keyword.Tokens,
                    Whitespace,
                    Operator,
                ),
            ),
            (
                r"(custom){_WHITESPACE}{}(\s+){}(\s*)(=)".format(
                    _TYPE, _BASE_ATTRIBUTE, _WHITESPACE=_WHITESPACE
                ),
                bygroups(
                    Keyword.Token,
                    Whitespace,
                    Keyword.Type,
                    Whitespace,
                    Name.Attribute,
                    Generic,
                    Name.Keyword.Tokens,
                    Whitespace,
                    Operator,
                ),
            ),
            (
                r"(uniform){_WHITESPACE}{}(\s+){}(\s*)(=)".format(
                    _TYPE, _BASE_ATTRIBUTE, _WHITESPACE=_WHITESPACE
                ),
                bygroups(
                    Keyword.Token,
                    Whitespace,
                    Keyword.Type,
                    Whitespace,
                    Name.Attribute,
                    Generic,
                    Name.Keyword.Tokens,
                    Whitespace,
                    Operator,
                ),
            ),
            (
                r"{}{_WHITESPACE}{}(\s*)(=)".format(
                    _TYPE, _BASE_ATTRIBUTE, _WHITESPACE=_WHITESPACE
                ),
                bygroups(
                    Keyword.Type,
                    Whitespace,
                    Name.Attribute,
                    Generic,
                    Name.Keyword.Tokens,
                    Whitespace,
                    Operator,
                ),
            ),
        ]
        + _keywords(KEYWORDS, Keyword.Tokens)
        + _keywords(SPECIAL_NAMES, Name.Builtins)
        + _keywords(COMMON_ATTRIBUTES, Name.Attribute)
        + [(r"\b\w+:[\w:]+\b", Name.Attribute)]
        + _keywords(OPERATORS, Operator)  # more attributes
        + [(type_ + r"\[\]", Keyword.Type) for type_ in TYPES]
        + _keywords(TYPES, Keyword.Type)
        + [(r"[\(\)\[\]{}]", Punctuation)],
        + [
            ("#.*?$", Comment.Single),
            (",", Generic),
            (";", Generic),  # ";"s are allowed to combine separate metadata lines
            ("=", Operator),
            ("[-]?([0-9]*[.])?[0-9]+", Number),
            (r"'''(?:.|\n)*?'''", String),
            (r'"""(?:.|\n)*?"""', String),
            (r"'.*'", String),
            (r'".*"', String),
            (r"<(\.\./)*([\w/]+|[\w/]+\.\w+[\w:]*)>", Name.Namespace),
            (r"@.*@", String.Interpol),
            (r'\(.*"[.\\n]*".*\)', String.Doc),
            (r"\A#usda .+$", Comment.Hashbang),
            (r"\s+", Text),
            (r"[\w_:\.]+", Generic),
        ],
    }
