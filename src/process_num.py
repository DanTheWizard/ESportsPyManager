import subprocess



# https://stackoverflow.com/a/29275361
def process_exists(process_name: str):
    call = 'TASKLIST', '/FI', 'imagename eq %s' % process_name
    # use buildin check_output right away
    output = subprocess.check_output(call, shell=True).decode()
    # check in the last line for process name
    last_line = output.strip().split('\r\n')[-1]
    # because Fail message could be translated
    return last_line.lower().startswith(process_name.lower())




def get_process_count(pname: str) -> int:
    call = 'TASKLIST', '/FI', f'imagename eq {pname}'
    output = subprocess.check_output(call, shell=True).decode()

    # Split the output into lines and remove the first two lines (headers)
    lines = output.strip().split('\n')[2:]  # Skip the first two lines

    # Count the number of lines that contain the process name
    count = sum(1 for line in lines if pname in line)

    return count



if __name__ == "__main__":
    #print("Hello, World!")
    print(get_process_count("cmd.exe"))
    print(process_exists("explorer.exe"))