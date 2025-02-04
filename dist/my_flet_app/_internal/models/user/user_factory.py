from models.user.user import User
from models.user.user_dao import UserDAO
from models.password.hasher import hash_password
from utils.logger import log


class UserFactory():
    """
    Users creation class
    """
    @classmethod
    def create(cls, username: str, value: str) -> bool:
        """
        Insert the user in database with hashed password. 
        If the user already exists, returns True, 
        if not, returns False
        """
        password = hash_password(value)

        user = User(
            username=username.strip(), 
            password=password
        )

        UserDAO.create_table()
        users = UserDAO.get_all()

        exists = False

        for element in users:
            if element[1] == user.username:
                exists = True
                break

        if exists == False:
            UserDAO.create(user.username, user.password)
            users = UserDAO.get_all()

            final_user = [user for user in users if user[1]==username and user[2]==password]

            if final_user != None:
                user.set_id(final_user[0][0])

                return {
                    'user_exists': exists,
                    'user': user
                }
            else:
                log(f'{__file__} - final_user its void')

        
        return {
            'user_exists': exists,
            'user': None
        }
        
            