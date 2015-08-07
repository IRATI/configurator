#
# Data Model for the RINA Configuration Generator
#
#    Sander Vrijders       <sander.vrijders@intec.ugent.be>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA  02110-1301  USA

class interface:
    """ A class representing an interface """
    def __init__(self, name = "", ip = ""):
        self.name = name
        self.ip = ip

class node:
    """ A class representing a node in the topology """
    def __init__(self, name):
        self.name = name
        self.ipcps = []
        self.apps = []

class link:
    """ A class representing a link in the topology """
    def __init__(self, id, \
                 node_a = "", \
                 node_b = "", \
                 int_a = interface(), \
                 int_b = interface()):
        self.id = id
        self.node_a = node_a
        self.node_b = node_b
        self.int_a = int_a
        self.int_b = int_b

class rina_name:
    """ Represents a RINA name """
    def __init__(self, ap_name, \
                 ap_inst = "", \
                 ae_name = "", \
                 ae_inst = ""):
        self.ap_name = ap_name
        self.ap_inst = ap_inst
        self.ae_name = ae_name
        self.ae_inst = ae_inst

class ipcp:
    """ A class that represents an IPC Process """
    def __init__(self, name, dif_name = ""):
        self.name = name
        self.dif_name = dif_name
        self.registrations = []

class app:
    """ A class representing an app in a node """
    def __init__(self, name, reg = ""):
        self.name = name
        self.reg = reg

class dif:
    """ A class that represents a Distributed IPC Facility """
    def __init__(self, name, dif_type = "", \
                 template = "", addr_count = 0):
        self.name = name
        self.dif_type = dif_type
        self.template = template
        self.addr_count = addr_count
