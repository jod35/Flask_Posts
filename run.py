from api import create_app
import gunicorn


app = create_app()

    
if __name__ == "__main__":
    app.run(port=8000)