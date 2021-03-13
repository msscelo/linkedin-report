from classes.LinkedinReport import LinkedinReport
import os, sys

executionPath = os.path.realpath(os.path.dirname(os.path.realpath(__file__)))
if len(sys.argv) > 1 and sys.argv[1] != '':
    executionPath = os.path.realpath(os.path.dirname(os.path.realpath(__file__)))

linkedinReport = LinkedinReport(executionPath)
linkedinReport.start()
