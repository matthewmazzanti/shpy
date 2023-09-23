from sh import builder as b, run, run_json, ExecutableError, show

print("Simple command, capture output to a string:")
print(b.ls)

print("Command with flags")
print(b.ls("-la"))

print("Simple pipeline:")
print(b.ls("-la") | b.grep("sh"))

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
