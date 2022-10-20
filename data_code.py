import os
from os.path import exists
import paramiko
from paramiko import SSHClient
from scp import SCPClient



class GUI:


    def __init__(self):
        pass

    def get_host_details(self):
        # get host machine details such as ip and u-name and .pem key
        print("ENTER HOST DETAILS - ")
        self.host_ip = input("Enter the IP(v4 Public) : ")
        self.u_name = input("Enter the User name : ")
        self.key = EC2.EC2_key_check(self)
        print("done : key :",self.key)
        host_details = [self.host_ip, self.u_name, self.key]
        return host_details
        # Lib_SSH.connect_shh_request(self, self.host_ip, self.u_name, self.key)

    def get_task_and_path(self):
        task = input("download OR upload : ")
        source_path = input("Enter the data source path : ")
        target_path = input("Enter the data target path : ")
        return task, source_path, target_path
            

class File_handling:


    def check_file_exist_status(self, path_to_file):
        # check wheather file exist on system or not
        try:
            file_exists_status = exists(path_to_file)
            print('File : {} exist status is {}'.format(path_to_file, file_exists_status))
        except Exception as e:
            print("Log : Exception occurared : ",e)
        return file_exists_status


class EC2:


    def __init__(self):
        pass

    def EC2_key_check(self):
        self.key_exist_status = True
        self.ec2_status = input("Is it a EC2 instance (yes / no) : ")
        if self.ec2_status == "yes":
            self.key = input('Please enter the .pem file path :')
            key_exist_status = File_handling.check_file_exist_status(self, self.key)
        elif self.ec2_status == "no":
            self.key = input('Enter the password : ')
            self.key_exist_status = True
    
        if self.key_exist_status == True:
            return self.key

    def os_compactibility_check(self, os):
        compactible_os = ['Linux', 'Mac', 'Ubuntu']
        for item in compactible_os:
            if item in str(os):
                print("Log : {} is compactible".format(os))
                status = True
                break
                
        if status is not True:
            print("Error Log : {} is not compactible".format(os))
            exit()


class Lib_SSH(GUI):
    
    
    def __init__(self):
        pass

    def connect_shh_request(self, *host_details):
        host_details = list(host_details)
        ip = host_details[0]
        user_name = host_details[1]
        key = host_details[2]
        # print("Log :: ip : {}, u_name: {}, key: {}".format(ip, user_name, key))
        try:
            print("Log :: ssh connection initiated")
            self.ssh = paramiko.SSHClient()
            self.ssh.load_system_host_keys()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(str(ip), username=str(user_name), key_filename=str(key))
            print("Log :: ssh connection successfull")
            #stdin, stdout, stderr = self.ssh.exec_command('pwd')
            #print (stdout.readlines())
            status = True
        except Exception as ex:
            print("Log : Exception :: {}".format(ex))
        return status
    
    def data_transfer(self, task, d_path, d_target):
        try:
            with SCPClient(self.ssh.get_transport()) as scp:
                if task == "download":
                    print("Log : download initiated")
                    scp.get(d_path, d_target)
                    print("Log : download completed")
                elif task == "upload":
                    print("Log : upload initiated")
                    scp.put(d_path, d_target)
                    print("Log : upload completed")
        except Exception as ex:
            print("Log : Exception {}".format(ex))

    def get_os_details(self):
        # Detect the Operating system details of connected machine
        stdin, stdout, stderr = self.ssh.exec_command('hostnamectl')
        self.out = stdout.readlines()
        print("Log : OS Detected : ",self.out[6])
        return self.out[6]
            

class Data_transfer_task:

    
    def __init__(self):
        pass

    def data_transfer_job(self):
        print("DATA TRANSFER JOB TRIGGERED..")
        data = GUI.get_host_details(self)
        print("Log : host details recived from user ",data)
        print("Log : calling connect ssh function")
        status = Lib_SSH.connect_shh_request(self, data[0], data[1], data[2])
        print("status : ",status)
        if status is True:
            os = Lib_SSH.get_os_details(self)
            EC2.os_compactibility_check(self, os)
            print("Log : Initiating data tranfer process..")
            self.task, self.data_source, self.target_path = GUI.get_task_and_path(self)
            Lib_SSH.data_transfer(self, self.task, self.data_source, self.target_path)
            print("Log : Task completed successfully..exiting..")
            
        
D = Data_transfer_task()
D.data_transfer_job()




    
        

        



        
