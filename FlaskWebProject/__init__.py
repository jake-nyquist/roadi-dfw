"""
The flask application package.
"""

from flask import Flask
app = Flask(__name__)

print "Hello. Importing"
import FlaskWebProject.views
print "Imported"

