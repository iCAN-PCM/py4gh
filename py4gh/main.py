import argparse
import logging

from py4gh.utility import decrypt_files, encrypt_files, get_files, process_output


def cli_parser() -> None:
    parser = argparse.ArgumentParser(
        description="Decrypt/Encrypt files in root dir and sub dir using crypt4gh"
    )
    parser.add_argument(
        "--filepath",
        "-f",
        required=True,
        type=str,
        nargs=1,
        help="Root dir where encrypted files are stored",
    )

    parser.add_argument(
        "--secret",
        "-s",
        required=True,
        nargs=1,
        type=str,
        help="Path to the secret file",
    )
    parser.add_argument(
        "--task",
        "-t",
        default=["decrypt"],
        nargs=1,
        help="to encrypt or to decrypt defaults to decrypt",
    )
    parser.add_argument(
        "--pubkey",
        "-pks",
        nargs="*",
        type=str,
        help="recipient public key, supports multiple public keys",
    )
    args = parser.parse_args()
    logging.info(f"Task received {args.task[0]}")
    # print(args.pubkey)
    if args.task[0] == "encrypt":
        if args.pubkey is None:
            print("Public key is missing : -pks cannot be empty for encrypt task")
            return
        allfiles = get_files(args.filepath[0])
        f, s = encrypt_files(
            sec_key=args.secret[0], pub_key=args.pubkey, files=allfiles
        )
        process_output(f, s, "encrypt")
    elif args.task[0] == "decrypt":
        allfiles = get_files(args.filepath[0], "c4gh")
        f, s = decrypt_files(args.secret[0], allfiles)
        process_output(f, s, "decrypt")
    else:
        print("received unknown task, task can only be encrypt or decrypt")


if __name__ == "__main__":
    cli_parser()
