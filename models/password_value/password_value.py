from dataclasses import dataclass


@dataclass
class PasswordValue:
    """
    class that stores passwords value, with the crypted value and a key
    """
    crypted_password: bytes
    key: bytes
    password_id: int=None
    
    def get_key_str(self) -> str:
        """
        returns the key as a text
        """
        return str(self.key.decode())
    
    def set_password_id(self, password_id):
        self.password_id = password_id

    def __str__(self):
        return f'crypted password: {self.crypted_password}'