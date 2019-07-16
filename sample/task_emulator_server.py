#
# Usage:
# $ make run           # for server process
# $ WORKER=1 make run  # for worker process
#

import os
import sys
import logging

from gumo.task_emulator import configure as task_emulator_configure
from gumo.task_emulator import task_emulator_app

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)


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
