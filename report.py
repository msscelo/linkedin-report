from classes.LinkedinReport import LinkedinReport
import os, sys

execution_path = os.path.realpath(os.path.dirname(os.path.realpath(__file__)))
if len(sys.argv) > 1 and sys.argv[1] != '':
    execution_path = os.path.realpath(os.path.dirname(os.path.realpath(__file__)))

linkedinReport = LinkedinReport(execution_path)
linkedinReport.start()
