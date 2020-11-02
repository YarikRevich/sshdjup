import paramiko


class SSHConnector:
    """SSHConnector sets connection to ssh and can return SSH instance."""

    def __init__(self):

        self.SSH = paramiko.SSHClient()

    def set_connection(self, host: str, username: str, port: int, password: str):
        """Sets connection to ssh using passed host, username, password."""

        self.SSH.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.SSH.load_system_host_keys()
        self.SSH.connect(
            host,
            port,
            username,
            password,
            look_for_keys=False,
            allow_agent=False)
    
    def get_connector(self):
        """Returns ssh connector."""
    
        return self.SSH


def start_ssh_connection(host: str, username: str, port: int, password: str):
    ssh_client = SSHConnector()
    ssh_client.set_connection(
        host,
        username,
        port,
        password
    )
    return ssh_client.get_connector()