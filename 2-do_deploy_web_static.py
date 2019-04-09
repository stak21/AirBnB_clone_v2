#!/usr/bin/python3
""" Transfers file from local to remote """
from fabric.api import *
import datetime


env.use_ssh_config = True
env.hosts = ['35.237.82.133', '35.196.231.32']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/holberton'
date = datetime.datetime.now().strftime("%Y%m%d%I%M%S")


def transfer():
    """ transfers a specific file """
    put('./0-setup_web_static.sh', '/tmp/')


def do_pack():
    """
        Generates a .tgz archive from the contents of web_static folder
        Return: the archive path if the archive has been correctly generated
        Otherwise Return: None
    """
    local("mkdir -p ./versions")
    local("tar czvf ./versions/web_static_{}.tgz ./web_static/*".format(date))


def do_deploy(archive_path):
    """ Distributes an archive to multiple webservers """
    try:
        if not archive_path:
            return False
        try:
            name = archive_path.split('/')[-1]
        except:
            name = archive_path

        put(archive_path, '/tmp/')
        run("mkdir -p /data/web_static/releases/{}/".format(name[:-4]))
        with cd('/tmp/'):
            run('tar xzf {} -C /data/web_static/releases/{}/'.format(name,
                name[:-4]))
            sudo('rm ./{}'.format(name))
        with cd('/data/web_static/'):
            run('mv releases/{}/web_static/*\
                    /data/web_static/releases/{}/'
                .format(name[:-4], name[:-4]))
            run('rm -rf ./current')
            run('ln -s /data/web_static/releases/{}/\
                    /data/web_static/current'.format(name[:-4]))
        return True
    except:
        return False
