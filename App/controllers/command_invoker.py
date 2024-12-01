from App.models import Command
class CommandInvoker():
    _instances = {}
    _on_start = None
    _on_finish = None

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

    def set_on_start(self, command: Command):
        self._on_start = command

    def set_on_finish(self, command: Command):
        self._on_finish = command

    def execute_command(self) -> None:
        if isinstance(self._on_start, Command):
            self._on_start.execute()
        if isinstance(self._on_finish, Command):
            self._on_finish.execute()


