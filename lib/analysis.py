'''this code currently only exists to log obedience simulator outputs
'''

class OSAnalysis:

    def __init__(self):
        self.name = 'Obedience Simulator Analysis'


    def log_outputs(self, outputs):
        with open('./output/output.txt', 'a') as logfile:
            for output in outputs:
                logfile.write('%s\n' % output)
        return

    def print_outputs(self, outputs):
        for output in outputs:
            print(output)
        return



