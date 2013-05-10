import os, os.path, sys
import json
import subprocess
import select
from logging import Formatter

from flask import Flask, request, abort

app = Flask(__name__)

def spawn_dir(directory):
    '''fork-exec run-parts on directory'''
    pid = os.fork()
    if pid:
        return
    print 'DIR is', directory
    p = subprocess.Popen(["run-parts", directory],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    while True:
        reads = [p.stdout.fileno(), p.stderr.fileno()]
        ret = select.select(reads, [], [])
        for fd in ret[0]:
# TODO: add some extra fields to logger clarifying where it all came from)
            if fd == p.stdout.fileno():
                app.logger.debug(p.stdout.readline().strip(),
                        extra={'from':directory})
            elif fd == p.stderr.fileno():
                app.logger.info(p.stderr.readline().strip(),
                        extra={'from':directory})
        if p.poll() is not None:
            sys.exit(0)

@app.route('/hook/<repo>',methods=['POST'])
def hook(repo):
    #data = json.loads(request.data)
    #print data
    #print "New commit: {}".format(data['commits'][0]['id'])
    repodir = os.path.abspath(os.path.join(app.config['BASEDIR'], repo))
    if not os.path.exists(repodir):
        app.logger.info("uff, path %s does not exist" % repodir)
        abort(404)
    y
    app.logger.debug("yay! path %s exists. Now running run-parts" % repodir)
#FIXME: we should have a always-running job handler to call spawn_dir
    spawn_dir(repodir)

    return "OK"

if __name__ == '__main__':
    import logging
    #TODO: option for sysloghandler?
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    app.logger.addHandler(handler)
    app.config.from_object('default_config')
    if len(sys.argv) ==  2:
        app.config.from_pyfile(sys.argv[1])
    app.logger.setLevel(logging.DEBUG)
    app.run()

