from clonevm import CloneVM
from loadcsv import LoadCSV
from getpass import getpass
import sys


class Main:
    def __init__(self, filename):
        self.vmlist = LoadCSV(filename)
        self.vmware = CloneVM()

    def connect(self, vc_ip, vc_id, vc_pwd):
        check_conn = self.vmware.connect(vc_ip, vc_id, vc_pwd)
        return check_conn

    def disconnect(self):
        self.vmware.disconnect()
        return

    def clone(self):
        for line in self.vmlist.export():
            print(line['VMName']+" - Checking status")
            self.vmware.set_folder(None, line['VMFolder'])
            self.vmware.set_vmlocation(line['Datastore'], line['ClusterName'])
            self.vmware.set_template(line['Template'])
            self.vmware.set_vmspec(int(line['NumCpu']), int(line['MemoryGB']))
            self.vmware.set_vmname(line['VMName'])
            self.vmware.set_network(line['IP'], line['Gateway'], line['Netmask'], line['DNS1'], line['DNS2'], line['VMGuestName'])
            self.vmware.set_portgroup(line['PortGroup'])
            print(line['VMName']+" - Starting clone VM from template")
            check_clone = self.vmware.clone()
            if check_clone is True:
                print(line['VMName'] + " - OK")
            else:
                print(line['VMName'] + " - Failed")
        return

    def table(self):
        table = self.vmlist.data_print2()
        return


if __name__ == '__main__':
    print("""#####################################
# VMware Virtaul Machine Clone Tool #
#####################################""")
    x = Main('vmlist.csv')
    check = x.connect(input('vcenter ip:'), input('vcenter id:'), getpass('password:'))
    if check is False:
        print("Login vCenter Server Failed")
        sys.exit()
    x.table()
    print("0.Clone VM")
    print("1.Exit")
    while True:
        user = str(input("choice:"))
        if user == '0':
            x.clone()
            x.disconnect()
            sys.exit()
        elif user == '1':
            x.disconnect()
            sys.exit()
        else:
            continue



