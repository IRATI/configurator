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
from ast import literal_eval

# FIXME: To be read from a config file
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

def get_ssh_client():
    ssh_client = paramiko.SSHClient()
    ssh_client.load_system_host_keys()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    return ssh_client

def execute_command(hostname, command, wall_config, time_out=3):
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
                           wall.username, wall.password,
                           look_for_keys=False, timeout=time_out)

        stdin, stdout, stderr = ssh_client.exec_command(command)
        debug(stderr.read())
        output = stdout.read()

        ssh_client.close()

        return output

    except Exception as e:
        err(str(e))

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
        debug(stderr.read())

        sftp_client = ssh_client.open_sftp()
        remote_file = sftp_client.open(file_name, 'w')

        remote_file.write(text)
        remote_file.close()

    except Exception as e:
        err(str(e))

def get_experiment_list(wall_config, project_name=None):
    '''
    Get list of made emulab experiments accessible with your credentials

    @param project_name: optional filter on project
    @param wall_config: vwall configuration data
    @return: list of created experiments (strings)
    '''
    cmd = '/usr/testbed/bin/sslxmlrpc_client.py -m experiment getlist'
    out = execute_command(ops_server(wall_config), cmd)

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
          ' direction=' + \
          direction

    execute_command(ops_server(wall_config), cmd)

def create_experiment(nodes, links, wall_config):
    '''
    Creates an emulab experiment

    @param nodes: Holds the nodes in the experiment
    @param links: Holds the links in the experiment
    @param wall_config: vwall configuration data
    '''
    proj_name = wall_config.proj_name
    exp_name = wall_config.exp_name

    exp_list = get_experiment_list()
    if exp_name in exp_list[proj_name][proj_name]:
        return 'Experiment already exists'

    ns = generate_ns_script(nodes, links)
    dest_file_name = '/users/'+ wall_config.username + \
                     '/temp_ns_file.%s.ns' % os.getpid()
    copy_file_to_vwall(ops_server(wall_config), ns, dest_file_name)

    cmd = '/usr/testbed/bin/sslxmlrpc_client.py startexp ' + \
          'batch=false wait=true proj="' + proj_name + \
          '" exp="' + exp_name + '" noswapin= true' + \
          'nsfilepath="' + file_name + '"'

    execute_command(ops_server(wall_config), cmd, time_out=None)
    execute_command(ops_server(wall_config), 'rm ' + dest_file_name)

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

    debug("Waiting until all nodes are up")

    cmd = '/usr/testbed/bin/script_wrapper.py expinfo -e' + \
          wall_config.proj_name + \
          ',' + \
          wall_config.exp_name + \
          ' -a | grep State | cut -f2,2 -d " "'

    active = False
    while !active:
        res = execute_command(ops_server(wall_config), cmd, wall_config)
        active = True if res == "active"
        debug("Still waiting")
        time.sleep(3)
