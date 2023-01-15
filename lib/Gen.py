from pywinauto.application import Application 
from pywinauto import backend
from pywinauto import mouse,keyboard
from pywinauto import win32structures
import time
import os,sys

class Obj:

    def __init__(self,win_name,par=None,l=None):
        try:
            self.g = Gen(backend)
            self.win_name = win_name
            if(not par):
                self.app_handle = self.g.get_handle(win_name)
                self.g.set_window(self.app_handle)
                self.win = self.g.get_window()
                self.win.set_focus()     
            self.maxattempts = 10
            self.minwait = 0.5
            self.l = l
        except Exception as e:
            if(l):
                self.l.add('Problem occured finding window:' + win_name)
            raise Exception('Problem occured finding window:' + win_name)
    def setLog(self,log):
        self.l = log
    def click_element(self,ele):
        rect = ele.rectangle()
        x = int(round((rect.right - rect.left)/2,0) + rect.left)
        y = int(round((rect.bottom - rect.top)/2,0) + rect.top)
        mouse.click(coords=(x,y))

    def clear_field(self,ele):
        self.click_element(ele)
        keyboard.SendKeys('^a^c')
        keyboard.SendKeys('{BACKSPACE}')

    def type_element(self,ele,text):
        self.click_element(ele)
        keyboard.SendKeys(text)

    def type_and_tab(self,ele,text):
        self.type_element(ele,text)
        self.type_element(ele,'{TAB}')

    def set_object(self,ele):
        self.ele = ele

    def pcis(self,dep=None):
        if(dep):
            self.win.print_control_identifiers(depth=dep)
        else: 
            self.win.print_control_identifiers()

    def kids(self,controltype):
        childs = self.win.children(control_type=controltype)
        print('Number of childs found:' + str(len(childs)))
        for child in childs:
            print(child.element_info.name)

    def child_window_handle(self,controltype):
        childs = self.win.children(control_type=controltype)
        for child in childs:
            print(child.element_info.name)
            if(child.element_info.name==self.win_name):                
                self.app_handle = child.element_info.handle
                self.win = child                
                break
    def print_win_name(self):
        print(self.win.element_info.name)


class Gen:
    def __init__(self,backend):
        self.backend = backend
        self.spaces = ""
        #print("Gen object created")

    def start_app(self,path):
        self.app = Application().start(path)

    def kill_app(self):
        self.app.kill()
        
    def get_handle(self,appname):
        handle = 0
        maxtries = 10
        currtry = 0
        while (handle==0 and currtry<maxtries):
            root = self.backend.registry.backends["uia"].element_info_class()
            handle = 0
            for w in root.children():
                print(w.name)
                if((w.name==appname) or (appname in w.name)):
                    handle=w.handle
                    break
            time.sleep(1)  
            currtry = currtry + 1      
        return handle    

    def print_windows(self):
        root = self.backend.registry.backends["uia"].element_info_class()    
        for w in root.children():
            print(w.name)  

    def set_window(self,handle_app):
        #print("Handle:"+ str(handle_app))
        self.handle_app = handle_app
        self.app = Application(backend="uia").connect(handle=handle_app)
        self.win = self.app.top_window()
        self.win.set_focus()

    def get_window(self):
        return self.win
    
    def print_win_tree(self):
        spaces = "-"
        self.objs = {}
        print(spaces)
        self.print_child_ele_details(spaces,self.win)
        
    def print_child_ele_details(self,spaces,root):
        eles = root.children()
        for ele in eles:
            rTxt = str(ele.element_info.rich_text)
            if(rTxt and not (rTxt in self.objs)):
                out = spaces + "["
                out = out + "control_type:" + str(ele.element_info.control_type)+","
                out = out + "name:" + str(ele.element_info.name)+","
                out = out + "class_name:" + str(ele.element_info.class_name)+","
                out = out + "control_id:" + str(ele.element_info.control_id)+","
                out = out + "rich_text:" + str(ele.element_info.rich_text)
                out = out + "]"
                print(out)
                out = ""
                self.objs[rTxt]  = rTxt
            self.print_child_ele_details(spaces+"-",ele)
    
    def print_ele_details(self,ele):
        out = self.spaces + "["
        out = out + "control_type:" + str(ele.element_info.control_type)+","
        out = out + "name:" + str(ele.element_info.name)+","
        out = out + "class_name:" + str(ele.element_info.class_name)+","
        out = out + "control_id:" + str(ele.element_info.control_id)+","
        out = out + "rich_text:" + str(ele.element_info.rich_text)
        out = out + "]"
        print(out)
        out = ""        
    def get_elements(self,obj_type):
        eles = self.win.children(control_type=obj_type)
        for ele in eles:
            self.print_ele_details(ele)

    def pcis(self):
        self.win.print_control_identifiers()