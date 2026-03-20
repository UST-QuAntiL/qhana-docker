# QHAna Architecture

```text
 ┌───────────────────────┐                      ┌───────────────────────────┐   
 │       QHAna UI        │                      │      Plugin Registry      │   
 │                       │─────────────────────>│                           │──┐
 │                       │                      │                           │  │
 │╭──iFrame─────────────╮│                      │                           │  │
 ││┌╶╶╶╶╶╶╶╶╶╶╶╶╶╶╶╶╶╶╶┐││                      └───────────────────────────┘  │
 ││╎                   ╎││                                                     │
 ││╎                   ╎││                                                     │
 ││╎                   ╎││                      ┏━━━━━━━━━━━━━━┳━━━━━━━━━━━━┓  │
 ││╎  Plugin A Micro-  ╎││─────────────────────>┃Micro-Frontend┃  Plugin A  ┃<─┤
 ││╎  Frontend         ╎││─────────────┐        ┠╌╌╌╌╌╌╌╌╌╌╌╌╌╌╄━━━━━━━━━━━━┫  │
 ││╎                   ╎││───────────┐ │        ┃Plugin API    ╎ Algorithm  ┃  │
 ││╎                   ╎││─────────┐ │ │        ┗━━━━━━━━━━━━━━┷━━━━━━━━━━━━┛  │
 ││╎                   ╎││         │ │ │        ┏━━━━━━━━━━━━━━┳━━━━━━━━━━━━┓  │
 ││└╶╶╶╶╶╶╶╶╶╶╶╶╶╶╶╶╶╶╶┘││         │ │ └───────>┃Micro-Frontend┃  Plugin B  ┃<─┤
 │╰─────────────────────╯│──┐      │ │          ┠╌╌╌╌╌╌╌╌╌╌╌╌╌╌╄━━━━━━━━━━━━┫  │
 └───────────────────────┘  │      │ │          ┃Plugin API    ╎ Algorithm  ┃  │
 ┌───────────────────────┐  │      │ │          ┗━━━━━━━━━━━━━━┷━━━━━━━━━━━━┛  │
 │     QHAna Backend     │  │      │ │          ┏━━━━━━━━━━━━━━┳━━━━━━━━━━━━┓  │
 │                       │  │      │ └─────────>┃Micro-Frontend┃  Plugin C  ┃<─┤
 │ ╭────────╮ ╭────────╮ │  │      │            ┠╌╌╌╌╌╌╌╌╌╌╌╌╌╌╄━━━━━━━━━━━━┫  │
 │ │        │ │        │ │<─┘      │            ┃Plugin API    ╎ Algorithm  ┃  │
 │ │        │ │        │ │         │            ┗━━━━━━━━━━━━━━┷━━━━━━━━━━━━┛  │
 │ │Database│ │  API   │ │         │            ┏━━━━━━━━━━━━━━┳━━━━━━━━━━━━┓  │
 │ │        │ │        │ │         └───────────>┃Micro-Frontend┃  Plugin D  ┃<─┘
 │ │        │ │        │ │                      ┠╌╌╌╌╌╌╌╌╌╌╌╌╌╌╄━━━━━━━━━━━━┫   
 │ ╰────────╯ ╰────────╯ │╶╶╶╶╶╶╶╶╶╶╶╶╶╶╶╶╶╶╶╶╶>┃Plugin API    ╎ Algorithm  ┃   
 └───────────────────────┘                      ┗━━━━━━━━━━━━━━┷━━━━━━━━━━━━┛   
```

The figure above depicts the idealized QHAna architecture.
This idealized version is true to the actual implementation, but hides a few details that have a huge impact on how plugins are developed and deploymed.
For example, the docker compose topology described in {doc}`docker-compose` does not match this idealized architecture 1-to-1.

The **QHAna UI** is the main user interface of the application.
It is implemented as an Angular single page application.

The **QHAna Backend** is responsible for storing the experiment state and data for the QHAna UI.
It implements a REST API and uses a database for persistent storage.
Once a plugin execution was started in the QHAna UI, the backend is informed and monitors the plugin execution.
The plugin results are stored in persistent storage for the QHAna UI to access at any time.
The backend is implemented in Ballerina.

The **Plugin Registry** collects and maintains information about the available plugins.
It provides a REST API to query the available plugins.
The registry is implemented using Python and the Flask framework.

The **Plugins** are microservices that follow specific conventions for their REST API and that provide a Micro-Frontend.
This Micro-Frontend can be loaded by the QHAna UI (and other applications).
It contains the controls for that plugin and allows users to interact with the plugin through a graphical interface, rather than directly calling the API.
Plugins are independent services and can have their own data storage and other infrastructure.
Plugins can interact with other plugins by calling their API or embedding their Micro-Frontend in their own.
They can discover the available plugins through the Plugin Registry.

The components can be found in their respective repository:

| Component        | Repository                                             |
|:-----------------|:-------------------------------------------------------|
| QHAna UI         | <https://github.com/UST-QuAntiL/qhana-ui>              |
| QHAna Backend    | <https://github.com/UST-QuAntiL/qhana-backend>         |
| Plugin Registry  | <https://github.com/UST-QuAntiL/qhana-plugin-registry> |
| Plugins          | <https://github.com/UST-QuAntiL/qhana-plugin-runner>   |



## Architecture Implementation

The idealized architecture above does not provide the full picture of the architecture as it is implemented.
This section discusses the omitted details.


### Plugins

Deploying dozens of plugins individually can quickly become a maintenance problem.
Therefore, all python plugins are developed and deployed using the **Plugin Runner**.
It provides a framework to develop QHAna plugins based on Flask, Celery and Python.
The runner can load the individual QHAna plugins using a plugin like mechanism itself.
It provides a basic API to list all loaded plugins into which the individual plugin APIs are integrated.
It also provides the plugins with utility functions and a persistence layer, e.g., for loading and storing data.
For long running computations, which is the expected case for QHAna plugins, it configures background task execution via Celery.

```text
┌─────────────────────────────────┐
│          Plugin Runner          │
│  ╭───────────╮  ╭────────────╮  │
│  │  Base     │  │  Plugin    │  │
│  │  API      │  │  Utils     │  │
│  ╰───────────╯  ╰────────────╯  │
│                                 │
│  ┏━━━━━━━━━━━━━━┳━━━━━━━━━━━━┓  │
│  ┃Micro-Frontend┃  Plugin A  ┃  │
│  ┠╌╌╌╌╌╌╌╌╌╌╌╌╌╌╄━━━━━━━━━━━━┫  │
│  ┃Plugin API    ╎ Algorithm  ┃  │
│  ┗━━━━━━━━━━━━━━┷━━━━━━━━━━━━┛  │
│  ┏━━━━━━━━━━━━━━┳━━━━━━━━━━━━┓  │
│  ┃Micro-Frontend┃  Plugin B  ┃  │
│  ┠╌╌╌╌╌╌╌╌╌╌╌╌╌╌╄━━━━━━━━━━━━┫  │
│  ┃Plugin API    ╎ Algorithm  ┃  │
│  ┗━━━━━━━━━━━━━━┷━━━━━━━━━━━━┛  │
│  ┏━━━━━━━━━━━━━━┳━━━━━━━━━━━━┓  │
└─────────────────────────────────┘
```

Using the Plugin Runner, all plugins can be deployed in a single* container.
This assumes, that the dependencies of the plugins do not have any conflicts.
If plugins with dependency conflicts must be deployed, then they must use different plugin runner instances.

*single = two, as at least one additional instance of the plugin runner must be used as a Celery worker to actually execute the background tasks.


### Plugin Registry

The plugin registry is first and foremost actually a plugin registry.
However, it has gained some additional functionalities as well.

 *  **Plugin discovery:**

    The Plugin Registry can automatically discover all plugins of a Plugin Runner instance.
    The URL to that instance must be added as a seed for discovery to work.
    To add individual plugins, their API URL can also be added as a seed, after which the plugin registry will regularly check them.
 *  **Plugin recommendations:**

    The Plugin Registry can recommend plugins given context clues, e.g., the last executed plugin.
    The recommendations mostly rely on the plugin metadata.
 *  **Configuration storage:**

    The Plugin Registry provides a configuration storage modeled after environment variables.
 *  **Service registry:**

    The Plugin Registry provides endpoints to manually register services that are not QHAna Plugins.
    For example, the QHAna Backend isautomatically registered by the docker compose configuration.
    Together with the configuration storage, this allows the QHAna UI to discover Plugins, services and configuration from a single source, the Plugin Registry.
 *  **UI Templates:**

    The plugin registry allows defining so called UI-Templates.
    These templates describe which plugins should be displayed where in the QHAna UI.
    The templates allow dynamically reconfiguring the QHAna UI based on current needs.
    This functionality is implemented in the Plugin Registry, since this allows the registry to automatically update the plugins matching the filters in the templates when changes are detected in the templates or the available plugins.

Additionally, the plugin registry also uses a second instance as a Celery worker for background tasks.


### Full Architecture

The final architecture looks closer to this:

```text
 ┌───────────────────────┐                     ┌───────────────────────────┐    
 │       QHAna UI        │                     │      Plugin Registry      │┐   
 │                       │────────────────────>│                           ││   
 │                       │                     │                           ││   
 │╭──iFrame─────────────╮│            ┌────────│                           ││   
 ││┌╶╶╶╶╶╶╶╶╶╶╶╶╶╶╶╶╶╶╶┐││            │        └───────────────────────────┘│   
 ││╎                   ╎││            │         └───────────────────────────┘   
 ││╎                   ╎││            │                                         
 ││╎                   ╎││            │                                         
 ││╎  Plugin A Micro-  ╎││            │  ┌─────────────────────────────────┐    
 ││╎  Frontend         ╎││───────┐    │  │          Plugin Runner          │┐   
 ││╎                   ╎││       │    │  │  ╭───────────╮  ╭────────────╮  ││   
 ││╎                   ╎││       │    └─>│  │  Base     │  │  Plugin    │  ││   
 ││╎                   ╎││       │       │  │  API      │  │  Utils     │  ││   
 ││└╶╶╶╶╶╶╶╶╶╶╶╶╶╶╶╶╶╶╶┘││       │       │  ╰───────────╯  ╰────────────╯  ││   
 │╰─────────────────────╯│──┐    │       │                                 ││   
 └───────────────────────┘  │    │       │  ┏━━━━━━━━━━━━━━┳━━━━━━━━━━━━┓  ││   
 ┌───────────────────────┐  │    └──────>│  ┃Micro-Frontend┃  Plugin A  ┃  ││   
 │     QHAna Backend     │  │            │  ┠╌╌╌╌╌╌╌╌╌╌╌╌╌╌╄━━━━━━━━━━━━┫  ││   
 │                       │  │            │  ┃Plugin API    ╎ Algorithm  ┃  ││   
 │ ╭────────╮ ╭────────╮ │  │            │  ┗━━━━━━━━━━━━━━┷━━━━━━━━━━━━┛  ││   
 │ │        │ │        │ │<─┘            │  ┏━━━━━━━━━━━━━━┳━━━━━━━━━━━━┓  ││   
 │ │        │ │        │ │               │  ┃Micro-Frontend┃  Plugin B  ┃  ││   
 │ │Database│ │  API   │ │               │  ┠╌╌╌╌╌╌╌╌╌╌╌╌╌╌╄━━━━━━━━━━━━┫  ││   
 │ │        │ │        │ │╶╶╶╶╶╶╶╶╶╶╶╶╶╶>│  ┃Plugin API    ╎ Algorithm  ┃  ││   
 │ │        │ │        │ │               │  ┗━━━━━━━━━━━━━━┷━━━━━━━━━━━━┛  ││   
 │ ╰────────╯ ╰────────╯ │               │  ┏━━━━━━━━━━━━━━┳━━━━━━━━━━━━┓  ││   
 └───────────────────────┘               └─────────────────────────────────┘│   
                                          └─────────────────────────────────┘   
```

Both, the Plugin Runner, and the Plugin Registry have a second instance running as a worker.
The infrastructure services, e.g., databases, S3 like blob storage, message queues for background tasks, etc., were omitted from this architecture for clarity.
