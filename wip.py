import os
import threading
import time
import subprocess as sp

with open("output") as f:
    os.set_inheritable(f.fileno(), True)
    sp.run(["cat", f"/dev/fd/3"], close_fds=False)

text = "a" * 100000

read, write = os.pipe()
os.set_inheritable(read, True)

def write_to_fd(fd: int, data: str):
    print("started!")
    with open(fd, "w") as f:
        f.write(data)

    print("done!")

write_to_fd(write, text)
sp.run([f"cat /dev/fd/{read} | wc -c"], shell=True, close_fds=False)
