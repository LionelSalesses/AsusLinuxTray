from subprocess import Popen, PIPE


class CmdExecError(Exception):
    def __init__(self, cmd, args, cmdExitCode, cmdStdOut, cmdStdErr):
        super().__init__()
        self.cmd = cmd
        self.args = args
        self.cmdExitCode = cmdExitCode
        self.cmdStdOut = cmdStdOut
        self.cmdStdErr = cmdStdErr
    
    def getMessage(self):
        msg = "<blockquote>"
        msg += "Command: '" + self.cmd + " " + " ".join(self.args) + "'"
        msg += "<br>"
        msg += "Exit code: " + str(self.cmdExitCode)
        msg += "<br>"
        if len(self.cmdStdOut) > 0:
            msg += "Output: " + self.cmdStdOut
            msg += "<br>"
        if len(self.cmdStdErr) > 0:
            msg += "Error: " + self.cmdStdErr
            msg += "<br>"
        msg += "</blockquote>"
        return msg


def execCommand(cmd, args):
    process = Popen([cmd] + args, stdout=PIPE, stderr=PIPE)
    (output, err) = process.communicate()
    exit_code = process.wait()
    if exit_code != 0:
        raise CmdExecError(
            cmd,
            args,
            exit_code,
            output.decode("utf-8").rstrip('\r\n'),
            err.decode("utf-8").rstrip('\r\n'), 
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
        self.availableProfiles = ['power-saver', 'balanced', 'performance']  # Currently hardcoded
    
    def getCurrentProfile(self):
        result = execCommand("powerprofilesctl", ["get"])
        mode = result.decode("utf-8").rstrip('\r\n').lower()
        return mode
    
    def setProfile(self, profile):
        assert profile in self.availableProfiles
        execCommand("powerprofilesctl", ["set", profile])


