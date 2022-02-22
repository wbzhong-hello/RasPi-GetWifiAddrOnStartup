# RasPi-GetWifiAddrOnStartup
This repo demonstates how to save WIFI IP address automatically to a USB memory stick for a Raspberry Pi at startup.
## Introduction
Many people prefer to connect a [headless](https://www.raspberrypi.com/documentation/computers/configuration.html#setting-up-a-headless-raspberry-pi) Raspberry Pi over WIFI, because wiring a Ethernet cable is inconvenivent or is just impossible (at least expensive, for Raspberry Pi Zero 2W, and laptops without Ethernet port). However, if you are moving the Raspberry Pi between office and home, the WIFI address may change and you may not have access to the router's dash board to get the IP address. This repo demonstates how to use python to save the WIFI IP address to a USB memory stick when the Raspberry Pi is booting up.
## Getting started
- Prepare a USB memory stick and create an empty file **ipaddr.txt** in its root directory.
- Create the mounting directory **/mnt/myusb** for the USB stick on your Raspberry Pi.
- Download **save_ip.py** to your Raspberry Pi, e.g. **/home/pi/scripts/**.
- Insert the USB memory stick and test the function with command:
  
  `sudo python save_ip.py`
## Run program on startup
There are many ways to run the program on startup (see [here](https://www.dexterindustries.com/howto/run-a-program-on-your-raspberry-pi-at-startup/)). Using **rc.local** file may be the easiest one.

Open the **rc.local** file:
  
`sudo nano /etc/re.loacl`

and add the following command just before `exit 0`:

`sudo python /home/pi/scripts/save_ip.py >>/home/pi/logs/save_ip.txt 2>&1 &`

The above command will run the python script at background, so it will not block the normal booting process. The `stdout` and `stderr` will be redirected to **/home/pi/logs/save_ip.txt** for diagnostic purpose.
## Pitfalls
Initially, I used `&>>` to redirect stdout and stderr, which did not work, because **/etc/rc.local** still uses **dash** shell (thanks to this [ansower](https://askubuntu.com/questions/937944/redirecting-output-in-rc-local-not-working)). A comparison of redirection command between bash shell and POSIX form is shown in below [table](https://askubuntu.com/questions/420981/how-do-i-save-terminal-output-to-a-file):
| Bash | POSIX |
| ----------- | ----------- |
| foo &> bar | foo >bar 2>&1 |
| foo &>> bar | foo >>bar 2>&1 |
| foo \|& bar | foo 2>&1 \| bar |