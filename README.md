# IITD-autologin
Here is the autologin script for IITD mac and linux (on a vm/rPi) users. 
The script is solid metal - takes care of all sort of state changes that occur example snoring-laptop/router-reset.

# The icing
The script speaks about its status on the mac and chats in color!

# Usage
grab the code!
select the options in the first few active lines of "autocomplete.py" 

```bash
$ python autocomplete.py 
```

It shall prompt for password/you may just put it in the file in plain text.

To kill all running instances:

```bash
$ sh killer.sh
```

* Ideally run it on a screen and detach it

P.S: This is derived from a bash script by the brave soul Shivanker who enlightened the house of Vindhyachal till 2014 when Mark Zuckerberg took him!

DISCLAIMER: This way of logging in is a little insecure to man in the middle attacks. btw, did you install the IITD-certificate? :P

Cheers!

Mayank


# ----------- Other proxy intel ------------
## sshing into your AWS servers:
You must be having an amazon VM for yourself! You have it right? *
And suban and his monstrous firewalls might be the massive roadblock to you and your aws instances. Although the user with bloated wallet might buy a good 3G data bundle; but lo behold, we can talk to your vm via the proxy server:

Mac users:
* Place the magical personal_bash_fns.sh into a file say .personal into your $HOME == ~/ directory.
* Add this line at the end to your .bash_profile:
```bash
source ~/.personal
```

* FOR EXACTLY ONCE somehow ssh into your aws instance (either by 3g or by ssh_torr**)
* Edit the /etc/sshd_config and add this line just below "Port 22"
```bash
Port 443 

```
* Then do:
```bash
sudo service ssh restart
```
* Hurray, you can now ssh into your instance

** To use ssh_torr, you just need to download the torr browser and start it. after this you can ssh_torr your AWS machine. BUT ITS SLOW. The good thing is that you need to do this only once.

# Why you should have your AWS VM?
* suban hates torrenting!
* suban does not like you to play dota, aoe on gameranger etc!
* suban has logs of 3 months of all the CDNs and hostnames which served you your flavour of delicious multimedia.
* Its free for an year, and you can get 100$ credits by winning coding contests :P

# Bonus: Quick torrenting via koding VMs:
* Make an account on koding, make vm, ...
* edit the /etc/sshd_config and add this line just below "Port 22"
```bash
Port 443 

```
* Then do:
```bash
sudo service ssh restart
```

* Restart ssh service: sudo service ssh restart
* On your machine do:
```bash
ssh_btech <username>@<IP> -D 8080
```

This creates a socks proxy server tunneled through your instance.
Enjoy suban free browsing, torrenting by pointing the browser/utorrent to that proxy. 

* To avoid vm shutdown due to inactivity in the koding browser, use the easy auto refresh extension and keep a terminal open inside the browser.

P.S: I have an imacro script as well, but they banned by account for its use, and have stopped responsing because I kept my VM on for a whole week contiously. 

P.S: The limit is 15 GB/week perhaps. Use multiple accounts! Its easy!


Cheers again brave soul!

Mayank
