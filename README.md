![example workflow](https://github.com/iCAN-PCM/py4gh/actions/workflows/main.yml/badge.svg)

## Installation
  - Dependency: If not already installed install [crypt4gh](https://crypt4gh.readthedocs.io/en/latest/index.html) `pip install crypt4gh`
  - `pip install git+https://github.com/iCAN-PCM/py4gh.git`

## Usage
- **To Encrypt**
  - `py4gh -f <root dir of files to encrypt> -s <path to secret key> -pks <path to public key> -t <encrypt>`
  - Note: Multiple public key can be added by space seprated path example `-pks <public key1> <publick key2> ...`
- **To Decrypt**
  - **To Decrypt**
  - `py4gh -f <root dir of files to decrypt> -s <path to secret key> -t <decrypt>`
  - Note: If --task / -t is empty it will default to decryption 
