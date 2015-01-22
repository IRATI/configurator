#!/usr/bin/python

#
# Data Model for the RINA Configuration Generator (frontend)
#
#    Francesco Salvestrini <f.salvestrini@nextworks.it>
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

class Interface:
    """ A class representing an interface """
    def __init__(self, name, ip = ""):
        self.name = name
        self.ip = ip

class Node:
    """ A class representing a node in the topology """
    def __init__(self, name):
        self.name = name
        self.interfaces = []
        self.ipcps = []
        self.apps = []

class RINA_Name:
    """ Represents a RINA name """
    def __init__(self, ap_name, \
                 ap_inst = "", \
                 ae_name = "", \
                 ae_inst = ""):
        self.ap_name = ap_name
        self.ap_inst = ap_inst
        self.ae_name = ae_name
        self.ae_inst = ae_inst

class IPCP:
    """ A class that represents an IPC Process """
    def __init__(self, name, dif_name = ""):
        self.name = name
        self.dif_name = dif_name
        self.registrations = []

class App:
    """ A class representing an app in a node """
    def __init__(self, name):
        self.name = name
        self.regs = []

class Data_Transfer_Constants:
    """ A class that holds the data transfer constants of a DIF """
    def __init__(self, addr_len, cep_id_len, len_len, \
                 port_id_len, qos_id_len, seq_nr_len, \
                 max_pdu_size, max_pdu_lifetime):
        self.addr_len = addr_len
        self.cep_id_len = cep_id_len
        self.len_len = len_len
        self.port_id_len = port_id_len
        self.qos_id_len = qos_id_len
        self.seq_nr_len = seq_nr_len
        self.max_pdu_size = max_pdu_size
        self.max_pdu_lifetime = max_pdu_lifetime

class QoS_Cube:
    """ A class that represents a QoS cube """
    def __init__(self, qos_id, name, \
                 part_del = "", ord_del = ""):
        self.qos_id = qos_id
        self.name = name
        self.part_del = part_del
        self.ord_del = ord_del

class Known_IPCP_Address:
    """ Holds the mapping of RINA name on address """
    def __init__(self, name, address):
        self.name = name
        self.address = address

class Link_State_Routing_Configuration:
    """ Holds parameters for Link State Routing """
    def __init__(self, obj_max_age = "", \
                 read_cdap_time = "", error_time = "", \
                 recompute_time = "", repropagate_time = "", \
                 increment_time = "", algorithm = ""):
        self.obj_max_age = obj_max_age
        self.read_cdap_time = read_cdap_time
        self.error_time = error_time
        self.recompute_time = recompute_time
        self.repropagate_time = repropagate_time
        self.increment_time = increment_time
        self.algorithm = algorithm

class PFT_Configuration:
    """ Class that holds the (current) PFT configuration """
    """                                                  """
    """ Has to be revised, since it is a policy          """
    def __init__(self, name, version = "", lsr_conf = ""):
        self.name = name
        self.version = version
        self.lsr_conf = lsr_conf

class DIF:
    """ A class that represents a Distributed IPC Facility """
    def __init__(self, name, dif_type = "", \
                 cdap_timeout = "", enroll_timeout = "", \
                 flow_alloc_timeout = "", watchdog_period = "", \
                 decl_dead_int = "", neigh_enroll_period = "", \
                 data_transfer_const = "", pft_conf= ""):
        self.name = name
        self.dif_type = dif_type
        self.cdap_timeout = cdap_timeout
        self.enroll_timeout = enroll_timeout
        self.flow_alloc_timeout = flow_alloc_timeout
        self.watchdog_period = watchdog_period
        self.decl_dead_int = decl_dead_int
        self.neigh_enroll_period = neigh_enroll_period
        self.data_transfer_const = data_transfer_const
        self.qos_cubes = []
        self.known_ipcp_addr = []
        self.pft_conf = pft_conf
