from connvc import ConnVC
from pyVmomi import vim


class CloneVM(ConnVC):
    def __init__(self):
        super().__init__()
        # Folder variables
        self.datacenter = None
        self.folder = None
        # vm_location variables
        self.relospec = None
        # vm cpu/mem spec
        self.vmconf = None
        # vm template
        self.template = None
        # vm name in vcsa
        self.vmname = None
        # vm network in os
        self.customspec = None
        # vm portgroup
        self.vmnic = None

    # Set the vm folder in vcsa
    def set_folder(self, datacenter_name, folder_name):
        self.datacenter = self.get_obj([vim.Datacenter], datacenter_name)
        # Get VM folder ID
        if folder_name:
            self.folder = self.get_obj([vim.Folder], folder_name)
        else:
            self.folder = self.datacenter.vmFolder
        return

    # Set the vm location in which datastore and cluster
    def set_vmlocation(self, datastore_name, cluster_name):
        # Get datastore ID
        if datastore_name:
            datastore = self.get_obj([vim.Datastore], datastore_name)
            if datastore is None:
                print("Datastore not found")
                return
        else:
            print("Datastore not defind")
            return
        # Get cluster ID
        if cluster_name:
            cluster = self.get_obj([vim.ClusterComputeResource], cluster_name)
            if cluster is None:
                print("Cluster not found")
                return
        else:
            print("Cluster not defind")
            return
        # Get resource pool ID
        resource_pool = cluster.resourcePool
        # Relocation spec
        self.relospec = vim.vm.RelocateSpec()
        self.relospec.datastore = datastore
        self.relospec.pool = resource_pool
        self.relospec.transform = 'sparse'
        # for thin provisioning , use sparse
        # for thick provisioning , use flat
        return

    # Set the vm cpu and mem
    def set_vmspec(self, cpu, mem):
        self.vmconf = vim.vm.ConfigSpec()
        self.vmconf.numCPUs = cpu
        self.vmconf.memoryMB = mem*1024
        self.vmconf.cpuHotAddEnabled = True
        self.vmconf.memoryHotAddEnabled = True
        return

    # Set the vm name in VCSA
    def set_vmname(self, vm_name):
        self.vmname = vm_name
        return

    # Set network in OS
    def set_network(self, ip, gw, netmask, dns1, dns2, hostname):
        # set ip / gateway / netmask
        vm_net = vim.vm.customization.AdapterMapping()
        vm_net.adapter = vim.vm.customization.IPSettings()
        vm_net.adapter.ip = vim.vm.customization.FixedIp(ipAddress=ip)
        vm_net.adapter.subnetMask = netmask
        vm_net.adapter.gateway = gw
        # set dns
        list_dns = list()
        list_dns.append(dns1)
        list_dns.append(dns2)
        vm_dns = vim.vm.customization.GlobalIPSettings(dnsServerList=list_dns)
        # set hostname
        vm_hostname = vim.vm.customization.LinuxPrep(hostName=vim.vm.customization.FixedName(name=hostname))
        # set network spec
        self.customspec = vim.vm.customization.Specification()
        self.customspec.nicSettingMap = [vm_net]
        self.customspec.globalIPSettings = vm_dns
        self.customspec.identity = vm_hostname

    # Set template name which be clone
    def set_template(self, template_name):
        # Get VM template ID
        if template_name:
            self.template = self.get_obj([vim.VirtualMachine], template_name)
            if self.template is None:
                print("Template not found")
                return
        else:
            print("Template not defind")
            return
        return

    def set_portgroup(self, portgroup_name):
        # Check portgroup is in dvs or vss
        if portgroup_name:
            portgroup_vds = self.get_obj([vim.dvs.DistributedVirtualPortgroup], portgroup_name)
            if portgroup_vds is None:
                portgroup_vss = self.get_obj([vim.Network], portgroup_name)
                if portgroup_vss is None:
                    print("Portgroup not found")
                    return
            else:
                portgroup = vim.dvs.PortConnection()
                portgroup.portgroupKey = portgroup_vds.key
                portgroup.switchUuid = portgroup_vds.config.distributedVirtualSwitch.uuid

        else:
            print("Portgroup not defind")
            return
        self.vmnic = vim.vm.device.VirtualDeviceSpec()
        self.vmnic.operation = vim.vm.device.VirtualDeviceSpec.Operation.edit
        # choice the vmnic type - vmxnet3
        self.vmnic.device = vim.vm.device.VirtualVmxnet3()
        # choice the device key
        self.vmnic.device.key = 4000
        self.vmnic.device.wakeOnLanEnabled = True
        # set portgroup on this nic
        if portgroup_vds is None:
            self.vmnic.device.backing = vim.vm.device.VirtualEthernetCard.NetworkBackingInfo()
            self.vmnic.device.backing.network = portgroup_vss
            self.vmnic.device.backing.deviceName = portgroup_name
        else:
            self.vmnic.device.backing = vim.vm.device.VirtualEthernetCard.DistributedVirtualPortBackingInfo()
            self.vmnic.device.backing.port = portgroup

        # set this vmnic settings
        self.vmnic.device.connectable = vim.vm.device.VirtualDevice.ConnectInfo()
        self.vmnic.device.connectable.startConnected = True
        self.vmnic.device.connectable.allowGuestControl = True
        self.vmnic.device.connectable.connected = True
        return

    # Starting clone VM from template
    def clone(self):
        if self.template is None or self.relospec is None:
            return False
        clonespec = vim.vm.CloneSpec()
        # VM Location
        clonespec.location = self.relospec
        # VM CPU/MEM SPEC and add vmnic settings into config
        self.vmconf.deviceChange = [self.vmnic]
        clonespec.config = self.vmconf
        # VM Power ON
        clonespec.powerOn = True
        # VM Template
        clonespec.template = False
        # VM network
        clonespec.customization = self.customspec
        task = self.template.Clone(folder=self.folder, name=self.vmname, spec=clonespec)
        self.wait_for_task(task)
        return True

