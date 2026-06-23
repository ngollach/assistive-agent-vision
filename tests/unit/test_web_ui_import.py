
def test_web_ui_module_imports():
    import app.web_ui

    assert app.web_ui.main is not None