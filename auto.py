
from pywinauto.application import Application
from pywinauto import backend
from pywinauto import mouse
from pywinauto import win32structures
import time
import os
import sys

from lib.Gen import Gen
from lib.mail import Mailing
from lib.log import Log
from bpe.login import Login
from bpe.bpe import BPE
from bpe.inv import Invoicing
from bpe.ss import SupplierSelection
from bpe.pa import PostAll
from bpe.pop import Popup
from bpe.notify import Notification

from lib.db import DB
from lib.prop import Prop

import configparser
import datetime

def arraySuccessOrder(order):
    successOrder.append(order)
    return successOrder

def emptySuccessOrder():
    successOrder.clear()

def startProcessing(p):
    g = Gen(backend)
    g.start_app(p.get("general", "app_url"))

    lg = Login()
    lg.setLog(l)
    lg.log_user(p.get("general", "app_user"), p.get("general", "app_pass"))
    return g

def updateDocStatus(docnumber, status):
    dbP = Prop("settings.cfg")
    dbU = DB("SQLSERVER")
    dbhost = p.get("db", "host")
    dbname = p.get("db", "db")
    dbuser = p.get("db", "user")
    dbpass = p.get("db", "pass")
    if (dbU.connect(dbhost, dbname, dbuser, dbpass)):
        dbU.update("update tblDocument set DocStatusID='" +
                   str(status)+"' where DocField4='"+str(docnumber)+"'")
        dbU.close()
        l.add("Updated Ferret for PO" +
              str(docnumber) + " to status" + str(status))
        return dbU.getRowCount()
    else:
        print("Connection error")

def sync():
    dbP = Prop("settings.cfg")
    dbU = DB("SQLSERVER")
    dbhost = p.get("db", "host")
    dbname = p.get("db", "db")
    dbuser = p.get("db", "user")
    dbpass = p.get("db", "pass")
    syncrc = 0
    syncsql = """\
        DECLARE @RC int;
        EXECUTE @RC =  [FerretAP].[dbo].[SynchPOfromBasePlan];
        SELECT @RC AS rc;
        """

    if (dbU.connect(dbhost, dbname, dbuser, dbpass)):
        print("synching")
        dbU.executeproc("exec [FerretAp].[dbo].[SynchPOfromBasePlan]")
        dbU.close()
        l.add("Synched" + str(syncrc))
    else:
        print("Connection error")

successOrder = []

p = Prop("settings.cfg")
p.setOption("general", "stop", "no")
dt = datetime.datetime.now()
logLoc = p.get("locations", "logs")
today = str('%02d' % dt.day)+"/"+str('%02d' % dt.month)+"/"+str(dt.year)
logFileName = logLoc + "/" + "Log_" + \
    str('%02d' % dt.day)+"_"+str('%02d' % dt.month)+"_"+str(dt.year) + ".log"
l = Log(logFileName)
sync()
l.add("-----------------START PO Proceesing-----------------------")
period = str(dt.year) + str('%02d' % dt.month)
print("Today is:" + today + " and period is:" + period)
# Start the log with date details and store in a file.
db = DB("SQLSERVER")
dbhost = p.get("db", "host")
dbname = p.get("db", "db")
dbuser = p.get("db", "user")
dbpass = p.get("db", "pass")

statusToSearch = p.get("general", "status_to_search")

notifyTo = p.get("notify", "notify_to")
copyTo = p.get("notify", "copy_to")
senderEmail = p.get("notify", "sender_email")
senderEmailPass = p.get("notify", "sender_email_pass")

n = Notification("gmail", notifyTo, copyTo, senderEmail, senderEmailPass, successOrder)

print("Status to search["+statusToSearch+"]")
emptySuccessOrder()

if (db.connect(dbhost, dbname, dbuser, dbpass)):
    db.execute("select * from CRD_Parameters")
    db.setColumns({"Period": 0})
    db.getRow(0)
    period = db.getValue("Period")
    n.set_EOM(period)

    l.add("Retrieved crd_parameters period as :" + str(period))

    db.execute("select * from PO_Ferret where Status='"+statusToSearch +
               "' AND FORMAT(CONVERT(DATE,INVOICE_DATE,103),'yyyyMM') <= '" + period+"' AND doctotal IS NOT NULL ORDER BY PO_Number")
    # db.execute("select * from PO_Ferret where Po_number<=157974 AND status='approved' and doctotal is not null")
    # db.execute("select * from PO_Ferret where po_number=152783")

    db.setColumns({"Supplier": 0, "PO_Number": 1, "Status": 2, "Ordered_By": 3, "BranchCode": 4, "Site": 5, "Delivery_Addresss": 6, "Warehouse": 7,
                  "Authorized_By": 8, "UserConfirmed": 9, "DateCreated": 10, "POType": 11, "PERIOD": 12, "Invoice_No": 13, "DocTotal": 14, "invoice_date": 15})

    # db.execute("select * from PO_Ferret where Status='"+statusToSearch+"' and PERIOD<='"+period+"' ORDER BY PO_Number")
    # db.setColumns({"Supplier":0,"PO_Number":1,"Status":2,"Ordered_By":3,"BranchCode":4,"Site":5,"Delivery_Addresss":6,"Warehouse":7,"Authorized_By":8,"UserConfirmed":9,"DateCreated":10,"POType":11,"PERIOD":12})

    # print("Number of records are:"+str(db.rowCount))
    rowCnt = db.rowCount
    ind = 0

    n.set_tPO(rowCnt)

    # print(period)

    g = startProcessing(p)
    l.add("Started iterating through " + str(rowCnt) + " number of POs")
    for ind in range(0, rowCnt):
        try:
            stopProcessing = p.get("general", "stop")
            if (stopProcessing == "yes"):
                l.add("User requested to stop processing")
                g.kill_app()
                break
            match = False
            db.getRow(ind)

            po_num = str(db.getValue("PO_Number"))
            l.add("Picked PO["+str(ind)+"]: " + po_num + " for processing")
            supplier = str(db.getValue("Invoice_No"))
            doctotal = str(db.getValue("DocTotal"))
            invoice_date = str(db.getValue("invoice_date"))
            # po_num = "143662"

            be = BPE()
            be.setLog(l)
            be.nav("Invoicing")
            l.add("navbar invoicing")

            invoicing = Invoicing()
            invoicing.setLog(l)
            invoicing.click_tool_bar("Add New")

            invoicing.select_po_number(po_num)
            invoicing.set_inv_det_date(invoice_date)
            invoicing.set_inv_recd_date(today)
            # print(supplier)
            invoicing.set_supplier_as_ref(supplier)
            ########################################
            try:
                l.add("pop up error")
                errP = Popup(invoicing, l)
                errMsg = errP.get_popup_message()
                if (errP.yes_btn().exists()):
                    errP.click_yes()
                elif (errP.ok_btn().exists()):
                    errP.click_ok()
            except Exception as e:
                print("no issues at all - fix v1.0 - 1")
            #######################################
            invoicing.set_document_total(doctotal)
            #######################################
            try:
                l.add("pop up error 2")
                errP = Popup(invoicing, l)
                errMsg = errP.get_popup_message()
                if (errP.yes_btn().exists()):
                    errP.click_yes()
                elif (errP.ok_btn().exists()):
                    errP.click_ok()
            except Exception as e:
                print("no issues at all - fix v1.0 - 2")
            # error pops up upon entering the doctotal
            # have to press yes, if any
            # invoicing.accept_Duplicate_Records()
            #######################################
            invoicing.select_action("Select")

            invoicing = Invoicing()
            invoicing.setLog(l)
            ss = SupplierSelection(invoicing, l)
            l.add("invoicing supplier selection")
            # ss.select_filter_all()

            if (ss.record_count() > 0):
                l.add("Records are available")
                ss.click_select_all_btn()
            else:
                l.add("records are not available")
                n.no_lines_notify(po_num)

            ss.click_ok_btn()
            invoicing = Invoicing()
            invoicing.setLog(l)
            l.add("get detail total")
            detailsTotal = invoicing.get_details_total()
            docNo = invoicing.get_doc_id()
            documentTotal = (invoicing.get_document_total())
            if (detailsTotal == documentTotal and (documentTotal != "$0.00")):
                l.add("Totals are matching")
                match = True
            else:
                l.add("Totals are not matching")
                n.totals_did_not_match_notify(
                    po_num, detailsTotal, documentTotal)

            invoicing = Invoicing()
            invoicing.setLog(l)
            invoicing.click_tool_bar("Post Current")
            l.add("posting current")

            if (match == False):
                l.add("expecting error message as totals are not matching")
                popup = Popup(invoicing, l)
                popup.click_yes()
                n.publish_failed_notify(po_num)
                popup = Popup(invoicing, l)
                popup.click_ok()
            else:
                l.add("expecting success post message as totals match")
                popup = Popup(invoicing, l)
                popup.click_ok()
                l.add("PO#:" + str(po_num) + " is posted successfully")
                cnt = updateDocStatus(po_num, 16)
                cnt = 1
                if (cnt == 1):
                    l.add("PO#:" + str(po_num) + " successfully updated status for docid:" +
                          str(docNo)+" to 16 n tblDocument table.")
                    n.set_Success_Fail(1, 0)
                    successOrder = arraySuccessOrder(po_num)
                else:
                    l.add("PO#:" + str(po_num) + " status updation for docid:" +
                          str(docNo)+" in tblDocument failed.")

            invoicing = Invoicing()
            invoicing.setLog(l)
            l.add("invoicing close")
            invoicing.click_tool_bar("Close")

        except Exception as e:
            l.add("Aborted processing PO#:" + str(po_num))
            l.add("Exception details:" + str(e))
            errMsg = "Unexpected error occurred when processing po#:" + po_num
            try:
                errP = Popup(invoicing, l)
                errMsg = errP.get_popup_message()
                l.add("error Message inside try block:" + errMsg)
                if (errP.yes_btn().exists()):
                    errP.click_yes()
                    l.add("yes button clicked")
                elif (errP.ok_btn().exists()):
                    l.add("no button clicked")
                    errP.click_ok()

            except Exception as e1:
                l.add("Exception occurred to get message from error popup if any")

            n.publish_failed_notify_unknown_error(po_num, errMsg)
            l.add("publish failed")
            l.add(errMsg)
            g.kill_app()
            # g = startProcessing(p)

    g.kill_app()
    db.close()

l.add("-----------------END PO Proceesing-----------------------")
if (n.outbox_Msgs1()):
    l.add("test if ")
    l.add("Digest sent")
else:
    l.add("Failed sending consolidated mail")
    l.add("test else ")