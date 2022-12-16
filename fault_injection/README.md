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
