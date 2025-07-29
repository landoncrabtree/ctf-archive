import base64
import subprocess
import tempfile
import sys
import os

def main():

    flag = open('flag.txt','r').read().rstrip()
    assert(len(flag) == 42)

    b64_data = input('Enter your base64-encoded rule file: ')

    try:
        rule_data = base64.b64decode(b64_data)
    except Exception:
        print(f'[ERROR] Failed to decode base64')
        exit()

    if len(rule_data) > 128:
        exit()

    # Save rule data to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".rule") as rule_file:
        rule_file.write(rule_data)
        rule_path = rule_file.name

    try:
        # Run hashcat and stream output to stdout
        process = subprocess.Popen(
            ['hashcat', '-m', '1400', '-r', rule_path, '--potfile-disable', 'hash.txt', 'flag.txt'],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )

        for line in process.stdout:
            if 'Status' in line.decode():
                print(line.decode())
                break

        process.stdout.close()
        process.wait()
    except Exception:
        print(f'[ERROR] Failed to run hashcat')
    finally:
        os.remove(rule_path)

if __name__ == "__main__":
    main()
