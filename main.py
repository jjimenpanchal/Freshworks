# import libraries
from App import fileio
import json
import datetime
import threading

#main 
def main():
    try:
        flag=0
        #creating object of fileio wich contains all of our features
        #if user wants to initialize path or change path 
        #example path is like -
        #E:\project\Freshworks
        #do not provide file name 
        #program will automatically create a data.txt file if not there
        print("Enter Path Of data store (Optinal), Press Enter If You Dont Want To Enter")
        path=input()
        if (len(path)>0):
            obj=fileio(path)
        else:
            obj=fileio()

        #clear function will start a thread every second to check and delete json objects with epired time_to_live
        def clear():
            if flag==-1:
                return
            obj.delete_expired_data()
            threading.Timer(1,clear).start() #starting a thread eveery second
        
        clear() #calling clear function first time
        while True:
            #printing menu
            print("********MENU********")
            print("Enter Integer From Following")
            print("1. Create")
            print("2. Read")
            print("3. Delete")
            # print("4. Change Directory/ Initialize Path")
            print("-1 For  exit")

            #taking user_input
            user_input=input()


            #if  user wants to add data
            if (user_input=='1'):
                print("Enter Key Name")
                key=input()
                print("Do You Want To Enter Time-To-Live Property (Enter Integer From Following)")
                print("1. Yes")
                print("2. No")
                choosen=input()
                seconds=-1
                if (choosen=='1'):
                    print("Enter Number Of Seconds")
                    seconds=int(input())

                data={}
                #taking input in python dictionary form and convert it into json format
                print("Enter Json Object In Key Value Pair Enter -1 As A Key To Break")
                while True:
                    print("Enter Json Object Key, -1 To Break")
                    josn_key=input()
                    if (josn_key=='-1'):
                        break
                    print("Enter Json Object Value ")
                    josn_val=input()
                    data[josn_key]=josn_val
                if (seconds!=-1):
                    data["time_to_live"]=(datetime.datetime.now()+ datetime.timedelta(seconds=seconds)).strftime('%m/%d/%Y, %H:%M:%S')

                data=json.dumps(data)
                d={}
                d[key]=data

                response=obj.create(d)
                if (response!=-1):
                    print(response)



            #if user wants to read data
            elif(user_input=='2'):
                print("Enter Key")
                key=input()
                response=obj.read(key)
                print(response)


            #if user wants to delete data
            elif (user_input=='3'):
                print("Enter Key To be deleted")
                key=input()
                obj.delete(key)


            #if user wants to initialize path or change path 
            #example path is like -
            #E:\project\Freshworks
            #do not provide file name 
            #program will automatically create a data.txt file if not there
            # elif (user_input=='4'):
            #     print("Enter Directory Path")
            #     path=input()
            #     obj=fileio(path)


            #condition for break
            elif (user_input=='-1'):
                flag=-1
                break


            #handling wrong input
            else:
                print("Invalid Input (-1 for exit)")
        return 
    except:
        print("Something Went Wrong Run Again")

if __name__ == '__main__':
    main()
    

