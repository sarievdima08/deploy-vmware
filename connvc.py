import atexit
import getpass
from pyVmomi import vim
from pyVim import connect
from pyVim.connect import Disconnect


class ConnVC:
    def __init__(self):
        self.service_instance = None
        self.content = None

    def connect(self, vc_ip, vc_id, vc_pwd):
        try:
            print("Connecting to vCenter Server")
            self.service_instance = connect.SmartConnectNoSSL('https', vc_ip, 443, vc_id, vc_pwd)
        except Exception:
            atexit.register(Disconnect, self.service_instance)

        try:
            self.content = self.service_instance.RetrieveContent()
        except AttributeError:
            return False
        return True

    def disconnect(self):
        Disconnect(self.service_instance)
        print("Disconnected")

    def get_obj(self, vimtype, name):
        """
        Return an object by name, if name is None the
        first found object is returned
        """
        obj = None
        container = self.content.viewManager.CreateContainerView(
            self.content.rootFolder, vimtype, True)
        for c in container.view:
            if name:
                if c.name == name:
                    obj = c
                    break
            else:
                obj = c
                break
        return obj

    def wait_for_task(self, task):
        """ wait for a vCenter task to finish """
        task_done = False
        while not task_done:
            if task.info.state == 'success':
                return task.info.result

            if task.info.state == 'error':
                print("there was an error")
                task_done = True


if __name__ == '__main__':
    v = ConnVC()
    check = v.connect(input('vcenter ip:'), input('vcenter id:'), input('passwd'))

    vm = v.get_obj([vim.VirtualMachine],'CRHEL-r5G')
    print(type(vm))
    #print(vm.config.hardware.device)
    v.disconnect()
