def test_live_assist_server_imports():
    # pyrefly: ignore [missing-import]
    import app.live_assist.server

    assert app.live_assist.server.app is not None