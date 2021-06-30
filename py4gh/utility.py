import logging
from os import strerror
from pathlib import Path
import subprocess
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
) -> Tuple[List[Tuple[str, int]], List[str]]:
    failed = []
    success = []

    for file in tqdm(files):
        out_file = remove_suffix(file, ".c4gh")
        with open(out_file, "w") as outf, open(file, "r") as inf:
            logging.info(f"processing file: {file}")
            proc = subprocess.run(
                ["crypt4gh", "decrypt", "--sk", key],
                stdin=inf,
                stdout=outf,
                shell=False,
                stderr=subprocess.STDOUT,
            )
            logging.info(f"output: {proc}")
            if proc.returncode == 0:
                success.append(file)
            else:
                failed.append((file, proc.returncode))
    return failed, success


def encrypt_files(
    sec_key: str, pub_key: List[str], files: List[str]
) -> Tuple[List[Tuple[str, int]], List[str]]:
    failed = []
    success = []
    pub_keys = [["--recipient_pk", key] for key in pub_key]
    pub_keys = [i for g in pub_keys for i in g]
    for file in tqdm(files):
        out_file = add_suffix(file)
        with open(out_file, "w") as outf, open(file, "r") as inf:
            logging.info(f"processing file: {file}")
            proc = subprocess.run(
                ["crypt4gh", "encrypt", "--sk", sec_key, *pub_keys],
                stdin=inf,
                stdout=outf,
                shell=False,
            )
            logging.info(f"output {proc}")
            if proc.returncode == 0:
                success.append(file)
            else:
                failed.append((file, proc.returncode))
    return failed, success


def process_output(failed: List[Tuple], success: List[str], task: str) -> None:
    print(f"Total file processed {len(failed)+len(success)}")
    print(f"Files successfully {task}ed: {len(success)}")
    for file in success:
        print(file)
    print(f"Files failed to {task}: {len(failed)}")
    for file in failed:
        print(f"file: {file[0]}, err code {file[1]}")
