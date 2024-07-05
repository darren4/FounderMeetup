class User:
    """Class Definition to handle Flask login for user"""

    def __init__(self, username: str):
        self.username: str = username

    @staticmethod
    def is_authenticated() -> bool:
        return True

    @staticmethod
    def is_active() -> bool:
        return True

    @staticmethod
    def is_anonymous() -> bool:
        return False
    
    def get_id(self) -> str:
        return self.username