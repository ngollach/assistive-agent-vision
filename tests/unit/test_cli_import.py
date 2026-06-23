def test_cli_module_imports():
    import app.cli

    assert app.cli.main is not None