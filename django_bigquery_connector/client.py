from django.db.backends.base.client import BaseDatabaseClient

class DatabaseClient(BaseDatabaseClient):
    executable_name = "bq"

    @classmethod
    def settings_to_cmd_args_env(cls, settings_dict, parameters):
        args = [cls.executable_name] + parameters
        return args, None