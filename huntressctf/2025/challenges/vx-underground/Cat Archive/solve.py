#!/usr/bin/env python3
"""
Shamir's Secret Sharing Scheme (SSSS) Recovery Script
Recovers a secret from shares extracted from EXIF data
"""

import re
from pathlib import Path


def extended_gcd(a, b):
    """Extended Euclidean Algorithm"""
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y


def mod_inverse(a, m):
    """Calculate modular inverse of a mod m"""
    gcd, x, _ = extended_gcd(a % m, m)
    if gcd != 1:
        raise ValueError("Modular inverse does not exist")
    return (x % m + m) % m


def lagrange_interpolation(points, prime):
    """
    Recover secret using Lagrange interpolation
    points: dictionary of {x: y} coordinates
    prime: the prime modulus
    """
    secret = 0
    x_values = list(points.keys())

    for i, x_i in enumerate(x_values):
        y_i = points[x_i]

        # Calculate Lagrange basis polynomial at x=0
        numerator = 1
        denominator = 1

        for j, x_j in enumerate(x_values):
            if i != j:
                # At x=0, we get: (0 - x_j) / (x_i - x_j)
                numerator = (numerator * (-x_j)) % prime
                denominator = (denominator * (x_i - x_j)) % prime

        # Calculate the term: y_i * numerator * denominator^(-1)
        denominator_inv = mod_inverse(denominator, prime)
        term = (y_i * numerator * denominator_inv) % prime
        secret = (secret + term) % prime

    return secret


def parse_exif_comment(comment):
    """
    Parse EXIF comment in format: index-hex_value
    Returns: (index, value_as_int)
    """
    match = re.match(r"^(\d+)-([0-9a-fA-F]+)$", comment.strip())
    if not match:
        return None, None

    index = int(match.group(1))
    hex_value = match.group(2)
    value = int(hex_value, 16)

    return index, value


def extract_shares_from_exif(directory="."):
    """
    Extract shares from image EXIF data in the given directory
    Requires exiftool to be installed
    """
    import subprocess

    shares = {}

    # Find all image files
    image_extensions = [".jpg", ".jpeg", ".png", ".gif", ".tiff", ".bmp"]
    files = []

    for ext in image_extensions:
        files.extend(Path(directory).glob(f"*{ext}"))
        files.extend(Path(directory).glob(f"*{ext.upper()}"))

    print(f"Found {len(files)} image files")

    for file_path in files:
        try:
            # Use exiftool to extract UserComment
            result = subprocess.run(
                ["exiftool", "-UserComment", "-s3", str(file_path)],
                capture_output=True,
                text=True,
                timeout=5,
            )

            if result.returncode == 0 and result.stdout.strip():
                comment = result.stdout.strip()
                index, value = parse_exif_comment(comment)

                if index is not None and value is not None:
                    shares[index] = value
                    print(f"  Extracted share {index} from {file_path.name}")

        except subprocess.TimeoutExpired:
            print(f"  Timeout reading {file_path.name}")
        except FileNotFoundError:
            print("Error: exiftool not found. Please install exiftool.")
            print("  Ubuntu/Debian: sudo apt-get install libimage-exiftool-perl")
            print("  macOS: brew install exiftool")
            return None
        except Exception as e:
            print(f"  Error reading {file_path.name}: {e}")

    return shares


def manual_share_input():
    """Manually input shares if exiftool is not available"""
    shares = {}
    print("\nManual share input mode")
    print("Enter shares in format 'index:hex_value' (e.g., 1:d278c2aad8f1c0de...)")
    print("Enter 'done' when finished\n")

    while True:
        line = input("Share: ").strip()
        if line.lower() == "done":
            break

        try:
            if ":" in line:
                index_str, hex_value = line.split(":", 1)
                index = int(index_str)
                value = int(hex_value, 16)
                shares[index] = value
                print(f"  Added share {index}")
        except Exception as e:
            print(f"  Invalid format: {e}")

    return shares


def main():
    print("=" * 60)
    print("Shamir's Secret Sharing Scheme - Secret Recovery")
    print("=" * 60)

    # Parse prime modulus
    prime_hex = "010000000000000000000000000000000000000000000000000000000000000129"
    prime = int(prime_hex, 16)
    print(f"\nPrime modulus: {prime}")
    print(f"Prime (hex): {prime_hex}\n")

    # Get directory from user
    directory = input(
        "Enter directory containing images (or '.' for current): "
    ).strip()
    if not directory:
        directory = "."

    # Try to extract shares from EXIF
    print(f"\nScanning directory: {directory}")
    shares = extract_shares_from_exif(directory)

    # Fallback to manual input if needed
    if shares is None or len(shares) == 0:
        use_manual = (
            input("\nNo shares found. Use manual input? (y/n): ").strip().lower()
        )
        if use_manual == "y":
            shares = manual_share_input()
        else:
            print("Exiting...")
            return

    if len(shares) < 2:
        print(f"\nError: Need at least 2 shares, found {len(shares)}")
        return

    print(f"\nTotal shares collected: {len(shares)}")
    print(f"Share indices: {sorted(shares.keys())}")

    # Recover the secret
    print("\nRecovering secret...")
    secret = lagrange_interpolation(shares, prime)

    # Convert to hex and bytes
    secret_hex = hex(secret)[2:]
    if len(secret_hex) % 2:
        secret_hex = "0" + secret_hex

    print(f"\nRecovered secret (decimal): {secret}")
    print(f"Recovered secret (hex): {secret_hex}")

    # Try to convert to ASCII if possible
    try:
        secret_bytes = bytes.fromhex(secret_hex)
        print(f"Recovered secret (bytes length): {len(secret_bytes)}")

        # Try to decode as ASCII/UTF-8
        try:
            secret_text = secret_bytes.decode("utf-8")
            print(f"Recovered secret (text): {secret_text}")
        except:
            print(f"Recovered secret (raw bytes): {secret_bytes}")

        # Save to file
        output_file = "recovered_secret.txt"
        with open(output_file, "w") as f:
            f.write(f"Secret (hex): {secret_hex}\n")
            f.write(f"Secret (decimal): {secret}\n")
            try:
                f.write(f"Secret (text): {secret_text}\n")
            except:
                pass

        print(f"\nSecret saved to: {output_file}")
        print("\nTry using this as the password for flag.zip!")

    except Exception as e:
        print(f"\nError converting secret: {e}")


if __name__ == "__main__":
    main()
