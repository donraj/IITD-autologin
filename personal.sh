function unsetproxy()   {
    unset HTTP_PROXY
    unset HTTPS_PROXY
    unset http_proxy
    unset https_proxy
    perl -n -i -e 'if($_ =~ /^\s*proxy\s*=/) {} else {print $_;}' ~/.curlrc
    perl -n -i -e 'if($_ =~ /^\s*proxy\s*=/) {} else {print $_;}' ~/.gitconfig
}

function setproxy()     {
    unsetproxy
    if [ $# -lt 1 ]; then
            n='22'
    else
            n=$1
    fi
    export PROXY_SERVER='proxy'"$n"'.iitd.ernet.in'
    export PROXY_PORT='3128'
    export HTTP_PROXY="http://$PROXY_SERVER:$PROXY_PORT"
    export HTTPS_PROXY="$HTTP_PROXY"
    export http_proxy="$HTTP_PROXY"
    export https_proxy="$HTTPS_PROXY"
    export NO_PROXY='localhost,*.iitd.ac.in,*.iitd.ernet.in,*.*.iitd.ernet.in,*.*.iitd.ac.in'
    export no_proxy="$NO_PROXY"
    echo 'proxy = "'"$HTTP_PROXY\"" >> ~/.curlrc
}

function ssh_dual() {
    ssh -p 443 -o ProxyCommand="nc -X connect -x 10.10.78.62:3128 %h %p" "$@"
}

function ssh_btech() {
    ssh -p 443 -o ProxyCommand="nc -X connect -x 10.10.78.22:3128 %h %p" "$@"
}

function ssh_torr() {
    ssh -o ProxyCommand="nc -X 5 -x 127.0.0.1:9150 %h %p" "$@"
}
