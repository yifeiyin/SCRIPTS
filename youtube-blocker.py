#! /Library/Frameworks/Python.framework/Versions/3.7/bin/python3

HOST_PATH = '/etc/hosts'

if __name__ == '__main__':
    file_content = []
    mode = ""

    # Reading
    with open(HOST_PATH) as file_in:
        for line in file_in:
            file_content.append(line)

    # Modifying
    for index, line in enumerate(file_content):
        if "# YouTube" in line:
            if line.startswith('#'):
                mode = "YouTube Not Blocked"
                file_content[index] = line[1:].strip()
            else:
                mode = "YouTube Blocked"
                file_content[index] = '# ' + line
            break
    else:
        print("tag '# YouTube' not found.")
        raise SystemExit(1)

    # Writing
    with open(HOST_PATH, 'w') as file_out:
        for line in file_content:
            file_out.write(line)

    # Exiting
    if mode == "YouTube Blocked":
        print("YouTube Enabled.")
    else:
        print("YouTube Disabled.")

    import os
    print("Restarting Safari . . . ", end='')
    os.system("killall Safari; sleep 0.1; open -a Safari")
    print("Done.")
