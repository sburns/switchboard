from flask import Flask
from switchboard import Switchboard

app = Flask(__name__)


def echo(**kwargs):
    print '\t'.join(['%s:%s' % (k, kwargs[k]) for k in sorted(kwargs.keys())])


receivers = [{'pid': 17921,
              'status': [1, 2],
              'form': ['demographics', 'imaging'],
              'func': echo},
            ]
app.config['SWITCHBOARD'] = receivers
Switchboard(app)


@app.route('/', methods=['GET'])
def index():
    return "Hello World", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
