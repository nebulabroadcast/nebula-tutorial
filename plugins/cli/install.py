import nebula
from pydantic import BaseModel, Field

from rich.prompt import Prompt
from rich.console import Console
from rich.text import Text

NEW_USER_INTRO = """
[bold]Create a new administrator[/bold]

[dim]This will create a new user with admin rights in the database[/dim]
[dim]Hit Ctrl-C to cancel[/dim]
"""


class Warning(Exception):
    pass


async def validate_username(username: str):
    if not username:
        raise ValueError("Username cannot be empty")
    res = await nebula.db.fetch("SELECT * FROM users WHERE login = $1", username)
    if res:
        raise ValueError("Username already exists")


async def validate_email(email: str):
    if not email:
        raise Warning("User will not have an email address")


class Users(nebula.plugins.CLIPlugin):
    """Create a user"""

    name = "user"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.console = Console()
        self.console.print(NEW_USER_INTRO)

    async def main(self):
        username = await self.prompt("Username", validate_username)
        email = await self.prompt("Email", validate_email)

        password1 = password2 = ""
        while True:
            password1 = Prompt.ask("Password", password=True)
            if not password1:
                self.console.print("[red]Password cannot be empty[/red]")
                continue
            password2 = Prompt.ask("Confirm password", password=True)
            if password1 != password2:
                self.console.print("[red]Passwords do not match[/red]")
                continue
            break

        user = nebula.User.from_meta(
            {
                "login": username,
                "email": email,
                "is_admin": True,
            }
        )
        user.set_password(password1)
        await user.save()
        self.console.print("[green]User created[/green]")

    async def prompt(self, name: str, validate=None):
        while True:
            value = Prompt.ask(name)
            try:
                await validate(value)
                return value
            except ValueError as e:
                self.console.print(f"[red]{e}[/red]")
            except Warning as e:
                self.console.print(f"[yellow]{e}[/yellow]")
                return value
