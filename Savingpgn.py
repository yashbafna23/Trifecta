import os
def backupTo(folder,text):
    ''' Saves the game into a pgn file in 'folder' folder.'''

    # Change currentdirectory to PGN folder
    os.chdir(folder)
    folder = os.path.abspath(folder)  # making sure folder is absolute
    print(folder)

    # Figure out the filename this code should use based on what files already exist.
    number = 1
    while True:
        txtFilename = os.path.basename(folder) + '_' + str(number) + '.pgn'
        if not os.path.exists(txtFilename):
            break
        number = number + 1

    #Writing the pgn
    fileptr = open(txtFilename,'w')
    fileptr.write(text)
    fileptr.close()


