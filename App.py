# import libraries
import json
import os
import os.path
import sys
from pathlib import Path
import datetime

class fileio: #class for All operations
    #path variabel is for path of the data store file
    path=None

    #constructor
    def __init__(self,path=None): 
        #if path is given than we will work in given path else we will work  in current directory
        #filename for our data storage is data.txt
        if (path==None):
            self.path=os.getcwd()
        else:
            self.path=path

        self.path=self.path+'/data.txt'
        try:
            open(self.path,'x')
        except:
            pass



    #function for reading data
    def read(self,key):
        try:
            file=open(self.path,'r')
            data=json.load(file)
            if (key in data):
                ans=data[key]
                # ans=json.dumps(ans)
                ans=json.loads(ans)
                if ("time_to_live" in ans):
                    ans.pop("time_to_live")

                return (ans)
            file.close()
            return "no data with this key"
        except:
            return "No Json Data"
    #function to create new key-value data and store it into file
    def create(self,obj):
        filesize=os.path.getsize(self.path)
        filesize=filesize/1000000
        filesize+=sys.getsizeof(obj)/1000000

        #Hanlind The case when file size will exceed 1GB
        if (filesize>1024):
            return "You cannot Intsert This Data (File Size Will Exceed 1GB limit)"


        file=open(self.path,'r')
        try:
            data=json.load(file)
        except:
            data={}
        file.close()
        for i in obj:
            if i in data:
                return "Key is already available"
        data.update(obj)
        file=open(self.path,'w')
        json.dump(data,file)
        file.close()
        return -1
        

    #function for deleting json object with given key
    def delete(self,key):
        file=open(self.path,'r')
        data=json.load(file)
        if (key in data):
            data.pop(key)
        file.close()
        file=open(self.path,'w')
        json.dump(data,file)
        file.close()
        return

    #function for deleting json objects whose time_to_live is expired
    def delete_expired_data(self):
        try:
            file=open(self.path)
            data=json.load(file)
            file.close()
            curtime=datetime.datetime.now()
            rewrite_data={}
            count=0
            # if time_to_live property is given to any object and if time is expired 
            # than we will delete that object and rewrite file
            for key in data:
                datainside=json.loads(data[key])
                
                if ("time_to_live" in datainside):
                    time_to_live=datetime.datetime.strptime(datainside["time_to_live"],'%m/%d/%Y, %H:%M:%S')
                    if time_to_live<=curtime:
                        count+=1
                        continue
                    else:
                        rewrite_data[key]=data[key]
                else:
                    rewrite_data[key]=data[key]
            # print(count)
            if (count>0):
                file=open(self.path,'w')
                json.dump(rewrite_data,file)
                file.close()
            return 
        except:
            return



