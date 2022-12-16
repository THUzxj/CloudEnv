pip install neutron-vpnaas

echo "[service_providers]
service_provider = VPN:strongswan:neutron_vpnaas.services.vpn.service_drivers.ipsec.IPsecVPNDriver:default" | sudo tee /etc/neutron/neutron_vpnaas.conf
echo "[AGENT]
extensions = vpnaas

[vpnagent]
vpn_device_driver = neutron_vpnaas.services.vpn.device_drivers.strongswan_ipsec.StrongSwanDriver" | sudo tee /etc/neutron/l3_agent.ini 

neutron-db-manage --subproject neutron-vpnaas upgrade head
