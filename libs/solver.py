import requests, json

keyCap = json.load(open('./config.json', 'r').read())['capsolver-key']

def payload(service:str="capsolver.com", proxy:str=None, user_agent:str=None) -> None:
    p = {
        "clientKey":keyCap,
        "task": {
            "websiteURL":"https://discord.com/",
            "websiteKey":"4c672d35-0701-42b2-88c3-78380b0db560",
        }
    }
    if service == "capsolver.com": 
        p['appId']="E68E89B1-C5EB-49FE-A57B-FBE32E34A2B4"
        p['task']['type'] = "HCaptchaTurboTask"
        p['task']['proxy'] = proxy 
        p['task']['userAgent'] = user_agent
    if service == "capmonster.cloud": 
        p['task']['type'] = "HCaptchaTask"
        p['task']['proxyType'] = "http"
        p['task']['proxyAddress'] = proxy.split("@")[1].split(":")[0]
        p['task']['proxyPort'] = proxy.split("@")[1].split(":")[1]
        p['task']['proxyLogin'] = proxy.split("@")[0].split(":")[0]
        p['task']['proxyPassword'] = proxy.split("@")[0].split(":")[1]
    return p

class Solver():
    def __init__(self, proxy:str, siteKey:str, siteUrl:str) -> None:
        self.debug = False

        #Requests
        self.proxy = proxy

        self.siteKey = siteKey
        self.siteUrl = siteUrl

        self.log(f'Solving Captcha, SiteKey: {self.siteKey} | SiteUrl: {self.siteUrl}')

    def log(self, txt:str) -> None:
        if self.debug: print(txt)

    def solveCaptcha(self) -> str:
        r = requests.post(f"https://api.capsolver.com/createTask",json=payload("capsolver.com",self.proxy,'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'))
        try:
            if r.json().get("taskId"):
                taskid = r.json()["taskId"]
            else:
                return None
        except:
            print("Couldn't retrieve captcha task id.",r.text,"failed")
            return None
        # Waiting for results
        while True:
            try:
                r = requests.post(f"https://api.capsolver.com/getTaskResult",json={"clientKey":keyCap,"taskId":taskid})
                if r.json()["status"] == "ready":
                    key = r.json()["solution"]["gRecaptchaResponse"]
                    return key
                elif r.json()['status'] == "failed":
                    return None
            except:
                print("Failed to get solving status.",r.text,"failed")
                return None
