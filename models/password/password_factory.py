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
                key=key,
                password_id=None
            )

            log(f'tipo de contraseña encriptada {type(crypted_value)}')
            
            return password_value

    @classmethod
    def create(cls, service: str, value: str, user_id: int) -> None:
        processed_value = cls.processing_password(value)

        password_id = PasswordDAO.create(
            service_name=service,
            password=processed_value,
            user_id=user_id
        )

        if password_id == None:
            log(f'{__file__} - pw_object is void')
            return None

        processed_value.set_password_id(password_id)
        ValueDAO.create(processed_value)

        return password_id