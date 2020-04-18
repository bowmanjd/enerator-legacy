"""Tests for enerator"""

import importlib
import json
import os
import pathlib
import sys

import enerator


def test_md_parse():
    html = enerator.md_parse("**Hello**, _World_!")
    assert html == "<p><strong>Hello</strong>, <em>World</em>!</p>\n"


def test_md_highlight_python():
    result = enerator.md_highlight(
        "# Heading\n\n```python\nimport sys\n```\n\nSome text"
    )
    assert result == (
        '# Heading\n\n<div class="highlight"><pre><span></span><span class="kn">'
        'import</span> <span class="nn">sys</span>\n</pre></div>\n\n\nSome text'
    )


def test_md_highlight_unclear():
    result = enerator.md_highlight(
        "# Heading\n\n```squirrels\nSome code\n```\n\nSome text"
    )
    assert result == (
        '# Heading\n\n<div class="highlight"><pre><span></span>Some code\n</pre>'
        "</div>\n\n\nSome text"
    )


def test_md_highlight_and_parse():
    result = enerator.md_highlight_and_parse(
        "# Heading\n\n```python\nimport sys\n```\n\nSome text"
    )
    assert result == (
        '<h1>Heading</h1>\n<div class="highlight"><pre><span></span><span class="kn">'
        'import</span> <span class="nn">sys</span>\n</pre></div>\n<p>Some text</p>\n'
    )


def test_module_to_path():
    result = enerator.module_to_path("pages.mydir.mypage")
    assert result.parts[len(pathlib.Path.cwd().parts) :] == ("pages", "mydir", "mypage")


def test_escape_braces():
    result = enerator.escape_braces("{variable}")
    assert result == "{{variable}}"


def test_create_dirs(tmp_path):
    os.chdir(tmp_path)
    dirpath = tmp_path / "parent_dir" / "child_dir"
    enerator.create_dirs(dirpath)
    content = (dirpath / "__init__.py").read_text()
    assert "import enerator" in content
    assert (dirpath.parent / "__init__.py").exists()
    assert not (tmp_path / "__init__.py").exists()


def test_cmd_add(tmp_path):
    os.chdir(tmp_path)
    sys.path.append(str(tmp_path))
    module = "pages.programming.home"
    enerator.cmd_add(sitepath="/programming", module=module, title="Programming")
    page = importlib.import_module(module)
    assert len(page.page()) > 0


def test_sitemap_read_no_file(tmp_path):
    os.chdir(tmp_path)
    (tmp_path / enerator.SITEMAP).unlink(missing_ok=True)
    enerator.sitemap_read.cache_clear()
    result = enerator.sitemap_read()
    assert result == {}


def test_sitemap_read_file(tmp_path):
    os.chdir(tmp_path)
    payload = {"key": "value"}
    (tmp_path / enerator.SITEMAP).write_text(json.dumps(payload))
    enerator.sitemap_read.cache_clear()
    result = enerator.sitemap_read()
    assert result == payload


def test_sitemap_write_file(tmp_path):
    os.chdir(tmp_path)
    payload = {"key2": "value2"}
    enerator.sitemap_write(payload)
    enerator.sitemap_read.cache_clear()
    result = enerator.sitemap_read()
    assert result == payload


def test_sitemap_update_new_file(tmp_path):
    os.chdir(tmp_path)
    sitepath = "/mypage"
    module = "pages.mypage"
    title = "My Page"
    enerator.sitemap_update(sitepath, module, title)
    enerator.sitemap_read.cache_clear()
    result = enerator.sitemap_read()
    assert result[sitepath]["module"] == module
    assert result[sitepath]["title"] == title
