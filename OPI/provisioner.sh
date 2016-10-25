#!/bin/bash
cd /root
#create the powersave script
cat > powersave.sh << EOL
#!/bin/bash
echo 0 > /sys/devices/system/cpu/cpu1/online
echo 0 > /sys/devices/system/cpu/cpu2/online
echo 0 > /sys/devices/system/cpu/cpu3/online
cpufreq-set -g powersave
EOL

chmod 777 powersave.sh

#create a systemd oneshot
cd /etc/systemd/system
cat > powersave.service << EOL
[Unit]
Description=Powersave

[Service]
ExecStart=/bin/bash /root/powersave.sh

[Install]
WantedBy=multi-user.target
EOL

chmod 777 powersave.service

systemctl enable powersave.service
systemctl start powersave.service

#create autologin script
cd /etc/systemd/system/getty@tty1.service.d
cat > autologin.conf << EOL
[Service]
ExecStart=
ExecStart=-/sbin/agetty --autologin raul --noclear %I 38400 linux
EOL

systemctl daemon-reload

#script start on login
userdir=$(ls /home)
cd /home/$usedir
#cp .profile .profile-orig
#cat .profile |  sed 's/\. "$HOME\/\.bashrc"/\. "$HOME\/\.bashrc"\n\t\tpython rawinput.py/g' > .profile
echo "python /home/$userdir/rawinput.py" >> .profile

apt-get update && apt-get install -y python sshpass 

echo "navigate to /etc/network and edit interfaces with your SSID and pass"
#interfaces example
#allow-hotlug wlan0
#iface wlan0 inet static
#	address 192.168.0.136
#	network 192.168.0.0
#	broadcast 192.168.0.255
#	gateway 192.168.0.1
#	wpa-ssid "NETWORKNAME"
#	wpa-psk "PASSWORD"

wget -O rawinput.py https://raw.githubusercontent.com/MitchRatquest/Inventory-Scanner/master/OPI/rawinput_on_pi.py
chmod 777 rawinput.py
userdir=$(ls /home)
chmod 777 /home/$userdir
mv rawinput.py /home/$userdir
