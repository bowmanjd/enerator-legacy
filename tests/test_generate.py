"""Tests for enerator."""

import enerator.add
import enerator.commands
import enerator.generate


def test_generate_page(make_pages: dict) -> None:
    for module in make_pages:
        content = enerator.generate.generate_page(module, {})
        assert "Hello" in content


def test_generate_page_devmode(make_pages: dict) -> None:
    for module in make_pages:
        content = enerator.generate.generate_page(module, {"devmode": True})
        assert "Hello" in content
        pyfile = enerator.add.module_to_path(module) / "__init__.py"
        new_content = pyfile.read_text().replace("Hello", "Goodbye")
        pyfile.write_text(new_content)
        content = enerator.generate.generate_page(module, {"devmode": True})
        assert "Goodbye" in content


def test_routes(make_pages: dict) -> None:
    new_pages = {v: k for k, v in make_pages.items()}
    assert new_pages == enerator.generate.routes()
