import os.path
import subprocess
import sys
import time
from datetime import datetime


def check_connection():
    '''Returns True if a wireless network is connected, otherwise False.'''
    try:
        # Try to get the ESSID of the connected network on wlan0
        # To check link status on eth0: cat /sys/class/net/eth0/operstate
        # output is "up" or "down"
        subprocess.run('iwgetid',
                       capture_output=True,
                       check=True,
                       text=True)
    except subprocess.CalledProcessError:
        return False
    else:
        return True


def wait_connection():
    '''Waits for the connection of a wireless network for a maximum of 30s.
    Returns True if a wireless network is connected, otherwise False.'''
    for i in range(30):
        if check_connection():
            return True
        else:
            time.sleep(1)
    return False


print('safe_ip starts at', datetime.now())

# Search for any USB memory stick
blkid = subprocess.run('blkid',
                       capture_output=True,
                       check=True,
                       text=True)

# A USB memory stick may appear as /dev/sda1
if -1 == blkid.stdout.find('/dev/sda1'):
    print('No USB memory stick is found.')
    sys.exit(-1)

# The mounting point /mnt/myusb must be created before hand
try:
    subprocess.run('mount /dev/sda1 /mnt/myusb',
                   capture_output=True,
                   check=True,
                   text=True,
                   shell=True)
except subprocess.CalledProcessError as err:
    print('Unable to mount the USB memory stick:', err.stderr)
    sys.exit(-1)

# Write IP address to ipaddr.txt if it exists in the root directory of the memory stick
if os.path.exists('/mnt/myusb/ipaddr.txt'):
    with open('/mnt/myusb/ipaddr.txt', 'w') as f:
        if wait_connection():
            ip = subprocess.run('ip address show',
                                capture_output=True,
                                check=True,
                                text=True,
                                shell=True)
            f.writelines(ip.stdout)
            print('IP address has been saved to ipaddr.txt.')
        else:
            print('Wait for the connection of a wireless network is timed out.')
else:
    print('ipaddr.txt is missing.')

# Clean up
subprocess.run('umount /mnt/myusb',
               check=True,
               shell=True)
