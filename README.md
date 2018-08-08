# powerline
*Invoke system commands from web requests.*

powerline is a web application that listens for HTTP requests and runs a corresponding script.

## Use Cases / Motivation
* **Respond to webhooks**: Plug in your powerline endpoint to GitHub's  [webhooks](https://developer.github.com/webhooks/) and automatically run `git pull` on your application server
  * *honestly, this is why I made powerline because all the existing continuous deployment solutions I found were ridiculously overcomplicated*
  * This use case is used as an example in the *Configuration* section below.
 
## Getting Started 

It's easy to get started with powerline. You'll need to install the application and then configure it. 

### Install

* Install system dependencies - below instructions for `dnf`, adapt as needed for your package manager

```
sudo dnf install systemd-devel
sudo dnf install python3
sudo dnf install python3-pip
```

*  Clone the project wherever you'd like, below example uses home directory

```
cd
git clone https://github.com/cuteworks/powerline.git
```

* Set up a Python virtual environment and install dependencies

```
cd ~/powerline
python3 -m virtualenv venv
source venv/bin/activate
pip3 install flask
pip3 install systemd
```

* Set application script executable and install systemd service

```
chmod +x powerline.sh setup.sh
sudo ./setup.sh
```


#### What does `setup.sh` do?
* Sets up a systemd unit file for powerline as `cuteworks-powerline.service` in `/etc/systemd/system/` referencing the `powerline.sh` script
  * If you ever move the directory you cloned powerline into, you'll want to run `setup.sh` again
* Enables the powerline service to start automatically and starts powerline for the first time
* Creates a user `cuteworks` to host the service


#### What's set up now?
At this point, the following is set up:
* System and Python dependencies have been installed
* The powerline application is installed in the directory it was cloned to
* A `cuteworks` user has been created (no login) which will run any commands invoked by powerline
* The `cuteworks-powerline` service is running and set to start automatically
* The service is ready to respond to HTTP requests on port 22026

At this point, check to make sure the service is running.

```
systemctl status cuteworks-powerline
```

The service should be "Active". If not, check the above steps again and make sure the installation directory and application script are accessible by the `cuteworks` user.

### Configure / How it Works

Actions for powerline are defined in *step* files. A step file maps HTTP endpoints to scripts. 
When powerline starts, it crawls everyone's home directory looking for files named `.cuteworks-powerline-steps`. 
Each of these step files is loaded into the configuration.

#### Anatomy of a Step File

Step files are formatted by specifying an endpoint name, followed by a script to run when that endpoint is hit. 
For example, the following step file listens for an HTTP request on `:22026/exampleupdate` and runs `/home/akersten/update-repos.sh`

```
exampleupdate:/home/akersten/update-repos.sh
```

You can add multiple endpoints to a step file. Each endpoint gets its own line.

```
exampleupdate:/home/akersten/update-repos.sh
reboot:/home/akersten/reboot-server.sh
```

After creating or changing any step files:
* Make sure they are readable by the `cuteworks` user (as well as directories in their path)
* Restart the powerline service to enumerate the step files and reload the endpoints

```
systemctl restart cuteworks-powerline
```

If multiple step files define the same endpoint, powerline will use the first one it found.

### Debug
powerline logs to the systemd journal. To view the log use `journalctl -u cuteworks-powerline`


## Contributors

### Alex Kersten ([@akersten](https://github.com/akersten))
*professional critic*


![Avatar](web/static/img/ak-t.png)
