#!/usr/bin/env python

# Copyright (C) 2008, Mathieu PASQUET <Mathieu PASQUET mpa@makina-corpus.com>
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

__docformat__ = 'restructuredtext en'

import os
import getpass
import pwd
import grp
import re

def conf(o, b):
    add = ''
    if os.uname()[0] == 'Darwin':
        add = '--disable-pcreposix'
    user=getpass.getuser()
    gid = pwd.getpwnam(user)[3]
    group = grp.getgrgid(gid)[0]
    os.chdir(o['compile-directory'])
    os.system(
        'export ac_cv_func_malloc_0_nonnull=yes && '
        './configure --prefix=%s --with-ssl=%s --with-owner=%s '
        '--with-group=%s %s' % (
            o['location'],
            o['ssl'],
            o.get('user', user),
            o.get('group', group),
            add
        )
    )
    os.environ['LD_RUN_PATH'] = o['ssl'] + '/parts/part/lib'
    f = open('Makefile').read()
    f = re.sub('CFLAGS=', 'CFLAGS=-I%s/include -I%s/include/openssl ' % (o['ssl'], o['ssl']), f)
    f = re.sub('LIBS=', 'LIBS=-L%s/lib -Wl,-rpath -Wl,%s/lib ' % (o['ssl'], o['ssl']), f)
    open('Makefile', 'w').write(f)

# vim:set et sts=4 ts=4 tw=80:
