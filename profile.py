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

params = pc.bindParameters()

# Validate parameters
if params.public_ip_count < 1:
    pc.reportError(portal.ParameterError('You must allocate at least 1 additional public ip.', ['public_ip_count']))
pc.verifyParameters()

if params.node_count < 1:
    pc.reportError(portal.ParameterError('You must create at least 1 node', ['node_count']))


# Create a variable number of nodes
nodes = []
for i in range(1, params.node_count + 1):
    nodes.append(request.RawPC('node' + str(i)))

# Set node images
for node in nodes:
    node.disk_image = CENTOS7_IMG

# Request a pool of dynamic publically routable ip addresses - pool name cannot contain underscores - hidden bug
addressPool = igext.AddressPool('addressPool', int(params.public_ip_count))
request.addResource(addressPool)

# Add LAN to the rspec. 
lan = request.LAN("lan")

# Must provide a bandwidth. BW is in Kbps
lan.bandwidth = 100000

interfaces = []
# Add interfaces to nodes
for node in nodes:
    interfaces.append(node.addInterface("eth1"))

# Add interfaces to LAN
for interface in interfaces:
    lan.addInterface(interface)

# Output RSpec
pc.printRequestRSpec(request)

