import paramiko
import os
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('-e', '--environ', type=str, required=True, help='Host name from ~/.ssh/config')
parser.add_argument('-d', '--directory', type=str, required=True, help='Directory of django app')


def main():
    args = parser.parse_args()

    ssh_config = paramiko.SSHConfig()
    with open(os.path.expanduser('/root/.ssh/config')) as f:
        ssh_config.parse(f)
    ssh_params = ssh_config.lookup(args.environ)

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    privatekey = ssh_params['identityfile']
    mkey = paramiko.RSAKey.from_private_key_file(privatekey)
    ssh.connect(ssh_params['hostname'], username=ssh_params['user'], pkey=mkey)

    stdin, stdout, stderr = ssh.exec_command(
        """
        #!/bin/bash
        cd {}
        . virtualenv/bin/activate
        python src/manage.py deployed refresh_celery
        """.format(args.directory)
    )
    ssh.close()
