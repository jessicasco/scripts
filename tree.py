#!/usr/bin/env python
#coding=utf-8
import argparse
import sys
import os
import stat
import re
import locale

args = None
dir_num = None
file_num = None
xdev = None
pattern = None
ipattern = None
colorize = True
color = {}

def strverscmp(s1, s2):
    if s1 == s2:
        return 0
    if len(s1) <= len(s2):
        length = len(s1)
    else:
        length = len(s2)
    for i in range(length):
        if s1[i] != s2[i]:
            break
    else:
        i += 1
    i -= 1
    while s1[i].isdigit():
        i -= 1
    i += 1
    if not s1[i:]:
        return -1
    elif not s2[i:]:
        return 1
    if not s1[i:].isdigit():
        return cmp(s1, s2)
    if not s2[i:].isdigit():
        return cmp(s1, s2)
    for i in range(len(s1)):
        if s1[i].isdigit():
            break
    s1 = s1[i:]
    s2 = s2[i:]
    if s1.startswith('0') and s2.startswith('0'):
        if len(s1) == 1:
            return 1
        elif len(s2) == 1:
            return -1
        if float('0.' + s1) < float('0.' + s2):
            return -1
        elif float('0.' + s1) > float('0.' + s2):
            return 1
        else:
            if len(s1) > len(s2):
                return 1
            elif len(s1) < len(s2):
                return -1
            else:
                raise
    elif s1.startswith('0') and not s2.startswith('0'):
        return -1
    elif not s1.startswith('0') and not s2.startswith('0'):
        return int(s1) - int(s2)
    else:
        return 1

def parse_dir_colors(force):
    global colorize, color
    if not os.getenv('TERM') or not os.isatty(1):
        colorize = False
        return
    s = os.getenv('LS_COLORS')
    if not s:
        if not force:
            colorize = False
            return
        else:
            s = 'rs=0:di=01;34:ln=01;36:mh=00:pi=40;33:so=01;35:do=01;35:bd=40;33;01:cd=40;33;01:or=01;05;37;41:mi=01;05;37;41:su=37;41:sg=30;43:ca=30;41:tw=30;42:ow=34;42:st=37;44:ex=01;32:*.tar=01;31:*.tgz=01;31:*.arj=01;31:*.taz=01;31:*.lzh=01;31:*.lzma=01;31:*.tlz=01;31:*.txz=01;31:*.zip=01;31:*.z=01;31:*.Z=01;31:*.dz=01;31:*.gz=01;31:*.lz=01;31:*.xz=01;31:*.bz2=01;31:*.bz=01;31:*.tbz=01;31:*.tbz2=01;31:*.tz=01;31:*.deb=01;31:*.rpm=01;31:*.jar=01;31:*.rar=01;31:*.ace=01;31:*.zoo=01;31:*.cpio=01;31:*.7z=01;31:*.rz=01;31:*.jpg=01;35:*.jpeg=01;35:*.gif=01;35:*.bmp=01;35:*.pbm=01;35:*.pgm=01;35:*.ppm=01;35:*.tga=01;35:*.xbm=01;35:*.xpm=01;35:*.tif=01;35:*.tiff=01;35:*.png=01;35:*.svg=01;35:*.svgz=01;35:*.mng=01;35:*.pcx=01;35:*.mov=01;35:*.mpg=01;35:*.mpeg=01;35:*.m2v=01;35:*.mkv=01;35:*.ogm=01;35:*.mp4=01;35:*.m4v=01;35:*.mp4v=01;35:*.vob=01;35:*.qt=01;35:*.nuv=01;35:*.wmv=01;35:*.asf=01;35:*.rm=01;35:*.rmvb=01;35:*.flc=01;35:*.avi=01;35:*.fli=01;35:*.flv=01;35:*.gl=01;35:*.dl=01;35:*.xcf=01;35:*.xwd=01;35:*.yuv=01;35:*.cgm=01;35:*.emf=01;35:*.axv=01;35:*.anx=01;35:*.ogv=01;35:*.ogx=01;35:*.pdf=00;32:*.ps=00;32:*.txt=00;32:*.patch=00;32:*.diff=00;32:*.log=00;32:*.tex=00;32:*.doc=00;32:*.aac=00;36:*.au=00;36:*.flac=00;36:*.mid=00;36:*.midi=00;36:*.mka=00;36:*.mp3=00;36:*.mpc=00;36:*.ogg=00;36:*.ra=00;36:*.wav=00;36:*.axa=00;36:*.oga=00;36:*.spx=00;36:*.xspf=00;36:'
    ss = s.split(':')
    for s in ss:
        if not s:
            continue
        a, b = s.split('=')
        if a.startswith('*'):
            color[a[1:]] = b
        else:
            color[a] = b
    if not 'lc' in color:
        color['lc'] = '\033['
    if not 'rc' in color:
        color['rc'] = 'm'
    if not 'no' in color:
        color['no'] = '00'
    if not 'ec' in color:
        color['ec'] = "%s%s%s" % (color['lc'], color['no'], color['rc'])

def colorify(abspath, path):
    global colorize, color
    if not colorize:
        return path
    stat_mode = os.lstat(abspath).st_mode
    if stat.S_ISFIFO(stat_mode):
        if 'pi' not in color:
            return path
        return "%s%s%s" % (("%s%s%s" % (color['lc'], color['pi'], color['rc'])), path, color['ec'])
    elif stat.S_ISCHR(stat_mode):
        if 'cd' not in color:
            return path
        return "%s%s%s" % (("%s%s%s" % (color['lc'], color['cd'], color['rc'])), path, color['ec'])
    elif stat.S_ISDIR(stat_mode):
        if 'di' not in color:
            return path
        return "%s%s%s" % (("%s%s%s" % (color['lc'], color['di'], color['rc'])), path, color['ec'])
    elif stat.S_ISBLK(stat_mode):
        if 'bd' not in color:
            return path
        return "%s%s%s" % (("%s%s%s" % (color['lc'], color['bd'], color['rc'])), path, color['ec'])
    elif stat.S_ISLNK(stat_mode):
        if 'ln' not in color:
            return path
        return "%s%s%s" % (("%s%s%s" % (color['lc'], color['ln'], color['rc'])), path, color['ec'])
    elif stat.S_ISSOCK(stat_mode):
        if 'so' not in color:
            return path
        return "%s%s%s" % (("%s%s%s" % (color['lc'], color['so'], color['rc'])), path, color['ec'])
    elif stat.S_ISREG(stat_mode):
        if 'ex' not in color:
            return path
        if (stat_mode & stat.S_IXUSR) or (stat_mode & stat.S_IXGRP) or (stat_mode & stat.S_IXOTH):
            return "%s%s%s" % (("%s%s%s" % (color['lc'], color['ex'], color['rc'])), path, color['ec'])
        else:
            ext = os.path.splitext(path)[1]
            if ext and (ext[1:] in color):
                return "%s%s%s" % (("%s%s%s" % (color['lc'], color[ext[1:]], color['rc'])), path, color['ec'])
            else:
                return path
    else:
        return path

def hsize(size):
    if size < 1024:
        return "%4d" % size
    else:
        unit = 'BKMGTPEZY'
        idx = 1
        while size >= (1024 * 1024):
            idx += 1
            size >>= 10
        if (size >> 10) >= 10:
            return "%3.0f%c" % ((size * 1.0 / 1024), unit[idx])
        else:
            return "%3.1f%c" % ((size * 1.0 / 1024), unit[idx])

def get_attrs(path):
    global args
    attrs = []
    stat_result = os.lstat(path)
    if args.inodes:
        attrs.append(stat_result.st_ino)
    if args.device:
        attrs.append(stat_result.st_dev)
    if args.p:
        if stat.S_ISDIR(stat_result.st_mode):
            p = 'd'
        else:
            p = '-'
        if stat_result.st_mode & stat.S_IRUSR:
            p += 'r'
        else:
            p += '-'
        if stat_result.st_mode & stat.S_IWUSR:
            p += 'w'
        else:
            p += '-'
        if stat_result.st_mode & stat.S_IXUSR:
            p += 'x'
        else:
            p += '-'
        if stat_result.st_mode & stat.S_IRGRP:
            p += 'r'
        else:
            p += '-'
        if stat_result.st_mode & stat.S_IWGRP:
            p += 'w'
        else:
            p += '-'
        if stat_result.st_mode & stat.S_IXGRP:
            p += 'x'
        else:
            p += '-'
        if stat_result.st_mode & stat.S_IROTH:
            p += 'r'
        else:
            p += '-'
        if stat_result.st_mode & stat.S_IWOTH:
            p += 'w'
        else:
            p += '-'
        if stat_result.st_mode & stat.S_IXOTH:
            p += 'x'
        else:
            p += '-'
        attrs.append(p)
    if args.u:
        attrs.append(stat_result.st_uid)
    if args.g:
        attrs.append(stat_result.st_gid)
    if args.s or args.h:
        if args.h:
            attrs.append(hsize(stat_result.st_size))
        else:
            attrs.append('%11ld' % stat_result.st_size)
    if args.D:
        attrs.append(stat_result.st_mtime)
    attrs = map(str, attrs)
    return attrs

def print_attrs(attrs):
    if attrs:
        print '[' + ' '.join(attrs) + ']',

def file_type(path):
    stat_mode = os.lstat(path).st_mode
    if stat.S_ISDIR(stat_mode):
        t = '/'
    elif stat.S_ISREG(stat_mode) and (
            (stat.S_IXUSR & stat_mode) or
            (stat.S_IXGRP & stat_mode) or
            (stat.S_IXOTH & stat_mode)):
        t = '*'
    elif stat.S_ISFIFO(stat_mode):
        t = '|'
    elif stat.S_ISLNK(stat_mode):
        t = '@'
    elif stat.S_ISSOCK(stat_mode):
        t = '='
    else:
        t = ''
    return t

def visit_dir(directory, indent, last=False, exceptions=[], level=0):
    global args, dir_num, file_num, xdev, pattern, ipattern
    s = ''
    if indent:
        for i in range(indent-1):
            if i in exceptions:
                s += '    '
            else:
                s += '│   '
        if last:
            s += '└──'
        else:
            s += '├──'
        if not args.i:
            print s,
        print_attrs(get_attrs(directory))
        if args.f:
            if args.F:
                print colorify(os.path.abspath(directory), os.path.abspath(directory)) + file_type(directory),
            else:
                print colorify(os.path.abspath(directory), os.path.abspath(directory)),
        else:
            if args.F:
                print colorify(os.path.abspath(directory), os.path.basename(directory)) + file_type(directory),
            else:
                print colorify(os.path.abspath(directory), os.path.basename(directory)),
        dir_num += 1
        num = len(os.listdir(directory))
        if os.path.islink(directory):
            print  '->', colorify(os.path.realpath(directory), os.path.realpath(directory)),
            if args.filelimit and (int(args.filelimit) > 0) and (int(args.filelimit) <= num ):
                print "[%s entries exceeds filelimit, not opening dir]" % num
                return
            if not args.l:
                print
                return
        if args.filelimit and (int(args.filelimit) > 0) and (int(args.filelimit) <= num ):
            print "[%s entries exceeds filelimit, not opening dir]" % num
            return
        print
    if args.L and (int(args.L) > 0) and (level >= int(args.L)):
        return
    dirs = []
    files = []
    if args.t:
        sorted_dir = sorted(os.listdir(directory), key=lambda d: os.stat(os.path.join(directory, d)).st_mtime, reverse=True)
    elif args.r:
        sorted_dir = sorted(os.listdir(directory), cmp=locale.strcoll, reverse=True)
    elif args.v:
        sorted_dir = sorted(os.listdir(directory), cmp=strverscmp)
    else:
        sorted_dir = sorted(os.listdir(directory), cmp=locale.strcoll)
    for name in sorted_dir:
        if os.path.isdir(os.path.join(directory, name)):
            if args.x and (os.lstat(os.path.join(directory, name)).st_dev != xdev):
                pass
            else:
                dirs.append(os.path.join(directory, name))
        else:
            if args.d:
                continue
            if args.P:
                if not pattern.search(name).group():
                    continue
            if args.I:
                if ipattern.search(name).group():
                    continue
            if args.f:
                files.append(os.path.abspath(os.path.join(directory, name)))
            else:
                files.append(name)
    if not args.a:
        dirs = [d for d in dirs if not os.path.basename(d).startswith('.')]
        files = [f for f in files if not os.path.basename(f).startswith('.')]
    s = ''
    for i in range(indent):
        if i in exceptions:
            s += '    '
        else:
            s += '│   '
    if args.dirsfirst:
        sorted_dir = dirs + files
    for name in sorted_dir:
        if os.path.isdir(os.path.join(directory, name)):
            if not os.path.join(directory, name) in dirs:
                continue
            name = dirs.pop(0)
            if dirs:
                visit_dir(name, indent+1, False, exceptions[:], level+1)
            elif files:
                visit_dir(name, indent+1, False, exceptions[:], level+1)
            else:
                visit_dir(name, indent+1, True, exceptions+[indent], level+1)
        else:
            if not name in files:
                continue
            name = files.pop(0)
            if files or dirs:
                if not args.i:
                    print s + '├──', 
            else:
                if not args.i:
                    print s + '└──', 
            print_attrs(get_attrs(os.path.join(directory, name)))
            if args.F:
                print colorify(os.path.abspath(os.path.join(directory, name)), name) + file_type(os.path.join(directory, name))
            else:
                print colorify(os.path.abspath(os.path.join(directory, name)), name)
            file_num += 1

def parse():
    parser = argparse.ArgumentParser(
            description='list contents of directories in a tree-like format.', 
            prog='tree',
            add_help=False,
            )
    parser.add_argument('-a', action='store_true',
            help='All files are listed.')
    parser.add_argument('-d', action='store_true',
            help='List directories only.')
    parser.add_argument('-l', action='store_true',
            help='Follow symbolic links like directories.')
    parser.add_argument('-f', action='store_true',
            help='Print the full path prefix for each file.')
    parser.add_argument('-i', action='store_true',
            help="Don't print indentation lines.")
    parser.add_argument('-p', action='store_true',
            help='Print the protections for each file.')
    parser.add_argument('-u', action='store_true',
            help='Displays file owner or UID number.')
    parser.add_argument('-g', action='store_true',
            help='Displays file group owner or GID number.')
    parser.add_argument('-s', action='store_true',
            help='Print the size in bytes of each file.')
    parser.add_argument('-h', action='store_true', 
            help='Print the size in a more human readable way.')
    parser.add_argument('-D', action='store_true',
            help='Print the date of last modification.')
    parser.add_argument('-F', action='store_true',
            help="Appends '/', '=', '*', or '|' as per ls -F.")
    parser.add_argument('-v', action='store_true',
            help='Sort files alphanumerically by version.')
    parser.add_argument('-r', action='store_true',
            help='Sort files in reverse alphanumeric order.')
    parser.add_argument('-t', action='store_true',
            help='Sort files by last modification time.')
    parser.add_argument('--dirsfirst', action='store_true',
            help='List directories before files.')
    parser.add_argument('-x', action='store_true',
            help='Stay on current filesystem only.')
    parser.add_argument('-L', metavar='level',
            help='Descend only level directories deep.')
    parser.add_argument('-n', action='store_true',
            help='Turn colorization off always (-C overrides).')
    parser.add_argument('-C', action='store_true',
            help='Turn colorization on always.')
    parser.add_argument('-P', metavar='pattern',
            help='List only those files that match the pattern given.')
    parser.add_argument('-I', metavar='pattern',
            help='Do not list files that match the given pattern.')
    parser.add_argument('-o', metavar='file', 
            help='Output to file instead of stdout.')
    parser.add_argument('--inodes', action='store_true',
            help='Print inode number of each file.')
    parser.add_argument('--device', action='store_true',
            help='Print device ID number to which each file belongs.')
    parser.add_argument('--noreport', action='store_true',
            help='Turn off file/directory count at end of tree listing.')
    parser.add_argument('--filelimit', metavar='#',
            help='Do not descend dirs with more than # files in them.')
    parser.add_argument('--version', action='version', 
            version='%(prog)s 1.0 by Isaiah Qian(qianlongzju@gmail.com)')
    parser.add_argument('--help', action='store_true', 
            help='show this help message')
    parser.add_argument('directory', default='.', nargs='*')
    args = parser.parse_args()
    if args.help:
        parser.print_help()
        sys.exit()
    return args

def main():
    global args, dir_num, file_num, xdev, pattern, ipattern, colorize
    args = parse()
    dir_num = 0
    file_num = 0
    if args.o:
        sys.stdout = open(args.o, 'w')
    if args.P:
        pattern = re.compile(args.P)
    if args.I:
        ipattern = re.compile(args.I)
    if args.n:
        colorize = False
    if args.C:
        colorize = True
        parse_dir_colors(True)
    elif colorize:
        parse_dir_colors(False)
    for directory in args.directory:
        print colorify(directory, directory)
        directory = os.path.abspath(directory)
        xdev = os.lstat(directory).st_dev
        visit_dir(directory, 0, False, [], 0)
    if args.noreport:
        return
    print
    print dir_num, 
    if dir_num > 1:
        print 'directories,', 
    else:
        print 'directory,',
    print file_num, 
    if file_num > 1:
        print 'files'
    else:
        print 'file'

if __name__ == '__main__':
    main()
