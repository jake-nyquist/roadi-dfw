"""
This script runs the FlaskWebProject application using a development server.
"""

from os import environ
from FlaskWebProject import app

if __name__ == '__main__':
    try:
        PORT = int(environ.get('PORT', '5000'))
    except ValueError:
        PORT = 5000
    app.run(host='0.0.0.0', port=PORT)
