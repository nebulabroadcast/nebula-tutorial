CasparCG playout
================

Controlling CasparCG from Docker
--------------------------------

Should your `play` service run in Docker and use `casparcg` engine,
you need to allow bi-directional communication between the service and the playout server.
CasparCG uses OSC protocol to provide information about the current state of playback.
When running in Docker, container has to expose an UDP port Caspar will connect to.

Let's assume there are two `play` services running in a container,
controlling two channels of the same CasparCG server.

Each channel must be configured with unique `controller_port` and `caspar_osc_port` values in the site template:

*settings/channels.py*

```python

from nebula.settings.models import PlayoutChannelSettings, AcceptModel

scheduler_accepts = AcceptModel(folders=[1, 2])
rundown_accepts = AcceptModel(folders=[1, 3, 4, 5, 6, 7, 8, 9, 10])

channel1 = PlayoutChannelSettings(
    id=1,
    name="Channel 1",
    fps=25.0,
    plugins=[],
    solvers=[],
    day_start=(7, 0),
    scheduler_accepts=scheduler_accepts,
    rundown_accepts=rundown_accepts,
    rundown_columns=[],
    send_action=2,
    engine="casparcg",
    allow_remote=False,
    controller_host="worker",
    controller_port=42101,
    playout_storage=3,
    playout_dir="media",
    playout_container="mxf",
    config={
        "caspar_host": "192.168.1.100",
        "caspar_port": 5250,
        "caspar_osc_port": 6251,
        "caspar_channel": 1,
        "caspar_feed_layer": 10,
    },
)

# Configure second channel similarly

CHANNELS = [channel1, channel2]
```

Then setup both controllers services to run on the `worker` host:

*settings/services.py*

```python

PLAY1 = "<settings><id_channel>1</id_channel></settings>"
PLAY2 = "<settings><id_channel>2</id_channel></settings>"

SERVICES = [
   # ...
   ServiceSettings(id=11, type="play", name="play2", host="worker", settings=PLAY1),  
   ServiceSettings(id=12, type="play", name="play2", host="worker", settings=PLAY2),
   # ...
]
```

And we create configuration files for both services:


In the `docker-compose.yml` we setup UDP port forwarding for both ports
we specified in the channels configuration to the host running the play services:

```yaml
ports:
  - "6251:6251/udp"
  - "6252:6252/udp"
```

And last, in the `casparcg.config` file, we enable sending OSC messages to the host.

```xml
<osc>
  <predefined-clients>
    <predefined-client>
      <address>IP_ADDRESS_OF_DOCKER_HOST</address>
      <port>6251</port>
    </predefined-client>
    <predefined-client>
      <address>IP_ADDRESS_OF_DOCKER_HOST</address>
      <port>6252</port>
    </predefined-client>
  </predefined-clients>
</osc>
```

Media
-----

Our best practice is to have `media.dir` directory
on the playout server data drive (e.g. `d:\media.dir` on Windows ), then we share the media drive,
so it's accesible as for example `\\playoutserver\playout`

In `casparcg.config` set the `<media-path>` to the local path to the directory.


Send to playout
---------------

In order to copy media files to the playout storage, create an action for each physical playout storage.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<settings>
    <allow_if>True</allow_if>
    <task mode="ffmpeg">
        <param name="filter:a">"loudnorm=I=-23"</param>
        <param name="ar">48000</param>
        <param name="c:v">"copy"</param>
        <param name="c:a">"pcm_s16le"</param>
        <output storage="asset.get_playout_storage(1)" direct="1"><![CDATA[asset.get_playout_path(1)]]></output>
    </task>
</settings>
```

PSM Service
-----------

PSM (Playout storage monitor) is a Nebula service which controls sending media filest to the playout
storage automatically based on the schedule. By default it start the job 24 hours before broadcast time.

Only one PSM instance is needed per installation as it handles all configured playout channels.
No further configuration of the service is required.

