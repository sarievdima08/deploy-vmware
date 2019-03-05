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

    def data_print(self):
        x = PrettyTable(['NO'] + self.headname)
        count = 1
        for line in self.vmlist:
            list = [count]

            for key, value in line.items():
                list.append(str(value))
            x.add_row(list)
            count += 1
        return x





if __name__ == '__main__':
    a = LoadCSV('vmlist.csv')
    #a.print()
    b = a.data_print()
    print(b)


