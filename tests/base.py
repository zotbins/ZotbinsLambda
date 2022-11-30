import requests

def getURL(host, path):
    if host.endswith("/"):
        host = host[:-1]
    if path.startswith("/"):
        path = path[1:]
    return "{0}/{1}".format(host, path)


def GET(host, path, params=None, headers=dict()):
    url = getURL(host, path)
    res = requests.get(url, headers=headers, params=params)
    return processResponse(res)


def POST(host, path, data, headers=dict()):
    url = getURL(host, path)
    res = requests.post(url, json=data, headers=headers)
    return processResponse(res)


def DELETE(host, path, data, headers=dict()):
    url = getURL(host, path)
    res = requests.delete(url, json=data, headers=headers)
    return processResponse(res, url)


def processResponse(res):
    if res.status_code == 200:
        return res.json()
    else:
        return {"status": res.status_code, "error" : res.text}
