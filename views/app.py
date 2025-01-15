import flet as ft
from models.user.user import User
from models.password.password import Password
from models.user.user_factory import UserFactory
from models.password.password_factory import PasswordFactory
from models.user.user_dao import UserDAO
from models.password.password_dao import PasswordDAO
from models.password_value.value_dao import ValueDAO
from utils.pw_generator import generator
from utils.logger import log
from .config import Styles
import re
import traceback


def init():
    '''
    The `init` function creates tables for PasswordDAO, ValueDAO, and UserDAO.
    '''
    PasswordDAO.create_table()
    ValueDAO.create_table()
    UserDAO.create_table()


def main(page: ft.Page):
    init()
    """
    ------------------------------------------------------------------------------------------
    Page Config
    ------------------------------------------------------------------------------------------
    """
    page.title = 'Random password generator'
    page.window.width = 1000
    page.window.height = 700
    page.padding = 0
    page.bgcolor = ft.colors.BACKGROUND
    page.theme_mode = ft.ThemeMode.DARK

    page.theme = Styles.PAGE_THEME.value

    """
    ------------------------------------------------------------------------------------------
    App functions
    ------------------------------------------------------------------------------------------
    """
    def login(e):
        """
        Tries to login with the values on inputs, if the user
        exists then redirect to the main view, if not,
        says to user that the credentials are incorrect.
        """
        try:
            founded = user.login(
                username=username_field.value, 
                password=login_password_field.value
            )
            if isinstance(founded, tuple):
                user.state.change_user_state(user=user)
                user.set_id(founded[0])
                user.set_username(founded[1])
                user.set_password(founded[2])
                btn_logout.visible = True
                update_view()
                update_listview()
            else:
                login_error_text.value = 'Invalid username or password'
                login_error_text.update()
        except Exception as e:
            log(f'{__file__} - {traceback.format_exc()}')
    
    def register(e):
        """
        tries to create a User with create function 
        that returns a boolean.
          Then, shows the user an alert if the user
        was created or not.
        """
        try:
            new_user = UserFactory.create(
                        username=username_register_field.value, 
                        value=password_register_field.value
                    )
            exists = new_user['user_exists']
            if exists:
                dialog = ft.AlertDialog(
                    title=ft.Text('User created successfully!')
                )
                page.overlay.append(dialog)
                dialog.open = True
                page.update()
            else:
                dialog = ft.AlertDialog(title=ft.Text('Cannot use these credentials'))
                page.overlay.append(dialog)
                dialog.open = True
                page.update()
        except Exception as e:
            log(f'{__file__} - {traceback.format_exc()}')
    

    def update_view():
        """
        If the user is authenticated change the view
        to the password generator, if not, returns
        to the login view
        """
        try:
            if user.is_authenticated():
                content_area.content = generator_view
            else:
                content_area.content = login_view
            page.update()
        except Exception as e:
            log(f'{__file__} - {traceback.format_exc()}')

    def open_register(e):
        """
        In charge to open the register form
        """
        page.overlay.append(register_view)
        register_view.open = True
        page.update()

    def close_register(e):
        """
        It's called when the register form are correct
        or if the user want to close the register form
        """
        register_view.open = False
        page.update()

    def on_change_length(e):
        """
        function that register changes in the length input
        """
        try:
            if not re.match(r'^(\d+)$', password_length.value):
                btn_create.disabled = True

                btn_create.color = ft.Colors.GREY
                btn_create.bgcolor = ft.Colors.BLUE_900

                validation_text.value = 'Only numbers'

            elif password_length.value == '':
                btn_create.disabled = True

                btn_create.color = ft.Colors.GREY
                btn_create.bgcolor = ft.Colors.BLUE_900
                
            else:
                validation_text.value = ''

                btn_create.color=ft.Colors.WHITE
                btn_create.bgcolor=ft.Colors.BLUE_700

                btn_create.disabled = False
            
            btn_create.update()
            validation_text.update()
        except Exception as e:
            log(f'{__file__} - {traceback.format_exc()}')

    def option_onchange(e):
        """
        function tath register the changes in dropdowns
        """
        try:
            if not uppercase_dropdown.value:
                uppercase_dropdown.value == 'YES'
            if not special_digits_dropdown.value:
                special_digits_dropdown.value == 'YES'
            page.update()
        except:
            log(f'{__file__} - {traceback.format_exc()}')
    
    def generate():
        """
        function that calls the password 'generator' function 
        and put it in the password field
        """
        try:
            if password_length.value != '':
                pw = generator(
                    length=password_length.value, 
                    mayusc=uppercase_dropdown.value, 
                    especiales=special_digits_dropdown.value, 
                    nums=nums_dropdown.value
                    )
                password_field.value = pw
                password_field.update()
            else:
                validation_text.value = 'Needs to specify the password length...'
        except Exception as e:
            log(f'{__file__} - {traceback.format_exc()}')

    def copy_to_clipboard():
        """
        function to copy the password to clipboard
        """
        try:
            page.set_clipboard(password_field.value)
        except Exception as e:
            log(f'{__file__} - {traceback.format_exc()}')
    
    def delete_password(password_id):
        try:
            # Delete the password from the database
            PasswordDAO.delete(password_id, user.get_id())
            ValueDAO.delete(password_id)
            
            # Update the list view
            update_listview()
        except Exception as e:
            log(f'{__file__} - {traceback.format_exc()}')

    def save_password():
        try:
            # Check if the password already exists
            passwords = PasswordDAO.get_all(user_id=user.get_id())
            for _, pw in enumerate(passwords):
                decrypted_password = Password.decrypt_value(pw[1])
                if decrypted_password == password_field.value:
                    # Show error message if password already exists
                    password_validation_text.value = 'This passwords its already saved'
                    password_validation_text.update()
                    return

            # Process and save the new password
            processed_value = PasswordFactory.processing_password(password_field.value)
            PasswordDAO.create(password=processed_value, user_id=user.get_id())
            ValueDAO.create(processed_value)

            # Update the list view
            update_listview()
        except Exception as e:
            log(f'{__file__} - {traceback.format_exc()}')
    
    def handle_logout(e):
        try:
            username_field.value = ''
            login_password_field.value = ''
            user.state.change_user_state(user=user)
            update_view()
        except Exception as e:
            log(f'{__file__} - {traceback.format_exc()}')
    
    def update_listview():
        # Clear all controls from the list
        list_passwords.controls.clear()
        list_passwords.update()

        # Fetch all passwords from the database
        passwords = PasswordDAO.get_all(user_id=user.get_id())
        log(passwords)

        # Add each password to the list view
        for _, pw in enumerate(passwords):
            decrypted_password = Password.decrypt_value(pw[1])
            password_component = ft.Row([
                ft.Text(
                    f'{pw[0]}',
                    size=Styles.MIN_TEXT_SIZE,
                    color=ft.Colors.WHITE,
                    width=300
                ),
                ft.Text(
                    f'{decrypted_password}',
                    size=Styles.MIN_TEXT_SIZE,
                    expand=True,
                    color=ft.Colors.WHITE
                ),
                ft.ElevatedButton(
                    'Delete',
                    color=ft.Colors.WHITE,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=Styles.BTN_RADIUS.value)
                    ),
                    bgcolor=ft.Colors.RED_900,
                    on_click=lambda e, pw_id=pw[0]: delete_password(pw_id)
                )
            ])
            list_passwords.controls.append(password_component)
        list_passwords.update()

        log(list_passwords.controls)

            

    """
    Instance that manage the user state to know if it's secure
    shows the generator view with the passwords list or needs to login
    """
    user = User()

    """
    ------------------------------------------------------------------------------------------
    Page Components
    ------------------------------------------------------------------------------------------
    """

    username_field = ft.TextField(
        label="Username",
        bgcolor=Styles.BG_COLOR.value,
        border_color=Styles.BORDER_COLOR.value
        )
    
    login_password_field = ft.TextField(
        label="Password",
        bgcolor=Styles.BG_COLOR.value,
        border_color=Styles.BORDER_COLOR.value,
        password=True,
        can_reveal_password=True
    )

    login_error_text = ft.Text(color=Styles.ERROR_COLOR.value)

    login_view = ft.Container(
        content=ft.Column([
            username_field,
            login_password_field,
            login_error_text,
            ft.Row([
                ft.Container(
                    content=ft.ElevatedButton(
                        'Log in',
                        on_click=login,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=Styles.BTN_RADIUS),
                            text_style=ft.TextStyle(size=Styles.MIN_TEXT_SIZE),
                            elevation=10,
                            padding=ft.padding.all(10),
                        ),
                        expand=True
                    ),
                    width=200
                ),
                ft.Container(
                    content=ft.ElevatedButton(
                        'Register',
                        on_click=open_register,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=Styles.BTN_RADIUS),
                            text_style=ft.TextStyle(size=Styles.MIN_TEXT_SIZE),
                            elevation=10,
                            padding=ft.padding.all(10)
                        ),
                        expand=True
                    ),
                    width=200
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            ),
        ],
        expand=True,
        alignment=ft.alignment.center,
        spacing=20,
        ),
        expand=True,
        margin=ft.margin.all(20),
        alignment=ft.alignment.center
    )

    username_register_field = ft.TextField(
        label="Username",
        bgcolor=Styles.BG_COLOR.value,
        border_color=Styles.BORDER_COLOR.value
    )

    password_register_field = ft.TextField(
        label="Password",
        bgcolor=Styles.BG_COLOR.value,
        border_color=Styles.BORDER_COLOR.value
    )

    register_view = ft.AlertDialog(
        content=ft.Column([
            username_register_field,
            password_register_field
        ],
        tight=True
        ),
        actions=[
            ft.TextButton('Close', on_click=close_register),
            ft.ElevatedButton(
                'Submit', 
                on_click=register,
                style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=Styles.BTN_RADIUS.value)
                        )
                )
        ]
    )

    # containter that shows the tool to duplicated files view
    content_area = ft.Container(
        content=login_view,
        expand=True
    )
    
    btn_logout = ft.FloatingActionButton(
                    icon=ft.Icons.LOGOUT,
                    on_click=handle_logout,
                    shape=ft.RoundedRectangleBorder(radius=Styles.BTN_RADIUS)
                )

    # text that shows an alert if the length input content it's not numbers
    validation_text = ft.Text('', color=Styles.ERROR_COLOR.value, size=Styles.MIN_TEXT_SIZE)

    password_validation_text = ft.Text('', color=Styles.ERROR_COLOR.value, size=Styles.MIN_TEXT_SIZE)

    # button to create the password
    btn_create = ft.ElevatedButton(
                        'Create',
                        color=ft.Colors.GREY,
                        bgcolor=Styles.BTN_NOT_ACTIATED_BG.value,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=Styles.BTN_RADIUS.value),
                            text_style=ft.TextStyle(size=Styles.MID_TEXT_SIZE),
                            padding=14
                        ),
                        on_click=lambda e:generate(),
                        disabled=True
                    )

    password_length = ft.TextField(
        hint_text='Length',
        keyboard_type=ft.KeyboardType.NUMBER,
        on_change=on_change_length,
        bgcolor=Styles.BG_COLOR.value,
        border_color=Styles.BORDER_COLOR.value
    )

    uppercase_dropdown = ft.Dropdown(
        on_change=option_onchange,
        options=[
            ft.dropdown.Option('YES'),
            ft.dropdown.Option('NO')
            ],
        value='YES',
        width=100,
        bgcolor=Styles.DROP_COLOR.value,
        border=None,
        border_color=Styles.BORDER_COLOR.value
    )

    special_digits_dropdown = ft.Dropdown(
        on_change=option_onchange,
        options=[
            ft.dropdown.Option('YES'),
            ft.dropdown.Option('NO')
            ],
        value='YES',
        width=100,
        bgcolor=Styles.DROP_COLOR.value,
        border=None,
        border_color=Styles.BORDER_COLOR.value
    )

    nums_dropdown = ft.Dropdown(
        on_change=option_onchange,
        options=[
            ft.dropdown.Option('YES'),
            ft.dropdown.Option('NO')
            ],
        value='YES',
        width=100,
        bgcolor=Styles.DROP_COLOR.value,
        border=None,
        border_color=Styles.BORDER_COLOR.value
    )

    # input tath shows the last created password
    password_field = ft.TextField(
        bgcolor=Styles.BG_COLOR.value,
        border_color=Styles.BORDER_COLOR.value,
        expand=True,
        color=ft.Colors.WHITE,
        text_size=Styles.MID_TEXT_SIZE
    )

    # list that shows all saved passwords
    list_passwords = ft.ListView(
        expand=True,
        spacing=10,
        height=200,
    )


    # password generator view
    generator_view = ft.Container(
        content=ft.Column([
            ft.Row([
                btn_logout
            ]),
            ft.Row([
                ft.Column([
                    password_length,
                    validation_text
                ]),
                ft.Column([
                    uppercase_dropdown,
                    ft.Text('Uppercase', color=ft.Colors.BLUE_200, size=Styles.MIN_TEXT_SIZE)
                ]),
                ft.Column([
                    special_digits_dropdown,
                    ft.Text('Signs', color=ft.Colors.BLUE_200, size=Styles.MIN_TEXT_SIZE)
                ]),
                ft.Column([
                    nums_dropdown,
                    ft.Text('Numbers', color=ft.Colors.BLUE_200, size=Styles.MIN_TEXT_SIZE)
                ]),
                ft.Column([
                    btn_create,
                    ft.Text('', size=Styles.MIN_TEXT_SIZE)
                ]),
            ]),
            ft.Row([
                ft.Row([
                    ft.Column([
                        password_field,
                        password_validation_text
                    ],
                    expand=True
                    ),
                    ft.Column([
                        ft.Row([
                            ft.Row([
                                ft.FloatingActionButton(
                                    icon=ft.Icons.COPY,
                                    on_click=lambda e: copy_to_clipboard(),
                                    shape=ft.RoundedRectangleBorder(radius=Styles.BTN_RADIUS)
                                ),
                                ft.FloatingActionButton(
                                    icon=ft.Icons.SAVE,
                                    on_click=lambda e:save_password(),
                                    shape=ft.RoundedRectangleBorder(radius=Styles.BTN_RADIUS)
                                )
                            ],
                            expand=True
                            ),
                        ],
                        expand=True
                        ),
                        ft.Text('', size=Styles.MIN_TEXT_SIZE)
                    ]),
                ],
                expand=True
                )
            ]),
            ft.Container(
                content=list_passwords,
                border=Styles.BORDER.value,
                border_radius=10,
                padding=20,
                margin=ft.margin.only(top=10),
                bgcolor=ft.Colors.GREY_900,
                expand=True
            ),
        ],
        expand=True
        ),
    expand=True,
    padding=30,
    )

    # adding the pages and navigator to the app
    page.add(
        ft.Container(
            content=content_area,
            expand=True
        )
    )
