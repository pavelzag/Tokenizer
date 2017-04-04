import paramiko

port = 22
username = 'root'
password = '<ADD HERE THE PASSWORD>'
command1 = 'oc get -n management-infra sa/management-admin ' \
           '--template=\'{{range .secrets}}{{printf "%s\\n" .name}}{{end}}\''


def get_parameters(command, hostname):
    s = paramiko.SSHClient()
    s.load_system_host_keys()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    s.connect(hostname, port, username, password)
    (stdin, stdout, stderr) = s.exec_command(command)
    return stdout.readlines()
    s.close()


def get_token_id(values_from_command):
    for value in values_from_command:
        if 'token' in value:
            return str(value.split("token-", 1)[1]).rstrip()


def get_token(command, hostname):
    value = get_parameters(command, hostname=hostname)
    for reply in value:
        return str(reply)


if __name__ == "__main__":
    server_address = raw_input('Enter your OSE address: ')
    values_from_command = get_parameters(command1, hostname=server_address)
    token_id = get_token_id(values_from_command)
    command2 = 'oc get -n management-infra secrets management-admin-token-' \
               + token_id + ' --template=\'{{.data.token}}\' | base64 -d'
    token = get_token(command2, hostname=server_address)
    print('Your token is: ' + token)
