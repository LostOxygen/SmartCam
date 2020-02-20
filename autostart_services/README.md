## Autostart Services for SmartCam Project

place service scripts in
```shell
/lib/systemd/system
```
and start/stop them with:
```shell
sudo systemctl enable|start|stop <name>.service
```
make sure you first enable the services!
