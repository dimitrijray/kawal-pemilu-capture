#!/usr/bin/env python3

import requests
import json
import time
import threading

def getRawData():
	request = requests.get('https://kawal-c1.appspot.com/api/c/0')
	return request.text

def getProvinceRows(rawResponse):
	rawJSON = json.loads(rawResponse)
	return rawJSON['data']

def getVotes(provinceRows):
	totalVoters = list()
	jokowiVoters = list()
	prabowoVoters = list()
	for provinceRow in provinceRows.values():
		provinceVoteData = provinceRow['sum']
		totalVoters.append(int(provinceVoteData['sah'])+int(provinceVoteData['tSah']))
		jokowiVoters.append(int(provinceVoteData['pas1']))
		prabowoVoters.append(int(provinceVoteData['pas2']))
	return {'total':sum(totalVoters), '01':sum(jokowiVoters), '02':sum(prabowoVoters)}

def getPercentage(votes):
	jokowiPercentage = (votes['01']/votes['total'])*100
	prabowoPercentage = (votes['02']/votes['total'])*100
	return (jokowiPercentage,prabowoPercentage)

def displayPercentage(percentage):
	prettyTimestamp = time.asctime(time.localtime(time.time()))
	print("{} | Jokowi/Amin: {:.2f}%; Prabowo/Sandi: {:.2f}%".format(prettyTimestamp,percentage[0],percentage[1]))

def savePercentageData(percentage,filename):
	fileToWrite = open(filename,"a")
	textToWrite = "{:.0f} 01:{} 02:{}\n".format(time.time(),percentage[0],percentage[1])
	fileToWrite.write(textToWrite)
	fileToWrite.close()

def getDataAndSavePeriodically():
	threading.Timer(300.0, getDataAndSavePeriodically).start()
	rawData = getRawData()
	provinceData = getProvinceRows(rawData)
	votes = getVotes(provinceData)
	percentages = getPercentage(votes)
	displayPercentage(percentages)
	savePercentageData(percentages,'data')

if __name__ == "__main__":
	getDataAndSavePeriodically()

