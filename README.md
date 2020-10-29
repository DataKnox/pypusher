# pypusher

# Requirements
You must have the Flask library installed to run the main code, frontend.py
```
pip install flask
```

# Configure Pushover
https://pushover.net/
Create an account AND verify your email. Take note of your User Key in the top right corner of the homepage.
Pushover requires 3 components to send a notification:
- Your user key
- An App Token
- and a message

Once you have verified your account, create an App to receive a token (towards the bottom of the homepage)

# Set Environment Variables - the API pulls this info from your local env vars
- APPKEY=\<Your App Token that you received when you generated the app\>
- PUSHOVERKEY=\<Your User Key\>
# Start the application
- cd to the directory that contains frontend.py
- python3 frontend.py

# Steps to configure on-box Python via Guestshell and an EEM Applet
Tested on a CSR1000v running IOS-XE 17.
```
conf t
! ASSIGN AN IP ADDRESS TO AN INTERFACE THAT CAN REACH THE INTERNET
! SET DEFAULT ROUTE
! SET DNS SERVER
```
# Now configure Guest Shell
```
iox
do show iox
interface virtualportgroup 0
ip add 192.168.144.15 255.255.255.0
no shut
ip nat inside
! go to outside int
int gig 1
ip nat outside
exit
ip access-list standard NATOUT
exit
ip nat inside source list NATOUT interface gigabitEthernet 1 overload
ip http server
app-hosting appid guestshell
vnic gateway1 virtualportgroup 0 guest-interface 0 guest-ipaddress 192.168.144.2 netmask 255.255.255.0 gateway 192.168.144.15 name-server 8.8.8.8 default

resource profile custom cpu 1500 memory 512
```
# Note that this version of code, for whatever reason, assigns the wrong default gateway to the wrong NIC
```
no app-default-gateway 192.168.144.15 guest-interface 1
app-default-gateway 192.168.144.15 guest-interface 0
end
guestshell enable
! wait until you receive a syslog message saying that it is alive
guestshell
```
# Now lets set up the box for Python HTTP requests and begin to write our script
```
[guestshell@guestshell ~]$ sudo pip3 install requests
[guestshell@guestshell ~]$ vi ospfsender.py
```
# Press I to begin typing - change the URL to be your Flask IP Address!!!!!!
```
import requests
import json

payload={
"hostname":"CSR1",
"messages":"OSPF is flapping"
}
headers={"Content-Type":"application/json","Accept":"application/json"}

r = requests.post(url="http://10.10.21.196:5000/ios",data=json.dumps(payload),headers=headers,verify=False)
print(r.text)
~
~
~
~
~
~
~
~
~
~
~
~
```
Press Esc to stop typing, then type :wq to write and quite
# Test from Guest shell and IOS
```
[guestshell@guestshell ~]$ python3 ospfsender.py
exit
!FROM IOS CLI
guestshell run python3 /home/guestshell/ospfsender.py
```
# Create the applet to fire off when ever an OSPF adjacency flaps
```
event manager applet OSPF
 event syslog pattern "from FULL to DOWN"
 action 0 cli command "en"
 action 1 syslog msg "OSPF Applet fired"
 action 2 cli command "guestshell run python3 /home/guestshell/ospfsender.py"
 ```
