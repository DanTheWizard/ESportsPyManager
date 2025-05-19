import subprocess
import hashlib

def get_machine_guid():
    """
    Returns the Machine GUID from the Windows registry.
    Stable unless the OS is reinstalled.
    """
    try:
        output = subprocess.check_output(
            ['reg', 'query', r'HKLM\SOFTWARE\Microsoft\Cryptography', '/v', 'MachineGuid'],
            text=True
        )
        for line in output.splitlines():
            if "MachineGuid" in line:
                return line.split()[-1]
    except subprocess.CalledProcessError:
        pass
    return "Unknown_GUID"

def get_system_uuid():
    """
    Returns the system UUID from the motherboard/firmware.
    Stable unless motherboard is changed.
    """
    try:
        # output = subprocess.check_output(['wmic', 'csproduct', 'get', 'UUID'], text=True)
        output = subprocess.check_output(["powershell", "-Command", "Get-CimInstance -Class Win32_ComputerSystemProduct | Select-Object -ExpandProperty UUID"], text=True)
        return output
    except subprocess.CalledProcessError:
        pass
    return "Unknown_UUID"

def get_volume_serial():
    """
    Returns the serial number of the C: drive volume.
    Changes if C: is reformatted.
    """
    try:
        output = subprocess.check_output('vol C:', shell=True, text=True)
        for line in output.splitlines():
            if "Serial Number" in line:
                return line.split("is")[-1].strip()
    except subprocess.CalledProcessError:
        pass
    return "Unknown_VOL"

def generate_device_fingerprint():
    """
    Combines stable identifiers to create an SHA-256 device fingerprint.
    Identifiers include Machine GUID, System UUID, and Volume Serial Number.
    """
    components = [
        get_machine_guid(),
        get_system_uuid(),
        get_volume_serial()
    ]
    raw_id = '-'.join(components)
    return hashlib.sha256(raw_id.encode()).hexdigest()

def get_fingerprint():
    """
    Gets the SHA-256 device fingerprint that is generated based on:
    Machine GUID, System UUID, and Volume Serial Number.
    """
    return generate_device_fingerprint()


def get_short_fingerprint():
    """
    Gets the last 10 digits of the SHA-256 device fingerprint that is generated based on:
    Machine GUID, System UUID, and Volume Serial Number.
    According to ChatGPT, in a place less than 500 devices, there is a chance of approximately
    1 in 17.6 million (0.0000057% chance of a collision) to have the same last 10 digits.
    """
    full_fingerprint = generate_device_fingerprint()
    alphanumerics = [char for char in full_fingerprint if char.isalnum()]
    return ''.join(alphanumerics[-10:])

if __name__ == "__main__":
    print("\nCollected Device Identifiers:")
    print("Machine GUID   :", get_machine_guid())
    print("System UUID    :", get_system_uuid())
    print("Volume Serial  :", get_volume_serial())
    print("\nGenerated Device Fingerprint (SHA-256):")
    print(get_fingerprint())
    print("\nShortened Device Fingerprint (SHA-256):")
    print(get_short_fingerprint())
