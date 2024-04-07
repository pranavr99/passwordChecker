#This is a simple python program that checks the strength of a user's inputed password
#based on the NIST SP800-63B
#Pranav Rao

import flet
from flet import *
import re

CONTROLS = []
STATUS = []

def store_control_sub_reference(function):
    def wrapper(*args, **kwargs):
        reference = function(*args, **kwargs)
        locals()["kwargs"]["control"]
        if kwargs["control"] == 0:
            CONTROLS.append(reference)
        else:
            STATUS.append(reference)
        return reference

    return wrapper

#This class is where the main logic using some common aspects of :NIST SP800-63B
#Minimum length of 8 characters 
#Allow usage of ASCII characters (including space) and Unicode characters.
#Password Strength Meter
#avoid common password or phrase
class PasswordStrengthChecker:
    def __init__(self, password):
        self.password = password
        self.common_passwords = ["password", "1234", "admin", "qwerty"]
        self.complexity_regex = re.compile(
            r"(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])"
        )

    # We return integers that represent points based on the user's input indicating the strength of password
    #This is the length check of how many passwords can be in it and if so so the password gets point 
    def length_check(self):
        length = len(self.password)
        if length > 0 and length < 8:
            return 0
        elif length >= 8 and length < 12:
            return 1
        elif length >= 12 and length < 16:
            return 2
        elif length >= 16 and length <= 64:
            return 3
        elif length > 64:
            return 0
        
    #This is just checks how many special characters a password can contain and if so they get a point
    def character_check(self):
        characters = set(self.password)
        lower_case = set("abcdefghijklmnopqrstuvwxyz")
        upper_case = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        digits = set("0123456789")
        special_characters = set("!@#$%^&*()_+-=[]{};:,.<>/?`~")

        score = 0
        if any(char in lower_case for char in characters):
            score += 1
        if any(char in upper_case for char in characters):
            score += 1
        if any(char in digits for char in characters):
            score += 1
        if any(char in special_characters for char in characters):
            score += 1

        if score == 1:
            return 0
        elif score == 2:
            return 1
        elif score == 3:
            return 2
        elif score == 4:
            return 3

    # Function checks if there's any reptition in the password and allocates the proper points
    def repeat_check(self):
        if len(self.password) == 0:
            return 2
        else:
            for i in range(len(self.password) - 2):
                if self.password[i] == self.password[i + 1] == self.password[i + 2]:
                    return 0
            return 1

    #Function checks like if there's any repeating sequences and then allocates more points
    def sequential_check(self):
        if len(self.password) == 0:
            return 2
        else:
            for i in range(len(self.password) - 2):
                #We look for passwords within a range of 3 characters
                if (
                    self.password[i : i + 3].isdigit()
                    or self.password[i : i + 3].islower()
                    or self.password[i : i + 3].isupper()
                ):
                    return 0
            return 1


#This class is the main UI class for the interactive interface
class AppWindow(UserControl):
    def __init__(self):
        super().__init__()

    #This function, we need a function to call all the above class inner functions
    def check_password(self, e):
        password_strength_checker = PasswordStrengthChecker(e.data)
    
        #call the length checker and give points based on the input and pass in the point 
        password_length = password_strength_checker.length_check()
        self.password_length_status(password_length) 
        #call the character checker
        character_checker = password_strength_checker.character_check()
        self.character_check_status(character_checker) 
        #call the repeat checker
        repeat_check = password_strength_checker.repeat_check()
        self.repeat_check_status(repeat_check) 
        #call the sequence checker
        sequential_check = password_strength_checker.sequential_check()
        self.sequential_check_status(sequential_check)
    
    #This function will help us showcase the length of status on the UI using GRID 
    def password_length_status(self, strength):
        if strength == 0:
            CONTROLS[0].controls[1].controls[0].bgcolor = "red"
            CONTROLS[0].controls[1].controls[0].width = 40
        elif strength == 1:
            CONTROLS[0].controls[1].controls[0].bgcolor = "yellow"
            CONTROLS[0].controls[1].controls[0].width = 70
        elif strength == 2:
            CONTROLS[0].controls[1].controls[0].bgcolor = "green400"
            CONTROLS[0].controls[1].controls[0].width = 100
        elif strength == 3:
            CONTROLS[0].controls[1].controls[0].bgcolor = "green900"
            CONTROLS[0].controls[1].controls[0].width = 130
        else:
            CONTROLS[0].controls[1].controls[0].width = 0

        CONTROLS[0].controls[1].controls[0].opacity = 1
        CONTROLS[0].controls[1].controls[0].update()


#This function will help us showcase the character of status on the UI using GRID 
    def character_check_status(self, strength):
        if strength == 0:
            CONTROLS[1].controls[1].controls[0].bgcolor = "red"
            CONTROLS[1].controls[1].controls[0].width = 40
        elif strength == 1:
            CONTROLS[1].controls[1].controls[0].bgcolor = "yellow"
            CONTROLS[1].controls[1].controls[0].width = 70
        elif strength == 2:
            CONTROLS[1].controls[1].controls[0].bgcolor = "green400"
            CONTROLS[1].controls[1].controls[0].width = 100
        elif strength == 3:
            CONTROLS[1].controls[1].controls[0].bgcolor = "green900"
            CONTROLS[1].controls[1].controls[0].width = 130
        else:
            CONTROLS[1].controls[1].controls[0].width = 0

        CONTROLS[1].controls[1].controls[0].opacity = 1
        CONTROLS[1].controls[1].controls[0].update()

#This function will help us showcase the repition status on the UI using GRID 
    def repeat_check_status(self, strength):
        if strength == 0:
            CONTROLS[2].controls[1].controls[0].bgcolor = "red"
            CONTROLS[2].controls[1].controls[0].width = 65
        elif strength == 1:
            CONTROLS[2].controls[1].controls[0].bgcolor = "green900"
            CONTROLS[2].controls[1].controls[0].width = 130
        else:
            CONTROLS[2].controls[1].controls[0].width = 0

        CONTROLS[2].controls[1].controls[0].opacity = 1
        CONTROLS[2].controls[1].controls[0].update()

#This function will help us showcase the sequential status on the UI using GRID 
    def sequential_check_status(self, strength):
        if strength == 0:
            CONTROLS[3].controls[1].controls[0].bgcolor = "red"
            CONTROLS[3].controls[1].controls[0].width = 65
        elif strength == 1:
            CONTROLS[3].controls[1].controls[0].bgcolor = "green900"
            CONTROLS[3].controls[1].controls[0].width = 130
        else:
            CONTROLS[3].controls[1].controls[0].width = 0

        CONTROLS[3].controls[1].controls[0].opacity = 1
        CONTROLS[3].controls[1].controls[0].update()


    @store_control_sub_reference
    def check_criteria_display(self, criteria, description, control: int):
        return Row(
            alignment=MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=CrossAxisAlignment.CENTER,
            spacing=5,
            controls=[
                Column(
                    spacing=2,
                    controls=[
                        Text(value=criteria, size=13, color= "white", weight="bold"),
                        Text(value=description, size=9, color="white54"),
                    ],
                ),
                Row(
                    spacing=0,
                    alignment=MainAxisAlignment.START,
                    controls=[
                        Container(
                            height=5,
                            opacity=0,
                            animate=350,
                            border_radius=10,
                            animate_opacity=animation.Animation(350, "decelerate"),
                        ),
                    ],
                ),
            ],
        )
    
    #This function is the main display area where it will highlight the strenght of the password
    def password_strength_display(self):
        return Container(
            width=350,
            height=400,
            bgcolor="#1f262f",
            border_radius=10,
            padding=10,
            clip_behavior=ClipBehavior.HARD_EDGE,
            content=Column(
                horizontal_alignment=CrossAxisAlignment.CENTER,
                spacing=2,
                controls=[
                    Divider(height=5, color="transparent"),
                    Text("Password Strength Checker", size=21, color="white", weight="bold"),
                    Text("Let's check and see how strong your password is!", size=11, color="white54", weight="w400",),
                    Divider(height=25, color="white"),
                    self.check_criteria_display(
                        "1. Length Check",
                        "Strong passwords are 8 characters or more.",
                        control=0,
                    ),
                    # self.check_status_display(control=1),
                    Divider(height=20, color="transparent"),
                    self.check_criteria_display(
                        "2. Character Check",
                        "Upper, lower, and special characters.",
                        control=0,
                    ),
                    # self.check_status_display(control=1),
                    Divider(height=20, color="transparent"),
                    self.check_criteria_display(
                        "3. Repeat Check",
                        "Check for any repetition....",
                        control=0,
                    ),
                    # self.check_status_display(control=1),
                    Divider(height=20, color="transparent"),
                    self.check_criteria_display(
                        "4. Sequential Check",
                        "Check for sequential strings...",
                        control=0,
                    ),
                    # self.check_status_display(control=1),
                ],
            ),
        )

    #This function is what allows the user to input password using a Text Field
    def password_text_field_display(self):
            return Row(
                spacing=20,
                vertical_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    Icon(
                        name=icons.LOCK_OUTLINE_ROUNDED,
                        size=16,
                        opacity=1,
                    ),
                    TextField(
                        border_color="transparent",
                        bgcolor="transparent",
                        height=20,
                        width=200,
                        text_size=16,
                        content_padding=3,
                        cursor_color="black",
                        cursor_width=1,
                        color="black",
                        hint_text="Type a password ...",
                        hint_style=TextStyle(
                            size=15,
                        ),
                        on_change=lambda e: self.check_password(e),
                        password=True,
                    ),
                ],
            )

# This function for the input diplay along with the copy password function on the main UI 
    def password_input_display(self):
        return Card(
            color="#808080",
            width= 350,
            height=60,
            elevation=12,
            offset=transform.Offset(0, -0.25),
            content=Container(
                padding=padding.only(left=15),
                content=Row(
                    alignment=MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        self.password_text_field_display(),
                        IconButton(
                            icon=icons.COPY,
                            icon_size=16,
                            opacity=1,
                        ),
                    ],
                ),
            ),
        )


    # This is the main UI CARD and everything else will be overlayed on this
    def build(self):
        return Card(
            elevation=20,
            content=Container(
                scale=Scale(1.05),
                width=400,
                height=450,
                border_radius=10,
                bgcolor="#1f262f",
                content=Column(
                    spacing=0,
                    horizontal_alignment="center",
                    controls=[
                        #add main classes here...
                        self.password_strength_display(),
                        self.password_input_display(),

                    ],
                ),
            ),
        )


def main(page: Page):
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.bgcolor = "#212328"
    page.add(AppWindow())
    page.update()


if __name__ == "__main__":
    flet.app(target=main)
