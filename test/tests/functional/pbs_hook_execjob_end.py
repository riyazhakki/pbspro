# coding: utf-8

# Copyright (C) 1994-2018 Altair Engineering, Inc.
# For more information, contact Altair at www.altair.com.
#
# This file is part of the PBS Professional ("PBS Pro") software.
#
# Open Source License Information:
#
# PBS Pro is free software. You can redistribute it and/or modify it under the
# terms of the GNU Affero General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# PBS Pro is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.
# See the GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Commercial License Information:
#
# For a copy of the commercial license terms and conditions,
# go to: (http://www.pbspro.com/UserArea/agreement.html)
# or contact the Altair Legal Department.
#
# Altair’s dual-license business model allows companies, individuals, and
# organizations to create proprietary derivative works of PBS Pro and
# distribute them - whether embedded or bundled with other software -
# under a commercial license agreement.
#
# Use of Altair’s trademarks, including but not limited to "PBS™",
# "PBS Professional®", and "PBS Pro™" and Altair’s logos is subject to Altair's
# trademark licensing policies.
from tests.functional import *


class TestPbsExecjobEnd(TestFunctional):
    """
    This tests the feature in PBS that allows
    execjob_end hook to execute such that
    pbs_mom is not blocked upon execution.
    """

    def setUp(self):
        TestFunctional.setUp(self)
        self.attr = {'event': 'execjob_end', 'enabled': 'True', 'alarm': '50'}
        self.hook_body = ("import pbs\n"
                          "import time\n"
                          "e = pbs.event()\n"
                          "pbs.logjobmsg(e.job.id, \
                                         'executed execjob_end hook')\n"
                          "time.sleep(10)\n"
                          "pbs.logjobmsg(e.job.id, \
                                         'execjob_end hook ended')\n"
                          "e.accept()\n")

    def test_execjob_end_non_blocking(self):
        """
        Test to make sure pbs_mom is not blocked upon
        execution of an execjob_end hook.
        """
        hook_name = "execjob_end_logmsg"
        self.server.create_import_hook(hook_name, self.attr, self.hook_body)
        hook_name = "exechost_periodic_logmsg"
        hook_body = ("import pbs\n"
                     "e = pbs.event()\n"
                     "pbs.logmsg(pbs.LOG_DEBUG, \
                                 'executed exechost_periodic hook')\n"
                     "e.accept()\n")
        attr = {'event': 'exechost_periodic', 'freq': '3', 'enabled': 'True'}
        attrj = {'Resource_List.select': 'ncpus=1'}
        j = Job(TEST_USER, attrs=attrj)
        j.set_sleep_time(1)
        self.server.create_import_hook(hook_name, attr, hook_body)
        jid = self.server.submit(j)
        self.mom.log_match("Job;%s;executed execjob_end hook" % jid,
                           n=100, max_attempts=10, interval=2)
        self.mom.log_match("executed exechost_periodic hook",
                           n=100, max_attempts=10, interval=2)
        self.mom.log_match("Job;%s;execjob_end hook ended" % jid,
                           n=100, max_attempts=10, interval=2)

    def test_execjob_end_hook_order_and_reject(self):
        """
        Test with mutiple execjob_end hooks with with
        different order for a job with one of the hooks rejecting the job.
        """
        hook_name1 = "execjob_end_logmsg1"
        hook_body = ("import pbs\n"
                     "e = pbs.event()\n"
                     "pbs.logjobmsg(e.job.id, \
                                  'executed %s hook' % e.hook_name)\n"
                     "e.accept()\n")
        attr = {'event': 'execjob_end', 'order': '1', 'enabled': 'True'}
        self.server.create_import_hook(hook_name1, attr, hook_body)
        hook_name = "execjob_end_logmsg2"
        hook_body1 = ("import pbs\n"
                      "e = pbs.event()\n"
                      "pbs.logjobmsg(e.job.id, 'executed execjob_end hook')\n"
                      "e.reject('Job is rejected')\n")
        attr = {'event': 'execjob_end', 'order': '2', 'enabled': 'True'}
        self.server.create_import_hook(hook_name, attr, hook_body1)
        hook_name2 = "execjob_end_logmsg3"
        attr = {'event': 'execjob_end', 'order': '170', 'enabled': 'True'}
        self.server.create_import_hook(hook_name2, attr, hook_body)
        attrj = {'Resource_List.select': 'ncpus=1'}
        j = Job(TEST_USER, attrs=attrj)
        j.set_sleep_time(1)
        jid = self.server.submit(j)
        self.mom.log_match("Job;%s;executed %s hook" % (jid, hook_name1),
                           n=100, max_attempts=10, interval=2)
        self.mom.log_match("Job;%s;Job is rejected" % jid,
                           n=100, max_attempts=10, interval=2)
        self.mom.log_match("Job;%s;executed %s hook" % (jid, hook_name2),
                           n=100, max_attempts=10, interval=2, existence=False)

    def test_execjob_end_multi_job(self):
        """
        Test a execjob_end hook for non-blocking of mom with mutiple jobs
        """
        hook_name = "execjob_end_logmsg4"
        self.server.create_import_hook(hook_name, self.attr, self.hook_body)
        attrj = {'Resource_List.select': 'ncpus=1'}
        j = Job(TEST_USER, attrs=attrj)
        j.set_sleep_time(1)
        jid1 = self.server.submit(j)
        j.set_sleep_time(1)
        jid2 = self.server.submit(j)
        self.mom.log_match("Job;%s;executed execjob_end hook" % jid1,
                           n=100, max_attempts=10, interval=2)
        self.mom.log_match("Job;%s;executed execjob_end hook" % jid2,
                           n=100, max_attempts=10, interval=2)
        self.mom.log_match("Job;%s;execjob_end hook ended" % jid1,
                           n=100, max_attempts=10, interval=2)
        self.mom.log_match("Job;%s;execjob_end hook ended" % jid2,
                           n=100, max_attempts=10, interval=2)
