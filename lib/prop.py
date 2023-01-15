import configparser

class Prop():
    def __init__(self,path):
        self.path = path
        self.config = configparser.RawConfigParser()

    def get(self,section,name):
        self.config.read(self.path)
        return self.config.get(section,name)

    def delOption(self,section,name):
        self.config.read(self.path)
        self.config.remove_option(section,name)
        with open(self.path, "w") as f:
            self.config.write(f)

    def delSection(self,section):
        self.config.read(self.path)
        self.config.remove_section(section)
        with open(self.path, "w") as f:
            self.config.write(f)            

    def setOption(self,section,name,value):
        self.delOption(section,name)
        self.config.read(self.path)
        self.config.set(section,name,value)
        with open(self.path, "w") as f:
            self.config.write(f)            
