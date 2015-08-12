#
# Emulab support for the RINA Configuration Generator
#
#    Sander Vrijders       <sander.vrijders@intec.ugent.be>
#    Wouter Tavernier      <wouter.tavernier@intec.ugent.be>
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

import socket
import paramiko
import time
import os
import re
from ast import literal_eval
import datamodel as dm

tag = "emulab-support"

def debug(message):
    print(tag + " DBG: : " + message)

def error(message):
    print(tag + " ERR: : " + message)

class wall_config:
    """ A class containing the vwall configuration """
    def __init__(self, wall = "wall1.ilabt.iminds.be", \
                 username = "", password = "", \
                 proj_name  = "", exp_name = "", \
                 image = ""):
        self.wall = wall
        self.username = username
        self.password = password
        self.proj_name = proj_name
        self.exp_name = exp_name
        self.image = image

def ops_server(wall_config):
    '''
    Return server name of the ops-server (is wall specific)

    @param wall_config: vwall configuration data
    @return: server name of the ops-server
    '''
    return 'ops.' + wall_config.wall

def full_name(node_name, wall_config):
    '''
    Return server name of a node

    @param node_name: name of the node
    @param wall_config: vwall configuration data
    @return: server name of the node
    '''
    return node_name + '.' + \
        wall_config.exp_name + '.' + \
        wall_config.proj_name + '.' + \
        wall_config.wall

def get_ssh_client():
    ssh_client = paramiko.SSHClient()
    ssh_client.load_system_host_keys()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    return ssh_client

def execute_command(hostname, command, wall_config, time_out = 3):
    '''
    Remote execution of a list of shell command on hostname. By
    default this function will exit (timeout) after 3 seconds.

    @param hostname: host name or ip address of the node
    @param command: *nix shell command
    @param time_out: time_out value in seconds, error will be generated if
    no result received in given number of seconds, the value None can
    be used when no timeout is needed
    @param wall_config: vwall configuration data

    @return: stdout resulting from the command
    '''
    ssh_client = get_ssh_client()

    try:
        ssh_client.connect(socket.gethostbyname(hostname), 22,
                           wall_config.username, wall_config.password,
                           look_for_keys=False, timeout=time_out)
        stdin, stdout, stderr = ssh_client.exec_command(command)
        err = str(stderr.read()).strip('b\'\"\\n')
        if err != "":
            error(err)
        output = str(stdout.read()).strip('b\'\"\\n')
        ssh_client.close()

        return output

    except Exception as e:
        error(str(e))
        return "Could not execute command"

def copy_file_to_vwall(hostname, text, file_name, wall_config):
    '''
    Write a string to a given remote file.
    Overwrite the complete file if it already exists!

    @param hostname: host name or ip address of the node
    @param text: string to be written in file
    @param file_name: file name (including full path) on the host
    @param wall_config: vwall configuration data
    '''
    ssh_client = get_ssh_client()

    try:
        ssh_client.connect(socket.gethostbyname(hostname), 22,
                           wall_config.username,
                           wall_config.password,
                           look_for_keys=False)

        cmd = "touch " + file_name + \
              "; chmod a+rwx " + file_name

        stdin, stdout, stderr = ssh_client.exec_command(cmd)
        err = str(stderr.read()).strip('b\'\"\\n')
        if err != "":
            error(err)

        sftp_client = ssh_client.open_sftp()
        remote_file = sftp_client.open(file_name, 'w')

        remote_file.write(text)
        remote_file.close()

    except Exception as e:
        error(str(e))

def get_experiment_list(wall_config, project_name=None):
    '''
    Get list of made emulab experiments accessible with your credentials

    @param project_name: optional filter on project
    @param wall_config: vwall configuration data
    @return: list of created experiments (strings)
    '''
    cmd = '/usr/testbed/bin/sslxmlrpc_client.py -m experiment getlist'
    out = execute_command(ops_server(wall_config), cmd, wall_config)

    try:
        if project_name != None:
            return  literal_eval(out)[project_name][project_name]
        else:
            return  literal_eval(out)
    except:
        return { project_name: { project_name: [] }}

def swap_exp_in(wall_config):
    '''
    Swaps experiment in

    @param wall_config: vwall configuration data
    '''
    cmd = '/usr/testbed/bin/sslxmlrpc_client.py swapexp proj=' + \
          wall_config.proj_name + \
          ' exp=' + \
          wall_config.exp_name + \
          ' direction=in'

    output = execute_command(ops_server(wall_config),
                             cmd, wall_config)
    return output

def create_experiment(nodes, links, wall_config):
    '''
    Creates an emulab experiment

    @param nodes: Holds the nodes in the experiment
    @param links: Holds the links in the experiment
    @param wall_config: vwall configuration data
    '''
    proj_name = wall_config.proj_name
    exp_name = wall_config.exp_name

    exp_list = get_experiment_list(wall_config)

    if exp_name in exp_list[proj_name][proj_name]:
        return 'Experiment already exists'

    ns = generate_ns_script(nodes, links, wall_config)
    dest_file_name = '/users/'+ wall_config.username + \
                     '/temp_ns_file.%s.ns' % os.getpid()
    copy_file_to_vwall(ops_server(wall_config), ns,
                       dest_file_name, wall_config)

    cmd = '/usr/testbed/bin/sslxmlrpc_client.py startexp ' + \
          'batch=false wait=true proj="' + proj_name + \
          '" exp="' + exp_name + '" noswapin=true ' + \
          'nsfilepath="' + dest_file_name + '"'

    execute_command(ops_server(wall_config), cmd,
                    wall_config, time_out=None)
    execute_command(ops_server(wall_config),
                    'rm ' + dest_file_name, wall_config)
    return 'New experiment succesfully created'

def generate_ns_script(nodes, links, wall_config):
    '''
    Generate ns script based on network graph.
    Enables to customize default node image.

    @param nodes: Holds the nodes in the experiment
    @param links: Holds the links in the experiment
    @param wall_config: vwall configuration data

    @return: ns2 script for Emulab experiment
    '''

    ns2_script = '''
    set ns [new Simulator]
    source tb_compat.tcl
    '''

    for node in nodes:
            ns2_script += "set " + node.name + " [$ns node]\n"
            ns2_script += "tb-set-node-os $" + node.name + " " + \
                          wall_config.image + "\n"

    for link in links:
            ns2_script += "set " + link.id + \
                          " [$ns duplex-link $" + \
                          link.node_a + " $" + \
                          link.node_b + " 1000Mb 0ms DropTail]\n"

    ns2_script += "$ns run\n"

    return ns2_script

def wait_until_nodes_up(wall_config):
    '''
    Checks if nodes are up

    @param wall_config: vwall configuration data
    '''
    debug("Waiting until all nodes are up")

    cmd = '/usr/testbed/bin/script_wrapper.py expinfo -e' + \
          wall_config.proj_name + \
          ',' + \
          wall_config.exp_name + \
          ' -a | grep State | cut -f2,2 -d " "'

    res = execute_command(ops_server(wall_config), cmd, wall_config)
    active = False
    if res == "active":
        active = True
    while active != True:
        res = execute_command(ops_server(wall_config), cmd, wall_config)
        if res == "active":
            active = True
        debug("Still waiting")
        time.sleep(5)

def emulab_topology(nodes, links, wall_config):
    '''
    Gets the interface (ethx) to link mapping

    @param nodes: Holds the nodes in the experiment
    @param links: Holds the links in the experiment
    @param wall_config: vwall configuration data
    '''

    node_full_name = full_name(nodes[0].name, wall_config)
    cmd = 'cat /var/emulab/boot/topomap'
    topomap = execute_command(node_full_name, cmd, wall_config)
    # Almost as ugly as yo momma
    index = topomap.rfind("# lans")
    topo_array = topomap[:index].split('\\n')[1:-1]
    # Array contains things like 'r2b1,link7:10.1.6.3 link6:10.1.5.3'
    for item in topo_array:
        item_array = re.split(',? ?', item)
        node_name = item_array[0]
        for item2 in item_array[1:]:
            item2 = item2.split(':')
            link_name = item2[0]
            link_ip = item2[1]
            for link in links:
                if link.id == link_name:
                    if link.node_a == node_name:
                        link.int_a.ip = link_ip
                    elif link.node_b == node_name:
                        link.int_b.ip = link_ip

    for node in nodes:
        cmd = 'cat /var/emulab/boot/ifmap'
        node_full_name  = full_name(node.name, wall_config)
        output = execute_command(node_full_name, cmd, wall_config)
        output = re.split('\\\\n', output)
        for item in output:
            item = item.split()
            for link in links:
                if link.node_a == node.name and \
                   link.int_a.ip == item[1]:
                    link.int_a.name = item[0]
                elif link.node_b == node.name and \
                     link.int_b.ip == item[1]:
                    link.int_b.name =  item[0]

def setup_vlan(node_name, vlan_id, int_name, wall_config):
    '''
    Gets the interface (ethx) to link mapping

    @param node_name: The node to create the VLAN on
    @param vlan_id: The VLAN id
    @param int_name: The name of the interface
    @param wall_config: vwall configuration data
    '''
    debug("Setting up VLAN on node " + node_name)

    node_full_name = full_name(node_name, wall_config)
    cmd = "sudo ip link add link " + \
          str(int_name) + \
          " name " + str(int_name) + \
          "." + str(vlan_id) + \
          " type vlan id " + str(vlan_id)
    execute_command(node_full_name, cmd, wall_config)
    cmd = "sudo ifconfig " + \
          str(int_name) + "." + \
          str(vlan_id) + " up"
    execute_command(node_full_name, cmd, wall_config)
    cmd = "sudo ethtool -K " + \
          str(int_name) + " rxvlan off"
    execute_command(node_full_name, cmd, wall_config)
    cmd = "sudo ethtool -K " + \
          str(int_name) + " txvlan off"
    execute_command(node_full_name, cmd, wall_config)

def insert_mods(nodes, wall_config):
    '''
    Insert the linux kernel modules of IRATI

    @param nodes: Holds the nodes in the experiment
    @param wall_config: vwall configuration data
    '''
    for node in nodes:
        node_full_name = full_name(node.name, wall_config)
        cmd = "sudo modprobe shim-eth-vlan"
        execute_command(node_full_name, cmd, wall_config)
        cmd = "sudo modprobe normal-ipcp"
        execute_command(node_full_name, cmd, wall_config)
        cmd = "sudo modprobe rina-default-plugin"
        execute_command(node_full_name, cmd, wall_config)
