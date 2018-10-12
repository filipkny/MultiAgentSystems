import requests
start = int(input())
end = int(input())
url = "https://ir.aboutamazon.com/node/{}/html"
for i in range(30510,32000,1):
    fmt_url = url.format(i)
    print("Trying --> {}".format(fmt_url))
    try:
        html = requests.get(fmt_url).text
        print(html.split('<font style=\"font-family:inherit;font-size:18pt;font-weight:bold;\">')[3].split("</font>")[0])
    except(IndexError):
        continue
