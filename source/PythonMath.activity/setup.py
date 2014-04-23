#!/usr/bin/env python
# Copyright (C) 2008 Red Hat, Inc.
# Copyright (C) 2012 Robert Deaton
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.

# This file is based on the bundlebuilder.py from sugar.activity
# It is to be used so that most of the features of bundlebuilder.py can happen
# outside of a sugar environment

import os
import sys
import zipfile
import tarfile
import shutil
import subprocess
import re
import gettext
from optparse import OptionParser
import logging
from fnmatch import fnmatch

source_dir = os.getcwd()
dist_dir = os.path.join(os.getcwd(), 'dist')
bundle_name = source_dir[source_dir.rfind(os.sep)+1:]
for l in open('activity/activity.info'):
    m = re.match('(.*?)=(.*?)\n', l)
    if m is None:
        continue
    key, value = m.groups()
    key, value = key.strip(), value.strip()
    if key == 'name':
        activity_name = value
    if key == 'bundle_id':
        bundle_id = value
IGNORE_DIRS = ['dist', '.git', 'profiles', 'skel']
IGNORE_FILES = ['.gitignore', 'MANIFEST', '*.pyc', '*~', '*.bak', 'pseudo.po']
        
def list_files(base_dir, ignore_dirs=None, ignore_files=None):
    result = []

    for root, dirs, files in os.walk(base_dir):
        if ignore_files:
            for pattern in ignore_files:
                files = [f for f in files if not fnmatch(f, pattern)]
                
        rel_path = root[len(base_dir) + 1:]
        for f in files:
            if rel_path:
                result.append('/'.join((rel_path, f)))
            else:
                result.append(f)

        if ignore_dirs:
            for ignore in ignore_dirs:
                if ignore in dirs:
                    dirs.remove(ignore)

    return result

class Builder(object):
    def build(self):
        self.build_locale()

    def build_locale(self):
        po_dir = '/'.join((os.getcwd(), 'po'))

        if not os.path.isdir(po_dir):
            logging.warn("Missing po/ dir, cannot build_locale")
            return
        
        locale_dir = '/'.join((source_dir, 'locale'))

        if os.path.exists(locale_dir):
            shutil.rmtree(locale_dir)

        for f in os.listdir(po_dir):
            if not f.endswith('.po') or f == 'pseudo.po':
                continue

            file_name = '/'.join((po_dir, f))
            lang = f[:-3]

            localedir = '/'.join((source_dir, 'locale', lang))
            mo_path = '/'.join((localedir, 'LC_MESSAGES'))
            if not os.path.isdir(mo_path):
                os.makedirs(mo_path)

            mo_file = '/'.join((mo_path, "%s.mo" % bundle_id))
            args = ["msgfmt", "--output-file=%s" % mo_file, file_name]
            retcode = subprocess.call(args)
            if retcode:
                print 'ERROR - msgfmt failed with return code %i.' % retcode

            cat = gettext.GNUTranslations(open(mo_file, 'r'))
            translated_name = cat.gettext(activity_name)
            linfo_file = '/'.join((localedir, 'activity.linfo'))
            f = open(linfo_file, 'w')
            f.write('[Activity]\nname = %s\n' % translated_name)
            f.close()
            
            print 'Built files for lang %s' % lang

    def get_files(self):
        self.fix_manifest()
        manifest = open('MANIFEST', 'r')
        files = [line.strip() for line in (manifest) if line]
        files.append('MANIFEST')

        return files

        
    def fix_manifest(self):
        self.build()

        allfiles = list_files(source_dir, IGNORE_DIRS, IGNORE_FILES)
        
        f = open(os.path.join(source_dir, "MANIFEST"), "wb")
        for line in allfiles:
            f.write(line + "\n")

class Packager(object):
    def __init__(self):
        self.package_path = None

        if not os.path.exists(dist_dir):
            os.mkdir(dist_dir)

class XOPackager(Packager):
    def __init__(self, builder):
        Packager.__init__(self)

        self.builder = builder
        self.package_path = os.path.join(dist_dir, activity_name + '.xo')

    def package(self):
        bundle_zip = zipfile.ZipFile(self.package_path, 'w',
                                     zipfile.ZIP_DEFLATED)
        for f in self.builder.get_files():
            bundle_zip.write('/'.join((source_dir, f)).strip(),
                             '/'.join((bundle_name, f.strip())))
        bundle_zip.close()
        print 'Wrote to %s' % self.package_path

class WindowsPackager(Packager):
    def __init__(self, builder):
        Packager.__init__(self)
        
        from distutils.core import setup
        import py2exe

        self.builder = builder
        self.package_path = os.path.join(dist_dir, activity_name + '.xo')

    def package(self):
        setup(console=['dev_launcher.py'])
        """
        bundle_zip = zipfile.ZipFile(self.package_path, 'w',
                                     zipfile.ZIP_DEFLATED)
        for f in self.builder.get_files():
            bundle_zip.write('/'.join((source_dir, f)).strip(),
                             '/'.join((bundle_name, f.strip())))
        bundle_zip.close()
        print 'Wrote to %s' % self.package_path
        """

class SourcePackager(Packager):
    def __init__(self, builder):
        Packager.__init__(self)
        self.builder = builder
        self.package_path = os.path.join(dist_dir,
                                         activity_name + '.tar.bz2')

    def package(self):
        tar = tarfile.open(self.package_path, 'w:bz2')
        for f in self.builder.get_files():
            tar.add(os.path.join(source_dir, f), f)
        tar.close()
        print 'Wrote to %s' % self.package_path

def cmd_dev(args):
    '''Setup for development'''
    print 'This works from within sugar only.'
        
def cmd_dist_xo(args):
    '''Create a xo bundle package'''

    if args:
        print 'Usage: %prog dist_xo'
        return
   
    packager = XOPackager(Builder())
    packager.package()

def cmd_dist_windows(args):
    '''Create a windows executable'''
    
    if args:
        print 'Usage: %prog dist_windows'
        return
    
    packager = WindowsPackager(Builder())
    packager.package()

def cmd_fix_manifest(args):
    '''Add missing files to the manifest'''

    if args:
        print 'Usage: %prog fix_manifest'
        return

    builder = Builder()
    builder.fix_manifest()

def cmd_dist_source(args):
    '''Create a tar source package'''

    if args:
        print 'Usage: %prog dist_source'
        return

    packager = SourcePackager(Builder())
    packager.package()

def cmd_install(args):
    '''Install the activity in the system'''

    print 'This works from within sugar only.'

def cmd_genpot(args):
    '''Generate the gettext pot file'''

    if args:
        print 'Usage: %prog genpot'
        return

    po_path = os.path.join(source_dir, 'po')
    if not os.path.isdir(po_path):
        os.mkdir(po_path)

    python_files = []
    for root_dummy, dirs_dummy, files in os.walk(source_dir):
        for file_name in files:
            if file_name.endswith('.py'):
                python_files.append(os.path.join(root_dummy, file_name))

    # First write out a stub .pot file containing just the translated
    # activity name, then have xgettext merge the rest of the
    # translations into that. (We can't just append the activity name
    # to the end of the .pot file afterwards, because that might
    # create a duplicate msgid.)
    pot_file = os.path.join('po', '%s.pot' % activity_name)
    escaped_name = re.sub('([\\\\"])', '\\\\\\1', activity_name)
    f = open(pot_file, 'w')
    f.write('#: activity/activity.info:2\n')
    f.write('msgid "%s"\n' % escaped_name)
    f.write('msgstr ""\n')
    f.close()

    args = [ 'xgettext', '--join-existing', '--language=Python',
             '--keyword=_', '--add-comments=TRANS:', '--output=%s' % pot_file ]

    args += python_files
    try:
        retcode = subprocess.call(args)
    except OSError:
        print 'ERROR - Do you have gettext installed?'
        return

    if retcode:
        print 'ERROR - xgettext failed with return code %i.' % retcode
        

def cmd_release(args):
    '''Do a new release of the bundle'''
    print 'This works from within sugar only.'

def cmd_build(args):
    '''Build generated files'''

    if args:
        print 'Usage: %prog build'
        return

    builder = Builder()
    builder.build()

def print_commands():
    print 'Available commands:\n'

    for name, func in globals().items():
        if name.startswith('cmd_'):
            print "%-20s %s" % (name.replace('cmd_', ''), func.__doc__)

    print '\n(Type "./setup.py <command> --help" for help about a ' \
          'particular command\'s options.'

def start(bundle_name=None):
    if bundle_name:
        logging.warn("bundle_name deprecated, now comes from activity.info")

    parser = OptionParser(usage='[action] [options]')
    parser.disable_interspersed_args()
    (options_, args) = parser.parse_args()

    # config = Config()

    try:
        globals()['cmd_' + args[0]](args[1:])
    except (KeyError, IndexError):
        print_commands()

if __name__ == "__main__":
    try:
        from sugar.activity import bundlebuilder
        bundlebuilder.start()
    except ImportError:
        start()