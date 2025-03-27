import subprocess
import random

MAX_ITER = 130
TARGET_PUBKEY = "02c6047f9441ed7d6d3045406e95c07cd85c778e4b8cef3ca7abac09b95c709ee5"

def run_keymath(pubkey, op):
    """Execute ./keymath command with the given operation."""
    cmd = f"./keymath {pubkey} {op}"
    try:
        result = subprocess.check_output(cmd, shell=True, text=True).strip()
        return result
    except subprocess.CalledProcessError:
        return "ERROR"

def find_target(start_pubkey):
    attempt = 1

    while True:  # Infinite loop until target is found
        pubkey = start_pubkey
        operations = []
        last_op = None  # Store last operation to prevent "-1" repeat
        used_ops = set()  # Track used operations to prevent repetition
        
        for i in range(1, MAX_ITER + 1):
            print(f"Attempt {attempt}, Iteration {i}: Current Public Key: {pubkey}")

            if pubkey == TARGET_PUBKEY:
                print(f"Target Public Key Found: {pubkey}")
                print("Operations performed to reach target:")
                for op in operations:
                    print(op)
                return
            
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
    start_pubkey = "02e493dbf1c10d80f3581e4904930b1404cc6c13900ee0758474fa94abe8c4cd13"
    find_target(start_pubkey)
          
