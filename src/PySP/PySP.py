import os
import argparse # https://docs.python.org/3/library/argparse.html
import jinja2
import shutil
import subprocess
import logging

from pathlib import Path
from rich.prompt import Prompt
from rich.console import Console

from .utils import print_except, setup_console_logger


cwd = Path(os.getcwd())
module_path = Path(__file__).parent
console = Console()
prompt = Prompt(console=console)
setup_console_logger(console=console)
log = logging.getLogger(__name__)


def main() -> None:
    global console

    args = arg_parser().parse_args()
    try:
        console.clear()
        console.print("[bold]Welcome to the utilitary that will create your "
              +"brand new Python project", justify="center")
        create_project_result = create_project(args.project_path)
        if not create_project_result[0] : raise Exception(
            "[red]Project folder creation failed, aborting")

        if create_project_result:
            create_venv_result, venv_path = create_venv(
                args.venv, create_project_result[1])
            if not create_venv_result : raise Exception(
                "[red]venv creation failed, aborting")

        if create_venv_result:
            install_build_tools_result = install_packages(venv_path,
                                                          args.proxy)
            if not install_build_tools_result :
                log.error("[red]build tools install failed")

    except KeyboardInterrupt:
        console.line()
        log.info("[red]exiting PySP after keyboardInterrupt catch.")


def create_project(project_path, asynchronus:bool=False) -> tuple[bool, str]:
    global cwd
    global console
    global prompt

    console.print("\n -> The project name will be the name of the containing "
                  +"folder")
    if not project_path:
        user_input = prompt.ask(
            f"    Chose your project path [bold cyan]({cwd})[/]",
            default=cwd,
            console=console)
        if user_input == "":
            project_path = cwd
        else:
            project_path = Path(user_input)
        console.print(f"    path received :\n    "
                      + f"\"[bold green]{project_path}[/]\"")
    else:
        project_path = Path(project_path)

    # create project folder
    if not project_path.exists():
        project_path.mkdir()
        if not project_path.exists():
            raise Exception(
                f"Failed to create {project_path.absolute()}")

    # copy the template files to the project folder
    project_name = project_path.name

    if not asynchronus:
        user_input = prompt.ask(
            "\n -> Would you like your project to have "
            + "[bold green]asynchronus[/] behavior ?",
            choices=["Y", "Yes", "", "N", "No"],
            default="No",
            case_sensitive=False,
            show_choices=True,
            show_default=True,
            console=console)
        console.print()
        if user_input.lower() in ["y", "yes", ""]:
            asynchronus = True

    # load templates
    data = {
        "project_name": project_name,
        "project_author": "user",
        "author_mail": "user@mail.com",
        "asynchronus": asynchronus
    }
    templates = [
        Path(f"{module_path}/templates/.gitignore"),
        Path(f"{module_path}/templates/LICENSE"),
        Path(f"{module_path}/templates/pyproject.toml"),
        Path(f"{module_path}/templates/README.md"),
        Path(f"{module_path}/templates/__main__.py"),
    ]
    for t in templates:
        with t.open() as f:
            template = jinja2.Environment().from_string(f.read())
            output = template.render(data)

        with Path(f"{project_path}/{t.name}").open("w") as f:
            f.write(output)

    # copy boiler plate files
    src_path = Path(f"{project_path}/src")
    if not src_path.exists(): src_path.mkdir()

    package_path = Path(f"{src_path}/{project_name}")
    if not package_path.exists(): package_path.mkdir()

    shutil.move(
        Path(f"{project_path}/__main__.py"),
        Path(f"{package_path}/__main__.py"))

    if asynchronus:
        shutil.copy(
            Path(f"{module_path}/templates/async_module_template.py"),
            Path(f"{package_path}/{project_name}.py"))
    else:
        shutil.copy(
            Path(f"{module_path}/templates/module_template.py"),
            Path(f"{package_path}/{project_name}.py"))

    shutil.copy(
        Path(f"{module_path}/utils.py"),
        Path(f"{package_path}/utils.py"))

    shutil.copy(
        Path(f"{module_path}/templates/__init__.py"),
        Path(f"{package_path}/__init__.py"))

    log.info(f"Project [bold green]{project_name}[/] "
          + f"created at [bold green]{project_path.absolute()}[/]")

    return True, project_path


def create_venv(virtual_env, project_path: Path) -> tuple[bool, str]:
    global console
    global prompt
    user_input = ""

    if not virtual_env:
        user_input = prompt.ask(
            f"\n -> Do you want to setup a venv for your project ?",
            choices=["Y", "Yes", "", "N", "No"],
            default="Yes",
            case_sensitive=False,
            show_choices=True,
            show_default=True)

    if user_input.lower() in ["y", "yes", ""] or virtual_env == True:
        try:
            import venv

            venv_name = prompt.ask(
                f"\n -> Would you like a specific name for your venv ?",
                default="pyenv",
                show_default=True)

            venv_path = Path(f"{project_path.absolute()}/{venv_name}")
            venv.create(venv_path, clear=True, with_pip=True)

        except Exception:
            log.error(
                "[red]Error trying importing venv module, ensure that venv "
                + "is installed (ie: pip install venv)")
            print_except()
        console.print()
        log.info(f"venv created in [bold green]{venv_path}[/]")

        return True, venv_path

    elif user_input.lower() in ["no", "n"]:
        return False, None

    else:
        log.warning("unknown option")
        return create_venv(False)


def install_packages(env_path: Path, proxy: str = "") -> bool:
    global console
    global prompt

    try:
        console.print("\n -> Installation of build tools with pip in the new "
                      + "pyenv")
        if not proxy :
            user_input = prompt.ask(
                f"    Do you have a proxy ?",
                choices=["Y", "Yes", "", "N", "No"],
                default="No",
                case_sensitive=False,
                show_choices=True,
                show_default=True)
            if user_input.lower() in ["y", "yes"]:
                proxy = prompt.ask(f"\n -> Type your proxy address")
        console.print()

        # install build package
        packages = [
            "setuptools",
            "build"
        ]

        pip_exe = f"{env_path}/Scripts/pip.exe" if os.name == "nt" \
            else f"{env_path}/bin/pip"

        pip_cmd = [pip_exe, "install", *packages]

        if proxy :
            pip_cmd = [*pip_cmd, "--proxy", proxy]
        subprocess.check_call(pip_cmd)

        # install project as editable
        pip_cmd = [
            pip_exe,
            "install",
            "--editable",
            f"{env_path.parent.absolute()}"
        ]

        if proxy :
            pip_cmd = [*pip_cmd, "--proxy", proxy]
        subprocess.check_call(pip_cmd)
    except Exception:
        log.error("[red]Error while trying to install pip packages")
        print_except()

    return True


def arg_parser() ->  argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="dirs-base-python",
        description="Tool that helps create a boiler plate python project "
        + "with arg management and logging built in"
    )
    p.add_argument("-p", "--project_path",
                   action="store",
                   help="new project path")
    p.add_argument("-e", "--venv",
                   action="store_true",
                   help="enable venv creation for the new project")
    p.add_argument("--proxy",
                   action="store",
                   help="define the proxy to use for package installation")

    return p
