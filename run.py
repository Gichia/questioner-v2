''' Creates the base of the API'''
from app import create_app

CONFIG_NAME = 'development'
app = create_app(CONFIG_NAME)

if __name__ == "__main__":
    app.run(debug=True)
