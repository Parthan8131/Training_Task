import paramiko
import os
from sys import platform
import subprocess
from paramiko import SSHClient
from scp import SCPClient

class Hosting:

    def __init__(self):
        self.supported_actions = ['download', 'upload']

    def ssh_logoff(self):
        #close ssh bridge
        c.close()

    def generate_command(self, task, system_type, user_name, ip, key, location, source_path, target_path):
        # generate the command according to the task want to perform
        if task == "connect" and system_type == "yes":
            self.cmd = "ssh -i ." + str(key) + " " + str(user_name) + "@ec2-" + str(ip) + "." + str(location) + ".compute.amazonaws.com"
        elif task == "download" and system_type == "yes":
            self.cmd = "scp -i " + str(key) + " " + str(source_path) + " " + str(user_name) + "@" + str(ip) + ":" + str(target_path)
        return self.cmd
     
    def connect_ec2_machine(self, hostname_, username_, pkey_):
        # Connect ec2 machine // Log exception on connection
        try:
            print("Machine connect initiated...")
            cert = paramiko.RSAKey.from_private_key_file("/Users/parthan/Desktop/AWS/EC2/task1/copy-task-test.pem")
            self.c = paramiko.SSHClient()
            self.c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            print("connecting...")
            #print("debug log : ",hostname_, username_, pkey_)
            self.c.connect( hostname = "43.204.36.248", username = "ec2-user", pkey = cert)
            print("connected!!!")
        except Exception as ex:
            print("User log:: Exception :",ex)

    def start_task(self):
        # Initital task method which take details of target machine and decide the task want to perform
        self.task = input("Please select the operation you want to perform ? (connect / close) : ")
        if self.task is not "close":
            self.target_system_user_name = input("Please provide the username of target system (ex: ec2-user ): ")
            self.target_system_ip = input("Please provide the public ip of target system (ex: 43-204-36-248) : ")
            self.system_type = input("EC2? (yes/no)")
            if self.system_type == "yes":
                self.key = input("Enter the .pem key including path (ex: /Desktop/AWS/EC2/task1/copy-task-test.pem): ")
                self.location = input("Enter the EC2 domaion location (ex: ap-south-1) : ")
                self.connect_ec2_machine(self.target_system_ip, self.target_system_user_name, self.key)
            else:
                self.key = input("Enter the password : ")
                self.connect_machine()
            self.local_task = input("Please enter the task you want to perform (download / upload) : ")
            cm = self.take_path(self.local_task, self.system_type, self.target_system_user_name, self.target_system_ip, self.key, self.location)
            self.os_output = self.get_os_details()
            print(self.os_output)
            if "Linux" in str(self.os_output):
                print("User LOG:: Calling Linux")
                self.linux_data_transfer(cm)
            elif "mac" in str(self.os_output):
                print("User LOG:: Calling MAC ")
                self.mac_x_data_transfer()
            elif "ubuntu" in str(self.os_output):
                print("User LOG:: Calling Linux")
                self.ubuntu_data_transfer()
            
        else:
            print("Closing..")
            exit()

    def take_path(self, local_task, system_type, target_system_user_name, target_system_ip, key, location):
        print(self.local_task, " initiated*")
        self.object_loc = input("Please enter the source data path : ")
        self.target_loc = input("Please enter the target location path : ")
        self.generated_cmd = self.generate_command(local_task, system_type, target_system_user_name, target_system_ip, key, location, self.object_loc, self.target_loc)
        print(self.generated_cmd)
        return self.generated_cmd

    def get_os_details(self):
        # Detect the Operating system details of connected machine
        stdin, stdout, stderr = self.c.exec_command('hostnamectl')
        self.out = stdout.readlines()
        print("U LOG:: OS Details:: ",self.out[6])
        return self.out[6]

    def next_task(self):
        # Task continue decision
        self.task = input("Please select the operation you want to perform ? ( download / upload / close ) : ")
        if self.task in self.supported_actions:
            self.take_path()
        else:
            print("closing")
            exit()

    def linux_data_transfer(self,copy_command):
        # Customize Call specific to linux machine :: in progress
        print("User LOG:: Data trasnfer initiated*")
        # list the items in EC2
        stdin, stdout, stderr = self.c.exec_command('ls')
        print("User LOG:: Current item listed on EC2 :: ", stdout.readlines())
        # copy item to EC2
        print("User LOG:: Starts copying")
        print("User LOG:: copy command:: ",copy_command)
        copy_call = subprocess.run([str(copy_command)], stdout=subprocess.PIPE)
        print("User LOG:: copy call response: ",ls_call.stdout)
        print("User LOG:: Cheking items on howt after copying..")
        stdin, stdout, stderr = self.c.exec_command('ls')
        print("User LOG:: items list after copying:: ",stdout.readlines())

    def subprocess_method_inprogress_one(self):
        try:
            p = subprocess.Popen(["scp", "/Users/parthan/Desktop/PYTHON_TASK/sftp_programming/two.txt", "ec2-user@43.204.36.248:/home/ec2-user/"])
            sts = os.waitpid(p.pid, 0)
            print(sts)
        except Exception as e:
            print("EXX : ",e)

    def subprocess_method_inprogress_two(self):  
        ssh = SSHClient()
        ssh.load_system_host_keys()
        ssh.connect('ec2-user@43.204.36.248:/home/ec2-user/')
        with SCPClient(ssh.get_transport()) as scp:
            scp.put('/Users/parthan/Desktop/PYTHON_TASK/sftp_programming/two.txt', 'my_file.txt')

    def ssh_remote_login(self):
        #do SSH Login to EC
        try:
            #step 1: get task
            #cert = paramiko.RSAKey.from_private_key_file("/Users/parthan/Desktop/AWS/EC2/task1/copy-task-test.pem")
            #self.host_file_path = "/Users/parthan/Desktop/PYTHON_TASK/sftp programming/first.txt"
            #self.copy_file_name = "copy_one.txt"
            self.start_task()
            #step x: Close SSH
            print("Closing SSH connection")
            self.c.close()
            print("SSH closed")
            
            
        except Exception as ex:
            print("Connection Failed!!!, EX:: ",ex)

    def mac(self):
        try:
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(hostname='192.168.1.3',username='parthan',password='8131', port=22)
            print("user log :: Connetion successfull")
        except Exception as ex:
            print("user log :: Exception occuared : ", ex)
        try:
            #useless_cat_call = subprocess.run(["cat"], stdout=subprocess.PIPE, text=True, input="Hello from the other side")
            #print(useless_cat_call.stdout)
            ls_call = subprocess.run(["scp -i “copy-task-test.pem” first.txt ec2-user@ec2-43-204-36-248.ap-south-1.compute.amazonaws.com:linux_home/"], stdout=subprocess.PIPE)
            print(ls_call.stdout) 
        except Exception as ex:
            print("Exception logged:: ",ex)

    def mac_x_transfer_file(self):
        try:
            self.take_path()
            self.sftp_client = self.ssh.open_sftp()
            print("user log:: sftp successfull")
            #print(dir(self.sftp_client))
            if str(self.task) == 'download':
                self.sftp_client.get(self.object_loc, self.target_loc)
            elif str(self.task) == 'upload':
                self.sftp_client.put(self.object_loc, self.target_loc)
            print("user log:: File transffered successfully")
        except Exception as ex:
            print("File transfer failed, user log:: ",ex)
        self.next_task()
        

H = Hosting()
H.ssh_remote_login()

            
            

    
        
        
