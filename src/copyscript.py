"""
brute force script to copy files from s3 requester pays buckets as fast as
possible, given that some high level s3 features lack requester pays
functionality, requiring use of s3api, which has no bulk features
"""

from subprocess import run

#get a list of all files
string = "aws s3 ls s3://arxiv/pdf --request-payer requester --human-readable --recursive"
a = run(string.split(), capture_output=True)
lister = a.stdout.splitlines()

#prep the next command
for i in range(len(lister)):
    lister[i] = "pdf"+ lister[i].split(b"pdf", 1)[1].decode("utf-8")

for i in range(len(lister)):
    line = lister[i]
    if ((line[-9] == "1") or (line[-9] == "2")): #seperated based on a particular id digit to divide up the set
        #copy each object
        copycmd = "aws s3api copy-object --copy-source arxiv/" + line + " --request-payer requester --key " + line[4:] + " --bucket tarlake"
        splitliner = copycmd.split()
        b = run(splitliner)
