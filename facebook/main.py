from flask import Flask, request
from facebook import group_post
import optparse

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return '<h1>Works!</h1>'


@app.route('/grouppost', methods=['POST'])
def group_post_handler():
    request_body = request.get_json()
    print('RB:', request_body)
    group_id = request_body['groupids']
    message = request_body['message']
    status = group_post(message, group_id)
    return status


def flaskrun(app, default_host="127.0.0.1", default_port="5000"):
    """
    Takes a flask.Flask instance and runs it. Parses
    command-line flags to configure the app.
    """

    # Set up the command-line options
    parser = optparse.OptionParser()
    parser.add_option("-H", "--host",
                      help="Hostname of the Flask app " + \
                           "[default %s]" % default_host,
                      default=default_host)
    parser.add_option("-P", "--port",
                      help="Port for the Flask app " + \
                           "[default %s]" % default_port,
                      default=default_port)

    # Two options useful for debugging purposes, but
    # a bit dangerous so not exposed in the help message.
    parser.add_option("-d", "--debug",
                      action="store_true", dest="debug",
                      help=optparse.SUPPRESS_HELP)
    parser.add_option("-p", "--profile",
                      action="store_true", dest="profile",
                      help=optparse.SUPPRESS_HELP)

    options, _ = parser.parse_args()

    # If the user selects the profiling option, then we need
    # to do a little extra setup
    if options.profile:
        from werkzeug.contrib.profiler import ProfilerMiddleware

        app.config['PROFILE'] = True
        app.wsgi_app = ProfilerMiddleware(app.wsgi_app,
                                          restrictions=[30])
        options.debug = True

    app.run(
        debug=options.debug,
        host=options.host,
        port=int(options.port)
    )


if __name__ == '__main__':
    flaskrun(app)
