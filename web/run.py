from flask_failsafe import failsafe

@failsafe
def create_app():
    # note that the import is *inside* this function so that we can catch
    # errors that happen at import time
    from app import app
    return app

if __name__ == "__main__":
    create_app().run(host="0.0.0.0", port=8080, debug=True)