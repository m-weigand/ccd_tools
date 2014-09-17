#!/usr/bin/python
import dd_single
from flask import Flask
app = Flask(__name__)


@app.route("/")
def hello():
    options = dd_single.get_cmd_parser()
    return_str = ''
    for i in options.option_list:
        return_str += '{0}<br />\n'.format(i)
    return return_str

if __name__ == "__main__":
    app.run()
