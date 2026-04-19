# MikroTik Router Configuration Script
# Based on MTCNA Certification
# Author: Salman Alhidamkara

# Reset configuration to default
/system reset-configuration

# Set identity router
/system identity set name="Router-Office"

# Set interface names
/interface ethernet
set [find] name="ether1-wan"
set [find default-name=ether2] name="ether2-lan"
set [find default-name=ether3] name="ether3-lan2"
set [find default-name=ether4] name="ether4-lan3"

# Set WAN IP (DHCP client)
/ip dhcp-client
add interface=ether1-wan disabled=no

# Set LAN IP address
/ip address
add address=192.168.1.1/24 interface=ether2-lan
add address=192.168.2.1/24 interface=ether3-lan2
add address=192.168.3.1/24 interface=ether4-lan3

# Setup DHCP Server for LAN
/ip pool
add name=dhcp-pool-1 ranges=192.168.1.10-192.168.1.200
add name=dhcp-pool-2 ranges=192.168.2.10-192.168.2.200
add name=dhcp-pool-3 ranges=192.168.3.10-192.168.3.200

/ip dhcp-server
add name=dhcp-server-1 interface=ether2-lan address-pool=dhcp-pool-1
add name=dhcp-server-2 interface=ether3-lan2 address-pool=dhcp-pool-2
add name=dhcp-server-3 interface=ether4-lan3 address-pool=dhcp-pool-3

/ip dhcp-server network
add address=192.168.1.0/24 gateway=192.168.1.1 dns-server=8.8.8.8,8.8.4.4
add address=192.168.2.0/24 gateway=192.168.2.1 dns-server=8.8.8.8,8.8.4.4
add address=192.168.3.0/24 gateway=192.168.3.1 dns-server=8.8.8.8,8.8.4.4

# Setup NAT for internet access
/ip firewall nat
add chain=srcnat out-interface=ether1-wan action=masquerade

# Basic Firewall Rules
/ip firewall filter

# Allow established/related connections
add chain=input connection-state=established,related action=accept

# Allow ICMP (ping)
add chain=input protocol=icmp action=accept

# Allow WinBox and SSH from LAN only
add chain=input src-address=192.168.1.0/24 protocol=tcp dst-port=8291 action=accept
add chain=input src-address=192.168.2.0/24 protocol=tcp dst-port=8291 action=accept
add chain=input src-address=192.168.3.0/24 protocol=tcp dst-port=8291 action=accept
add chain=input src-address=192.168.1.0/24 protocol=tcp dst-port=22 action=accept

# Block all other input
add chain=input action=drop

# Simple Bandwidth Management (Queue)
/queue simple
add name="Limited-1M" target=192.168.1.0/24 max-limit=1M/1M
add name="Limited-2M" target=192.168.2.0/24 max-limit=2M/2M
add name="Limited-3M" target=192.168.3.0/24 max-limit=2M/1M

# DNS Configuration
/ip dns
set allow-remote-requests=yes servers=8.8.8.8,8.8.4.4

# Save configuration
/export file=router-config-backup

# Display configuration summary
/ip address print
/ip dhcp-server print
/ip firewall nat print
