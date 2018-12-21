'''
Created on 2018-12-19
@author: nan
'''

import base64,json,logging,requests,unittest,uuid

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%d-%b-%Y %H:%M:%S',
                    )

usr = "FRC_WSUSER"
pwd = "Welcome1"
token = "Basic %s" % base64.b64encode(b'FRC_WSUSER:Welcome1').decode('ascii')
header = {
    "Authorization": token,
    "Content-Type": "application/vnd.oracle.adf.resourceitem+json"
}
# All REST urls
DOMAIN = "https://fuscdrmsmc268-fa-ext.us.oracle.com/fscmRestApi/resources/latest/"

URL_FRC_ISSUES = DOMAIN + "frcIssues"
URL_ADVANCED_CONTROLS = DOMAIN + "advancedControls"
URL_ADVANCED_CONTROLS_JOBS = DOMAIN + "advancedControlsJobs"
URL_ADVANCED_CONTROLS_RUNS = DOMAIN + "advancedControlsRuns"
URL_FRC_CONTROLS = DOMAIN + "frcControls"
URL_ADVANCED_CONTROLS_ASSESSMENT_RESULTS = DOMAIN + "frcControlAssessmentResults"
URL_FRC_RISKS = DOMAIN + "frcRisks"
URL_FRC_PROCESSES = DOMAIN + "frcProcesses"
URL_FRC_ASSESSMENT_RESULTS = DOMAIN + "frcRiskAssessmentResults"
URL_FRC_PROCESS_ASSESSMENT_RESULTS = DOMAIN + "frcProcessAssessmentResults"

"""Test GRC REST"""


class TestMathFunc(unittest.TestCase):



    def testAdvancedControls(self):
        # REST advancedControls
        resp = self.doGet(URL_ADVANCED_CONTROLS)
        if (not self.checkItem(resp)): return
        # GET /advancedControls/{itemId}
        itemId = resp.json()['items'][1]['Id']
        URL_ITEM = URL_ADVANCED_CONTROLS + "/" + str(itemId)
        self.doGet(URL_ITEM)
        self.doPatch(URL_ITEM, {"Description": str(uuid.uuid4())})
        # child comment
        URL_CHILD_COMMENTS = URL_ITEM + '/child/comments'
        self.doGet(URL_CHILD_COMMENTS)
        data = {"UserComment": "HP Comments post", "ObjectTypeCode": "GRC_CONTROL"}
        id = self.doPost(URL_CHILD_COMMENTS, data)['Id']
        URL_CHILD_COMMENTS_ITEM = URL_CHILD_COMMENTS + '/' + str(id)
        logging.warning("the post data is not exist ,TODO update")
        # self.doPatch(URL_CHILD_COMMENTS_ITEM, {"UserComment": str(uuid.uuid4())})
        # self.doDelete(URL_CHILD_COMMENTS_ITEM)

    def testAdvancedControlsJobs(self):
        resp = self.doGet(URL_ADVANCED_CONTROLS_JOBS)
        if (not self.checkItem(resp)): return
        itemId = resp.json()['items'][0]['Id']
        URL_ITEM = URL_ADVANCED_CONTROLS_JOBS + "/" + str(itemId)
        self.doGet(URL_ITEM)
        URL_ITEM=URL_ADVANCED_CONTROLS_JOBS+'?q=JobType%3DWORKLIST_SYNC_JOB'
        self.doGet(URL_ITEM)

    def testAdvancedControlsRuns(self):
        URL_ADVANCED_CONTROLS_RUNS=DOMAIN + "advancedControlsRuns"
        data = self.doPost(URL_ADVANCED_CONTROLS_RUNS, {"ControlId": "10007"})
        itemId = data['JobRunId']
        #TODO no data
        URL_ITEM = URL_ADVANCED_CONTROLS_RUNS + '/' + str(itemId)
        resp = self.doGet(URL_ITEM)

    def testFrcIssues(self):
        #REST frcIssues
        resp = self.doGet(URL_FRC_ISSUES)
        if (not self.checkItem(resp)): return
        itemId = resp.json()['items'][0]['IssueId']
        URL_FRC_ISSUES_ITEM = URL_FRC_ISSUES + "/" + str(itemId)
        self.doGet(URL_FRC_ISSUES)
        self.doPatch(URL_FRC_ISSUES_ITEM,{'Name': 'HP Issue1 Testing2 patch'})
        data = {"Name": "HP Issue Testing" + str(uuid.uuid4()), "Status": "OPEN", "Severity": "DEFICIENCY"}
        self.doPost(URL_FRC_ISSUES, data)
        # child additionalInformation
        URL_ITEM_CHILD = URL_FRC_ISSUES_ITEM + "/child/additionalInformation"
        resp = self.doGet(URL_ITEM_CHILD)
        if (not self.checkItem(resp)): return
        id = resp.json()['items'][0]['IssueId']
        URL_ITEM_CHILD_ITEM = URL_ITEM_CHILD + "/" + str(id)
        resp = self.doGet(URL_ITEM_CHILD_ITEM)
        self.doPatch(URL_ITEM_CHILD_ITEM,{'qaiss120610c': 'test'})

    def testFrcControls(self):
        #REST frcControls
        resp = self.doGet(URL_FRC_CONTROLS)
        if (not self.checkItem(resp)): return
        itemId = resp.json()['items'][0]['ControlId']
        URL_FRC_CONTROLS_ITEM = URL_FRC_CONTROLS + "/" + str(itemId)
        self.doGet(URL_FRC_CONTROLS_ITEM)
        self.doPost(URL_FRC_CONTROLS, {"Name":str(uuid.uuid4())})
        self.doPatch(URL_FRC_CONTROLS_ITEM, {"Name": "Auto Risk Control1 patch"})
        # child additionalInformation
        URL_FRC_CONTROLS_CHILD_AI = URL_FRC_CONTROLS_ITEM + "/child/additionalInformation"
        resp = self.doGet(URL_FRC_CONTROLS_CHILD_AI)
        if (not self.checkItem(resp)): return
        itemId = resp.json()['items'][0]['ControlId']
        URL_CHILD_AI_ITEM = URL_FRC_CONTROLS_CHILD_AI + "/" + str(itemId)
        self.doGet(URL_CHILD_AI_ITEM)
        data = {"qacontrol120610c": "test"}
        self.doPatch(URL_CHILD_AI_ITEM, data)
        # child comments
        URL_CHILD_COMMONTS = URL_FRC_CONTROLS_ITEM + "/child/comments"
        resp = self.doGet(URL_CHILD_COMMONTS)
        data = {"UserComment": "HP Comments"}
        if (not self.checkItem(resp)): return
        itemId = resp.json()['items'][0]['Id']
        URL_CHILD_COMMONTS_ITEM = URL_CHILD_COMMONTS + "/" + str(itemId)
        self.doGet(URL_CHILD_COMMONTS_ITEM)
        data = {"UserComment": "HP Comments"}
        self.doPatch(URL_CHILD_COMMONTS_ITEM, data)
        data = self.doPost(URL_CHILD_COMMONTS, data)
        URL_CHILD_COMMONTS_ITEM = URL_CHILD_COMMONTS + "/" + str(data['Id'])
        self.doDelete(URL_CHILD_COMMONTS_ITEM)

    def testFrcControlAssessmentResults(self):
        resp = self.doGet(URL_ADVANCED_CONTROLS_ASSESSMENT_RESULTS)
        if (not self.checkItem(resp)): return
        itemId = resp.json()['items'][0]['ResultId']
        URL_ITEM = URL_ADVANCED_CONTROLS_ASSESSMENT_RESULTS + "/" + str(itemId)
        self.doGet(URL_ITEM)
        self.doPatch(URL_ITEM,{'ResponseCode': 'PASS'})
        # child additionalInformation
        URL_ITEM_CHILD_AI = URL_ITEM + "/child/additionalInformation"
        resp = self.doGet(URL_ITEM_CHILD_AI)
        if (not self.checkItem(resp)): return
        itemId = resp.json()['items'][0]['ResultId']
        URL_ITEM_CHILD_AI_ITEM = URL_ITEM_CHILD_AI + "/" + str(itemId)
        self.doGet(URL_ITEM_CHILD_AI_ITEM)

    def testFrcRisks(self):
        resp = self.doGet(URL_FRC_RISKS)
        if (not self.checkItem(resp)): return
        itemId = resp.json()['items'][0]['RiskId']
        URL_ITEM = URL_FRC_RISKS + "/" + str(itemId)
        self.doGet(URL_ITEM)
        self.doPatch(URL_ITEM,{"Name": str(uuid.uuid4())})
        # child comments
        URL_ITEM_CHILD = URL_ITEM + "/child/comments"
        resp = self.doGet(URL_ITEM_CHILD)
        itemId=self.doPost(URL_ITEM_CHILD,{"UserComment": "testing12345"})['Id']
        URL_ITEM_CHIL1_ITEM = URL_ITEM_CHILD + "/" + str(itemId)
        self.doGet(URL_ITEM_CHIL1_ITEM)
        self.doPatch(URL_ITEM_CHIL1_ITEM,{'UserComment':str(uuid.uuid4())})
        self.doDelete(URL_ITEM_CHIL1_ITEM)
        # child additionalInformation
        URL_ITEM_CHILD = URL_ITEM + "/child/additionalInformation"
        resp = self.doGet(URL_ITEM_CHILD)
        if (not self.checkItem(resp)): return
        itemId = resp.json()['items'][0]['RiskId']
        URL_ITEM_CHILD_ITEM = URL_ITEM_CHILD + "/" + str(itemId)
        self.doPatch(URL_ITEM_CHILD_ITEM,{"sampleTestRiskDff":"test"})
        # child  relatedProcesses
        URL_ITEM_CHILD = URL_ITEM + "/child/relatedProcesses"
        self.doGet(URL_ITEM_CHILD)
        if (not self.checkItem(resp)): return
        itemId = resp.json()['items'][0]['RiskId']
        URL_ITEM_CHILD_ITEM = URL_ITEM_CHILD + "/" + str(itemId)
        # resp = self.doGet(URL_ITEM_CHILD_ITEM) TODO not pass
        # child perspectives TODO no data
        URL_ITEM_CHILD1 = URL_ITEM + "/child/perspectives"
        resp = self.doGet(URL_ITEM_CHILD1)
        itemId = self.doPost(URL_ITEM_CHILD1, {"UserComment": "testing12345"})['Id']
        URL_ITEM_CHILD1_ITEM = URL_ITEM_CHILD1 + "/" + str(itemId)
        self.doGet(URL_ITEM_CHILD1_ITEM)
        self.doPatch(URL_ITEM_CHILD1_ITEM, {'UserComment': str(uuid.uuid4())})
        self.doDelete(URL_ITEM_CHILD1_ITEM)

    def testFrcProcesses(self):
        resp = self.doGet(URL_FRC_PROCESSES)
        if (not self.checkItem(resp)): return
        itemId = resp.json()['items'][0]['ProcessId']
        URL_ITEM = URL_FRC_PROCESSES + "/" + str(itemId)
        self.doGet(URL_ITEM)
        self.doPatch(URL_ITEM, {"Name": str(uuid.uuid4())})
        # child comments
        URL_ITEM_CHILD = URL_ITEM + "/child/comments"
        resp = self.doGet(URL_ITEM_CHILD)
        itemId = self.doPost(URL_ITEM_CHILD, {"UserComment": "testing12345"})['Id']
        URL_ITEM_CHIL1_ITEM = URL_ITEM_CHILD + "/" + str(itemId)
        self.doGet(URL_ITEM_CHIL1_ITEM)
        self.doPatch(URL_ITEM_CHIL1_ITEM, {'UserComment': str(uuid.uuid4())})
        self.doDelete(URL_ITEM_CHIL1_ITEM)
        # child additionalInformation
        URL_ITEM_CHILD = URL_ITEM + "/child/additionalInformation"
        resp = self.doGet(URL_ITEM_CHILD)
        if (not self.checkItem(resp)): return
        itemId = resp.json()['items'][0]['ProcessId']
        URL_ITEM_CHILD_ITEM = URL_ITEM_CHILD + "/" + str(itemId)
        self.doPatch(URL_ITEM_CHILD_ITEM, {"sampleTestRiskDff": "1"})
        # child perspectives TODO need playload
        URL_ITEM_CHILD = URL_ITEM + "/child/perspectives"
        resp = self.doGet(URL_ITEM_CHILD)
        itemId = self.doPost(URL_ITEM_CHILD, {"test": "testing12345"})['Id']
        URL_ITEM_CHILD1_ITEM = URL_ITEM_CHILD + "/" + str(itemId)
        self.doGet(URL_ITEM_CHILD1_ITEM)
        self.doPatch(URL_ITEM_CHILD1_ITEM, {'UserComment': str(uuid.uuid4())})
        self.doDelete(URL_ITEM_CHILD1_ITEM)

    def testFrcRiskAssessmentResults(self):
        resp = self.doGet(URL_FRC_ASSESSMENT_RESULTS)
        if (not self.checkItem(resp)): return
        itemId = resp.json()['items'][0]['ResultId']
        URL_ITEM = URL_FRC_ASSESSMENT_RESULTS + "/" + str(itemId)
        self.doGet(URL_ITEM)
        self.doPatch(URL_ITEM, {"Status": "'ACTIVE'"})
        # child additionalInformation
        URL_ITEM_CHILD = URL_ITEM + "/child/additionalInformation"
        resp = self.doGet(URL_ITEM_CHILD)
        if (not self.checkItem(resp)): return
        itemId = resp.json()['items'][0]['ResultId']
        URL_ITEM_CHILD_ITEM = URL_ITEM_CHILD + "/" + str(itemId)
        self.doPatch(URL_ITEM_CHILD_ITEM, {"sampleTestAssessRisk": "test"})

    def testFrcProcessAssessmentResults(self):
        resp = self.doGet(URL_FRC_PROCESS_ASSESSMENT_RESULTS)
        if (not self.checkItem(resp)): return
        itemId = resp.json()['items'][0]['ResultId1']
        itemId='00020000000EACED000577080000000000003E9E0000000EACED000577080000000000003E9E' #TMP
        URL_ITEM = URL_FRC_PROCESS_ASSESSMENT_RESULTS + "/" + str(itemId)
        self.doGet(URL_ITEM)
        self.doPatch(URL_ITEM, {"StateCode": "COMPLETED"})
        # child additionalInformation
        URL_ITEM_CHILD = URL_ITEM + "/child/additionalInformation"
        resp = self.doGet(URL_ITEM_CHILD)
        if (not self.checkItem(resp)): return
        itemId = resp.json()['items'][0]['ResultId']
        URL_ITEM_CHILD_ITEM = URL_ITEM_CHILD + "/" + str(itemId)
        self.doPatch(URL_ITEM_CHILD_ITEM, {"qaprocasmt1206150c": str(uuid.uuid4())})

    def doGet(self, url):
        resp = requests.get(url, auth=(usr, pwd))
        if resp.status_code != 200:
            logging.error("GET failed %s content:%s", url, resp.content.decode('ascii'))
        self.assertEqual(resp.status_code, 200)
        logging.info('GET request %s %d', url, resp.status_code)
        return resp

    def doGetWithCheck(self, url):
        resp = self.doGet(url)
        if (len(resp.json()['items']) == 0):
            logging.error("GET request URL_FRC_ISSUES item is empty!")
            return False
        else:
            return True

    def checkItem(self, resp):
        if (len(resp.json()['items']) == 0):
            logging.error("GET request %s item is empty!", resp.url)
            return False
        else:
            return True

    def doPatch(self, url, data):
        payload = json.dumps(data)
        resp = requests.patch(url, payload, headers=header)
        if resp.status_code != 200:
            logging.error("PATCH failed %s content:%s", url, resp.content.decode('ascii'))
        self.assertEqual(resp.status_code, 200)
        logging.info('PATCH request %s %d', url, resp.status_code)

    def doPost(self, url, data):
        payload = json.dumps(data)
        resp = requests.post(url, payload, headers=header)
        self.assertEqual(resp.status_code, 201)
        logging.info('POST request %s %d', url, resp.status_code)
        data = json.loads(resp.text)
        return data;

    def doDelete(self, url):
        resp = requests.delete(url, headers=header)
        if resp.status_code != 204:
            logging.error("DELETE failed %s content:%s", url, resp.content.decode('ascii'))
        self.assertEqual(resp.status_code, 204)
        logging.info('DELETE request %s %d', url, resp.status_code)

    if __name__ == '__main__':
        unittest.main()
