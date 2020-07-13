# PY HealthCheck

This code is useful to restart the dead services which can happen due to multitude of reasons. The code works well with systemd services(support for old will be added). More changes coming soon

## How to

1. add the entry for **check.py** in your crontab.
2. add the name of your services in **services.conf**
3. logs maintained in **/var/log/pyhealthcheck.log**

## Timeline

- [x] create basic service healthcheck
- [x] add start stop restart and status check
- [ ] auto installation script
- [ ] create a UI for more ease
- [ ] enable service checking for old systems(init.d)
