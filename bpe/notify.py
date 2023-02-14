from lib.mail import Mailing
import datetime


class Notification:

    def __init__(self, mail_type, to_email, cc_email, user_name, pass_word, successOrder):
        self.to_email = to_email
        self.cc_email = cc_email
        self.mail_type = mail_type
        self.user_name = user_name
        self.pass_word = pass_word
        self.digest_log = []
        self.EOM = "199012"
        self.totalPOs = 0
        self.allGood = 0
        self.monkeyWrench = 0
        self.successOrder = successOrder

    def set_Success_Fail(self, goodie, bumpie):
        self.allGood += goodie
        self.monkeyWrench += bumpie

    def set_EOM(self, eom):
        self.EOM = eom

    def set_tPO(self, allofthem):
        self.totalPOs = allofthem

    def no_lines_notify(self, po_num):
        # m = Mailing(self.mail_type,self.user_name,self.pass_word)
        # m.setSubject("AutoNotify::No lines for PO:" + str(po_num))
        # html = "<html><head></head><body>Hi User!<br/><br/>It is observed that Purchase Order:"+str(po_num)+" does not have any lines.<br/><br/>Thank You,<br/>Regards,<br/>Automation Script.</body></html>"
        # m.sendHTMLMail(self.to_email,html)
        # m.close()
        self.add_to_digest("no lines", po_num, str(
            po_num)+" <b>Missing lines: <br/>")
        self.set_Success_Fail(0, 1)

    def totals_did_not_match_notify(self, po_num, details_total, doc_total):
        # m = Mailing(self.mail_type,self.user_name,self.pass_word)
        # m.setSubject("AutoNotify::Totals do not match for PO:" + str(po_num))
        # html = "<html><head></head><body>Hi User!<br/><br/>It is observed that Purchase Order["+str(po_num)+"]'s totals do not match.<br/><br/> <b>Details Total:</b>"+str(details_total)+"<br/><b>Document Total:</b>"+str(doc_total)+"<br/><br/>Thank You,<br/>Regards,<br/>Automation Script.</body></html>"
        # m.sendHTMLMail(self.to_email,html)
        # m.close()
        self.add_to_digest("totals mismatch", po_num, str(po_num)+" <b>Total mismatch:</b> <b>Details Total:</b>" +
                           str(details_total)+"<br/><b>Document Total:</b>"+str(doc_total)+"<br/>")
        self.set_Success_Fail(0, 1)

    def publish_failed_notify(self, po_num):
        # m = Mailing(self.mail_type,self.user_name,self.pass_word)
        # m.setSubject("AutoNotify::Failed publishing the PO:" + str(po_num))
        # html = "<html><head></head><body>Hi User!<br/><br/>It is observed that publishing of Purchase Order:"+str(po_num)+" had failed.<br/><br/>Thank You,<br/>Regards,<br/>Automation Script.</body></html>"
        # m.sendHTMLMail(self.to_email,html)
        # m.close()
        self.add_to_digest("publish failed", po_num,
                           str(po_num)+" <b>failed.</b><br/>")
        self.set_Success_Fail(0, 1)

    def publish_failed_notify_unknown_error(self, po_num, msg):
        # m = Mailing(self.mail_type,self.user_name,self.pass_word)
        # m.setSubject("AutoNotify::Failed publishing the PO:" + str(po_num))
        # html = "<html><head></head><body>Hi User!<br/><br/>It is observed that publishing of Purchase Order:"+str(po_num)+" had failed.<br/><b>Exception message:</b>"+msg+"<br/><br/>Thank You,<br/>Regards,<br/>Automation Script.</body></html>"
        # m.sendHTMLMail(self.to_email,html)
        # m.close()
        self.add_to_digest("unknown error", po_num, str(
            po_num)+" <b>erred with message:</b> "+msg+".<br/>")
        self.set_Success_Fail(0, 1)

    def add_to_digest(self, er_type, po_num, msg):
        this_msg = [er_type, po_num, msg]
        self.digest_log.append(this_msg)

    def outbox_Msgs1(self):
        dt = datetime.datetime.now()
        print("test 1")
        if (self.digest_log):
            print("test if 1")
            print("sent to "+self.to_email)
            html = "<html><head></head><body>Hi User,<br/><br/>"
            # html += "Here is the digest for the ap automation on "+dt.strftime('%c')+" for "+self.EOM+".<br/><br/>"
            html += "Automation triggered at " + \
                dt.strftime('%c')+" with the EOM cutoff set as " + \
                self.EOM+".<br/><br/>"
            # html += "A total of "+str(self.totalPOs)+" were looked into and following POs has problems.<br/><br/>"
            html += str(self.totalPOs) + \
                " invoices processed from Ferret via AP Automation<br/><br/>"
            html += str(self.allGood) + \
                " processed are OK with no issues and need to be Posted in BasePlan - these PO's are: <br/><br/>"
            if(len(self.successOrder)):
                for i in range(0, len(self.successOrder)):
                    html += self.successOrder[i] + "<br/>"
                html += "<br/>"
            else:
                html += "no successful PO found.<br/><br/>"
            html += "But "+str(self.monkeyWrench) + \
                " of the following issues were encountered <br/><br/>"
            for indx, item in enumerate(self.digest_log):
                html += item[2]
            html += "<br/><br/>Thank You,<br/>Regards,<br/>Automation Script.</body></html>"
            m = Mailing("gmail", self.user_name, self.pass_word)
            m.setSubject(
                "AutoNotify::Mail digest from AP Automation for cutoff "+self.EOM)
            succss = m.sendHTMLMail(self.to_email, self.cc_email, html)
            m.close()
            if (succss):
                print("test if 2")
                return 1
            else:
                print("else 2")
                return 0
