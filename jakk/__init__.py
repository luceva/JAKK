from flask import Flask

from jakk.views import main
import os.path

app = Flask(__name__)
app.config['BASE_DIR'] = os.path.dirname(os.path.abspath(__file__))
app.config['DB_PATH'] = os.path.join(app.config['BASE_DIR'], 'students_v1.db')
app.register_blueprint(main, url_prefix='/')

