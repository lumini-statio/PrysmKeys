from models.password.password_dao import PasswordDAO
from models.password_value.value_dao import ValueDAO
from models.password_value.password_value import PasswordValue
from cryptography.fernet import Fernet
from utils.logger import log


class PasswordFactory:
    """
    passwords factory class to manage the object creation
    """

    @staticmethod
    def processing_password(value: str) -> PasswordValue:
        key = Fernet.generate_key()
        crypted = Fernet(key)

        if value:
            crypted_value = crypted.encrypt(value.encode())
            password_value = PasswordValue(
                crypted_password=crypted_value, 
                key=key
            )
            
            return password_value

    @classmethod
    def create(cls, value: str, user_id: int) -> None:
        processed_value = cls.processing_password(value)

        PasswordDAO.create_table()
        PasswordDAO.create(
                        password=processed_value,
                        user_id=user_id
                    )
        
        passwords = PasswordDAO.get_all(user_id=user_id)
        pw_object = [pw for pw in passwords if pw[1]==processed_value.crypted_password]
        if pw_object:
            processed_value.set_password_id(pw_object[0][0])
        else:
            log(f'{__file__} - pw_object is void')

        ValueDAO.create(processed_value)

        return pw_object[0]