import hashlib
import time

def calculate_sha256(file_path):
    """
    Calculate SHA-256 hash of a file.
    """
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as file:
        while True:
            data = file.read(4096)
            if not data:
                break
            sha256.update(data)
    return sha256.hexdigest()


def calculate_hash_difference(hash1, hash2):
    """
    Calculate percentage of different bits
    between two SHA-256 hashes.
    """
    binary1 = bin(int(hash1, 16))[2:].zfill(256)
    binary2 = bin(int(hash2, 16))[2:].zfill(256)
    different_bits = sum(
        bit1 != bit2
        for bit1, bit2 in zip(binary1, binary2)
    )
    percentage = (different_bits / 256) * 100
    return different_bits, round(percentage, 2)

def get_risk_level(difference):
    """
    Determine risk level based on
    hash difference percentage.
    """
    if difference > 50:
        return "HIGH"
    elif difference > 20:
        return "MEDIUM"
    else:
        return "LOW"

def measure_performance(file_path):
    """
    Measure SHA-256 execution time.
    """
    start_time = time.perf_counter()
    calculate_sha256(file_path)
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    return round(execution_time, 6)

def analyze_file(original_hash, current_hash, file_path):
    """
    Perform complete security analysis.
    """
    # Integrity check
    integrity_verified = original_hash == current_hash
    if integrity_verified:
        status = "INTEGRITY VERIFIED"
    else:
        status = "FILE MODIFIED"
    # Avalanche / hash difference
    different_bits, difference = calculate_hash_difference(
        original_hash,
        current_hash
    )
    # Risk
    risk = get_risk_level(difference)
    # Performance
    execution_time = measure_performance(file_path)
    return {
        "status": status,
        "different_bits": different_bits,
        "difference": difference,
        "risk": risk,
        "execution_time": execution_time
    }