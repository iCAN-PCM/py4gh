import subprocess
from pathlib import Path

import pytest
# from py4gh import __version__
from py4gh.utility import decrypt_files, encrypt_files, get_files


# def test_version():
#     assert __version__ == "0.1.0"


@pytest.fixture(scope="session")
def keys(tmpdir_factory):
    test_pub1 = tmpdir_factory.mktemp("data").join("test1.pub")
    test_sec1 = tmpdir_factory.mktemp("data").join("test1.sec")
    test_pub2 = tmpdir_factory.mktemp("data").join("test2.pub")
    test_sec2 = tmpdir_factory.mktemp("data").join("test2.sec")
    # with open(stdout, "w") as sdf:
    #     subprocess.run(["echo", "blablaalbla"], stdout=sdf)
    p1 = subprocess.Popen(
        ["crypt4gh-keygen", "--sk", test_sec1, "--pk", test_pub1, "--nocrypt"],
        stdin=subprocess.PIPE,
    )
    p1.stdin.write(b"")
    p1.communicate()[0]
    p1.stdin.close()

    subprocess.run(
        ["crypt4gh-keygen", "--sk", test_sec2, "--pk", test_pub2, "--nocrypt"],
        # stdin=subprocess.PIPE,
        text=True,
        input="",
        # encoding="ascii",
    )
    return [(test_pub1, test_sec1), (test_pub2, test_sec2)]


@pytest.fixture(scope="session")
def files(tmp_path):
    d = tmp_path / "sub"
    p = d / "hello.txt"
    p.write_text("This is a secret message")
    return p


# def test_file(files):
#     with open(files, "r") as f:
#         print(f.read())
#         assert 1 == 3


def test_encryption(keys, tmpdir):
    d = tmpdir.mkdir("sub")
    f = d / "hello.txt"
    f.write("This is a secret message")
    files = get_files(d)
    err, res = encrypt_files(keys[0][1], [keys[0][0]], files)
    proc = subprocess.run(["ls", d], capture_output=True, text=True)
    output_list = proc.stdout.split("\n")
    assert output_list[1] == "hello.txt.c4gh"

    encrypted_file = Path(d / output_list[1])
    assert encrypted_file.stat().st_size != 0
    print(err)
    print(res)


def test_multiple_encryption(keys, tmpdir):
    d = tmpdir.mkdir("sub")
    f = d / "hello.txt"
    message = "This is a secret message"
    f.write(message)
    files = get_files(d)
    encrypt_files(keys[0][1], [keys[0][0], keys[1][0]], files)
    proc = subprocess.run(["ls", d], capture_output=True, text=True)
    print(proc.stdout)
    output_list = proc.stdout.split("\n")
    assert output_list[1] == "hello.txt.c4gh"
    encrypted_file = Path(d / output_list[1])
    # print(encrypted_file.read_bytes()[0])
    # assert encrypted_file.read_text() != message
    assert encrypted_file.stat().st_size != 0


def test_muliple_encryption_decryption(keys, tmpdir):
    d = tmpdir.mkdir("sub")
    f = d / "hello.txt"
    message = "This is a secret message"
    f.write(message)
    files = get_files(d)
    encrypt_files(keys[0][1], [keys[0][0], keys[1][0]], files)
    subprocess.run(["ls", d], capture_output=True, text=True)
    subprocess.run(["rm", f])
    proc2 = subprocess.run(["ls", d], capture_output=True, text=True)
    proc2_out = proc2.stdout.split("\n")
    assert len(proc2_out) == 2
    assert proc2_out[0] == "hello.txt.c4gh"
    assert proc2_out[1] == ""
    files2 = get_files(d)
    decrypt_files(keys[1][1], files2)
    proc = subprocess.run(["ls", d], capture_output=True, text=True)
    output_list = proc.stdout.split("\n")
    print(output_list)
    assert output_list[0] == "hello.txt"
    decrypted_file = Path(d / output_list[0])
    assert decrypted_file.read_text() == message
    assert decrypted_file.stat().st_size != 0
