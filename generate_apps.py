import os
application_path = fr"C:\Backup\ng\backend\site"
os.chdir(application_path)
app_folder = 'rental'
app_list = ['units', 'cart', 'checkout', 'notifications', 'payment', 'products', 'order']

# os.system(f'cmd /k "conda activate dj"')
commands = []
# commands.append(f'cd "{application_path}"')

for app in app_list:
    # command = f'python manage.py startapp {app}'
    is_app_path = os.path.join(application_path, fr"apps\{app_folder}\{app}")
    if not os.path.exists(is_app_path):
        os.mkdir(is_app_path)
        print(is_app_path)

    command = f'call python manage.py startapp {app} ./apps/{app_folder}/{app}'
    commands.append(command)


# Define the path for the batch file
batch_file_path = 'generate_apps.bat'  # Replace with your desired file path

# Create the batch file and add the commands
with open(batch_file_path, 'w') as batch_file:
    for command in commands:
        batch_file.write(f'{command}\n')

print(f'Batch file "{batch_file_path}" created successfully with the commands.')

# command = ' & '.join(commands)
# print(command)
# os.system(f'cmd /k {command}')