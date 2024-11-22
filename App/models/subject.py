from .observer import Observer

class Subject:
    def register_observer(self, observer: 'Observer'):
        """Register an observer to receive notifications."""
        pass

    def remove_observer(self, observer: 'Observer'):
        """Remove an observer from notifications."""
        pass

    def notify_observers(self):
        """Notify all registered observers."""
        pass