import requests, re

"""
Automating JS Deobfuscating/Beautifying using jsnice.org's beautify functionality.
For easier reverse. 
"""
# proxies={'http':'127.0.0.1:8081','https':'127.0.0.1:8081'}
# proxies=proxies # For BurpSuite (or other listeners)

# To-Do: Make it command line tool that takes commandline Arguments


JSFilesURLs = []
JSFileNames = []

def readJSAndPrettify(JSFileName):
    URL = "http://jsnice.org/beautify?pretty=1&rename=1&types=1&suggest=0"

    try:
        with open(JSFileName, 'r') as jsfile:
            JSFileData = jsfile.read().encode('utf-8')

        JSONResponseBody = requests.post(URL,data=JSFileData,headers={}).json()

        PrettyJS = JSONResponseBody['js']  # Parse the JSON => Get the prettified JS only 

        with open('PRETTY_'+JSFileName, 'w', encoding='utf-8') as jsFile:
            jsFile.write(PrettyJS)

    except Exception as e :
        print(e,"\n\nThis wasn't supposed to happen")

def checkIfJS(URL):
    # figure out if it is a javascript file
    pattern = r"\.js(\?|\#|$)" # using only \.js as a pattern won't work, because it'll also be positive for json files and other files or directories that include .js
    if ((re.search(pattern,URL))):
        return True


def getJSFileName(JSURL):
    JSFn = re.search(r"([^/]+\.js)(?=\?|#|$)", str(JSURL)).group()
    JSFileNames.append(JSFn)
    return JSFn

def saveOriginalJS(JSURL, JSFileName):
    jsResponse = requests.get(JSURL).text
    with open(str(JSFileName), 'w') as JSFile:
        JSFile.write(jsResponse)


def PrettifyJSFiles(f):
    # loop through the file lines
    with open(f,'r') as urlsFile:
        URLS = urlsFile.readlines()
    
    for url in URLS:
        url = str(url).strip().replace('\n','')
        if checkIfJS(url):
            JSFilesURLs.append(url)
            fnOfJSURL = getJSFileName(url)
            saveOriginalJS(url,fnOfJSURL)


# Loop through the list and pass each item as a string to  readJSAndPrettify

PrettifyJSFiles('urls.txt')
[readJSAndPrettify(fn) for fn in JSFileNames]
