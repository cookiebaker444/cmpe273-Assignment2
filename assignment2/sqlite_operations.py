import sqlite3
import json

def addSolution(testId):
      with open('solution.json') as f:
            jFile = json.load(f)
            conn = sqlite3.connect('test.db')
            print ("Opened database successfully")
            conn.execute('''CREATE TABLE IF NOT EXISTS TESTSOLUTION 
                  (TESTID        INT     NOT NULL,
                  SUBJECT       TEXT        NOT NULL,
                  QUESTIONNUM   INT     NOT NULL,
                  ANSWER        CHAR(1)     NOT NULL,
                  PRIMARY KEY(TESTID, QUESTIONNUM));''')
            print ("Table created successfully")
            for key in jFile["answer_keys"]:
                  curKey = jFile["answer_keys"][key]
                  testNo = testId
                  que = int(key)
                  sub = jFile["subject"]
                  temp = (testNo, sub, que, curKey)
                  c = conn.cursor()
                  conn.execute("INSERT INTO TESTSOLUTION (TESTID,SUBJECT, QUESTIONNUM, ANSWER) VALUES (?,?,?,?)", temp)
                  conn.commit()
            print ("Records created successfully")
            conn.close()
'''
conn.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
      VALUES (1, 'Paul', 32, 'California', 20000.00 )")

'''

def addScantron(testId, scanId):
      with open('scantron.json') as f:
            jFile = json.load(f)
      conn = sqlite3.connect('test.db')
      print ("Opened database successfully")
      conn.execute('''CREATE TABLE IF NOT EXISTS SCANTRON 
                  (TESTID        INT     NOT NULL,
                  SCANID           INT    NOT NULL,
                  SUBJECT       TEXT        NOT NULL,
                  QUESTIONNUM   INT     NOT NULL,
                  ANSWER        CHAR(1)     NOT NULL,
                  NAME             TEXT   NOT NULL,
                  PRIMARY KEY(TESTID, QUESTIONNUM, NAME, SCANID));''')
      print ("Table created successfully")

      for key in jFile["answers"]:
            curKey = jFile["answers"][key]
            testNo = testId
            scantronId = scanId
            que = int(key)
            sub = jFile["subject"]
            name = jFile["name"]
            temp = (testNo, scantronId, sub, que, curKey, name)
            conn.execute("INSERT INTO SCANTRON (TESTID,SCANID,SUBJECT, QUESTIONNUM, ANSWER, NAME) VALUES (?, ?, ?, ?, ?, ?)",temp)
            conn.commit()
      print ("Records created successfully")
      conn.close()

def getSolution(testId):
      conn = sqlite3.connect('test.db')
      c = conn.cursor()
      c.execute("""SELECT * FROM TESTSOLUTION;""")
      #temp = c.fetchone()
      #print(temp)
      testSol = {}
      answerkeys = {}
      for row in c:
            print(row)
            thisTestId = row[0]
            thisTestSub = row[1]
            if thisTestId == testId:
                  testSol["test_id"] = thisTestId
                  testSol["Subject"] = row[1]
                  answerkeys[row[2]] = row[3]
      testSol["answer_keys"] = answerkeys
      conn.close()
      return testSol
      
def getScantron (testId, scantronNum):
      conn = sqlite3.connect('test.db')
      c = conn.cursor()
      c.execute("""SELECT * FROM SCANTRON;""")
      #temp = c.fetchone()
      #print(temp)
      
      allScantrons = []
      curScan = 1
      scanTron = {}
      answerkeys = {}
      while curScan <= scantronNum:
            for row in c:
                  print(row)
                  thisTestId = row[0]
                  thisScanId = row[1]
                  if thisTestId == testId  and thisScanId == curScan:
                        scanTron["scantron_id"] = row[1]
                        scanTron["test_id"] = thisTestId
                        scanTron["Subject"] = row[2]
                        answerkeys[row[3]] = row[4]
                        scanTron["name"] = row[5]
                        scanTron["answers"] = answerkeys
            allScantrons.append(scanTron)
            curScan += 1
      conn.close()
      return allScantrons

def getScore(sol, jFile):
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
                  if int(realAns[i][0]) == int(scantronAns[j][0]):
                        if realAns[i][1] == scantronAns[j][1]:
                              score += 1
                        replaceAns = {"actual": scantronAns[j][1], "expected": realAns[i][1]}
                        jFile["answers"][scantronAns[j][0]] = replaceAns
      jFile["score"] = score
      return jFile