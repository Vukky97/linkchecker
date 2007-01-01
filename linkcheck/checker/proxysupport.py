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
"""
Mixin class for URLs that can be fetched over a proxy.
"""

import urllib
import linkcheck

class ProxySupport (object):
    """
    Get support for proxying and for URLs with user:pass@host setting.
    """

    def set_proxy (self, proxy):
        """
        Parse given proxy information and store parsed values.
        Note that only http:// proxies are supported, both for ftp://
        and http:// URLs.
        """
        self.proxy = proxy
        self.proxyauth = None
        if not self.proxy:
            return
        if self.proxy[:7].lower() != "http://":
            # Note that invalid proxies might raise TypeError in urllib2,
            # so make sure to stop checking at this point, not later.
            msg = _("Proxy value %r must start with 'http://'.") % self.proxy
            raise linkcheck.LinkCheckerError(msg)
        self.proxy = urllib.splittype(self.proxy)[1]
        self.proxy = urllib.splithost(self.proxy)[0]
        self.proxyauth, self.proxy = urllib.splituser(self.proxy)
        if self.ignore_proxy_host():
            # log proxy without auth info
            self.add_info(_("Ignoring proxy setting %r") % self.proxy)
            self.proxy = None
            self.proxyauth = None
            return
        self.add_info(_("Using proxy %r.") % self.proxy)
        if self.proxyauth is not None:
            if ":" not in self.proxyauth:
                self.proxyauth += ":"
            import base64
            self.proxyauth = base64.encodestring(self.proxyauth).strip()
            self.proxyauth = "Basic "+self.proxyauth


    def ignore_proxy_host (self):
        """
        Check if self.host is in the no-proxy-for ignore list.
        """
        for ro in self.aggregate.config["noproxyfor"]:
            if ro.search(self.host):
                return True
        return False
