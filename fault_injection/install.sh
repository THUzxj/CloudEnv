source ../common.sh

git clone https://ghproxy.com/https://github.com/dessertlab/thorfi

sudo apt install python python-dev
pip install virtualenv
virtualenv fi_env --python=python2.7
cd fi_env
source ./bin/activate

cd ../thorfi
pip2 install -r ./requirements.txt
pip2 install decorator==4.4.1 pyrsistent==0.14.0 python-keystoneclient python-novaclient python-neutronclient python-glanceclient python-heatclient pyinstaller==3.4
make

export OS_USER_DOMAIN_NAME=default
export OS_PROJECT_DOMAIN_NAME=demo

python thorfi_frontend_agent.py -i controller.example -p 7777 -a http://controller.example/identity/v3

python thorfi_client.py -i controller.example -p 7777 -a http://controller.example/identity/v3 -pi admin -d tenant -rt router -ri be88692c-d532-4e49-92eb-a948064d0a23 -f loss -fa '75%'
python thorfi_client.py -i 127.0.0.1 -p 7777 -a http://127.0.0.1/identity/v3 -pi 6fc32712b163426eba9afba2a01fb76b -d tenant -rt router -ri 47572616-bb60-420d-935a-a9050cbf2b33 -f loss -fa "75%"

python thorfi_client.py -i $OPENSTACK_MANAGER_IP -p 7777 -a http://$OPENSTACK_MANAGER_IP/identity/v3 -pi 6fc32712b163426eba9afba2a01fb76b -d tenant -rt floatingip -ri $K8S_MASTER_IP  -f loss -fa "75%" -itime 60