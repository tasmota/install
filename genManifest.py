#!/usr/bin/python3

from platform import release
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

def getPathAndName(manifest):
    entry = {}
    with open(manifest) as json_file:
        data = json.load(json_file)
        entry['path'] = "https://tasmota.github.io/install/" + manifest
        entry['name'] = data['name']
        return entry



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
        # for file in m_e_files:
        #     remove(file)
    else:
        mkdir(path_manifests_ext)
    
    
    output = {} #deprecated
    output_new = {}

    for file in files:
        # create absolute path-version of each manifest file in /manifest_ext
        convertJSON(path.join(path_manifests,file),path.join(path_manifests_ext,file))
        line = file.split('.')
        if len(line) != 4:
            print("Incompatible path name, ignoring file:",file)
            continue
        print(line[1])
        if line[0] not in output:
            output[line[0]] = [[],[]] #deprecated
            output_new[line[0]] = [[],[]]
        if line[1] == "tasmota":
            output[line[0]][0].insert(0,line[1]) #deprecated
            output_new[line[0]][0].insert(0,getPathAndName(path.join(path_manifests_ext,file)))
            continue
        if line[1] == "tasmota32":
            output[line[0]][1].insert(0,line[1]) #deprecated
            output_new[line[0]][1].insert(0,getPathAndName(path.join(path_manifests_ext,file)))
            continue
        if line[1].split('-')[0] == "tasmota":
            output[line[0]][0].append(line[1]) #deprecated
            output_new[line[0]][0].append(getPathAndName(path.join(path_manifests_ext,file)))
            continue
        if line[1].split('-')[0] == "tasmota32":
            output[line[0]][1].append(line[1]) #deprecated
            output_new[line[0]][1].append(getPathAndName(path.join(path_manifests_ext,file)))
    print(output)

    for section in output:
        merged = sorted(output[section][0]) + sorted(output[section][1])
        # print(sorted(merged))
        # del output[section][0]
        # del output[section][0]
        output[section] = merged


    for section in output_new:
        merged_new = sorted(output_new[section][0],key=lambda d: d['name']) + sorted(output_new[section][1],key=lambda d: d['name'])
        output_new[section] = merged_new

    # deprecated version
    release = output.pop("release")
    development  = output.pop("development")
    unofficial = output.pop("unofficial")


    final_json = {}
    final_json["release"] = release
    final_json["development"] = development
    final_json["unofficial"] = unofficial
    for key in output:
        final_json[key] = output[key] # just in case we have another section in the future

    print(final_json)

    j = json.dumps(final_json,indent=4)
    f = open("manifests.json", "w")
    f.write(j)
    f.close()
    # end deprecated version

    #future version
    release_new = output_new.pop("release")
    development_new  = output_new.pop("development")
    unofficial_new = output_new.pop("unofficial")

    final_json = {}
    final_json["release"] = release_new
    final_json["development"] = development_new
    final_json["unofficial"] = unofficial_new
    for key in output_new:
        final_json[key] = output_new[key] # just in case we have another section in the future

    print(final_json)

    j = json.dumps(final_json,indent=4)
    f = open("manifests_new.json", "w")
    f.write(j)
    f.close()

if __name__ == '__main__':
  sys.exit(main(sys.argv))
# end if
