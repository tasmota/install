#!/usr/bin/python3

import sys
from os import listdir
from os import mkdir
from os import remove
from os import path
import json

def convertJSON(infile,outfile):
    with open(infile) as json_file:
        data = json.load(json_file)
        for build in data['builds']:
            for path in build['parts']:
                print(path['path'])
                path['path'] = path['path'].replace("..", "https://tasmota.github.io/install")
                # maybe add "?raw=true
                print(path['path'])
        print(data)
        j = json.dumps(data,indent=4)
        f = open(outfile,"w")
        f.write(j)
        f.close()

    



def main(args):
    path_manifests          = path.join('manifest')
    path_manifests_ext      = path.join('manifest_ext')
    if not path.exists(path_manifests):
        print("No manifest folder, exiting ...")
        return -1
    files = listdir(path_manifests)
    if len(files) == 0:
        print("Empty manifest folder, exiting ...")
        return -1
    if path.exists(path_manifests_ext):
        m_e_files = listdir(path_manifests_ext)
        #for file in m_e_files:
        #    remove(file)
    else:
        mkdir(path_manifests_ext)
    
    
    output = {}

    for file in files:
        convertJSON(path.join(path_manifests,file),path.join(path_manifests_ext,file))
        line = file.split('.')
        if len(line) != 4:
            print("Incompatible path name, ignoring file:",file)
            continue
        print(line[1])
        if line[0] not in output:
            output[line[0]] = [[],[]]
        if line[1] == "tasmota":
            output[line[0]][0].insert(0,line[1])
            continue
        if line[1] == "tasmota32":
            output[line[0]][1].insert(0,line[1])
            continue
        if line[1].split('-')[0] == "tasmota":
            output[line[0]][0].append(line[1])
            continue
        if line[1].split('-')[0] == "tasmota32":
            output[line[0]][1].append(line[1])
    print(output)

    for section in output:
        merged = sorted(output[section][0]) + sorted(output[section][1])
        # print(sorted(merged))
        del output[section][0]
        del output[section][0]
        output[section] = merged

    j = json.dumps(output,indent=4)
    f = open("manifests.json", "w")
    f.write(j)
    f.close()

if __name__ == '__main__':
  sys.exit(main(sys.argv))
# end if
