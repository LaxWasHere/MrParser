import json, re
import urllib.request as urlr


def parse(url):
    key = url.split("/")[3].split(".")[0]
    if "pastebin.com" in url:
        data = urlr.urlopen(urlr.Request("https://pastebin.com/raw/"+key, headers={'User-Agent': 'Mozilla/5.0'})).read().decode("utf-8")
        return parseError("\n".join(str(data).split("\\n")).splitlines())
    if getDomain(url) is not None:
        data = json.loads(urlr.urlopen(urlr.Request(getDomain(url)+key, headers={'User-Agent': 'Mozilla/5.0'})).read().decode("utf-8"))
        return parseError(data["data"].splitlines())


def getDomain(url):
    if "hasteb.in" in url:
        return "https://hasteb.in/documents/"
    if "hastebin.com" in url:
        return "https://hastebin.com/documents/"
    if "paste.md-5.net" in url:
        return "https://paste.md-5.net/documents/"


def parseError(error):
    founds = {}
    for line in error:
        if any(re.findall("Cracked by|BlackSpigotMC", line, re.IGNORECASE)) and "PIRATED" not in founds:
            founds["PIRATED"] = line
        if any(re.findall(".v1_7|.v1_8|.v1_9|.v1_10|MC: 1.8", line, re.IGNORECASE)) and "OUTDATED" not in founds:
            founds["OUTDATED"] = line
        if any(re.findall("AuthMe", line, re.IGNORECASE)) and "CRACKED" not in founds:
            founds["CRACKED"] = line
    return founds
