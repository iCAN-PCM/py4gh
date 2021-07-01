import logging
from pathlib import Path
from subprocess import PIPE, Popen
from typing import List, Tuple

from tqdm import tqdm


def get_files(path: str, file_extension: str = "*") -> list:
    paths = []
    path = Path(path)
    for p in path.rglob(f"*.{file_extension}"):
        paths.append(str(p))
    return paths


def remove_suffix(filename: str, suffix: str) -> str:
    if filename.endswith(suffix):
        filename = filename[: -len(suffix)]
    return filename


def add_suffix(filename: str, suffix: str = "c4gh") -> str:
    return f"{filename}.{suffix}"


def decrypt_files(
    key: str, files: List[str]
) -> Tuple[List[Tuple[str, str]], List[str]]:
    failed = []
    success = []

    for file in tqdm(files):
        out_file = remove_suffix(file, ".c4gh")
        with open(out_file, "w") as outf, open(file, "r") as inf:
            logging.info(f"processing file: {file}")
            proc = Popen(
                ["crypt4gh", "decrypt", "--sk", key],
                stdin=inf,
                stdout=outf,
                shell=False,
                stderr=PIPE,
            )
            logging.info(f"output: {proc}")
            _, err = proc.communicate()
            if proc.returncode == 0:
                success.append(file)
            else:
                failed.append((file, f"{proc.returncode}, err msg:{err}"))
    return failed, success


def encrypt_files(
    sec_key: str, pub_key: List[str], files: List[str]
) -> Tuple[List[Tuple[str, str]], List[str]]:
    failed = []
    success = []
    pub_keys = [["--recipient_pk", key] for key in pub_key]
    pub_keys = [i for g in pub_keys for i in g]
    for file in tqdm(files):
        out_file = add_suffix(file)
        with open(out_file, "w") as outf, open(file, "r") as inf:
            logging.info(f"processing file: {file}")
            proc = Popen(
                ["crypt4gh", "encrypt", "--sk", sec_key, *pub_keys],
                stdin=inf,
                stdout=outf,
                shell=False,
                stderr=PIPE,
            )
            _, err = proc.communicate()
            logging.info(f"output {proc}")
            if proc.returncode == 0:
                success.append(file)
            else:
                failed.append((file, f"{proc.returncode}, err msg:{err}"))
    return failed, success


def process_output(failed: List[Tuple], success: List[str], task: str) -> None:
    print(f"Total file processed \U0001F916: {len(failed)+len(success)}")
    print(f"Files successfully \U0001F973: {task}ed: {len(success)}")
    for file in success:
        print(file)
    print(f"Files failed to {task} \U0001F631: {len(failed)}")
    for file in failed:
        print(f"file: {file[0]}, err code {file[1]}")
