#!/usr/bin/python3

from curses.ascii import isupper
from platform import release
import sys
import os
from os import listdir
from os import mkdir
from os import remove
from os import path
import json

def filter_builds(data):
    """
    Removes non-existing MCU firmware variant from manifest, indicated by 'size' entry is None.
    """
    filtered_builds = []
    for build in data['builds']:
        if all(part['size'] is not None for part in build['parts']):
            filtered_builds.append(build)
    data['builds'] = filtered_builds
    return data

def convertJSON(infile, outfile, tag):
    with open(infile) as json_file:
        data = json.load(json_file)
        for build in data['builds']:
            for part in build['parts']:
                components = part['path'].split("/")
                firmware_path = part['path']
                part['path'] = "https://github.com/tasmota/install/releases/download/" + tag + "/" + components[-1]
                # Add firmware size with ugly path fix for firmware path
                firmware_path = firmware_path.replace(".factory", "").replace("../", "./").replace("//", "/")
                if os.path.exists(firmware_path):
                    part['size'] = os.path.getsize(firmware_path)
                else:
                    part['size'] = None  # If the file doesn't exist, set size to None

        filter_builds(data)
        j = json.dumps(data, indent=4)
        # Write updated data to JSON
        with open(outfile, "w") as f:
            f.write(j)

def getManifestEntry(manifest, tag):
    entry = {}
    with open(manifest) as json_file:
        data = json.load(json_file)
        components = manifest.split("/")
        entry['path'] = "https://github.com/tasmota/install/releases/download/" + tag + "/" + components[-1]
        entry['name'] = data['name']
        entry['chipFamilies'] = []
        for build in data['builds']:
            entry['chipFamilies'].append(build['chipFamily'])
        return entry

def getTag():
        with open("tag_latest.txt") as tag:
            tag_latest = tag.readline().strip()
            return tag_latest


def main(args):
    path_manifests          = path.join('manifest')
    path_manifests_release  = path.join('manifest_release')
    if not path.exists(path_manifests):
        print("No manifest folder, exiting ...")
        return -1
    files = listdir(path_manifests)
    if len(files) == 0:
        print("Empty manifest folder, exiting ...")
        return -1
    if path.exists(path_manifests_release):
        m_e_files = listdir(path_manifests_release)
        # for file in m_e_files:
        #     remove(file)
    else:
        mkdir(path_manifests_release)

    tag_latest = getTag()

    output = {}

    for file in files:
        # create absolute path-version of each manifest file in /manifest_ext
        convertJSON(path.join(path_manifests,file),path.join(path_manifests_release,file),tag_latest)
        line = file.split('.')
        if len(line) != 4:
            print("Incompatible path name, ignoring file:",file)
            continue
        # print(line[1])
        if line[0] not in output:
            output[line[0]] = [[],[],[],[],[],[]]
        if line[1] == "tasmota":
            print(path.join(path_manifests_release,file),tag_latest)
            output[line[0]][0].insert(0,getManifestEntry(path.join(path_manifests_release,file),tag_latest)) # vanilla first
            continue
        elif line[1] == "tasmota32":
            output[line[0]][1].insert(0,getManifestEntry(path.join(path_manifests_release,file),tag_latest))
            continue
        else: #solo1,4M,...
            output[line[0]][2].append(getManifestEntry(path.join(path_manifests_release,file),tag_latest))
            continue
        name_components = line[1].split('-')
        if name_components[0] == "tasmota":
            if len(name_components[1]) and name_components[1].isupper():
                output[line[0]][1].append(getManifestEntry(path.join(path_manifests_release,file),tag_latest)) # language versions last
                continue
            output[line[0]][0].append(getManifestEntry(path.join(path_manifests_release,file),tag_latest))
            continue
        elif name_components[0] == "tasmota32":
            if len(name_components[1]) and name_components[1].isupper():
                output[line[0]][3].append(getManifestEntry(path.join(path_manifests_release,file),tag_latest)) # language versions last
                continue
            output[line[0]][2].append(getManifestEntry(path.join(path_manifests_release,file),tag_latest))
            continue
        else: #solo1,4M,...
            if len(name_components[1]) and name_components[1].isupper():
                output[line[0]][5].append(getManifestEntry(path.join(path_manifests_release,file),tag_latest)) # language versions last
                continue
            output[line[0]][4].append(getManifestEntry(path.join(path_manifests_release,file),tag_latest))
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

    #print(final_json)
    j = json.dumps(final_json,indent=4)
    f = open("manifests_release.json", "w")
    f.write(j)
    f.close()
    # end deprecated version

if __name__ == '__main__':
  sys.exit(main(sys.argv))
# end if
