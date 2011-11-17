import os, sys
from launchpadlib.launchpad import Launchpad

def fetchtask():
    try:
        launchpad = Launchpad.login_anonymously(os.path.basename(sys.argv[0]), 'production')
        ius = launchpad.projects.search(text='ius')[0]
    except:
        print 'Failed to make connection'
    else:
        task = ius.searchTasks()
        return task
