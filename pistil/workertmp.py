# -*- coding: utf-8 -
#
# This file is part of pistil released under the MIT license.
# See the NOTICE for more information.

import os
import tempfile

from pistil import util

class WorkerTmp(object):

    def __init__(self, cfg):
        old_umask = os.umask(cfg.get("umask", 0))
        fd, name = tempfile.mkstemp(prefix="wgunicorn-")

        # allows the process to write to the file
        util.chown(name, cfg.get("uid", os.geteuid()), cfg.get("gid",
            os.getegid()))
        os.umask(old_umask)

        # unlink the file so we don't leak tempory files
        try:
            os.unlink(name)
            self._tmp = os.fdopen(fd, 'w+b', 1)
        except:
            os.close(fd)
            raise

        self.spinner = 0

    def notify(self):
        try:
            self.spinner = (self.spinner+1) % 2
            os.fchmod(self._tmp.fileno(), self.spinner)
        except AttributeError:
            # python < 2.6
            self._tmp.truncate(0)
            os.write(self._tmp.fileno(), "X")

    def fileno(self):
        return self._tmp.fileno()

    def close(self):
        return self._tmp.close()
