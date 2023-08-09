# coding=utf8
# the above tag defines encoding for this document and is for Python 2.x compatibility

import re

regex = r"((^ \*.*?$))"


with open('encoder.c', 'r') as f:
    test_str = f.read()

matches = re.finditer(regex, test_str, re.MULTILINE)

for matchNum, match in enumerate(matches, start=1):
    
    for groupNum in range(0, len(match.groups())):
        groupNum = groupNum + 1
        
        print (match.group(groupNum)[2:])

# Note: for Python 2.7 compatibility, use ur"" to prefix the regex and u"" to prefix the test string and substitution.
