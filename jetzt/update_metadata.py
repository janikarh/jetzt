import json
import os
import re
import sys

metadata_filename = 'jetzt_metadata.json'
metadata = {}

dep_type = 'PROD'
package = ''
package_with_version = ''
action = ''

''' Read existing metadata if available. '''
if os.path.exists(metadata_filename):
    with open(metadata_filename) as metadata_file:
        metadata = json.load(metadata_file)

argv_count = 0
for arg in sys.argv:
    if argv_count > 0:
        key, value = arg.split('___')
        if key == 'dep_type':
            dep_type = value
        elif key == 'package':
            package = value
        elif key == 'package_with_version':
            package_with_version = value
        elif key == 'action':
            action = value
        else:
            metadata[key] = value
    argv_count += 1

dependencies = 'dependencies'
if dep_type == 'DEV':
    dependencies = 'dev_dependencies'

if action == 'REMOVE':
    ''' Removing a dependency '''
    if dependencies in metadata:
        if isinstance(metadata[dependencies], dict):
            try:
                del metadata[dependencies][package]
            except KeyError as e:
                print(f"Could not remove dependency {package} from jetzt_metadata.json ({dependencies}/{package}), please remove manually.")

elif action == 'INSTALL':
    ''' Installing a new dependency. '''
    installed_package, installed_version = re.split("==|>=", package_with_version)  # package==0.13.2
    # Pinned version
    if '==' in package:
        installed_version = f"=={installed_version}"
    else:
        installed_version = f">={installed_version}"

    if dependencies in metadata:
        if isinstance(metadata[dependencies], dict):
            metadata[dependencies][installed_package] = installed_version
    else:
        metadata[dependencies] = {}
        metadata[dependencies][installed_package] = installed_version

''' Dump updated metadata. '''
with open(metadata_filename, 'w') as dump:
    json.dump(metadata, dump, indent=2, ensure_ascii=False)
