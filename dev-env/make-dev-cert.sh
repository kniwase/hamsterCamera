cd `dirname $0`
mkdir -p cert
mkcert -key-file cert/key.pem -cert-file cert/cert.pem localhost