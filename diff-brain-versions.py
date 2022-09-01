#!/usr/bin/env python
"""
Compare two brain versions.
"""

import os
import shutil
import pathlib
import subprocess
import sys
import json
import tempfile

log_command_output: bool = False

def print_highlighted(message: str):
    # Send special escape sequences that print text in the color blue on most terminals.
    print(f"\033[94m{message}\033[0m")

def run_command(command: str, return_string: bool=False, errors_expected: bool=False):
    print(f"  > {command}")
    process = subprocess.run(command, capture_output=return_string, text=True, shell=True)
    if log_command_output:
        print(f"""
returncode: {process.returncode}
stderr: {process.stderr}
stdout: {process.stdout}
""".strip())
    if process.returncode != 0:
        if not errors_expected:
            if process.stderr != None:
                print(process.stderr)
            sys.exit()
        return None
    if not return_string:
        return None
    return process.stdout

def main(brainA: str, versionA: int, brainB: str, versionB: int):
    has_error = False
    if not "SIM_WORKSPACE" in os.environ:
        print("test-fmu.py: error: SIM_WORKSPACE environment variable must be set to your Bonsai workspace ID.")
        has_error = True
    if not "SIM_ACCESS_KEY" in os.environ:
        print("test-fmu.py: error: SIM_ACCESS_KEY environment variable must be set to your Bonsai workspace access key.")
        has_error = True

    if has_error:
        return

    # Run a simple Bonsai CLI command. This will prompt the user if they need to log in for the CLI.
    print_highlighted("Log in to Bonsai CLI (if needed)")
    run_command("bonsai -s")

    def write_version(brain, version):
        inkling = run_command(f"bonsai brain version get-inkling -n {brain} --version {version}", return_string=True)
        inkling_file = tempfile.TemporaryFile(prefix=f'{version}-{brain}', suffix='.ink', mode="w+", delete=False)
        inkling_file.write(inkling)
        inkling_file.close()
        return inkling_file.name

    inklingA = write_version(brainA, versionA)
    inklingB = write_version(brainB, versionB)
    run_command(f'git difftool --no-index {inklingA} {inklingB}')
    os.remove(inklingA)
    os.remove(inklingB)

if __name__ == "__main__":

    import argparse

    print(sys.argv)

    epilog_text = """
Examples:
 diff-brain-versions mybrain 2 3
    Compare versions 2 and 3 of the brain mybrain.
 diff-brain-versions mybrain 2 otherbrain 3
    Compare version 2 of mybrain to version 3 of otherbrain.
""".strip()

    parser = argparse.ArgumentParser(
        description="Compare the inkling of two brain versions.",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=epilog_text)

    parser.add_argument("brainA", type=str, help="The brain name containing the first version.")
    parser.add_argument("versionA", type=int, help="The first version number.")
    parser.add_argument("brainB", nargs='?', type=str, help="Optional: The brain name containing the second version. If not specified, the first brain will be used.")
    parser.add_argument("versionB", type=int, help="The second version number.")

    args = parser.parse_args()
    main(args.brainA, args.versionA, args.brainB if args.brainB else args.brainA, args.versionB)