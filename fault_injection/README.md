# Fault Injection

(ThorFI)[https://github.com/dessertlab/thorfi]

# Faults

```bash
python thorfi_frontend_agent.py -i $OPENSTACK_MANAGER_IP -p 7777 -a http://$OPENSTACK_MANAGER_IP/identity/v3

openstack image create --disk-format qcow2 --container-format bare --public --file thorfi_image.qcow2 thorfi_image

python thorfi_client.py -i $OPENSTACK_MANAGER_IP -p 7777 -a http://$OPENSTACK_MANAGER_IP/identity/v3 -pi 6fc32712b163426eba9afba2a01fb76b -d tenant -rt router -ri 47572616-bb60-420d-935a-a9050cbf2b33 -f loss -fa "75%"
```

# Network Fault Injection with OVN

## OVN

# Load Test

[load-test](https://github.com/microservices-demo/load-test)

# Target Error Model

- Virtual network components' performance problem
- Virtual network components' misconfiguration 


```bash
sudo tc qdisc add dev br-ex root netem loss 20% delay 300ms
sudo tc qdisc del dev br-ex root netem

sudo tc qdisc add dev tap81a0af59-a6 root netem loss 20% delay 300ms # 10.0.0.10
sudo tc qdisc del dev tap81a0af59-a6 root netem

# misconfiguration
loss 100%
openstack router # delete
openstack security group

```

# Data Collection

```
locust -f locustfile.py --headless -u 500 -r 10 -H http://172.24.4.150:30001
```
