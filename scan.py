# -*- coding: utf-8 -*-
import os
import sys
import subprocess
import getopt
import shutil
import re

tasks = []

class RunCMD:
    def __init__(self, cmd):
        self.p = None
        self.cmd = cmd

    def run_cmd(self):
        self.p = subprocess.Popen(self.cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        tasks.append(self)
        return self.p.communicate()

    @property
    def is_running(self):
        if self.p.poll() is None:
            return True
        else:
            tasks.remove(self)
            return False

    def stop(self):
        self.p.kill()
        tasks.remove(self)

    def log(self):
        return ''.join([str(item, encoding='utf-8') for item in self.p.communicate()])


def printUse():
    print('''
    Usage:      
        python3 scan.py -i xxx.ipa -f checklist
    
        -h show help
        -i <IPA Path>
        -f <CheckList Path>
    ''')


def add_escape(value):
    reserved_chars = r'''?&|!{}[]()^~*:\\"'+- '''
    replace = ['\\' + l for l in reserved_chars]
    trans = str.maketrans(dict(zip(reserved_chars, replace)))
    return value.translate(trans)


def main(argv):
    inputfile = ''
    checklist = ''
    try:
        opts, args = getopt.getopt(argv, "hi:f:", ["ipath=fpath="])
    except getopt.GetoptError:
        printUse()
        sys.exit(2)

    for (opt, arg) in opts:
        if opt == "-h":
            printUse()
            sys.exit()
        elif opt in ("-i", "--ipath"):
            inputfile = arg
        elif opt in ("-f", "--fpath"):
            checklist = arg
    
    if not inputfile.endswith('.ipa'):
        printUse()
        sys.exit()
    RunCMD("unzip -o "+inputfile+" -d ./").run_cmd()
    runner = RunCMD("cd Payload && ls")
    path = './Payload/'+str(runner.run_cmd()[0].decode('utf-8')).strip()
    arr = []
    machOArr = []
    for (dir_path, dir_names, file_names) in os.walk(path):
        for file_name in file_names:
            ppp = str(os.path.join(dir_path, file_name))
            if str(file_name).endswith('.zip'):
                cmd = "unzip -o " + ppp + " -d " + path + "/" + str(file_name)[:-4]
                arr.append(cmd)
            if len(os.path.splitext(file_name)[1]) == 0:
                machOArr.append(ppp)
    for cmd in arr:
        RunCMD(cmd).run_cmd()[1]
    with open(checklist, 'r') as f:
        for line in f:
            result = []
            line = line.strip()
            if re.compile(u'[\u4e00-\u9fa5]').search(line):
                # 转小端
                s = str(line.encode('unicode_escape').decode('utf-8')).replace('\\u', '')
                bitArr = re.findall(r'.{2}', s)
                jiArr = []
                ouArr = []
                for i in range(len(bitArr)):
                    if i % 2 == 1:
                        jiArr.append(bitArr[i])
                    if i % 2 == 0:
                        ouArr.append(bitArr[i])
                strrr = ''
                for i in range(len(jiArr)):
                    strrr += jiArr[i] + ouArr[i]
                for p in machOArr:
                    with open(p, 'rb') as f:
                        sf = f.read()
                        if sf.find(bytes().fromhex(strrr)) != -1:
                            result.append(p)
            if len(result) > 0:
                print("以下文件包含" + line)
                for item in result:
                    print(item)
                print("==========================================")
    with open(checklist, 'r') as f:
        for line in f:
            resultArr = []
            chinaArr = []
            source = line.strip()
            line = add_escape(source)
            chinaArr.append("grep -i -r '" + line + "' " + path)
            if re.compile(u'[\u4e00-\u9fa5]').search(line):
                chinaArr.append("grep -i -r '" + add_escape(str(line.encode('unicode_escape').decode('utf-8'))) + "' " + path)
            for cmd in chinaArr:
                result = RunCMD(cmd).run_cmd()[0].decode('utf-8')
                if len(result) > 0:
                    arrs = result.split('\n')
                    for item in arrs:
                        if ' matches' in item and 'Binary file ' in item:
                            if item not in resultArr:
                                resultArr.append(item)
                            continue
                        if path in item:
                            file = item.split(':')[0]
                            if file not in resultArr:
                                resultArr.append(file)
                            continue
            if len(resultArr) > 0:
                print("以下文件包含" + source)
                for item in resultArr:
                    print(item)
                print("==========================================")
    shutil.rmtree('./Payload')


if __name__ == '__main__':
    main(sys.argv[1:])
