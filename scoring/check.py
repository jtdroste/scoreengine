import subprocess

"""
Check Thread Object

    - responsible for calling the bash script, and reporting back to the
team thread
"""
class Check(object):
    
    def __init__(self, master, teamid, serviceid, name, script, args):
        self.master = master
        self.teamid = teamid
        self.serviceid = serviceid
        self.servicename = name
        self.script = script
        self.args = args
    
    def main(self, addScore=True, addLog=True):
        desc_start = "Starting check %s for %d" % (self.servicename, self.teamid)
        desc_end = "Finished check %s for %d" % (self.servicename, self.teamid)
        
        if addLog == True:
            self.master.log("Check", desc_start)
        
        script = ["/bin/bash", self.script] + self.args

        proc = subprocess.Popen(script, executable="/bin/bash", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (output, stderr) = proc.communicate()

        status = proc.returncode

        if addLog == True:
            self.master.addScore(self.teamid, self.serviceid, status, output)
        
        if addScore == True:
            self.master.log("Check", desc_end)
        else:
            return (status, output)