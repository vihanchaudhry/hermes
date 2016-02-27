from flask import Flask
from flask import request
from mako.template import Template
import mako.runtime
from utils import lyft

mako.runtime.UNDEFINED = ''

app = Flask(__name__, static_url_path='')

@app.route('/')
def hello_world():
    template = Template(filename='templates/index.html')
    parameters = {
        'authorization_url': lyft.generate_authorization_url().url
    }
    return template.render(**parameters)


@app.route('/success/')
def auth_success():
    template = Template(filename='templates/index.html')
    user_token = lyft.get_user_token(request.args['code'])
    print user_token.json()
    return template.render()
