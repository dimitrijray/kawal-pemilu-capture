#!/usr/bin/env python3

import requests
import json
import time
import threading

def getTimestamp():
	return time.asctime(time.localtime(time.time()))

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
	prettyTimestamp = getTimestamp()
	print("{} | Jokowi/Amin: {:.2f}%; Prabowo/Sandi: {:.2f}%".format(prettyTimestamp,percentage[0],percentage[1]))

def writeToFile(content,filename):
	fileToWrite = open(filename,"a")
	fileToWrite.write(content)
	fileToWrite.close()

def savePercentageData(percentage,filename):
	textToWrite = "{:.0f} 01:{} 02:{}\n".format(time.time(),percentage[0],percentage[1])
	writeToFile(textToWrite,filename)

def displayAndLogConnectionError(logFile):
	prettyTimeStamp = getTimestamp()
	print("{} | Connection lost.")
	textToWrite = "{} Unable to connect to server.".format(prettyTimestamp)
	writeToFile(textToWrite,logFile)

def displayAndLogEmptyResponse(logFile):
	prettyTimeStamp = getTimestamp()
	print("{} | Server returns empty response.")
	textToWrite = "{} Empty response.".format(prettyTimestamp)
	writeToFile(textToWrite,logFile)

def getDataAndSavePeriodically(timeInMinutes,saveFile):
	try:
		timeInSeconds = timeInMinutes * 60.0
		threading.Timer(timeInSeconds, getDataAndSavePeriodically, args= [timeInMinutes,saveFile]).start()
		rawData = getRawData()
		provinceData = getProvinceRows(rawData)
		votes = getVotes(provinceData)
		percentages = getPercentage(votes)
		displayPercentage(percentages)
		savePercentageData(percentages,saveFile)
	except:
		displayAndLogEmptyResponse('log')

if __name__ == "__main__":
	getDataAndSavePeriodically(10,'data3')
