# The Docker-Compose File Explained

A short overview over the docker compose file.

## The Services

The file 8 services, 7 are required while 1 is optional.
The `ui` and `backend` service are the QHAna UI and the QHAna backend respectively.
The UI is a web frontend written in Angular.
The backend stores all experiment data and is written in ballerina.
The plugins use 5 services in total in the default configuration.
The `qhana-plugin-runner` service serves the REST APIs of the plugins, while the worker perferms the background computation tasks.
`Redis` is used as the task queue service and data is stored in the `postgres` database.
Data is also stored in the `minio` instance per default (requires the minio plugin to be loaded).
The `muse-db` service is optional and provides the muse data in a live mysql database.

```{warning}
The services `qhana-plugin-runner` and `worker` must have the exact same configuration apart from the concurrency settings.
They must have the same plugins loaded, use the same task broker for the task queue and use the same database.
Because the default implementation assumes a shared file system between the worker and the plugin runner they also need to share a file system!
```


```yml
services:
  qhana-plugin-runner:
    platform: linux/amd64
    image: ghcr.io/ust-quantil/qhana-plugin-runner:main
    depends_on:
      - redis
      - postgres
  redis:
    image: "redis:latest"
  postgres:
    image: "postgres:latest"
  minio:
    image: quay.io/minio/minio 
  muse-db:
    image: "muse-db"
    profiles:
      - with_db
  worker:
    platform: linux/amd64
    image: ghcr.io/ust-quantil/qhana-plugin-runner:main
    depends_on:
      - qhana-plugin-runner
  backend:
    image: ghcr.io/ust-quantil/qhana-backend:main
  ui:
    image: ghcr.io/ust-quantil/qhana-ui:main
```


## Open Ports

```yml
services:
  qhana-plugin-runner:
    ports:
      - "5005:8080"
  redis:
    ports:
      - "6379:6379"
  postgres:
  minio:
    ports:
      - "9000:9000"
      - "9001:9001"
  muse-db:
  worker:
  backend:
    ports:
      - 9090:9090
  ui:
    ports:
      - 8080:8080
```

```{todo}
Expose redis port for other plugin runners started outside the docker compose.
```

The docker-compose file maps 4 ports to the outside.
The user interface is available at port `8080`.
This port can be changed to any other open port.
The QHAna UI expects the backend to answer at port 9090.
If the backend port is changed in the docker-compose file, then the port must be changed in the settings page of the QHAna UI for each client using the UI.
The plugin runner api service is exposed under port `5005` by default.
The addresses of all known plugin runners can be edited in the settings page of the QHAna UI.
This has to be done only once as the list is stored in the QHAna backend.
The exposed redis port is for debugging purposes.
Minio ports are exposed and can be used to inspect data in the minio store.
Other plugin runners can use the redis broker for their task queue only if they also use the same database and data store.
All other services are only available in the internal network created by docker-compose (using the service name as hostname).
They are used internally by the plugin runner.


## Settings

```yml
services:
  qhana-plugin-runner:
    environment:
      CONCURRENCY: 2
      BROKER_URL: redis://redis:6379
      RESULT_BACKEND: redis://redis:6379
      SQLALCHEMY_DATABASE_URI: "postgresql+psycopg2://user:password@postgres:5432/default_db"
      DEFAULT_FILE_STORE: "minio"
      MINIO_CLIENT: '{"endpoint": "minio:9000", "access_key": "QHANA", "secret_key": "QHANAQHANA", "secure": false}'
      URL_MAP: '{"(https?://)(localhost|host.docker.internal):9090": "\\1backend:9090"}'
      GIT_PLUGINS: "git+https://github.com/UST-QuAntiL/qhana-plugin-runner.git@main#subdirectory=/plugins"
  redis:
  postgres:
    environment:
      POSTGRES_PASSWORD: password
      POSTGRES_USER: user
      POSTGRES_DB: default_db
  minio:
    environment: 
      MINIO_ROOT_USER: QHANA
      MINIO_ROOT_PASSWORD: QHANAQHANA
  worker:
    environment:
      CONTAINER_MODE: worker
      CONCURRENCY: 2
      BROKER_URL: redis://redis:6379
      RESULT_BACKEND: redis://redis:6379
      SQLALCHEMY_DATABASE_URI: "postgresql+psycopg2://user:password@postgres:5432/default_db"
      DEFAULT_FILE_STORE: "minio"
      MINIO_CLIENT: '{"endpoint": "minio:9000", "access_key": "QHANA", "secret_key": "QHANAQHANA", "secure": false}'
      URL_MAP: '{"(https?://)(localhost|host.docker.internal):9090": "\\1backend:9090"}'
      GIT_PLUGINS: "git+https://github.com/UST-QuAntiL/qhana-plugin-runner.git@main#subdirectory=/plugins"
  backend:
    environment:
      QHANA_URL_MAPPING: '{"(?<=^|https?://)(localhost|host.docker.internal):5005": "qhana-plugin-runner:8080", "(?<=^|https?://)localhost(:[0-9]+)?": "host.docker.internal$$1"}'
```

The QHAna plugin runner and worker share mostly the same configuration.
The variables {envvar}`BROKER_URL`, {envvar}`RESULT_BACKEND`, {envvar}`SQLALCHEMY_DATABASE_URI`, and {envvar}`GIT_PLUGINS` **must** be configured to the same values!
The environent variable for {envvar}`CONCURRENCY` can have different values.
The worker container must have the environment variable {envvar}`CONTAINER_MODE` set to worker to start the image as a worker (since the exact same image as the plugin runner is used as API server and as worker).
The user and password set in the `redis` service must be used to construct the {envvar}`SQLALCHEMY_DATABASE_URI` (replace the existing `user:password` section with the changed user and password).
The variable `MINIO_CLIENT` is a json object that holds the client configuration used to access the minio server.
Because URLs from outside just point to the docker host (often "localhost") they must be mapped to the correct container.
This can be done with the `URL_MAP``variable which holds a JSON map.
The keys of this map are (python!) regex patterns that will get replaced with their replacement string.
The backend has a similar configuration `QHANA_URL_MAPPING` that uses java regex patterns and replacement!

The containers that use (or can use) a database are configured with a wait script.
See the console output of these containers for more information.


### Advanced Configuration

The plugin runner and worker and the QHAna backend can be configured by mapping a configuration file into the container.
The configuration file must be loaded under `/app/instance/config.[json|toml]` for the plugin runner and worker.
The backend expects the configuration under `/app/data/Config.toml` but all configurations can be set via env variables documented in the (README.md)[https://github.com/UST-QuAntiL/qhana-backend#configuration-handling].
For the information of what config options are available in the config files please refer to <https://github.com/UST-QuAntiL/qhana-plugin-runner> and <https://github.com/UST-QuAntiL/qhana-backend/blob/main/Config-template.toml>.


## Volumes

The docker compose file configures three volumes for persistent data storage.
The plugin runner and worker container share the same volume named `instance` that is used as a shared file system.
All data generated by the plugin runner is saved to that shared file system or the configured minio instance (which has its own volume).
To achieve true persistence the `redis` and `postgres` services need to be configured with volumes too (this is only needed for production setups).
Please refer to the image documentations on docker hub for how these volumes should be configured.

The volume named `experiments` is used by the QHAna backend to persist the backend data.
It contains all data stored for the experiments (as files in the file system) and an sqlite database.
The backend can also be configured to use a MariaDB database with the `Config.toml` file.

```yml
services:
  qhana-plugin-runner:
    volumes:
      - instance:/app/instance
  minio:
    volumes:
      - minio:/data
  worker:
    volumes:
      - instance:/app/instance
  backend:
    volumes:
      - experiments:/app/data
volumes:
  minio:
  instance:
  experiments:
```

```{hint}
As a basic security measure all QHAna containers run as an unpriviledged user.
This can lead to problems with mounting folders into the same space as the volumes.
This stack overflow question might be a good starting point for researching a solution: https://stackoverflow.com/questions/40462189/docker-compose-set-user-and-group-on-mounted-volume

The QHAna backend uses the user `ballerina` while the plugin runner containers use `gunicorn` as the username.
For completeness: the QHAna UI runs as the user `nginx`.
```

