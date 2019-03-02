# restart_router
Restarting my Vodafone Router to make sure the performance is good...
I am assuming you are running this script on a RPi.

# Install
Clone it

# Install Chromium
todo, install it in docker
``


# Run chromium with debugging port
`--remote-debugging-port=9222`

# Install Python Dependencies
`pip3 install -r requirements.txt`

# Run
Replace `abc` with your actual password. Change IP to your router ip address.
`python3 PASSWORD=abc IP=192.168.0.1 restart_router.py`
