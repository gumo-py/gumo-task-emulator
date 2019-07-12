import os
import sys
import logging

from gumo.core import configure as core_configure
from gumo.datastore import configure as datastore_configure
from gumo.task import configure as task_configure
from gumo.task_emulator import configure as task_emulator_configure
from gumo.task_emulator import task_emulator_app

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)


# Application framework initialization process.
core_configure()
datastore_configure()
task_configure()

task_emulator_configure(
    server_host=os.environ.get('SERVER_HOST'),
    server_port=os.environ.get('SERVER_PORT'),
)

app, worker = task_emulator_app()


if __name__ == '__main__':
    if os.environ.get('WORKER'):
        worker.start()
    else:
        server_port = os.environ.get('TASK_EMULATOR_PORT', '8083')
        app.run(host='0.0.0.0', port=server_port, debug=True)
