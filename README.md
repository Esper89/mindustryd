# mindustryd

***Note:*** _This repository is a fork of [marcsello/minecraftd](https://github.com/marcsello/minecraftd)._

Mindustry server daemonizer for systemd compatiblity

## What dis?
This is a replacement for 'screen' when you run a Mindustry server using systemd (or any other init system).

Mindustryd daemonizes the mindustry server by capturing and buffering it's output, and giving commands to it, when needed. It also allows the administrator to access the server any time with a simple console.

## Why dis?
I find it an ugly hack, to use screen with systemd, and I had weird issues with it.
Since google led me nowhere with this problem, I decided to write my own script for it.

## Features
- Service like start/stop/restart of a mindustry server. No more screens and tmuxes
- Automatic startup and shutdown commands
- Attachable/detachable console with unix permissions
- Compatible with any flavour of mindustry server, or init system (example for systemd provided)

## Usage

### How to install & setup

#### Prerequirements
Git, python3, and pip3 are required by this software, so we install those first:

##### Debian
```bash
sudo apt install git python3 python3-pip
```

You'll also need java to run the mindustry server, but I assume you solved this already :)

#### Install mindustry server

You can follow the [guide on the mindustry wiki](https://mindustrygame.github.io/wiki/servers/) for downloading the mindustry server.

Once downloaded, create the server directory and move the `server.jar` to it:
```bash
sudo mkdir -p /srv/mindustry
sudo mv server.jar /srv/mindustry
```

#### Basic setup

First, clone the repo, and install mindustryd:
```bash
git clone https://github.com/Esper89/mindustryd.git
cd mindustryd
sudo ./install.sh
```

Next you should copy the example configuration file to it's place:  
(in the folder you cloned the repo)
```bash
sudo cp mindustryd.json.example /etc/mindustryd.json
```

After that you should edit the config file:
```bash
sudo nano /etc/mindustryd.json
```
```json5
{

        "server": { // configurations related to your server
                "server_path" : "/srv/mindustry", // the path that contains your mindustry server
                "server_jar" : "server.jar", // the name of your server's jar file
                "java" : "java", // the command which launches java (usually java)

                "jvm_arguments" : [ // additional arguments to the JVM, only one argument per entry
                        "-XX:+UnlockExperimentalVMOptions",
                        "-XX:+UseG1GC",
                        "-XX:G1NewSizePercent=20",
                        "-XX:G1ReservePercent=20",
                        "-XX:MaxGCPauseMillis=50",
                        "-XX:G1HeapRegionSize=16M",
                        "-server",
                        "-Xms1G",
                        "-Xmx2G"
                ],
                
                "startup_commands" : [ // commands to run, when the daemon is started up
                        "load world"
                ],


                "shutdown_commands" : [ // commands to run, when the daemon is about to shutdown
                        "save world",
                        "stop",
                        "exit"
                ]

        },

        "mindustryd": { // configurations related to mindustryd behaviour
		"logfile" : false, // Redirect logging from stderr to a file (won't ever needed probably)
                "console_socket_path" : "/var/lib/mindustryd/control.sock", // where to place the socket file that is used by the attachable console
                "history_length" : 10, // last n lines to transmit when a new client is connected (use false or null to disable)
                "log_level" : "INFO" // ... the log level
        }

}
```
**You are done with the basic configuration of mindustryd**  
But you need to add it to your init system

**If you are fine with the basic setup, you should change the** `"console_socket_path"` **entry in the above config to** `/tmp/md.sock` **otherwise the daemon will fail to start, since we not created the default directory yet!**

#### Installing systemd service

Now we need an user, that runs the mindustry server, and a system group which members are allowed to attach to the the console.

```bash
sudo groupadd -r mindustry
sudo useradd -d "/srv/mindustry" -M -r -g mindustry mindustry
```

Set this user as the owner of the server directory:

```bash
sudo chown -R mindustry:mindustry /srv/mindustry
```

After that we should create the directory for the daemon's socket. (see the config above)
We will give write permissions to the daemon user, and read permissions to it's group (so that anyone in the group can access to the socket):

```bash
sudo mkdir /var/lib/mindustryd
sudo chown mindustry:mindustry /var/lib/mindustryd
sudo chmod 750 /var/lib/mindustryd
```

Copy the systemd unit file to it's place:  
(in the folder you cloned the repo)
```bash
sudo cp mindustryd.service.example /etc/systemd/system/mindustryd.service
```

#### Set up the mindustry world

Run the mindustry server as the right user:
```bash
sudo su mindustry
cd ~
java -jar server.jar
```

Change the server config or rules, if you would like to.
Then, create and save the world:
```
host MAPNAME MODE
save world
exit
```

#### Start the daemon

Exit the mindustry user with `exit` if you haven't already, then enable and start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable mindustryd
sudo systemctl start mindustryd
```

#### Give permission to connect the server console

Add yourself to the mindustry group, so that you can use the console:
```bash
sudo usermod -a -G mindustry $USER
```
After that log out, and log back in.

**And you are done! Enjoy your mindustry server!**

### How to use
When the mindustryd is running (and you have permission to access the console), you can access the console with the following command:
```bash
mindustryd
```

You can stop or restart the mindustry server with systemctl from now on:
```bash
sudo systemctl stop mindustryd
sudo systemctl restart mindustryd
```
