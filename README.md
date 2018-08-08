# powerline
Invoke system commands from web requests

## Install

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


### What does `setup.sh` do?
* Sets up a systemd unit file for powerline as `cuteworks-powerline.service` in `/etc/systemd/system/` referencing the `powerline.sh` script
  * If you ever move the directory you cloned powerline into, you'll want to run `setup.sh` again
* Enables the powerline service to start automatically and starts powerline for the first time

## Configure

- [ ] Todo

## Debug
powerline logs to the systemd journal. To view the log use `journalctl -u cuteworks-powerline`


## Todo
- [ ] Start service as a user other than root