# This should be the main file to run the program
import test

TestBool = False

MakeAllAnthsBool = False
DownloadAllAnthsBool = False

if not TestBool:
    from app import main
    main.app.display()
else:
    if MakeAllAnthsBool:
        test.makeAllAnths()
    if DownloadAllAnthsBool:
        test.downloadAllAnths()
