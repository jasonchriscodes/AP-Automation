from pywinauto.application import Application 
from pywinauto import backend
from pywinauto import mouse
from pywinauto import win32structures

from lib.Gen import Obj
import time
import os,sys

class Invoicing(Obj):
    def __init__(self,par=None):
        super(Invoicing,self).__init__("Baseplan Enterprise - Supplier Invoices/Credit Notes",par)        

    def toolBar(self):
        return self.win.child_window(title="Toolbar", control_type="ToolBar")

    def click_tool_bar(self,btn_name):
        #self.win.child_window(title=btn_name,control_type='Button').print_control_identifiers()
        #self.win.print_control_identifiers()
        #self.win.child_window(title="Toolbar", control_type="ToolBar").print_control_identifiers()
        clicked = False
        eles = self.toolBar().children()

        print("Number of buttons in toolbar are:" + str(len(eles)))
        myException = None
        try:
            withLabels = True
            if ( self.toolBar().child_window(title=btn_name,control_type='Button').exists()):    
                print('Entered main if of tool bar that is identifying with button name')  
                
                #self.toolBar().child_window(title=btn_name,control_type='Button').click()
                rect = self.win.child_window(title="Toolbar", control_type="ToolBar").child_window(title=btn_name,control_type='Button').rectangle()
                mouse.click(coords=(rect.left+10,rect.top+5))
                clicked = True
            else:
                withLabels = False
                #print("Button name:"+btn_name)
                if(len(eles)==7):
                    print("Entered 7 buttons toolbar")
                    if(btn_name == "Add New"):        
                        print("Entered Add New Button if condition")            
                        eles[5].draw_outline(colour='red',thickness=1)
                        eles[5].click()
                        print("clicked add new button")
                        clicked = True
                    else:
                        print("Enterd else condition")                
                elif (len(eles)==15):
                    print("Entered 15 buttons toolabr")
                    if(btn_name=="Post Current"):
                        eles[14].draw_outline(colour='red',thickness=3)
                        eles[14].click()
                        clicked = True
                    elif (btn_name=="Close"):  
                        eles[0].draw_outline(colour='red',thickness=3)
                        eles[0].click()
                        clicked = True
                    else:
                        print("entered else in 15 elemetns tool bar")
                elif (len(eles)==13):
                    print("Entered 13 buttons toolbar")
                    if (btn_name=="Close"):  
                        eles[0].draw_outline(colour='red',thickness=3)
                        eles[0].click()
                        clicked = True
                elif (len(eles)==14):
                    print("Entered 13 buttons toolbar")
                    if (btn_name=="Close"):  
                        eles[0].draw_outline(colour='red',thickness=3)
                        eles[0].click()
                        clicked = True

        except Exception as e:
            print("Exception occured when labels are available:" + str(withLabels))
            print ("Exception details:" + str(e))
            if(withLabels):
                #self.win.print_control_identifiers()
                if(btn_name=="Post Current"):
                    print("Clicking with duplicate option")
                    self.win.PostCurrent2.draw_outline(colour='red',thickness=1)
                    self.win.PostCurrent2.click()
                    clicked = True
                    
            else:
                self.l.add("Exception occured when toolbar icon is not identified by labels")
        if(clicked):
            self.l.add("Clicked tool bar icon:" + btn_name)
        else:
            self.l.add("Could not click the icon:" + btn_name)
            #raise e

    def set_supplier_as_ref(self,supplier):
        ###################### am working here####kkkk#######
        #print(supplier)
        self.win.print_control_identifiers()
        try:
            ref = self.win.child_window(title="Pay Ref:", auto_id="txtRef", control_type="Edit")
            self.type_and_tab(ref,supplier)  
            self.l.add("Entered supplier:" + supplier + " in Ref field")
        except Exception as e:
            self.l.add("Problem occured entering the reference info")
            raise e


    def select_po_number(self,ponumber):
        try:
            cb = self.win.child_window(auto_id="tlpPONo", control_type="Pane").child_window(auto_id="BPPONumber", control_type="ComboBox")     
            self.type_and_tab(cb,ponumber)   
            """
            self.click_element(cb)
            self.type_element(cb,ponumber)
            self.type_element(cb,'{TAB}')
            """
            self.l.add("Entered PO#:" + ponumber + " in PO field")
        except Exception as e:
            self.l.add("Problem occured to enter PO#: "+ponumber+" for retrieving details")
            raise e

    def inv_date_recd(self):
        return self.win.child_window(auto_id="txtDateReceived", control_type="Edit")

    def set_inv_recd_date(self,dateValue):
        try:
            self.inv_date_recd().set_text(dateValue)        
            self.inv_date_recd().type_keys('{TAB}')
            self.l.add("Entered \"" + dateValue + " \" in Received date")
        except Exception as e:
            self.l.add("Problem occurred to enter \"" + dateValue + " \" in Received date")
            raise e

    def inv_det_date(self):
        return self.win.child_window(auto_id="txtDate", control_type="Edit")

    def set_inv_det_date(self,dateValue):
        try:
            self.inv_det_date().set_text(dateValue)        
            self.inv_det_date().type_keys('{TAB}')
            self.l.add("Entered \"" + dateValue + " \" in Details date")
        except Exception as e:
            self.l.add("Problem occurred to enter \"" + dateValue + " \" in Details date")
            raise e

    def actions_menu_item(self):
        return self.win.child_window(title="Actions", control_type="MenuItem")

    def actions_sub_menu_item(self,menu_item):
        tries = 0
        while not self.win.child_window(title=menu_item, control_type="MenuItem").isVisible() and tries < self.maxattempts:
            time.sleep(self.minwait)
            tries = tries + 1
            print("attempt:" + tries)
        return self.win.child_window(title=menu_item, control_type="MenuItem")
    def get_doc_id(self):
        valueToReturn = 0
        try:
            docNo = self.win.child_window( auto_id="tlpDocumentDetails", control_type="Pane").child_window( auto_id="txtTranID", control_type="Edit")
            valueToReturn=docNo.get_value()
            self.l.add("Got " + str(valueToReturn) + " value from doc no")
        except Exception as e:
            self.l.add("Could not get value from doc number field")
            raise e
        
        return valueToReturn
    def get_details_total(self):
        valueToReturn = 0
        try:
            #dtl = self.win.child_window(title="Authorised by:", auto_id="tlpTotals", control_type="Pane").child_window(title="Authorised by:", auto_id="txtDetailsTotal", control_type="Edit")
            dtl = self.win.child_window(title="External Ref:", auto_id="tlpTotals", control_type="Pane").child_window(auto_id="txtDetailsTotal", control_type="Edit")
            valueToReturn=dtl.get_value()
            self.l.add("Got " + str(valueToReturn) + " value from details total")
            #self.l.add("Authorisation is disabled")
        except Exception as e:
            self.l.add("Could not get value from details total field")
            raise e
        
        return valueToReturn

    def set_document_total(self,amt):
        if(str(amt)!="None" ):
            try:
                #self.win.print_control_identifiers()
                doc = self.win.child_window(title="External Ref:", auto_id="tlpTotals", control_type="Pane").child_window(title="External Ref:", auto_id="txtDocTotal", control_type="Edit")
                #doc = self.win.child_window(title="Authorised by:", auto_id="txtDocTotal", control_type="Edit")
                doc.set_text(amt)
                doc.type_keys('{TAB}')
                self.l.add("Entered " + str(amt) + " in document total.")
            except Exception as e:
                self.l.add("Problem occured to enter document total: "+ str(amt))
                raise e

    def accept_Duplicate_Records(self):
        try:
            self.l.add("attempted accepting duplicate records error")
            doc = self.win.child_window(title="Supplier Invoices//Credit Notes", auto_id="MainContentLayoutPanel", control_type="Pane")
            #print(doc)
            doc.type_keys('{enter}')
        except Exception as e:
            self.l.add("no duplicate records found")

    def get_document_total(self):
        valueToReturn = 0
        try:
            #doc = self.win.child_window(title="Authorised by:", auto_id="tlpTotals", control_type="Pane").child_window(title="Authorised by:", auto_id="txtDocTotal", control_type="Edit")
            doc = self.win.child_window(title="External Ref:", auto_id="tlpTotals", control_type="Pane").child_window(title="External Ref:", auto_id="txtDocTotal", control_type="Edit")
            valueToReturn = doc.get_value()
            self.l.add("Got " + str(valueToReturn) + " value from document total field")
        except Exception as e:
            self.l.add("Could not get value from Document total field")
            raise e

        return valueToReturn


    def select_action(self,action_name):
        try:
            #self.win.print_control_identifiers()        
            self.click_element(self.actions_menu_item())
            time.sleep(1)
            sub_menu = ""
            for si in self.actions_menu_item().children():
                #print (si.element_info.name)
                #print (si.rectangle().top)
                if(si.element_info.name == action_name):
                    sub_menu = si 
                    break
            self.click_element(sub_menu)  
            self.l.add("Selected action:" + action_name )   
        except Exception as e:
            self.l.add("Could not select menu:" + action_name)
            raise e

