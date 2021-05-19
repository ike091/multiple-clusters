"""Spins up nodes for installing multiple SLATE clusters.

Instructions:
Wait for the profile instance to start, and then follow instructions on the SLATE website for cluster install.
"""

import geni.portal as portal
import geni.rspec.pg as pg
import geni.rspec.emulab as emulab
import geni.rspec.igext as igext

# Define OS image
CENTOS7_IMG = 'urn:publicid:IDN+emulab.net+image+emulab-ops:CENTOS7-64-STD'

# Create a portal context, needed to define parameters
pc = portal.Context()

# Create a Request object to start building RSpec
request = pc.makeRequestRSpec()


# Create some user-configurable parameters
pc.defineParameter('public_ip_count', 'The number of additional public IPs to allocate', portal.ParameterType.INTEGER, 2)
pc.defineParameter('node_count', 'The number of nodes to create', portal.ParameterType.INTEGER, 2)
pc.defineParameter('lan_latency', 'Simulated additional latency (ms)', portal.ParameterType.INTEGER, 0)
pc.defineParameter('lan_packet_loss', 'Simulated additional packet loss (0.0 - 1.0)', portal.ParameterType.STRING, '0.0')

params = pc.bindParameters()

# Validate public ip count
if params.public_ip_count < 1:
    pc.reportError(portal.ParameterError('You must allocate at least 1 additional public ip.', ['public_ip_count']))
pc.verifyParameters()

# Validate node count
if params.node_count < 1:
    pc.reportError(portal.ParameterError('You must create at least 1 node.', ['node_count']))

# Validate simulated latency
if params.lan_latency < 0:
    pc.reportError(portal.ParameterError('The latency parameter must be positive.', ['lan_latency']))

# Validate simulated packet loss
packet_loss_float = 0
try:
    packet_loss_float = float(params.lan_packet_loss)
except:
    pc.reportError(portal.ParameterError('The packet loss parameter is not valid.', ['lan_packet_loss']))
if packet_loss_float < 0.0 or packet_loss_float > 1.0:
    pc.reportError(portal.ParameterError('The packet loss parameter must be between 0.0 and 1.0', ['lan_packet_loss']))


# Create a variable number of nodes
nodes = []
for i in range(1, params.node_count + 1):
    #  nodes.append(request.RawPC('node' + str(i)))
    nodes.append(request.XenVM('node' + str(i)))

# Set node images
for node in nodes:
    node.disk_image = CENTOS7_IMG

# Request a pool of dynamic publically routable ip addresses - pool name cannot contain underscores - hidden bug
addressPool = igext.AddressPool('addressPool', int(params.public_ip_count))
request.addResource(addressPool)

# Add LAN to the rspec. 
lan = request.LAN("lan")

# Add a link to the request and then add the interfaces to the link
link = request.Link("link")

# Specify duplex parameters for each of the nodes in the link (or lan).
# BW is in Kbps
link.bandwidth = 110000
# Latency is in milliseconds
link.latency = params.lan_latency
# Packet loss is a number 0.0 <= loss <= 1.0
link.plr = packet_loss_float

interfaces = []
# Add interfaces to nodes
for node in nodes:
    interfaces.append(node.addInterface("eth1"))

# Add interfaces to LAN
for interface in interfaces:
    lan.addInterface(interface)

# Declare install script function
def run_install_script(this_node, script_name):
    """Runs a bash script from the install/ directory on a specific node."""

    this_node.addService(pg.Execute(shell='sh', command='chmod +x /local/repository/install/' + script_name))
    this_node.addService(pg.Execute(shell='sh', command='/local/repository/install/' + script_name))


run_install_script(nodes[0], 'install_perfsonar.sh')


# Output RSpec
pc.printRequestRSpec(request)

