from sh import builder as b, run, run_json, ExecutableError, show

print("Simple command, capture output to a string:")
print(b.ls)
"""
LICENSE
README.md
__pycache__
sh.py
test.py
wip.py
"""

print("Command with flags")
print(b.ls("-la"))
"""
total 24
drwxr-xr-x 10 user user  320 Sep 23 16:19 .
drwxr-xr-x 19 user user  608 Sep 23 15:28 ..
drwxr-xr-x 13 user user  416 Sep 23 16:19 .git
-rw-r--r--  1 user user   22 Sep 23 16:15 .gitignore
-rw-r--r--  1 user user 1060 Sep 23 16:19 LICENSE
-rw-r--r--  1 user user   83 Sep 23 16:18 README.md
drwxr-xr-x  3 user user   96 Sep 23 16:13 __pycache__
-rw-r--r--  1 user user 1832 Sep 23 16:13 sh.py
-rw-r--r--  1 user user  921 Sep 23 16:15 test.py
-rw-r--r--  1 user user  485 Sep 23 15:31 wip.py
"""

print("Simple pipeline:")
print(b.ls("-la") | b.grep("sh"))
"""
-rw-r--r--  1 mmazzanti staff 1832 Sep 23 16:13 sh.py
"""

try:
    data = run_json(b.docker.image.ls("--all", "--format=json") | b.jq("-s"))
    print("Read output as json:")
    print(data[0]["Repository"])
except ExecutableError as e:
    print("You should install docker or jq!")

print()
print("Use files as input/output pipes")
with open("test.py") as i, open("output", "w") as o:
    run(i | b.grep("print") | o)
print("print" in str(b.cat("output")))
run(b.rm("output"))

# Also handles infinite reading
# with open("/dev/urandom") as i, open("output", "w") as o:
#     run(i | b.tr("-dc", "A-Z") | o)

try:
    run(b.foobar)
except ExecutableError as e:
    print()
    print("Get an error for missing executables")
    print(e)
