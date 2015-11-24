# python script for autologin ...
# Script automatically resumes in case of failures like:
#   - Net dead etc.
# May be of use:
# kill $(ps aux | grep '[p]ython csp_build.py' | awk '{print $2}')

import sys, subprocess, time, signal, getpass
BTECH = 22
DUAL = 62
PHD = 61

# ---- tweak here -----
SELECT = DUAL
RECOVERY_TIME = 10 # the lower the faster but, it shall take more CPU cycles.

proxy_add='https://10.10.78.%d/cgi-bin/proxy.cgi'%SELECT
username='cs5110284'
passwd='' # keep it blank for the prompt

## --- error codes ---
BOLD = '\033[1m'
WARNING = '\033[93m'
FAIL = '\033[31m'
ENDC = '\033[0m'
OKGREEN = '\033[92m'

def Warn(message):
    return BOLD + WARNING + message + ENDC

def Error(message):
    return BOLD + FAIL + message + ENDC

def Info(msg):
    return BOLD + OKGREEN + msg + ENDC


error = {
    'no-sid': 'could not get sid',
    'no-conn': 'could not connect to host ' + proxy_add,
    'login-fail': 'server rejected the credentials',
    'login-already': 'Someone is logged in for this ip, proxy',
    'logout-fail': 'The session had already expired. umm Weird!',
    'refresh-fail': 'The session expired perhaps.',
}

def err(x, extra_msg='', debug_level=Error):
    print debug_level(x), ':', error.get(x, '??'), Warn(extra_msg)



## ---
def get_output(cmd):
    try:
        ans = subprocess.check_output(cmd, shell=True)
    except:
        err('no-conn')
        return None
    return ans

def speak(msg):
    from sys import platform as _platform
    if _platform == "darwin":
        cmd = 'say %s'%msg
    get_output(cmd)


def get_sessionid(): 
    cmd = ("""curl -x "" %s -s -k --no-progress-bar --max-time 10""" + 
        """|  grep -m 1 sessionid[\\"=[:alpha:]\ ]*[[:digit:]]* """ +
        """| sed 's/<input name="sessionid" type="hidden" value="//g'""" +
        """| sed 's/">//g'"""
    )%(proxy_add)
    # print cmd
    sid = get_output(cmd).strip()
    if (sid == None):
        return None
    if (set(sid).intersection(set('0123456789abcdef')) == set(sid)):
        return sid
    err('no-sid')
    return None


def login(sid):
    cmd =('curl -x "" %s -k -s --max-time 10 ' +
        '-d "sessionid=%s&action=Validate&userid=%s&pass=%s"'
    )%(proxy_add, sid, username, passwd)
    login_response = get_output(cmd) or ''
    if 'logged in successfully' in login_response:
        print Info('Logged in successfully')
        speak('Logged in successfully')
        return True

    if 'already logged in' in login_response:
        err('login-already', '', Warn)
        return False

    err('login-fail')
    return False


def do_action(sid, action):
    cmd = ('curl -x "" -d "sessionid=%s&action=%s" %s -k -s --max-time 10 '%
        (sid, action, proxy_add)
    )
    return get_output(cmd)
    

def logout(sid):
    response = do_action(sid, 'logout')
    if 'you have logged out' in response:
        print Info("Successfully Logged Out")
        speak('Successfully Logged Out')
    else:
        err('logout-fail')


def refresh(sid):   
    response = do_action(sid, 'Refresh')
    if 'logged in successfully' not in response:
        err('refresh-fail')
        return False 
    return True 
# ------------- script ---------

print Warn('spcial usage info: python autologin.py <sid> <?logout/login>')
if len(sys.argv) > 1:
    sid = sys.argv[1]
    action = 'logout'
    if len(sys.argv) > 2:
        action = sys.argv[2]
    if action == 'logout':
        logout(sid)
    else:
        login(sid)
    sys.exit(0)


# sid = get_sessionid()
# print Info('sid = %s'%sid)
# login(sid)
sid = None

def signal_handler(signal, frame):
    print('You pressed Ctrl+C! - Logging out')
    logout(sid)
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

if not passwd:
    print Info('username: '), username
    passwd = getpass.getpass()

while True:
    if not sid:
        sid = get_sessionid()
        print Info('sid = %s'%sid)

        if not login(sid):
            time.sleep(RECOVERY_TIME)
            sid = None
            continue

    time.sleep(120)
    if not refresh(sid):
        sid = None
    else:
        print Info(time.asctime( time.localtime(time.time()) )) + ': page refreshed'