from subprocess import Popen, PIPE


class CmdExecError(Exception):
    def __init__(self, message, errors):
        super().__init__(message)
        self.message = message
        self.errors = errors


def execCommand(cmd, args):
    process = Popen([cmd] + args, stdout=PIPE)
    (output, err) = process.communicate()
    exit_code = process.wait()
    if exit_code != 0:
        raise CmdExecError(
            "Something failed when calling ''" + cmd + " " + " ".join(args) + "'",
            (output, err, exit_code, cmd, args)
        )
    return output


class GfxController:
    def __init__(self):
        self.supportedModes = self.getSuportedModes()
    
    def getCurrentMode(self):
        result = execCommand("supergfxctl", ["-g"])
        mode = result.decode("utf-8").rstrip('\r\n').lower()
        return mode
        
    def getPendingModeChange(self):
        result = execCommand("supergfxctl", ["-P"])
        mode = result.decode("utf-8").rstrip('\r\n').lower()
        return mode
        
    def get_dGPUStatus(self):
        result = execCommand("supergfxctl", ["-S"])
        mode = result.decode("utf-8").rstrip('\r\n').lower()
        return mode

    def getSuportedModes(self):
        result = execCommand("supergfxctl", ["-s"])
        modes = result.decode("utf-8").rstrip('\r\n')
        modes = modes[1:-1]  # Remove '[' and ']'
        modes = modes.split(',')
        modes = [m.lower().strip(' ') for m in modes]
        return modes
    
    def getGPUVendor(self):
        result = execCommand("supergfxctl", ["-V"])
        vendor = result.decode("utf-8").rstrip('\r\n').upper()
        return vendor
    
    def setMode(self, mode):
        assert mode in self.supportedModes
        execCommand("supergfxctl", ["-m", mode])


class PowerProfileController:
    def __init__(self):
        self.availableProfiles = ['power-saver', 'balanced', 'performance']
    
    def getCurrentProfile(self):
        result = execCommand("powerprofilesctl", ["get"])
        mode = result.decode("utf-8").rstrip('\r\n').lower()
        return mode
    
    def setProfile(self, profile):
        assert profile in self.availableProfiles
        execCommand("powerprofilesctl", ["set", profile])


