# This script kills the autologin script
kill -INT $(ps aux | grep -i '[p]ython autologin.py' | awk '{print $2}')