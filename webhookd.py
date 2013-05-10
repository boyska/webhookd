import os, os.path, sys
import json
from subprocess import Popen

from flask import Flask, request, abort

app = Flask(__name__)

@app.route('/hook/<repo>',methods=['POST'])
def hook(repo):
    #data = json.loads(request.data)
    #print data
    #print "New commit: {}".format(data['commits'][0]['id'])
    repodir = os.path.join(app.config['BASEDIR'], repo)
    if not os.path.exists(repodir):
        app.logger.info("uff, path %s does not exist" % repodir)
        abort(500)
    app.logger.debug("yay! path exists. Now running run-parts")
# FIXME: run-parts is killed when server is. Need to fork-exec
    Popen(["run-parts", repodir])
# TODO: handle run-parts output and redirect it to logger (with some extra
# fields clarifying where it all come from

    return "OK"

if __name__ == '__main__':
    import logging
    app.logger.addHandler(logging.StreamHandler(sys.stderr))
    #TODO: option for sysloghandler?
    app.config.from_object('default_config')
    if len(sys.argv) ==  2:
        app.config.from_pyfile(sys.argv[1])
    app.logger.setLevel(logging.DEBUG)
    app.run(debug=False)

