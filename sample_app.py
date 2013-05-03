from flask import Flask
from switchboard import Switchboard, Workflow

app = Flask(__name__)


class TestWorkflow(Workflow):
    pid, form, status = 17921, 'demographics', 2

    def execute(self, trigger):
        print "ah ha"


app.config['SWITCHBOARD_WORKFLOWS'] = [TestWorkflow()]
Switchboard(app)


@app.route('/', methods=['GET'])
def index():
    return "Hello World", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
