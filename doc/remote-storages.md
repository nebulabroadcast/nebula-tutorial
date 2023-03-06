Remote storages
===============

By default, nebula-example uses local storage on the server where it is installed (`storage` directory mounted directly to the docker container). 
However, you can also configure Nebula to use network storage for your media files. 

In this tutorial, we will show you how to set up and configure network storage for Nebula.

Prerequisites
-------------
Before you begin, you should have the following:

 - A network share that you want to use for Nebula storage
 - Access to the server where Nebula is installed
 - Basic knowledge of Docker and Docker Compose


Updating docker-compose
-----------------------

In the docker-compose.yml file, remove the volume definitions for both the backend and server services that point to the storages directory:

```yaml
services:
  backend:
    volumes:
      # Remove this line
      - ./storages:/mnt/nebula_01
      
  worker:
    volumes:
      # Remove this line
      - ./storages:/mnt/nebula_01
```

Docker containers must be privileged in order to be allowed to mount samba storages:
Add the following lines to their definition in the `docker-compose.yml`

```yaml
    cap_add:
        - SYS_ADMIN
        - DAC_READ_SEARCH
    privileged: true
```

Define a remote storage in Nebula
---------------------------------

In the settings directory of the Nebula repository, create a storages.py file with the following contents:

from nebula.settings.models import StorageSettings

```python
STORAGES = [
    StorageSettings(
        id=1,
        name="production",
        protocol="samba",
        path="//server/share",
        options={
            "login": "user",
            "password": "password",
        },
    )
]
```

Start the stack again with `docker compose up`
