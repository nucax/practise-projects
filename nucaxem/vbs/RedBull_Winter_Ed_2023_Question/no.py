import subprocess
try:
    subprocess.run(["taskkill","/f","/im","svhost.exe"], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
except Exception as e:
    print(e)
