from comtypes.client import GetModule
from comtypes.client import CreateObject
import sys

# Run GetModule once to generate comtypes.gen.VisaComLib.
module = GetModule("C:\Program Files (x86)\IVI Foundation\VISA\VisaCom\GlobMgr.dll")
print("created module is: ", module)