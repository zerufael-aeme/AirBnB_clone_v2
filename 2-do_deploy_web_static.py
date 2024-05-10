#!/usr/bin/python3
#  Fabric script that generates a .tgz archive from the
# contents of the web_static folder of your AirBnB Clone repo
# using the function do_pack
import os
from fabric.api import run, put, env

env.hosts = ['52.91.182.253', '52.201.229.108']
env.user = "ubuntu"


def do_deploy(archive_path):

    # Checks if the archive path exists
    if not os.path.exists(archive_path):
        print("Archive path not found")
        return False
    
    archive_name = os.path.basename(archive_path)
    folder_name = archive_name.split('.')[0]
    
    try:
        with prefix(put(archive_path, "/tmp/")):
            run("mkdir -p /data/web_static/releases/{}/".format(folder_name))
            run("bsdtar -xf /tmp/{} -C /data/web_static/releases/{}/".format(archive_name, folder_name))
            run("rm /tmp/{}".format(archive_name))
            run("mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/".format(folder_name))
            run("rm -rf /data/web_static/releases/{}/web_static/".format(folder_name))
            run("rm -rf /data/web_static/current")
            run("ln -sf /data/web_static/releases/{}/ /data/web_static/current".format(folder_name))
    except Exception as e:
        print("Operation Failed: {}".format(e))
        return False
    return True
