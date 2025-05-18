2025-05-16
Black Scholes Pricing

Q] How effective is this with American options? What adaptations are needed if any?
6? inputs and the expected price output for European style options. These inputs are: 

Inputs
  Ticker list
  API Key

Current price of the underlying asset (S),
the strike price of the option (K), 
the time until expiration (T), 
the risk-free interest rate (r), 
the volatility of the underlying asset (σ), and 
the dividend yield (q). 


Frequency: Every 5?

Traffic Estimation
  API Calls: Data gathering
  Tickers 100
  Underlying price (every 5 minutes?)
  Option price REAL


Output
  Top return contracts from a set of tickers and expirations.

Alerting
  5% swing? 



Get pricing for a particular ticker, strike, expiration
https://polygon.io/pricing?product=options
  $300 / yr for unlimited API calls, options

https://databento.com/pricing#cme
  $150/month starting. Paygo model too but historic only

https://finnhub.io/docs/api/introduction
  No options data

https://intrinio.com/options/options-realtime
  Intrinio
  $2500/mo

# Kiosk Installation

Referenced https://desertbot.io/blog/raspberry-pi-touchscreen-kiosk-setup

## Console Auto Login NOT desktop
UPDATE: This isn't needed  ` sudo apt-get install lightdm `


## Install these without extras to get Chromium going
` sudo apt-get install --no-install-recommends xserver-xorg x11-xserver-utils xinit openbox `


## Install Chromium
sudo apt-get install --no-install-recommends chromium-browser

Openbox window manager will be configured to launch Chromium
` /etc/xdg  `
(X Development Group) allows autostarting desktop elements on boot

` sudo nano /etc/xdg/openbox/autostart `
```
# EAC adding specs 2021 April
xset -dpms      #turn off display power management system
xset s noblanK  #turn off screen blanking
xset s off      #turn of screen saver

# EAC other article commands to keep Chromium from throwing errors 
sed -i 's/"exited_cleanly":false/"exited_cleanly":true/' ~/.config/chromium/'Local State'
sed -i 's/"exited_cleanly":false/"exited_cleanly":true/; s/"exit_type":"[^"]\+"/"exit_type":"Normal"/' ~/.config/chromium/Default/Preferences

chromium-browser  --noerrdialogs --disable-infobars --kiosk $KIOSK_URL
# Chromium flag to only check annually
#--check-for-update-interval=31536000 
```

` sudo nano /etc/xdg/openbox/environment `
```
export KIOSK_URL=https://desertbot.io
```

Created ```~/.bash_profile``` because didn't exist before. Have ```~/.profile && ~/.bashrc```
To profile, add this line
```
[[ -z $DISPLAY && $XDG_VTNR -eq 1 ]] && startx -- -nocursor
```

# EXTRAS
``` pkill -o chromium ``` Will kill the -o oldest process with Chromium, all other children will end as well, clearing your kiosk


#TODO Chromium refresh frequency for Chromium. Scroll?
#TODO read other guys version https://bdking71.wordpress.com/2018/11/06/setup-an-information-kiosk-using-a-raspberry-pi-zero-w/#:~:text=This%20guide%20provides%20a%20lightweight,Chromium%20browser%20in%20Kiosk%20mode.

# Installing Docker

As of Dec 6 2021,  Raspbian link on server page takes me to Debian install page here
https://docs.docker.com/engine/install/debian/

Prereqs ask for Buster(10) or Bullseye (11)
Says supports armhf  -- is this hard floating point?

2022 April 3  Dockerfiles

### Says Raspbian not supported, but the packages are in the archive, trying that.

Swapping in Raspbian for debian as that URI exists with similar tree for dists and contents. Check sources file is correct after created. This worked in subsequent sudo apt update.
```
 echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/raspbian \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

With that change, the rest of the install instructions work correctly, including sudo docker run hello-world, which produces expected output.

Can then use sudo systemctl edit docker.service to provide config for the docker systemd unit
https://docs.docker.com/engine/install/linux-postinstall/
This is important as it includes remote access, if desired.

# Flask App

`export FLASK_APP=hello`

`flask run`