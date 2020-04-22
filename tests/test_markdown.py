"""Tests for enerator's markdown parsing and code highlighting."""


import enerator.markdown


def test_md_parse():
    html = enerator.markdown.md_parse("**Hello**, _World_!")
    assert html == "<p><strong>Hello</strong>, <em>World</em>!</p>\n"


def test_md_highlight_python():
    result = enerator.markdown.md_highlight(
        "# Heading\n\n```python\nimport sys\n```\n\nSome text"
    )
    assert result == (
        '# Heading\n\n<div class="highlight"><pre><span></span><span class="kn">'
        'import</span> <span class="nn">sys</span>\n</pre></div>\n\n\nSome text'
    )


def test_md_highlight_unclear():
    result = enerator.markdown.md_highlight(
        "# Heading\n\n```squirrels\nSome code\n```\n\nSome text"
    )
    assert result == (
        '# Heading\n\n<div class="highlight"><pre><span></span>Some code\n</pre>'
        "</div>\n\n\nSome text"
    )


def test_md_highlight_and_parse():
    result = enerator.markdown.md_highlight_and_parse(
        "# Heading\n\n```python\nimport sys\n```\n\nSome text"
    )
    assert result == (
        '<h1>Heading</h1>\n<div class="highlight"><pre><span></span><span class="kn">'
        'import</span> <span class="nn">sys</span>\n</pre></div>\n<p>Some text</p>\n'
    )


def test_escape_braces():
    result = enerator.markdown.escape_braces("{variable}")
    assert result == "{{variable}}"
