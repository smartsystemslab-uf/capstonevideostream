# HOW TO SET THE ENVIRONMENT

## Install crtmpserver on ubuntu (Server Computer)
`sudo apt-get install crtmpserver`

## Enable rtsp protocol in crtmpserver
0. Save a backup of the configuration file
`sudo cp /etc/crtmpserver/applications/flvplayback.lua /etc/crtmpserver/applications/flvplayback.lua.back`
1. Open crtmpserver config file
`sudo vim /etc/crtmpserver/applications/flvplayback.lua`
2. Uncomment RTSP protocol config line
```
{
	ip="0.0.0.0",
	port=554,
	protocol="inboundRtsp"
},
```

3. Restart the server
`sudo systemctl restart crtmpserver`

## Open ports for incomming trafic (Server Computer)
### Linux Settings Supporting UFW (Tested Ubuntu 18.04 and 20.04)
### Enable firewall with `ufw`
`sudo ufw enable`

### Open the following TCP port using ufw
`sudo ufw allow 554`
`sudo ufw allow 1935`
`sudo ufw allow 6666`
`sudo ufw allow 6665`
`sudo ufw allow 9999`
`sudo ufw allow 8080`

To read to able stream from the server, some udp port should be opened. The only problem is that they are automatically generated. Two to allow these udp port using ufw.
- The first approach which is safe, but tedious, consist in opening every single port manually. To get the list of port, run the following command:
`sudo netstat -tunelp | egrep -o "^(udp).*(crtmpserver)" | egrep -o ":[0-9]{4,5}" | egrep -o "[0-9]{4,5}"`
- The second way is to allow all incomming udp communication to the server local address
`sudo ufw allow from 192.168.1.0/24 to 192.168.1.11 proto udp`


At this port, all cameras should be able to stream image to crtmpserver and the stream can be read with vlc. The link to stream has the this structure `rtsp://<server_address>:554/test<camera_mac_address>`. The camera mac address is the hex representation concatenated. ex: rtsp://127.0.0.1:554/testB827EB3C6B0A

The ![IpDisco](http://dev.camertronix.com/Immersion-Grp/IpDisco-Prj) (Ip dicorvery module) module is a client-server module design to retrieved camera settings from the server side including the camera mac address to read the stream.

More about ![UFW here](https://help.ubuntu.com/community/UFW).

## Install and Configure the environment on Raspberry
- To install the capstonevideostream to images and stream to the server, use the `playbook-pi.yml`
  cmd: `ansible-playbook -i hosts.txt playbook-pi.yml --limit pi_host_name`
  The `pi_host_name` is the name of the list of RPI to configure on the filename `hosts.txt`. Ip addresses should be set directly in that file.

- To install the discorery client on the Raspberry Pi use the second playbook `playbook-pi_2.yml`
   cmd: `ansible-playbook -i hosts.txt playbook-pi_2.yml --limit pi_host_name`
   For the discorver to be launch, the server should be up running.
   cmd:  `python3 ip_disc_server.py`

- To clean up the discovery client
   cmd: `ansible pi_host_new -i hosts.txt -m shell -a '$(which python3) /home/pi/IpDisco-Prj/ip_disco_client/ip_disc_client.py'`
   
   
   

