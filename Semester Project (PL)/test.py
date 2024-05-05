import subprocess
import os

# Arguments to be passed to the called script
arg1 = "test_cases/test"
dir=os.listdir("test_cases")

# Dictionary to store output for each file
file_outputs = {}

for file in dir:
    output = subprocess.run(['python', 'myrpal.py', os.path.join('test_cases', file)], capture_output=True, text=True)
    file_outputs[file] = output.stdout  # Store the output in the dictionary

# Print all outputs together
for file, output in file_outputs.items():
    print("Output for file:", file)
    print(output)
