from zipfile import ZipFile

if __name__ == '__main__':
    input_files = [
        '/home/jorgenr/entestfolder/uddata2/enfiles1.zip',
        '/home/jorgenr/entestfolder/zipmappe/minfil2.txt',
        '/home/jorgenr/entestfolder/uddata/enfiles.zip',
        '/home/jorgenr/entestfolder/zipmappe/minfil3.txt',
           ]
    with ZipFile('/home/jorgenr/entestfolder/uddata3/enfiles1.zip', mode='w') as zf:
        for f in input_files:
            zf.write(f)
            