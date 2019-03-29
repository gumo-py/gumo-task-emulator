import os
import sys
import logging

from gumo.core import MockAppEngineEnvironment
from gumo.core import configure as core_configure
from gumo.datastore import configure as datastore_configure
from gumo.task import configure as task_configure
from gumo.task_emulator import configure as task_emulator_configure
from gumo.task_emulator import task_emulator_app

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)

if os.environ.get('GOOGLE_APPLICATION_CREDENTIALS') is None:
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/path/to/credential.json'

# Initialization process in development environment.
if __name__ == '__main__' or 'PYTEST' in os.environ:
    app_yaml_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'app.yaml'
    )
    MockAppEngineEnvironment.load_app_yaml(app_yaml_path=app_yaml_path)

# Application framework initialization process.
core_configure(
    google_cloud_project=os.environ.get('PROJECT_NAME'),
    google_cloud_location=os.environ.get('PROJECT_LOCATION'),
)
datastore_configure(
    use_local_emulator='DATASTORE_EMULATOR_HOST' in os.environ,
    emulator_host=os.environ.get('DATASTORE_EMULATOR_HOST'),
    namespace=os.environ.get('DATASTORE_NAMESPACE'),
)

task_configure(
    default_queue_name='gumo-default-queue',
    use_local_task_emulator=os.environ.get('USE_TASK_EMULATOR'),
)

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
