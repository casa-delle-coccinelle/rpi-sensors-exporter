### Overview
During development, I've used two Raspberry Pi Zero W boards, named dev0 and dev1, connected to my home network and Prometheus stack installed in Kubernetes cluster in the same network.
![overview](./images/schematics/overview.png)

### dev0
* dev0 schematics:

![dev0](./images/schematics/dev0.png)

* dev0 wiring:

![dev0](./images/pictures/dev0_1.JPG)
![dev0](./images/pictures/dev0_2.JPG)
![dev0](./images/pictures/dev0_3.JPG)
![dev0](./images/pictures/dev0_4.JPG)
![dev0](./images/pictures/dev0_5.JPG)

* [dev0 sample logs](./logs/dev0.log)

### dev1
* dev1 schematics:

![dev1](./images/schematics/dev1.png)

* dev1 wiring:

![dev1](./images/pictures/dev1_1.JPG)
![dev1](./images/pictures/dev1_2.JPG)
![dev1](./images/pictures/dev1_3.JPG)
![dev1](./images/pictures/dev1_4.JPG)
![dev1](./images/pictures/dev1_5.JPG)
![dev1](./images/pictures/dev1_6.JPG)

* [dev1 sample logs](./logs/dev1.log)


### Prometheus k8s operator configuration
dev0:
* [endpoint](./config/dev0-endpoints.yaml)
* [service](./config/dev0-service.yaml)
* [serviceMonitor](./config/dev0-serviceMonitor.yaml)

dev1:
* [endpoint](./config/dev1-endpoints.yaml)
* [service](./config/dev1-service.yaml)
* [serviceMonitor](./config/dev1-serviceMonitor.yaml)

### Grafana Dashboard
[Sample Grafana dashboard](./config/grafana_dashboard.json)

![grafana](./images/screenshots/dashboard_screenshot_1.png)
![grafana](./images/screenshots/dashboard_screenshot_2.png)
![grafana](./images/screenshots/dashboard_screenshot_3.png)
![grafana](./images/screenshots/dashboard_screenshot_4.png)
![grafana](./images/screenshots/dashboard_screenshot_5.png)
![grafana](./images/screenshots/dashboard_screenshot_6.png)
![grafana](./images/screenshots/dashboard_screenshot_7.png)
![grafana](./images/screenshots/dashboard_screenshot_8.png)
![grafana](./images/screenshots/dashboard_screenshot_9.png) ![grafana](./images/screenshots/dashboard_screenshot_10.png) ![grafana](./images/screenshots/dashboard_screenshot_11.png)

