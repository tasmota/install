#!/usr/bin/python3

from platform import release
import sys
from os import listdir
from os import mkdir
from os import remove
from os import path
import json
import requests
import gzip
import re



def handle_map_gz(data):
    decompressed = gzip.decompress(data).decode()

    features = {"Xdrv":[],"Xlgt":[],"Xnrg":[],"Xsns":[]}
    for line in decompressed.splitlines():
        m = re.search('Xdrv\d\d', line)
        if(m):
            number = int(m.group()[4:])
            if(number not in features["Xdrv"]):
                features["Xdrv"].append(number)
                features["Xdrv"].sort()
        m = re.search('Xlgt\d\d', line)
        if(m):
            number = int(m.group()[4:])
            if(number not in features["Xlgt"]):
                features["Xlgt"].append(number)
                features["Xlgt"].sort()
        m = re.search('Xnrg\d\d', line)
        if(m):
            number = int(m.group()[4:])
            if(number not in features["Xnrg"]):
                features["Xnrg"].append(number)
                features["Xnrg"].sort()
        m = re.search('Xsns\d\d', line)
        if(m):
            number = int(m.group()[4:])
            if(number not in features["Xsns"]):
                features["Xsns"].append(number)
                features["Xsns"].sort()

    # print("Features:",features)
    return features


def add_features_from_map(infile):
    print("Processing ",infile)
    file_name = infile.split('/')[1]
    file_name = file_name.split('.')[1]
    # We need a repo, which holds all the map.gz files too
    # This is perhaps not the final solution
    url = ' https://github.com/arendst/Tasmota-firmware/raw/main/firmware/map/'+file_name+'.map.gz'
    r = requests.get(url)
    if(r):
        # print("Found map for ",infile)
        features = handle_map_gz(r.content)
        return features
    else:
        # Fallback to Jasons special builds
        # print("No map for: ",url, " , will try:")
        url = ' https://github.com/Jason2866/Tasmota-specials/raw/firmware/firmware/map/'+file_name+'.map.gz'
        r = requests.get(url)
        # print(url)
        if(r):
            # print("On 2nd try found map for ",infile)
            features = handle_map_gz(r.content)
            return features
    print("Could not find map.gz for",infile)
    return {"Xdrv":[],"Xlgt":[],"Xnrg":[],"Xsns":[]}


def convertJSON(infile,outfile):
    with open(infile) as json_file:
        data = json.load(json_file)
        for build in data['builds']:
            for path in build['parts']:
                # print(path['path'])
                path['path'] = path['path'].replace("..", "https://tasmota.github.io/install")

            features = add_features_from_map(infile)
            # print(features)
            if 'features' not in data:
                data['features'] = features
        # print(data)
        j = json.dumps(data,indent=4)
        f = open(outfile,"w")
        f.write(j)
        f.close()

def getManifestEntry(manifest):
    entry = {}
    with open(manifest) as json_file:
        data = json.load(json_file)
        entry['path'] = "https://tasmota.github.io/install/" + manifest
        entry['name'] = data['name']
        entry['chipFamilies'] = []
        for build in data['builds']:
            entry['chipFamilies'].append(build['chipFamily'])
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


    output = {}

    for file in files:
        # create absolute path-version of each manifest file in /manifest_ext
        convertJSON(path.join(path_manifests,file),path.join(path_manifests_ext,file))
        line = file.split('.')
        if len(line) != 4:
            print("Incompatible path name, ignoring file:",file)
            continue
        # print(line[1])
        if line[0] not in output:
            output[line[0]] = [[],[],[],[],[],[]]
        if line[1] == "tasmota":
            output[line[0]][0].insert(0,getManifestEntry(path.join(path_manifests_ext,file))) # vanilla first
            continue
        elif line[1] == "tasmota32":
            output[line[0]][1].insert(0,getManifestEntry(path.join(path_manifests_ext,file)))
            continue
        elif len(line[1].split('-')) == 1: #solo1,4M,...
            output[line[0]][2].append(getManifestEntry(path.join(path_manifests_ext,file)))
            continue
        name_components = line[1].split('-')
        if name_components[0] == "tasmota":
            if len(name_components[1]) == 2 and name_components[1].isupper():
                output[line[0]][1].append(getManifestEntry(path.join(path_manifests_ext,file))) # language versions last
                continue
            output[line[0]][0].append(getManifestEntry(path.join(path_manifests_ext,file)))
            continue
        elif name_components[0] == "tasmota32":
            if len(name_components[1]) == 2 and name_components[1].isupper():
                output[line[0]][3].append(getManifestEntry(path.join(path_manifests_ext,file))) # language versions last
                continue
            output[line[0]][2].append(getManifestEntry(path.join(path_manifests_ext,file)))
            continue
        else: #solo1,4M,...
            if len(name_components[1]) == 2 and name_components[1].isupper():
                output[line[0]][5].append(getManifestEntry(path.join(path_manifests_ext,file))) # language versions last
                continue
            output[line[0]][4].append(getManifestEntry(path.join(path_manifests_ext,file)))
    # print(output)

    for section in output:
        merged = sorted(output[section][0],key=lambda d: d['name']) + sorted(output[section][1],key=lambda d: d['name']) + sorted(output[section][2],key=lambda d: d['name']) + sorted(output[section][3],key=lambda d: d['name']) + sorted(output[section][4],key=lambda d: d['name']) + sorted(output[section][5],key=lambda d: d['name'])
        output[section] = merged

    release = output.pop("release")
    development  = output.pop("development")
    unofficial = output.pop("unofficial")


    final_json = {}
    final_json["release"] = release
    final_json["development"] = development
    final_json["unofficial"] = unofficial
    for key in output:
        final_json[key] = output[key] # just in case we have another section in the future

    # print(final_json)

    j = json.dumps(final_json,indent=4)
    f = open("manifests.json", "w")
    f.write(j)
    f.close()

    # intermediate version with double output (DEPRECATED)
    f = open("manifests_new.json", "w")
    f.write(j)
    f.close()
    # end deprecated version

if __name__ == '__main__':
  sys.exit(main(sys.argv))
# end if
