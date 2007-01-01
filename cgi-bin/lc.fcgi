#!/usr/bin/python2.4
# -*- coding: iso-8859-1 -*-
# Copyright (C) 2000-2007 Bastian Kleineidam
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

import fcgi
import linkcheck
import linkcheck.lc_cgi

# access: a list of IP numbers
ALLOWED_HOSTS = ['127.0.0.1']
ALLOWED_SERVERS = ['127.0.0.1']
# main
try:
    while fcgi.isFCGI():
        req = fcgi.FCGI()
        linkcheck.lc_cgi.startoutput(out=req.out)
        if linkcheck.lc_cgi.checkaccess(out=req.out, hosts=ALLOWED_HOSTS,
                                        servers=ALLOWED_SERVERS, env=req.env):
            linkcheck.lc_cgi.checklink(out=req.out,
                                       form=req.getFieldStorage(),
                                       env=req.env)
        req.Finish()
except:
    import traceback
    traceback.print_exc(file = open('traceback', 'a'))

