import subprocess

# Update and install necessary packages
subprocess.run(['apt-get', 'update'])
subprocess.run(['apt-get', 'install', '-y', 'dnsmasq', 'hostapd'])

# Downgrade iptables
# Directory to store downloaded Debian packages
download_dir = '/wifi'

# Download the required Debian packages using wget
packages = [
    "http://old.kali.org/kali/pool/main/i/iptables/iptables_1.6.2-1.1_arm64.deb",
    "http://old.kali.org/kali/pool/main/i/iptables/libip4tc0_1.6.2-1.1_arm64.deb",
    "http://old.kali.org/kali/pool/main/i/iptables/libip6tc0_1.6.2-1.1_arm64.deb",
    "http://old.kali.org/kali/pool/main/i/iptables/libiptc0_1.6.2-1.1_arm64.deb",
    "http://old.kali.org/kali/pool/main/i/iptables/libxtables12_1.6.2-1.1_arm64.deb"
]

# Download the packages to the specified directory
for package in packages:
    subprocess.run(['wget', package, '-P', download_dir], check=True)

# Get a list of downloaded .deb files
deb_files = [os.path.join(download_dir, filename) for filename in os.listdir(download_dir) if filename.endswith('.deb')]

# Install the downloaded packages using dpkg
for deb_file in deb_files:
    subprocess.run(['dpkg', '-i', deb_file], check=True)

# Mark packages on hold to prevent automatic upgrades
packages_to_hold = ['iptables', 'libip4tc0', 'libip6tc0', 'libiptc0', 'libxtables12']
for package in packages_to_hold:
    subprocess.run(['apt-mark', 'hold', package], check=True)

# Create hostapd.conf file
hostapd_conf_content = """\
interface=wlan1
#driver=nl80211
#ssid=PAV2_5G
ssid=Unitest
hw_mode=b
channel=7
#bssid=28:87:BA:14:25:43
bssid=22:87:BA:14:25:43
"""
with open('hostapd.conf', 'w') as file:
    file.write(hostapd_conf_content)

# Append configurations to dnsmasq.conf
dnsmasq_conf_content = """\
interface=wlan1
dhcp-range=192.168.43.100,192.168.43.230,255.255.255.0,12h
dhcp-option=3,192.168.43.1
dhcp-option=6,192.168.43.1
server=192.168.43.1
server=1.1.1.1
log-queries
log-dhcp
listen-address=127.0.0.1
listen-address=192.168.43.1
"""
with open('/etc/dnsmasq.conf', 'w') as file:
    file.write(dnsmasq_conf_content)

# Configure wlan1 interface and routing
subprocess.run(['ifconfig', 'wlan1', 'up', '192.168.43.1', 'netmask', '255.255.255.0'])
subprocess.run(['route', 'add', '-net', '192.168.43.0', 'netmask', '255.255.255.0', 'gw', '192.168.43.1'])

# Start dnsmasq service
subprocess.run(['service', 'dnsmasq', 'start'])
subprocess.run(['service', 'dnsmasq', 'restart'])

# Configure iptables rules
subprocess.run(['rfkill', 'unblock', 'wlan'])
subprocess.run(['iptables', '--policy', 'INPUT', 'ACCEPT'])
subprocess.run(['iptables', '--policy', 'FORWARD', 'ACCEPT'])
subprocess.run(['iptables', '--policy', 'OUTPUT', 'ACCEPT'])
subprocess.run(['iptables', '-F'])
subprocess.run(['iptables', '-t', 'nat', '-F'])
subprocess.run(['iptables', '-t', 'nat', '-A', 'POSTROUTING', '-o', 'wlan0', '-j', 'MASQUERADE'])
subprocess.run(['iptables', '-A', 'FORWARD', '-i', 'wlan1', '-o', 'wlan0', '-j', 'ACCEPT'])
#subprocess.run(['iptables', '--table', 'nat', '--append', 'POSTROUTING', '--out-interface', 'wlan0', '-j', 'MASQUERADE'])
#subprocess.run(['iptables', '--append', 'FORWARD', '--in-interface', 'wlan1', '-j', 'ACCEPT'])

# Edit /proc/sys/net/ipv4/ip_forward file
ip_forward_content = """\
1
"""
with open('/proc/sys/net/ipv4/ip_forward', 'w') as file:
    file.write(ip_forward_content)

# Start hostapd with hostapd.conf
subprocess.run(['hostapd', 'hostapd.conf'])
