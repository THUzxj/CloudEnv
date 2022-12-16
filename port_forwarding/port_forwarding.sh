source ../common.sh
set -x

# OpenStack Horizon
ssh -L 8080:$OPENSTACK_MANAGER_IP:80 -L 30001:$K8S_MASTER_IP:30001  $SSH_SERVER
