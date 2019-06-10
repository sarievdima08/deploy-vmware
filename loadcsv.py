import csv
from prettytable import PrettyTable, from_csv


class LoadCSV:
    def __init__(self,filename):
        self.vmlist = []
        self.headname = ['VMName', 'VMGuestName', 'Template', 'NumCpu', 'MemoryGB', 'Datastore', 'IP', 'Netmask',
                         'Gateway', 'DNS1', 'DNS2', 'PortGroup', 'ClusterName', 'VMFolder']

        with open(filename, newline='') as f:
            f_csv = csv.DictReader(f)
            for row in f_csv:
                self.vmlist.append(row)

        # Check the csv is in correct format
        for line in self.vmlist:
            count = 0
            for key, value in line.items():
                if key != self.headname[count]:
                    print("vmlist file format is not correct - " + line['VMName'])
                    quit()
                count += 1
            print(line['VMName']+" - vmlist file check ok")

    def export(self):
        return self.vmlist

    def print(self):
        return

    def data_print2(self):
        table_header01 = ['NO'] + self.headname[0:6]
        table_header02 = ['NO'] + self.headname[0:1] + self.headname[6:14]
        x1 = PrettyTable(table_header01)
        x2 = PrettyTable(table_header02)
        count = 1
        for vminfo in self.vmlist:
            vminfo['NO'] = count
            line1 = []
            line2 = []
            for header in table_header01:
                line1.append(vminfo[header])
            for header in table_header02:
                line2.append(vminfo[header])
            x1.add_row(line1)
            x2.add_row(line2)
            count += 1
        print(x1)
        print(x2)


if __name__ == '__main__':
    a = LoadCSV('vmlist.csv')
    a.data_print2()


