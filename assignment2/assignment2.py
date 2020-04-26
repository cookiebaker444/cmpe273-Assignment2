##Author: Kuang Sheng
import os
import json
import sqlite3
from flask import Flask, escape, request, jsonify
import sqlite_operations
app = Flask(__name__)

testSol = {}

submissions = []

testId = 0
scantronId = 0

@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'


@app.route('/api/tests', methods=['POST'])
def create_solution():
    global testId
    ##print(request.get_json())
    #typedName = input("please input the name of the student:")
    with open('solution.json') as f:
        jFile = json.load(f)
        testId += 1
        testSol = jFile
        testSol["test_id"] = testId
        testSol["submission"]= submissions
        f.close()
    sqlite_operations.addSolution(testId)
    return testSol



@app.route('/api/tests/<thistestId>/scantrons', methods = ['POST'])
def post_scantron(thistestId):
    testId = int(thistestId)
    global scantronId 
    with open('scantron.json') as f:
        jFile = json.load(f)
        thisScantron = jFile
        thisScantron["test_id"] = testId
        scantronId = scantronId + 1
        jFile["scantron_id"] = scantronId
        sqlite_operations.addScantron(testId, scantronId)
        #sol = {}
        sol = sqlite_operations.getSolution(int(thistestId))
        #print(sol)
        return sqlite_operations.getScore(sol, jFile)

        '''
        score = 0
        returnDic = {}
        scantronAns = []
        for key in jFile["answers"]:
            tempTup = (key, jFile["answers"][key])
            scantronAns.append(tempTup)
        #print(scantronAns)
        realAns = []
        for key in sol["answer_keys"]:
            tempTup = (key, sol["answer_keys"][key])
            realAns.append(tempTup)
        #print(realAns)
        for i in range (len(realAns)):
            for j in range(len(scantronAns)):
                if realAns[i][0] == int(scantronAns[j][0]):
                    if realAns[i][1] == scantronAns[j][1]:
                        score += 1
                    replaceAns = {"actual": scantronAns[j][1], "expected": realAns[i][1]}
                    jFile["answers"][scantronAns[j][0]] = replaceAns
        jFile["score"] = score
        return jFile
        '''

@app.route('/api/tests/<thisTestId>', methods = ['GET'])
def get_submissions(thisTestId):
    thisTI = int(thisTestId)
    global scantronId
    global submissions
    print (scantronId)
    submissions = sqlite_operations.getScantron(thisTI, 1)
    print(submissions)
    solution = sqlite_operations.getSolution(thisTI)
    for i in range (len(submissions)):
        submissions[i] = sqlite_operations.getScore(solution, submissions[i])
    
    solution["submissions"] = submissions
    return solution

    
