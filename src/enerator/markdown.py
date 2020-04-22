"""Markdown processing and syntax highlighting."""

import re
import typing

import cmarkgfm  # type: ignore
import pygments  # type: ignore
import pygments.formatters  # type: ignore
import pygments.lexers  # type: ignore

BRACE_RE = re.compile(r"{([^}]+)}")
CODE_RE = re.compile(r"^```([a-z]+)?$(.+?)^```$", re.S | re.M)
CMARK_FLAGS = 132096  # UNSAFE = 1 << 17; SMART = 1 << 10; CMARK_FLAGS = UNSAFE | SMART
FORMATTER = pygments.formatters.HtmlFormatter()


def escape_braces(text: str, pattern: typing.Pattern = BRACE_RE) -> str:
    """Escape interpolated variables so they will not be expanded yet.

    Args:
        text: a string containing the block of text.
        pattern: a compiled regex for matching the interpolated variables.

    Returns:
        A string with the now-escaped interpolated variables.
    """
    return pattern.sub(r"{{\1}}", text)


def md_codeblock(match: typing.Match) -> str:
    """Substitution method to replace markdown code blocks with pygmented HTML.

    Should be called from substition (sub) regex method.

    Args:
        match: matched block

    Returns:
        A string containing the highlighted (HTML) code block.
    """
    lang, code = match.groups()
    try:
        lexer = pygments.lexers.get_lexer_by_name(lang)
    except ValueError:
        lexer = pygments.lexers.TextLexer()
    return pygments.highlight(code, lexer, FORMATTER)


def md_highlight(md: str) -> str:
    """Replace markdown code blocks with pygmented HTML.

    Args:
        md: Markdown string with possible code fences.

    Returns:
        A string containing Markdown with code fenced blocks
        replaced with highlighted HTML.
    """
    return CODE_RE.sub(md_codeblock, md)


def md_highlight_and_parse(md: str) -> str:
    """Code highlight then convert to HTML.

    Args:
        md: Markdown string.

    Returns:
        A string with all the Markdown converted to HTML.
    """
    coded = md_highlight(md)
    return md_parse(coded)


def md_parse(md: str) -> str:
    """Parse Markdown.

    Args:
        md: Markdown string.

    Returns:
        HTML converted from the Markdown input.
    """
    return cmarkgfm.markdown_to_html(md, CMARK_FLAGS)
