# Copyright (C) 2012 Johnny Vestergaard <jkv@unixcluster.dk>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging

import gevent
import logging

from loggers import loggerbase
from loggers import testlogger
from loggers import hpfeeds

logger = logging.getLogger(__name__)


class Consumer:
    def __init__(self, sessions):
        logging.debug('Consumer created.')
        self.sessions = sessions

    def start_handling(self):
        active_loggers = self.get_loggers()

        while True:
            for session_id in self.sessions.keys():
                session = self.sessions[session_id]
                if not session.is_connected:
                    for log in active_loggers:
                        log.log(session)
                    del self.sessions[session_id]
                    logger.debug('Removed {0} connection from {1}. ({2})'.format(session.protocol,
                                                                                 session.attacker_ip,
                                                                                 session.id))
            gevent.sleep(5)

    def stop_handling(self):
        pass

    def get_loggers(self):
        loggers = []
        for l in loggerbase.LoggerBase.__subclasses__():
            logger = l()
            loggers.append(logger)
        return loggers