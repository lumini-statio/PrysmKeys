from dataclasses import dataclass
from models.password_value.password_value import PasswordValue
from models.password_value.value_dao import ValueDAO
from utils.logger import log
from cryptography.fernet import Fernet

@dataclass
class Password:
    """
    Password model
    """
    id: int
    service_name: str
    value: PasswordValue
    user_id: int

    def decrypt_value(value: bytes):
        values = ValueDAO.get_all()
        passwords = [val for val in values if val[1]==value]
        
        if passwords:
            crypted = Fernet(passwords[0][2])

            decrypted_value = crypted.decrypt(passwords[0][1]).decode()
            
            return decrypted_value
        else:
            log(f'{__file__} - password value didnt founded')
    
    def __str__(self):
        return f'value: {self.value.crypted_password}, user: {self.user_id}'