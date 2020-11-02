import sys
from .core import Updater
from .analizer import Analizer
import paramiko
import typing


class Utils:

    def chose_param_value(self, value: str) -> list:
        """Gets values after chosen param."""

        index_to_start_from = self.commands.index(value)+1
        commands_to_start_next_params_research = [
            self.commands[index] for index in range(index_to_start_from, len(self.commands))
        ]
        dirs_to_delete_put = []
        for dir_ in commands_to_start_next_params_research:
            if "--" in dir_:
                break 
            dirs_to_delete_put.append(dir_)
        return dirs_to_delete_put

    def _check_whether_has_params(self, params) -> bool:
        if params:
            return True
        return False

    def _check_path_availability(self, methods: typing.Iterable[str]) -> None:
        for method in methods:
            self.analizer._check_path_availability(method)
        
    def write_debug_message(self, message: str):
        return sys.stdout.write(message)

    def write_error_message(self, message: str):
        return sys.exit(message)
    
    def write_help_message(self):
        return sys.stdout.write("it works!\n")


class Commands(Utils):

    def __init__(self, ssh_client: paramiko.SSHClient):
        
        self.commands = sys.argv
        self.updater = Updater(ssh_client)
        self.analizer = Analizer()
    
    def update_settings(self):
        param = "settings.py"
        self._check_path_availability(["get_settings_dir", "get_settings_dir_to"])
        self.updater.update_files(
            self.analizer.get_settings_dir(),
            self.analizer.get_settings_dir_to(),
            param,
        )
        return self.write_debug_message("Settings upgrade is done!\n")

    def update_static_files(self):
        params = self.chose_param_value("--static")
        self._check_path_availability(["get_static_dir", "get_static_dir_to"])
        if self._check_whether_has_params(params):
            self.updater.update_files(
                self.analizer.get_static_dir(),
                self.analizer.get_static_dir_to(),
                params
            )
            return self.write_debug_message("Static files upgrade is done!\n")
        return self.write_error_message("You haven't passed any params about static files")

    def update_templates(self):
        params = self.chose_param_value("--temp")
        self._check_path_availability(["get_template_dir", "get_template_dir_to"])
        if self._check_whether_has_params(params):
            self.updater.update_files(
                self.analizer.get_template_dir(),
                self.analizer.get_template_dir_to(),
                params
            )
            return self.write_debug_message("Temp files upgrade is done!\n")
        return self.write_error_message("You haven't passed any params about template files")

    def update_app(self):
        param = self.chose_param_value("--app")
        self._check_path_availability(["get_project_dir", "get_project_dir_to"])
        if self._check_whether_has_params(param):
            self.updater.update_files(
                self.analizer.get_project_dir(),
                self.analizer.get_project_dir_to(),
                param
            )
            return self.write_debug_message("App files upgrade is done!\n")
        return self.write_error_message("You haven't passed any params about application files")

    def update_mysql_files(self):
        param = None
        self._check_path_availability(["get_db_dir", "get_db_dir_to"])
        self.updater.update_files(
            self.analizer.get_db_dir(),
            self.analizer.get_db_dir_to(),
            param
        )
        return self.write_debug_message("Mysql files upgrade is done!\n")

    def main_command_loop(self) -> None:
        """Main loop which chose available commands to execute."""

        self.commands.pop(0)
        for command in self.commands:
            if "--static" == command:
                self.update_static_files()
            elif "--temp" == command:
                self.update_templates()
            elif "--app" == command:
                self.update_app()
            elif "--settings" == command:
                self.update_settings()
            elif "--mysql-files" == command:
                self.update_mysql_files()
            elif "--help" == command or "-h" == command:
                self.write_help_message()
