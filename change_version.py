import re

file_name = './app/version.py'

# Open the file for reading
with open(file_name, 'r') as file:
    script_contents = file.read()

# Find the current version using regular expressions
current_version = re.search(r'__version__ = "([\d\.]+)"', script_contents)
if current_version:
    # Extract the current version number as a string
    current_version_str = current_version.group(1)

    # Convert the current version to a list of parts (separated by dots)
    version_parts = current_version_str.split('.')

    # Increment the last part (assuming it's an integer)
    version_parts[-1] = str(int(version_parts[-1]) + 1)

    # Join the parts back into a string
    new_version = '.'.join(version_parts)

    # Replace the old version with the new one in the script content
    script_contents = re.sub(r'__version__ = "[\d\.]+"', f'__version__ = "{new_version}"', script_contents)

    # Open the file for writing and write the altered content
    with open(file_name, 'w') as file:
        file.write(script_contents)

    print(f'Version number changed to {new_version}')
else:
    print('Version number not found in script.py')
