# mindustryd

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/72cadff98c534291947b1ad3c3c93496)](https://app.codacy.com/app/marcsello/mindustryd?utm_source=github.com&utm_medium=referral&utm_content=marcsello/mindustryd&utm_campaign=Badge_Grade_Dashboard)

Mindustry server daemonizer for systemd compatiblity

## What dis?
This is a replacement for 'screen' when you run a Mindustry server using systemd (or any other init system).

Mindustryd daemonizes the mindustry server by capturing and buffering it's output, and giving commands to it, when needed. It also allows the administrator to access the server any time with a simple console.

## Why dis?
I find it an ugly hack, to use screen with systemd, and I had weird issues with it.
Since google led me nowhere with this problem, I decided to write my own script for it.

## Features
- Service like start/stop/restart of a mindustry server. No more screens and tmuxes
- Easy to configure and run
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

#### Basic setup

First, clone the repo, and install mindustryd:
```bash
git clone https://github.com/marcsello/mindustryd.git
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
                "server_path" : "/opt/mindustry", // the path that contains your mindustry server
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
                        "-Xms4G",
                        "-Xmx6G"
                ],


                "shutdown_commands" : [ // commands to run, when the daemon is about to shutdown
                        "save-all",
                        "stop"
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

**If you are fine with the basic setup, you should change the** `"console_socket_path"` **entry in the above config to** `/tmp/mc.sock` **otherwise the daemon will fail to start, since we not created the default directory yet!**

#### Installing systemd service

Now we need an user, that runs the mindustry server, and a system group which members are allowed to attach to the the console.

```bash
sudo groupadd -r mindustry
sudo useradd -d "YOUR MINDUSTRY SERVER DIRECTORY" -M -r -s /bin/false -g mindustry mindustry
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

And then enable and start it:
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
