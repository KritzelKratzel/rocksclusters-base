# $Id: __init__.py,v 1.1 2010/04/30 22:07:16 bruno Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		       version 5.2 (Chimichanga)
# 
# Copyright (c) 2000 - 2009 The Regents of the University of California.
# All rights reserved.	
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
# 
# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright
# notice unmodified and in its entirety, this list of conditions and the
# following disclaimer in the documentation and/or other materials provided 
# with the distribution.
# 
# 3. All advertising and press materials, printed or electronic, mentioning
# features or use of this software must display the following acknowledgement: 
# 
# 	"This product includes software developed by the Rocks(r)
# 	Cluster Group at the San Diego Supercomputer Center at the
# 	University of California, San Diego and its contributors."
# 
# 4. Except as permitted for the purposes of acknowledgment in paragraph 3,
# neither the name or logo of this software nor the names of its
# authors may be used to endorse or promote products derived from this
# software without specific prior written permission.  The name of the
# software includes the following terms, and any derivatives thereof:
# "Rocks", "Rocks Clusters", and "Avalanche Installer".  For licensing of 
# the associated name, interested parties should contact Technology 
# Transfer & Intellectual Property Services, University of California, 
# San Diego, 9500 Gilman Drive, Mail Code 0910, La Jolla, CA 92093-0910, 
# Ph: (858) 534-5815, FAX: (858) 534-7345, E-MAIL:invent@ucsd.edu
# 
# THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS''
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN
# IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# 
# @Copyright@
#
# $Log: __init__.py,v $
# Revision 1.1  2010/04/30 22:07:16  bruno
# first pass at the firewall commands. we can do global and host level
# rules, that is, we can add, remove, open (calls add), close (also calls add),
# list and dump the global rules and the host-specific rules.
#
#

import rocks.commands

class Command(rocks.commands.HostArgumentProcessor,
	rocks.commands.open.command):
	"""
	Open a service for hosts in the cluster. This will open up the
	firewall for all the specified hosts to allow the packets for a
	service to flow into the hosts.

	<arg type='string' name='host'>
	Host name of machine
	</arg>

	<arg type='string' name='service'>
	The service identifier, port number or port range. For example
	"www", 8080 or 0:1024.
	</arg>

	<param type='string' name='protocol'>
	The protocol associated with the service. For example, "tcp" or "udp".
	</param>
	
        <param type='string' name='network'>
        The network this service should be opened on. This is a named network
        (e.g., 'private') and must be listable by the command
        'rocks list network'.
	</param>
	"""

	def run(self, params, args):
		(args, service) = self.fillPositionalArgs(('service'))
		(network, protocol) = self.fillParams([
			('network', ),
			('protocol', )
			])

		if len(args) == 0:
			self.abort('must supply at least one host')

		if not service:
			self.abort('service required')
		if not network:
			self.abort('network required')
		if service not in [ 'all', 'nat' ] and not protocol:
			self.abort('protocol required')

		hosts = self.getHostnames(args)
		
		cmd = ()
		if service:
			cmd += ('service=%s' % service, )
		if network:
			cmd += ('network=%s' % network, )
		if protocol:
			cmd += ('protocol=%s' % protocol, )

		#
		# since this is an 'open' command, we assume the action is
		# "ACCEPT" and the chain is "INPUT"
		#
		cmd += ('action=ACCEPT', )
		cmd += ('chain=INPUT', )

		for host in hosts:
			self.command('add.host.firewall', (host, ) + cmd)
