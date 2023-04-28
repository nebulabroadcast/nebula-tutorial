Nebula Tutorial
===============

In this tutorial, we will guide you through the process of setting up Nebula 6 on your machine, step by step. 
By the end of this tutorial, you will have a fully functional Nebula instance up and running.

Keep in mind that Nebula 6 is still in beta, and it lacks some features that will be available in the final release.

Note: This tutorial is designed for Debian-based Linux distributions such as Ubuntu, 
and has been tested on Ubuntu. If you're using a different distribution, 
the steps may be slightly different. 

But don't worry, the basic idea should be the same and you should be able to figure it out.


What's included
---------------

At the end of this tutorial, your instance will:

 - Scan watchfolders for new files
 - Create assets in Nebula for each file
 - Exctract metadata from the files
 - Create low-res proxies for each video file
 - Spin up a Conti playout server for linear playout in HLS format

Install Docker
--------------

Install the required dependencies:

```bash
sudo apt-get update
sudo apt-get install -y curl git
```

Download and run the Docker installation script using curl:

```bash
curl -fsSL get.docker.com -o get-docker.sh
sh get-docker.sh
```

Add your user to the Docker group:

```bash
sudo usermod -aG docker $USER
```

Log out and log back in to apply the group change.
Verify that Docker is installed and running:

```bash
docker info
```

Clone this repository
---------------------

Clone a Git repository:
  
```bash
git clone https://github.com/nebulabroadcast/nebula-tutorial
```

Test run
--------

Now you can dry-test the setup by running the following command:

```bash
docker compose up
```

This will download all the required Docker images, setup the database and start the Nebula services.
You can now open your browser and go to http://localhost:4455 to see the Nebula web interface.

Default login credentials are:

 - Username: admin
 - Password: nebula

If you see the Nebula web interface, you're good to go! 
It is now a good idea to stop the services by pressing Ctrl+C in the terminal window and setup 
everything properly. But it is okay to continue with the default settings for now.

To learn more about configuration, scroll down to the "Configuration" section.


Managing the server
-------------------

You can use command line to perform various tasks on the server.
All scripts are bundled into a single Makefile, so you can run them like this:

```bash
make <command>
```

Following commands are available:

 - `make dbshell` - open a shell to the PostgreSQL database
 - `make setup` - apply settings from the `settings` directory.
 - `make reload` - reload the Nebula server (not the worker)
 - `make restart` - restart the Nebula server and worker
 - `make update` - Update the Nebula server and worker to the latest version
 - `make user` - Create a new user
 - `make password` - Change the password of an existing user


Default workflow
----------------

### Ingest

By default, assets are created using watchfolders. 
There is a watchfolder for each type of asset, which we call "Folders" in Nebula. 

Folders contain assets with similar characteristics, sharing the same metadata fields. 
For instance, there are folders for "Movies," "Episodes," "Songs," "Commercials," etc.

When you add a file to its corresponding watchfolder, Nebula automatically creates an asset for it. 
The process can be monitored in the console output.

Nebula waits for a while before turning the asset into a "ONLINE" state to ensure that the file is
fully written to disk. Meanwhile it extracts metadata from the file.  

### Proxies

As soon as the asset is created, Nebula starts creating low-res proxies for it.
The process can be monitored in the **jobs** page of the web interface.

When a proxy is created you can preview it in the web interface in **preview** page.

### Browsing assets

In **Editor** and **Preview** pages, left part of the screen shows the list of assets.
Basic filtering is done by selecting **View** from the top menu. 

Views by default vaguely resemble the folder structure, but they can be defined with more
specific criteria. For example **Main** view contains movies and serie episodes, which are
not trashed nor archived, **Fill** contains trailer, jingles and graphics, etc.

Additionally fulltext search is available in the search box in the top right corner of the browser.

### Metadata

In the **Editor** page, you can edit the metadata of the selected asset or create a new one (if enabled).

### Scheduling and playout

Linear playout scheduling and control is available only using Firefly application.
See [Nebula 5 documentation](https://nebulabroadcast.com/doc/nebula/) for more information.

Configuration
-------------

 - [CasparCG integration](https://github.com/nebulabroadcast/nebula-tutorial/blob/main/doc/casparcg.md)
