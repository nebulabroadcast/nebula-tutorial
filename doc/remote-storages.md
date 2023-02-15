Remote storages
===============


Docker
------

Docker containers must be privileged in order to be allowed to mount samba storages:
Add the following lines to their definition in the `docker-compose.yml`

```yaml
    cap_add:
        - SYS_ADMIN
        - DAC_READ_SEARCH
    privileged: true
```
