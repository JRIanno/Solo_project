from flask_app import app
from flask_app.controllers import index, roasts

if __name__ == '__main__':
    app.run(debug=True)