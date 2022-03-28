#!/usr/bin/python3

import os
import shutil
import subprocess
import sys
from zipfile import ZipFile


class FileSorter:

    def __init__(self, mappecounterstart, udFolder):
        self.mappecounter = mappecounterstart
        self.unZipMappeCount = 0
        self.udFolder = udFolder
        self.tempFolder = os.path.join(os.getcwd(), 'temp')

        # lav en ny ren temp mappe
        shutil.rmtree(self.tempFolder, ignore_errors=True)
        os.mkdir(self.tempFolder)
        # lav mappe struktur til sortering
        mkSortDirTree(self.udFolder)

    def naestefil(self) -> str:
        self.mappecounter += 1
        return f'{self.mappecounter}'

    def naesteUnzipMappe(self):
        self.unZipMappeCount += 1
        return os.path.join(self.tempFolder, f'Z{self.unZipMappeCount}')

    def sorter(self, minfil) -> None:

        if minfil[-4:] == '.txt':
            if minfil[-5:] == '8.txt':
                targetFolder = 'utf'
                targetFile = self.naestefil() + '8.txt'
            else:
                targetFolder = 'txt'
                targetFile = self.naestefil() + '.txt'

        elif minfil.endswith('.pdf'):
            targetFolder = 'pdf'
            targetFile = self.naestefil() + '.pdf'
        elif minfil.endswith('.mp3'):
            targetFolder = 'mp3'
            targetFile = self.naestefil() + '.mp3'
        else:
            targetFolder = 'andrefiler'
            targetFile = self.naestefil() + minfil[-4:]

        target = os.path.join(self.udFolder, targetFolder, targetFile)
        # print(f'kopierer {minfil} til {target}')
        shutil.copy(minfil, target)

    def myunzip(self, zipfil):
        print(f'{zipfil=}')
        unzipMappe = self.naesteUnzipMappe()
        if not os.path.isdir(unzipMappe):
            os.mkdir(unzipMappe)
        else:
            print(f'Advarsel dobbelt brug af unzipmappe: {unzipMappe}', file=sys.stderr)

        try:
            with ZipFile(zipfil, 'r') as zipObject:
                zipObject.extractall(unzipMappe)
        except NotImplementedError:
            # python own zipfile do not support all compression types, so we use an external unzipper for this one.
            status = subprocess.call(["unzip", f'{zipfil}', f'-d{unzipMappe}'])
            if status:
                print(f'Something went wrong with unzipping {zipfil}', file=sys.stderr)
        return unzipMappe

    def gennemGaaMappe(self, mappeNavn):
        for denneMappe, _, filnavne in os.walk(mappeNavn):
            # print(f'{denneMappe=}')
            for fil in filnavne:
                pFil = os.path.join(denneMappe, fil)
                # print(fil)
                if fil.endswith('.zip'):
                    tempZipMappe = self.myunzip(pFil)
                    self.gennemGaaMappe(tempZipMappe)
                    # tempZipMappen er nu gennegået og sorteret, så den kan fjernes igen.
                    shutil.rmtree(tempZipMappe)
                else:
                    self.sorter(pFil)


def mkSortDirTree(root):
    # create root folder
    os.makedirs(root, exist_ok=True)
    subdirs = ['utf', 'txt', 'pdf', 'mp3', 'andrefiler']
    for subdir in subdirs:
        os.makedirs(os.path.join(root, subdir), exist_ok=True)


if __name__ == '__main__':
    pwd = os.getcwd()
    datafolder = os.path.join(pwd, 'data')
    sortfolder = os.path.join(pwd, 'output')

    filesorter = FileSorter(100, sortfolder)
    filesorter.gennemGaaMappe(datafolder)
