import os
import json
import requests
import tornado.web
import tornado.ioloop
import tornado.autoreload
import sys
import asyncio
import psycopg2
import time

# On IBM Cloud Cloud Foundry, get the port number from the environment variable PORT
# When running this app on the local machine, default the port to 8000
#port = int(os.getenv('PORT', 8080))
port=8000
class landingPage(tornado.web.RequestHandler):
    def get(self):
        self.render("static/trial.html")
        
class HomePage(tornado.web.RequestHandler):
    def get(self):
        self.render("static/indexx.html")

class Login(tornado.web.RequestHandler):
    def post(self):
        #base_url = 'https://api.eu-gb.apiconnect.appdomain.cloud/m1ganeshtcscom1543928228162-dev/sb/payments/custReg?acctId='
        # 100000001001 is the only working answer
        #headers = {'Content-Type': 'application/json'}
        print("inside login")
        username = str(self.get_body_argument("uname"))
        print(username)
        pwd = str(self.get_body_argument("pass"))
        print(pwd)
        #end_url= base_url+str(self.get_body_argument("accnt"))
        #req = requests.get(end_url, headers=headers, auth=('701e3938-c7c7-4568-9e3b-d474bfb39700', ''), verify=False)
        #json_out = req.json()
        print("json")
        if username =="admin" and pwd == "adminpass":
            print("success")
            self.render("static/indexx.html")
        else:
            print("no")
            self.render("static/trial.html")
        #print(json_out)
        #self.render("static/genericresp.html",msg=json_out['CSRGRES']['CSRGRES']['MESSAGES'],cname=json_out['CSRGRES']['CSRGRES']['CUSTOMER_NAME'],cid=json_out['CSRGRES']['CSRGRES']['CUSTOMER_ID'],date=json_out['CSRGRES']['CSRGRES']['SYS_DATE'],time=json_out['CSRGRES']['CSRGRES']['SYS_TIME'],bloc="regreq")




class basicRequestHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("static/register.html")



class regRequ(tornado.web.RequestHandler):
    def post(self):
        base_url = 'https://192.86.33.94:19443/cbsrgdbbapi/cusreg?AcctNo='
        # 100000001001 is the only working answer
        #https://192.86.33.94:19443/cbs/cusreg?AcctNo=
        #https://192.86.33.94:19443/cbsrgdbbapi/cusreg?AcctNo=
        headers = {'Content-Type': 'application/json'}
        end_url= base_url+str(self.get_body_argument("accnt"))
        print("before")
        req = requests.get(end_url, headers=headers, auth=('ibmuser', 'ibmuser'), verify=False)
        json_out = req.json()
        print("json")
        print(json_out)
        self.render("static/genericresp.html",msg=json_out['CSRGRES']['CSRGRES']['MESSAGES'],cname=json_out['CSRGRES']['CSRGRES']['CUSTOMER_NAME'],cid=json_out['CSRGRES']['CSRGRES']['CUSTOMER_ID'],date=json_out['CSRGRES']['CSRGRES']['SYS_DATE'],time=json_out['CSRGRES']['CSRGRES']['SYS_TIME'],bloc="regreq")

class basicDeRequestHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("static/deregister.html")

class deRegRequ(tornado.web.RequestHandler):
    def post(self):
        base_url = 'https://api.eu-gb.apiconnect.appdomain.cloud/m1ganeshtcscom1543928228162-dev/sb/payments/custDreg?acctId='
        #base_url = 'https://192.86.33.94:19443/cbscs/cusdereg?AcctNo='
        #'https://gateway.aipc1.cp4i-b2e73aa4eddf9dc566faa4f42ccdd306-0001.us-east.containers.appdomain.cloud/sachinsorg/sandbox/payments/custDreg?acctId='
        # 100000001001 is the only working answer
        headers = {'Content-Type': 'application/json'}
        end_url= base_url+str(self.get_body_argument("accnt"))
        print("dereg")
        req = requests.get(end_url, headers=headers, auth=('ef748535-de65-4edb-a0fd-89f94ed994d3', ''), verify=False)
        json_out = req.json()
        print("dereg req")
        self.render("static/genericresp.html",msg=json_out['CSDGRES']['CSRGRES']['MESSAGES'],cname=json_out['CSDGRES']['CSRGRES']['CUSTOMER_NAME'],cid=json_out['CSDGRES']['CSRGRES']['CUSTOMER_ID'],date=json_out['CSDGRES']['CSRGRES']['SYS_DATE'],time=json_out['CSDGRES']['CSRGRES']['SYS_TIME'],bloc="deregreq")

class basicPayHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("static/pay.html")

class payRequ(tornado.web.RequestHandler):
    def post(self):
        # base_url  = 'https://192.86.33.94:19443/cuspymtauth/cuspay?debitamt='
        # #base_url = 'https://gateway.aipc1.cp4i-b2e73aa4eddf9dc566faa4f42ccdd306-0001.us-east.containers.appdomain.cloud/sachinsorg/sandbox/payments/pymntAuth?acctId='
        base_url =  'https://api.eu-gb.apiconnect.appdomain.cloud/m1ganeshtcscom1543928228162-dev/sb/payments/pymntAuth?acctId='
        	# 100000001001   is the only working answer
        headers = {'Content-Type': 'application/json'}
        acct=str(self.get_body_argument("accnt"))
        end_url= base_url+str(self.get_body_argument("accnt"))+"&debitAmt="+str(self.get_body_argument("debit_amt"))
        req = requests.get(end_url, headers=headers, auth=('ef748535-de65-4edb-a0fd-89f94ed994d3', ''), verify=False)
        json_out = req.json()
        self.render("static/genericresp.html",msg=json_out['CSPYRES']['CSPYRES']['MESSAGES'],cname=json_out['CSPYRES']['CSPYRES']['CUSTOMER_NAME'],hbal=json_out['CSPYRES']['CSPYRES']['HOLD_BALANCE'],lbal=json_out['CSPYRES']['CSPYRES']['LEDGER_BL'],bal=json_out['CSPYRES']['CSPYRES']['AVAILABLE_BALANCE'],cid=json_out['CSPYRES']['CSPYRES']['CUSTOMER_ID'],damt=json_out['CSPYRES']['CSPYRES']['DEBIT_AMOUNT_RES'],tid=json_out['CSPYRES']['CSPYRES']['TRANSACTION_ID'],date=json_out['CSPYRES']['CSPYRES']['SYS_DATE'],time=json_out['CSPYRES']['CSPYRES']['SYS_TIME'],bloc="payauth")
        print("message")
        mes=json_out['CSPYRES']['CSPYRES']['MESSAGES']
        cust_name=json_out['CSPYRES']['CSPYRES']['CUSTOMER_NAME']
        hold_bal=json_out['CSPYRES']['CSPYRES']['HOLD_BALANCE']
        ldgr_bal=json_out['CSPYRES']['CSPYRES']['LEDGER_BL']
        avail_bal=json_out['CSPYRES']['CSPYRES']['AVAILABLE_BALANCE']
        cust_id=json_out['CSPYRES']['CSPYRES']['CUSTOMER_ID']
        sysDate=json_out['CSPYRES']['CSPYRES']['SYS_DATE']
        debitAmt=json_out['CSPYRES']['CSPYRES']['DEBIT_AMOUNT_RES']
        transID=json_out['CSPYRES']['CSPYRES']['TRANSACTION_ID']
        sysTime1=json_out['CSPYRES']['CSPYRES']['SYS_TIME']
        sysTime = sysTime1.replace(".", ":")
        systimestamp=time.ctime()
        try:
            connection = psycopg2.connect(host="dbaas901.hyperp-dbaas.cloud.ibm.com",port=29491,database="admin",user="admin",password="fading2White!!!")
            print("Connected")
            cursor = connection.cursor()
            postgres_insert_query = """ INSERT INTO "TCS-Schema"."PayLog"(cust_name, message, "timestampSys","Customer_ID", "Response_Date", "Response_Time", "Trans_ID","debitAmt", "Balance", hold_bal, ledger_bal,acct_no) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            record_to_insert = (cust_name,mes,systimestamp,cust_id,sysDate,sysTime,transID,debitAmt,avail_bal,hold_bal,ldgr_bal,acct)
            cursor.execute(postgres_insert_query, record_to_insert)
            
            connection.commit()
            count = cursor.rowcount
            print(count, "Record inserted successfully into Paylog table")
            print(mes)
            
        except (Exception, psycopg2.Error) as error:
            print("Failed to insert record into mobile table", error)
        finally:
            # closing database connection.
            if connection:
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")



class History(tornado.web.RequestHandler):
    def get(self):
        self.render("static/history.html")
    


class HistoryAction(tornado.web.RequestHandler):
    def post(self):

        try:
            acct=str(self.get_body_argument("accnt"))
            connection = psycopg2.connect(host="dbaas901.hyperp-dbaas.cloud.ibm.com",port=29491,database="admin",user="admin",password="fading2White!!!")
            print("Connected to history tran")
            cursor = connection.cursor()
            print("Connected to history tran")
            postgres_insert_query = """ SELECT  cust_name, message, "timestampSys","Customer_ID", "Response_Date", "Response_Time", "Trans_ID","debitAmt", "Balance", hold_bal, ledger_bal,acct_no from "TCS-Schema"."PayLog" """
            print("Connected to history tran")
            #record_to_insert = (cust_name,mes,systimestamp,cust_id,sysDate,sysTime,transID,debitAmt,avail_bal,hold_bal,ldgr_bal,acct)
            cursor.execute(postgres_insert_query) 
            print("Connected to history tran")
            array_records=cursor.fetchall()
            print("Connected to history tran")
            for i in array_records:
                print(i[0])
            self.render("static/histresp.html",array_record=array_records,bloc="history")
            print("message")
            print( "Record inserted successfully into Paylog table")
            
            
        except (Exception, psycopg2.Error) as error:
            print("Failed ", error)
        finally:
            # closing database connection.
            if connection:
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")








class basicRevHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("static/reversal.html")

class revRequ(tornado.web.RequestHandler):
    def post(self):
        # base_url = 'https://192.86.33.94:19443/cusdereg/AccountNo?acctno='
        #base_url = 'https://gateway.aipc1.cp4i-b2e73aa4eddf9dc566faa4f42ccdd306-0001.us-east.containers.appdomain.cloud/sachinsorg/sandbox/payments/pymntRev?acctId='
        base_url = 'https://api.eu-gb.apiconnect.appdomain.cloud/m1ganeshtcscom1543928228162-dev/sb/payments/pymntRev?acctId='
        # 100000001001 is the only working answer
        headers = {'Content-Type': 'application/json'}
        end_url= base_url+str(self.get_body_argument("accnt"))+"&transId="+str(self.get_body_argument("trans"))+"&revAmt="+str(self.get_body_argument("debit_amt"))
        req = requests.get(end_url, headers=headers, auth=('ef748535-de65-4edb-a0fd-89f94ed994d3', ''), verify=False)
        json_out = req.json()
        self.render("static/genericresp.html",msg=json_out['CSREVRES']['CSREVRES']['MESSAGES'],cname=json_out['CSREVRES']['CSREVRES']['CUSTOMER_NAME'],hbal=json_out['CSREVRES']['CSREVRES']['HOLD_BALANCE'],lbal=json_out['CSREVRES']['CSREVRES']['LEDGER_BL'],bal=json_out['CSREVRES']['CSREVRES']['AVAILABLE_BALANCE'],cid=json_out['CSREVRES']['CSREVRES']['CUSTOMER_ID'],credamt=json_out['CSREVRES']['CSREVRES']['CREDIT_AMOUNT_RES'],tid=json_out['CSREVRES']['CSREVRES']['TRANSACTIONS_ID'],date=json_out['CSREVRES']['CSREVRES']['SYS_DATE'],time=json_out['CSREVRES']['CSREVRES']['SYS_TIME'],bloc="payrev")

class basicBatchHandler(tornado.web.RequestHandler):
    def get(self):
        print("I'm listening on port specified")
        self.render("static/batchapi.html")

class batchrequ(tornado.web.RequestHandler):
    def post(self):
        base_url = 'https://192.86.33.94:19443/batchpgm/cbs?AcctNo='
        # 100000001001 is the only working answer
        headers = {'Content-Type': 'application/json'}
        end_url= base_url+str(self.get_body_argument("accnt"))
        req = requests.get(end_url, headers=headers, auth=('ibmuser', 'ibmuser'), verify=False)
        json_out = req.json()
        print("json")
        print(json_out)
        self.render("static/genericresp.html",msg=json_out['HMSBATCHOperationResponse']['svc_resp_variables'],bloc="batch")


class basicDVMHandler(tornado.web.RequestHandler):
    def get(self):
        print("I'm listening on port specified")
        self.render("static/dvmapi.html")

class dvmRequ(tornado.web.RequestHandler):
    def post(self):
        base_url = 'https://192.86.33.94:19443/dvmget/dvmget'
        # 100000001001 is the only working answer
        headers = {'Content-Type': 'application/json'}
        #end_url= base_url+str(self.get_body_argument("accnt"))
        req = requests.get(base_url, headers=headers, auth=('ibmuser', 'ibmuser'), verify=False)
        json_out = req.json()
        print("json")
        print(json_out)
        self.render("static/dvmresp.html",type0=json_out['Records'][0]['account_type'],name0=json_out['Records'][0]['account_name'],stat0=json_out['Records'][0]['account_status'],id0=json_out['Records'][0]['customer_id'],acct0=json_out['Records'][0]['account_no'],branch0=json_out['Records'][0]['branch'],type1=json_out['Records'][1]['account_type'],name1=json_out['Records'][1]['account_name'],stat1=json_out['Records'][1]['account_status'],id1=json_out['Records'][1]['customer_id'],acct1=json_out['Records'][1]['account_no'],branch1=json_out['Records'][1]['branch'],bloc="dvm")




if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/", landingPage),
        (r"/register", basicRequestHandler),
        (r"/regrequ", regRequ),
        (r"/deregister", basicDeRequestHandler),
        (r"/deregrequ", deRegRequ),
        (r"/paymentauth", basicPayHandler),
        (r"/payrequ", payRequ),
        (r"/paymentrevauth", basicRevHandler),
        (r"/revRequ", revRequ),
        (r"/batchapi", basicBatchHandler),
        (r"/batchrequ", batchrequ),
        (r"/dvmapi", basicDVMHandler),
        (r"/dvmreq", dvmRequ),
        (r"/login", Login),
        (r"/homepage", HomePage),
        (r"/history", History),
        (r"/historyaction", HistoryAction),
    ])
    print("commit")
    if sys.platform == 'win32':
    	asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
	    #print("inside win")
    #server=HTTPServer(app)
    app.listen(port)
    # TODO remove in prod
    tornado.autoreload.start()
    print("I'm listening on port specified")
    print(port)
    tornado.ioloop.IOLoop.current().start()
