# Author: Chatchawal Sangkeettrakarn
# Date: September 20,2020.

from fastapi import FastAPI
import uvicorn
import numpy as np
import re
import math
import requests
from bs4 import BeautifulSoup
from fastapi.responses import PlainTextResponse
from collections import Counter
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def result(res):
    return {"result": res}


@app.get("/")
async def main():
    return 'Hello World'


@app.get("/test")
async def test():
    return 'Test Tutorial'


@app.get("/add")
async def add(a: int = 0, b: int = 0):
    return a+b


@app.get("/mul")
async def mul(a: int = 0, b: int = 0):
    return a*b


@app.get("/work")
async def work(text: str = ""):
    # remove lead and ending space
    # text.strip()
    # replace all spaces with nothing
    #text = text.replace(' ','')
    # space " " is count as string/letter/character

    # variable
    char_frequency = {}
    string_out = ""

    # loop for dictionary
    for i in text:
        if i in char_frequency:
            char_frequency[i] += 1
        else:
            char_frequency[i] = 1

    # loop for  rearrange character
    x = sorted(char_frequency.items(), key=lambda item: item[1], reverse=True)
    for obj in x:
        string_out += obj[0] + ' = ' + str(obj[1]) + '\n'

    #result = [item for items, c in Counter(char_frequency).most_common() for item in [items] * c]
    jsonout =  {'char' : sorted(char_frequency.items(),key=lambda item: item[1], reverse= True) }

    return jsonout


@app.get("/CountWordInString", response_class=PlainTextResponse)
async def CountWordInString(InputText: str = "Sample Text!", CountRange: str = "1,1"):
    Result = ""
    CheckCount =[CountRange[i:i+1] for i in range(0, len(CountRange), 1)]
    CountComma = CheckCount.count(',')
    if ',' in CheckCount and CountComma == 1 and re.findall('^[1-9]|.0(?=[0])+[\,]+[1-9]+',CountRange):
        RangeList = CountRange.split(',')
        InitialRange = int(RangeList[0])
        LastRange = int(RangeList[1]) + 1
        PresentRange = InitialRange
        for PresentRange in range(InitialRange, LastRange):
            RawList = [InputText[i:i+PresentRange]
                    for i in range(0, len(InputText), PresentRange)]
            CountedList = Counter(RawList)
            SortedList = sorted(CountedList.items(),
                                key=lambda item: item[1], reverse=True)
            Result += 'Range =' + str(PresentRange) + '\n'
            for SortedResult in SortedList:
                Result += '"' + SortedResult[0] + '"' + \
                    ' = ' + str(SortedResult[1]) + '\n'
        PresentRange += 1
    else :
        Result = "Wrong format ,please input CountRange with right format"

    return Result


@app.get("/pow")
async def pow(a: int = 0, b: int = 0):
    return math.pow(a, b)


def tonumlist(li):
    ls = li.split(',')
    for i in range(len(ls)):
        ls[i] = float(ls[i])
    return list(ls)


@app.get("/asc")
async def asc(li):
    ls = tonumlist(li)
    ls.sort()
    return ls


@app.get("/bmi")
async def bmi(h: int = 1, w: int = 0):
    h = (h/100) ** 2
    des = ""
    bmi = w/h
    if (bmi > 30):
        des = "อ้วนมากๆ"
    elif (bmi > 25 and bmi < 30):
        des = "อ้วน"
    elif (bmi > 23 and bmi < 25):
        des = "ท้วม"
    elif (bmi > 18 and bmi < 23):
        des = "สมส่วน"
    elif (bmi < 18.5):
        des = "ผอมจัง"
    jsonout = {'bmi': f'{bmi:.2f}', 'des': des}
    return jsonout


@app.get("/desc")
async def desc(li):
    ls = tonumlist(li)
    ls.sort(reverse=True)
    return ls


@app.get("/sum")
async def sum(li):
    ls = tonumlist(li)
    return np.sum(np.array(ls))


@app.get("/avg")
async def avg(li):
    ls = tonumlist(li)
    return np.average(ls)


@app.get("/mean")
async def mean(li):
    ls = tonumlist(li)
    return np.mean(ls)


@app.get("/max")
async def max(li):
    ls = tonumlist(li)
    return np.amax(ls)


@app.get("/min")
async def min(li):
    ls = tonumlist(li)
    return np.amin(ls)


@app.get("/validation-ctzid")
async def validation_ctzid(text):
    if(len(text) != 13):
        return False

    sum = 0
    listdata = list(text)

    for i in range(12):
        sum += int(listdata[i])*(13-i)

    d13 = (11-(sum % 11)) % 10

    return d13 == int(listdata[12])


@app.get("/validation-email")
async def validation_email(text):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if re.search(regex, text):
        return True
    else:
        return False


@app.get("/google-search", response_class=PlainTextResponse)
def google_search(text):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:81.0) Gecko/20100101 Firefox/81.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    url = 'https://www.google.com/search?q=' + str(text)
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.content, 'html.parser')

    t = soup.findAll('div', {'class': "r"})
    i = 0
    result = ''
    for a in t:
        href = a.a['href']
        head = a.h3.text
        result = result + head + '<br>' + href + '<br><br>'
        i += 1
        if(i >= 5):
            break

    return(result)


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=80, debug=True)
