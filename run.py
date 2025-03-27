import subprocess
import random

MAX_ITER = 256
TARGET_FILE = "target.txt"
OUTPUT_FILE = "found.txt"

def load_targets():
    """Load target public keys from target.txt file."""
    with open(TARGET_FILE, "r") as f:
        return {line.strip() for line in f if line.strip()}  # Remove empty lines

def run_keymath(pubkey, op):
    """Execute ./keymath command with the given operation."""
    cmd = f"./keymath {pubkey} {op}"
    try:
        result = subprocess.check_output(cmd, shell=True, text=True).strip()
        return result
    except subprocess.CalledProcessError:
        return "ERROR"

def generate_random_number():
    """Generate a random 40 or 41 digit number."""
    digits = random.choice([40, 41])
    return random.randint(10**(digits-1), 10**digits - 1)

def save_result(target, attempt, subtracted_value, operations):
    """Save successful attempt details to a file and stop execution."""
    with open(OUTPUT_FILE, "w") as f:
        f.write(f"Target Public Key Found: {target}\n")
        f.write(f"Attempts: {attempt}\n")
        f.write(f"Random Subtracted Value: {subtracted_value}\n")
        f.write("Operations performed:\n")
        for op in operations:
            f.write(f"{op}\n")
    print(f"Target public key found! Details saved in {OUTPUT_FILE}")
    exit(0)  # Stop execution once a target is found

def modify_pubkey(pubkey):
    """Subtract a random 40 or 41 digit value from the pubkey."""
    random_number = generate_random_number()
    new_pubkey = run_keymath(pubkey, f"- {random_number}")
    return new_pubkey, random_number

def find_target(start_pubkey, targets):
    attempt = 1

    # First, subtract a random 40 or 41 digit value from start_pubkey
    modified_pubkey, subtracted_value = modify_pubkey(start_pubkey)

    while True:  # Infinite loop until any target is found
        pubkey = modified_pubkey
        operations = [f"Modified Start: {start_pubkey} - {subtracted_value} = {pubkey}"]
        last_op = None  # Store last operation to prevent "-1" repeat
        used_ops = set()  # Track used operations to prevent repetition

        for i in range(1, MAX_ITER + 1):
            print(f"Attempt {attempt}, Iteration {i}: Current Public Key: {pubkey}")

            if pubkey in targets:
                save_result(pubkey, attempt, subtracted_value, operations)

            if pubkey == "1" or pubkey == "ERROR":
                break  # Stop this attempt if error occurs

            # Select valid operations based on last operation
            available_ops = ["/ 2", "- 1"] if last_op != "- 1" else ["/ 2"]

            # Filter out already used operations for this pubkey
            available_ops = [op for op in available_ops if (pubkey, op) not in used_ops]
            
            if not available_ops:
                break  # Stop this attempt if all possible operations are already used

            op = random.choice(available_ops)  # Randomly pick an allowed operation
            new_pubkey = run_keymath(pubkey, op)
            
            if new_pubkey == "ERROR":
                continue  # Skip to next iteration if error occurs

            operations.append(f"{pubkey} {op} -> {new_pubkey}")
            used_ops.add((pubkey, op))  # Mark this operation as used
            pubkey = new_pubkey
            last_op = op  # Store last operation to prevent "-1" repeat

        print(f"Attempt {attempt} failed, retrying...")
        attempt += 1

if __name__ == "__main__":
    targets = load_targets()  # Load target public keys from target.txt
    start_pubkey = "02145d2611c823a396ef6712ce0f712f09b9b4f3135e3e0aa3230fb9b6d08d1e16"
    find_target(start_pubkey, targets)
    
