'''
Created on 2017-9-6
This script do one thing : parse the violation csv file and upload the violations to apex rest services.
the violation csv file is download form
https://apex.oraclecorp.com/pls/apex/f?p=19568:943:6268616912122:::CIR:IREQ_PRODUCT_FAMILY,IREQ_AUDIT_INITIATIVE,IREQ_AUDIT_CATEGORY:hcm,Coding,Category%202
login to the page then select columns add file_path then download.
Notice!!! the url maybe changed.


So if developer can not use the script, they can also write a script with their familiar language.
@author: longjiabo
'''
import csv
import json
import queue
import re
import threading
import time
from datetime import datetime

import requests

# threads number
concurrent = 50
# apex rest url
RESTURL = 'https://apex.oraclecorp.com/pls/apex/caproject/nwa/violations'
# workspace vp dict
WORKSPACE_VP = {'HcmAbsences.jws': 'Lewis', 'HcmAnalytics.jws': 'Subraya', 'HcmBenefits.jws': 'Reza',
                'HcmCompensation.jws': 'Shenoy', 'HcmCoreSetup.jws': 'Shared*', 'HcmCore.jws': 'Shenoy',
                'HcmEngagement.jws': 'Hernan', 'HcmEss.jws': 'Shared*', 'HcmPayroll.jws': 'Lewis',
                'HcmRecruiting.jws': 'Nagaraj', 'HcmSchedules.jws': 'Lewis', 'HcmSemSearch.jws': 'Reza',
                'HcmTalent.jws': 'Shenoy', 'HcmTime.jws': 'Lewis', 'HcmWorkforceMgmt.jws': 'Shenoy',
                'HcmWorkforceReputation.jws': 'Reza', 'Tablet.jws': 'Hernan', 'HcmTap.jws': 'Hernan'}
# rule_id phase dict
RULE_PHASE = {'donot-use-blacklist-apis-File_AdfModel_143': '1.1',
              'donot-use-blacklist-apis-1-1-File_AdfModel_143': '1.1',
              'donot-use-blacklist-apis-1-2-File_AdfModel_143': '1.2',
              'donot-use-blacklist-apis-1-3-File_AdfModel_143': '1.3',
              # 'oracle.jdeveloper.audit.export.concealed-api': 'Concealed API'}
              'oracle.jdeveloper.audit.export.concealed-api': 'Concealed API',
              'oracle.apps.ta.only-allow-whitelist-apis-pending-File_AdfModel_143': "Whitelist API"}
# csv titles
CSV_TITLE = ["Initiative", "Rule Name", "Rule Id", "Mandated For", "RemainingDays", "GSCC Standard", "Family",
             "Workspace", "Project", "File Name", "Line Number", "Error Text______________________________",
             "Audit Category", "ADE Label"]
# alias of csv titles which will be used for post data
TITLE = [{'name': 'Workspace', 'index': 7}, {'name': 'Project', 'index': 8}, {'name': 'File_Name', 'index': 9},
         {'name': 'Line_Number', 'index': 10}, {'name': 'Error_Text', 'index': 11}, {'name': 'ADE_Label', 'index': 13},
         {'name': 'Rule_Id', 'index': 2}]

# phase api object dict
api_v2 = {"1.1": [{'applyViewCriteria(': 'oracle.jbo.server.ViewObjectImpl, oracle.jbo.ViewObject'},
                  {'applyViewCriteria(': 'oracle.jbo.server.ViewObjectImpl, oracle.jbo.ViewObject'},
                  # {'setNamedWhereClauseParam(':'oracle.jbo.server.ViewObjectImpl, oracle.jbo.RowSet'},
                  {'setWhereClause(': 'oracle.jbo.server.ViewObjectImpl'},
                  {'addWhereClause(': 'oracle.jbo.server.ViewObjectImpl'},
                  {'commit(': 'oracle.jbo.server.DBTransactionImpl'},
                  {'rollback(': 'oracle.jbo.server.DBTransactionImpl'}],
          '1.2': [{'setApplyViewCriteriaName(': 'oracle.job.server.ViewObjectImpl'},
                  {'setApplyViewCriteriaNames(': 'oracle.job.server.ViewObjectImpl'},
                  {'clearViewCriterias(': 'oracle.job.server.ViewObjectImpl'},
                  {'setQuery(': 'oracle.job.server.ViewObjectImpl'},
                  {'setNestedSelectForFullSql(': 'oracle.job.server.ViewObjectImpl'},
                  {'setFullSqlMode(': 'oracle.job.server.ViewObjectImpl'},
                  {'setAssociationConsistent(': 'oracle.job.server.ViewObjectImpl'},
                  {'clearVariables(': 'oracle.jbo.VariableManager'},
                  {'populateAttribute(': 'oracle.jbo.server.ViewRowImpl, oracle.jbo.server.EntityImpl'},
                  {'getApplicationModule(': 'oracle.job.server.ViewObjectImpl, oracle.jbo.server.ViewRowImpl'},
                  ],
          '1.3': [{'getRow(': 'oracle.jbo.server.ViewObjectImpl, oracle.jbo.RowIterator'},
                  {'lock(': 'oracle.jbo.server.ViewRowImpl'},
                  {'afterCommit(': 'oracle.jbo.server.EntityImpl'},
                  {'setPostedToDB(': 'oracle.jbo.server.EntityImpl'},
                  {'setSelectClause(': 'oracle.jbo.server.ViewObjectImpl'},
                  {'reconnect(': 'oracle.jbo.server.DBTransaction'},
                  {'setClearCacheOnRollback(': 'oracle.jbo.server.DBTransactionImpl'},
                  {'setUseGlueCode(': 'oracle.jbo.server.ViewDefImpl'},
                  {'executeCommand(': 'oracle.jbo.server.ApplicationModuleImpl'}]}

api_dict = {}
q = queue.Queue()
threads = []
num = 0
risky = {}


def download_csv(session, url, path):
    r = session.get(url, stream=True)
    if r.status_code == 200:
        with open(path, 'wb') as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)


def download(category, url):
    date = datetime.now().strftime("%Y-%m-%d-%H-%M")
    file = "%s-%s.csv" % (category, date)
    if not url:
        url = "https://apex.oraclecorp.com/pls/apex/f?p=19568:943::IR_default::CIR:IREQ_PRODUCT_FAMILY,IREQ_AUDIT_INITIATIVE,IREQ_AUDIT_CATEGORY:hcm,Coding," + category
    session, response = login_oracle.login(url, "jiabo.long@oracle.com", "Ljbbushi2b")
    vals = response.url.split("=")[1].split(":")
    app, page, apex_session = (vals[0], vals[1], vals[2])
    u = "https://apex.oraclecorp.com/pls/apex/f?p=%s:%s:%s:CSV::::" % (app, page, apex_session)
    download_csv(session, u, file)
    return file


def read_risky():
    with open('Risk.csv') as f:
        f_csv = csv.reader(f)
        next(f_csv)
        for row in f_csv:
            if row[1] != 'hcm':
                continue
            risky[row[2]] = row[4]


def read_csv(path):
    with open(path) as f:
        f_csv = csv.reader(f)
        next(f_csv)
        result = []
        for row in f_csv:
            data = {}
            for t in TITLE:
                data[t['name']] = row[(t['index'])]
            flag = parse(data)
            if flag:
                result.append(data)
        return result


def get_phase(rule_id):
    for r in RULE_PHASE:
        if r in rule_id:
            return RULE_PHASE[r]


def parse(data):
    rule_id = data['Rule_Id'].strip()
    workspace = data['Workspace'].strip()
    phase = get_phase(rule_id)
    if phase:
        data['Phase'] = phase
        for k, v in WORKSPACE_VP.items():
            if workspace in k:
                data['VP'] = v
                parse_risky(data)
                return parse_api(data)
        print(workspace)
    return False


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


def parse_risky(data):
    # data['risky'] = "Less Risky"
    # data['NON_WHITELIST_APIS'] = "ApplCore"
    data['risky'] = "TBD"
    pattern = 'is (concealed|restricted): (.*) Audit rule info'
    error = data['Error_Text']
    m = re.search(pattern, error, re.I)
    if m:
        st = m.group(2)
        if st in risky:
            data['risky'] = risky[st]


def parse_api(data):
    error = data['Error_Text'].strip().lower()
    for i in api_dict.keys():
        if i.lower().strip() in error:
            data['obj'] = api_dict[i]['obj']
            data['api'] = i + ")"
            return True
    data['obj'] = ""
    data['api'] = ""
    return True


def read_api():
    for k, v in api_v2.items():
        for i in v:
            for n, m in i.items():
                api_dict[n] = {'Phase': k, 'obj': m}


def send_apex(data):
    s = json.dumps({'data': data})
    header = {'text': s}
    try:
        r = requests.post(RESTURL, headers=header)
        if r.text:
            print(r.text)
            send_apex(data)
    except:
        send_apex(data)


def do_work():
    while True:
        l = q.get()
        if l is None:
            q.task_done()
            break
        global num
        num = num + 1
        print("result", num)
        send_apex(l)
        # print(s)
        q.task_done()


def upload_violations(file):
    print(time.time())
    read_api()
    read_risky()
    result = read_csv(file)
    print(len(result))

    for i in range(concurrent):
        t = threading.Thread(target=do_work)
        t.start()
        threads.append(t)
    for l in chunks(result, 5):
        q.put(l)
    q.join()
    print(time.time())
    for i in range(concurrent):
        q.put(None)
    for t in threads:
        t.join()
    print(time.time())


def process_category(category, url=None):
    file = download(category, url)
    upload_violations(file)


def del_apex_violation_data():
    requests.delete("https://apex.oraclecorp.com/pls/apex/caproject/nwa/violations")


if __name__ == '__main__':
    # del_apex_violation_data()
    # process_category("Whitelist")
    # concealed_url = "https://apex.oraclecorp.com/pls/apex/f?p=19568:943:6268616912122:::CIR:IREQ_PRODUCT_FAMILY,IREQ_AUDIT_INITIATIVE,IREQ_AUDIT_CATEGORY:hcm,Coding,Category%202"
    # # concealed_url = "https://apex.oraclecorp.com/pls/apex/f?p=19568:943:106939093031005:::CIR:IREQ_PRODUCT_FAMILY,IREQ_RULE_ID:hcm,oracle.jdeveloper.audit.export.concealed-api"
    # process_category("Concealed API", concealed_url)
    upload_violations("missing_concealed_applcore (002).csv")