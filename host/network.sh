set -x

source ../common.sh

sudo ip route del $FLOATING_IP_SUBNET
sudo ip route add $FLOATING_IP_SUBNET via $OPENSTACK_MANAGER_IP
echo "Now the Route Table is:"
sudo ip route
