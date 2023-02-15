Importing media
===============

Watchfolders
------------

The easiest way to import media files to nebula is to use watchfolders. 
That way, new assets are created automatically for each file uploaded to 
a defined directory. To use watchfolders, use a single instance of the `watch`
service. Service configuration may contain one or more watchfolders.

```xml
<service>
    <folder id_storage="1" path="media.dir/movies"/>
    <folder id_storage="2" path="media.dir/episodes"/>
</service>
```
Folder tag attributes:

- `id_storage` (required)
- `path` (required)
- `id_folder` (default 12 - Incoming)
- `recursive` (default True)
- `hidden` (default False) - Ignore dotfiles
- `quarantine_time` (default 10)
- `case_sensitive_exts` (default False)

It is also possible to execute a script to add/modify the metadata of the new asset:

```xml
<service>
  <folder id_storage="1" path="media.dir" recursive="1" id_folder="1">
    <post>
<![CDATA[
import shortuuid
asset["id/main"] = shortuuid.uuid()
]]>
    </post>
  </folder>
</service>
```

If you are using watchfolders, a media file (quite obviously) must exist prior to the creation of the asset.

Manual asset creation
---------------------

Nebula also supports the opposite method: Create an asset first using the web interface 
or Firefly and enforce the user to fill all required metadata before they are able to upload the file. 
This can be done using an asset validation plugin.

See `plugins/validator/asset.py` for an example.
