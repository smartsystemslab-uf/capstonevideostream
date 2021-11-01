# HOW TO SET THE ENVIRONMENT

## Install crtmpserver on ubuntu (Server Computer)
sudo apt-get install crtmpserver

## Open port 554 for incomming trafic (Server Computer)

## Install and Configure the environment on Raspberry
- To install the capstonevideostream to images and stream to the server, use the `playbook-pi.yml`
  cmd: ansible-playbook -i hosts.txt playbook-pi.yml --limit [`pi_host`]
  The `pi_host` is the list of RPI to configure on the filename `hosts.txt`. Ip addresses should be set directly in that file.

- To install the discorery client on the Raspberry Pi use the second playbook `playbook-pi_2.yml`
   cmd: ansible-playbook -i hosts.txt playbook-pi_2.yml --limit [`pi_host`]
   For the discorver to be launch, the server should be up running.
   cmd:  python3 ip_disc_server.py

- To clean up the discovery client
   cmd: ansible pi_host_new -i hosts.txt -m shell -a '$(which python3) /home/pi/IpDisco-Prj/ip_disco_client/ip_disc_client.py'
