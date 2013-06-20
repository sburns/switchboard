Switchboard
===

`switchboard` is a generic middlware add-on for Flask web apps designed to handle REDCap Data Entry Triggers.

About
---

A new [REDCap][rc] feature, the Data Entry Trigger, opens up to ability to automate many workflows/processes/etc related to REDCap data capture. In a nutshell, you can associate a URL (most likely on your webserver) to a project that REDCap will send an HTTP POST request to with specific parameters whenever a particular form is saved within that project.

Because a project can only be associated to one URL, we need a simple web application to parse incoming requests and execute particular functions. Such middleware should filter the incoming REDCap triggers and execute specific functions based on the incoming POST data. Then, you can just use one URL to accept requests from all your projects.

Installation and Setup
---

First:

```console
$ git clone git://github.com/sburns/switchboard.git switchboard
```

The repository comes with a `sample_app.py` that looks like this:

```python
from flask import Flask
from switchboard import Switchboard, Workflow

app = Flask(__name__)


class TestWorkflow(Workflow):
    pid, status, form = 1, [1, 2], ['demographics', 'imaging']

    def execute(self, trigger):
        print "Bingo"

app.config['SWITCHBOARD_WORKFLOWS'] = [TestWorkflow()]
Switchboard(app)


@app.route('/', methods=['GET'])
def index():
    return "Hello World", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
```

(Obviously, you should have [Flask][flask] installed in your python environment)

Running this from the terminal (`$ python sample_app.py`) will start up a very basic Flask app at `http://0.0.0.0:5000` that will respond on the `/trigger/` URL (note the trailing slash) to POSTs. The external-facing URL should be set in your REDCap project's Data Entry Trigger URL. Once this is set, "Bingo" will be printed to the screen everytime the `demographics` or `imaging` forms are saved as `Unverified` or `Complete` (assuming the project ID of your REDCap project is 1).

To change the URL the app will respond to by doing:

```python
Switchboard(app, url_prefix='/whatever-you-would-like')
```

The `url_prefix` *should not* have a trailing slash in it.

In production use, you'll want to deploy your Flask app to run within a better webserver than what's shipped with Flask. [This page in the Flask docs](http://flask.pocoo.org/docs/deploying/mod_wsgi/) is a good start for deploying Flask apps in Apache using `mod_wsgi`.


Filtering and Customization
---

To hook in your own workflows, `app.config['SWITCHBOARD_WORKFLOWS']` should be set to a list of instantiated objects (all whom inherit from `switchboard.Workflow`). These classes should contain at least one of the following class attributes:

- `pid`: The Project ID for your project. This can be a string, integer, or list of integers (if you'd like to run a certain function for multiple projects, for example).
- `form`: The Instrument to which you'd like to trigger functions based off. Should be a string or list of strings.
- `status`: This ties in to the form complete dropdown. Should be 0 (Incomplete), 1 (Unverified), or 2 (Complete) or a list with any of those choices.
- `dag`: Data Access Group. Should be a string or list of strings.
- `event`: For longitudinal projects, the unique event name will be here and can be used to filter.
- `record`: If you'd like to run a function against a single record in the project, you can specify it here (or a list of records).

Not specifying any of the above attributes is considered to be a wildcard, i.e. not specifying `form` will lead to a match on all form saves from the REDCap project.

When a request comes through that matches a particular workflow, that object's `execute` method will be called and passed a `trigger` argument which is a dictionary containing the above keys and the specific value from the request.

Bugs, Ideas, etc.
---

`switchboard` is still very much in development and the API may change.

This was developed with some specific workflows in mind and if for some reason it's not flexible enough for your setup, please open an issue and we can discuss what you'd like to be able to do.


[rc]: http://project-redcap.org
[flask]: http://flask.pocoo.org/