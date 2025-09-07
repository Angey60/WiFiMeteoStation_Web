from django.db.backends.base.client import BaseDatabaseClient
from django.db.backends.base.base import logger

import os
import subprocess
import signal

class DatabaseClient(BaseDatabaseClient):
    """Encapsulate backends-specific methods for opening a client shell."""

    # This should be a string representing the name of the executable
    # (e.g., "psql"). Subclasses must override this.
    executable_name = "ydb-client"

    @classmethod
    def settings_to_cmd_args_env(cls, settings_dict, parameters):
        args = [cls.executable_name]
        
        if "NAME" in settings_dict:
            args.extend(["dbname", settings_dict["NAME"]])
            
        if "PROTOCOL" in settings_dict:
            args.extend(["protocol", settings_dict["PROTOCOL"]])

        if "HOST" in settings_dict:
            args.extend(["host", settings_dict["HOST"]])

        if "PORT" in settings_dict:
            args.extend(["port", settings_dict["PORT"]])

        if "DATABASE" in settings_dict:
            args.extend(["database", settings_dict["DATABASE"]])
            
        if "CREDENTIALS" in settings_dict:
            args.extend(["credentials", settings_dict["CREDENTIALS"]])

        if parameters:
            args.extend(parameters)

        env = {}

        return args, env
    
    def runshell(self, parameters):
        sigint_handler = signal.getsignal(signal.SIGINT)
        try:
            # Allow SIGINT to pass to psql to abort queries.
            signal.signal(signal.SIGINT, signal.SIG_IGN)
            super().runshell(parameters)
        finally:
            # Restore the original SIGINT handler.
            signal.signal(signal.SIGINT, sigint_handler)
    