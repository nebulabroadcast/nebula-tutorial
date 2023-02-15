import nebula

from rich.prompt import Prompt
from rich.console import Console


CHANGE_PASSWORD_INTRO = """
[bold]Change user password[/bold]

[dim]This will change the password of an existing user[/dim]
[dim]Hit Ctrl-C to cancel[/dim]
"""


class Password(nebula.plugins.CLIPlugin):
    """Create a user"""

    name = "password"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.console = Console()
        self.console.print(CHANGE_PASSWORD_INTRO)

    async def main(self):

        user: nebula.User | None = None
        while True:
            try:
                username = Prompt.ask("Username")
                if not username:
                    raise ValueError("Username cannot be empty")

                res = await nebula.db.fetch(
                    "SELECT * FROM users WHERE login = $1", username
                )
                if not res:
                    raise ValueError("User with this name does not exists")

                user = nebula.User.from_row(res[0])

            except ValueError as e:
                self.console.print(f"[red]{e}[/red]")
                continue

            break

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

        user.set_password(password1)
        await user.save()
        self.console.print("[green]Password updated[/green]")
