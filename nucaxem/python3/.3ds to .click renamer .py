import os
d = input('Folder path: ')
for f in os.listdir(d):
    if f.endswith('.3ds'):
        os.rename(os.path.join(d, f), os.path.join(d, f[:-4] + '.cci'))
