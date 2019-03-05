import npyscreen
from main import Main


class LoginForm(npyscreen.ActionForm):
    def create(self):
        self.name = "VMware Clone Virtual Machine Tool"
        self.parentApp.value = ""
        self.vc_ip = None
        self.vc_id = None
        self.vc_pwd = None
        self.tui_vc_ip = self.add(npyscreen.TitleText, name="vCenter IP:")
        self.tui_vc_id = self.add(npyscreen.TitleText, name="vCenter ID:")
        self.tui_vc_pwd = self.add(npyscreen.TitlePassword, name="vCenter Pwd:")

    def beforeEditing(self):
        self.vc_ip = None
        self.vc_id = None
        self.vc_pwd = None
        self.tui_vc_ip.value = ''
        self.tui_vc_id.value = ''
        self.tui_vc_pwd.value = ''

    def on_ok(self):
        self.vc_ip = self.tui_vc_ip.value
        self.vc_id = self.tui_vc_id.value
        self.vc_pwd = self.tui_vc_pwd.value

        if len(self.vc_ip) == 0 or len(self.vc_id) == 0 or len(self.vc_pwd) == 0:
            npyscreen.notify_confirm("Failed")
        else:
            check = x.connect(self.vc_ip,self.vc_id,self.vc_pwd)
            if check is True:
                npyscreen.notify_confirm("Login vCenter SUCCESS")
                self.parentApp.switchForm("VMFORUM")
            else:
                npyscreen.notify_confirm("Login vCenter Failed")

    def on_cancel(self):
        self.parentApp.switchForm(None)


class VMForum(npyscreen.ActionForm):
    def create(self):
        self.name = "VMware Clone Virtual Machine Tool"
        self.box = self.add(npyscreen.BoxTitle, name='hello', max_height=30)
        box_text = []
        for line in str(x.table()).splitlines():
            box_text.append(line)
        self.box.values = box_text

    def on_cancel(self):
        x.disconnect()
        self.parentApp.switchForm(None)




class LoginApp(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm("MAIN", LoginForm, name="VMware Clone Virtual Machine Tool", color="IMPORTANT")
        self.addForm("VMFORUM", VMForum, name="VMFroum", color="IMPORTANT")
        #self.addForm("SUCCESSFORM", SuccessForm, name="SUCCESS", color="WARNING")

if __name__ == '__main__':
    x = Main('vmlist.csv')
    #print(x.connect(input('vcenter ip:'),input('vcenter id:'),input('passwd')))
    LoginApp().run()
