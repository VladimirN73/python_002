#
# validate.py
#
import os
import glob
import zipfile


def unzip_file():
    #
    zipFile = "voc.zip"
    zips = glob.glob('vox.zip.*')
    for source in zips:
        with open(zipFile, "ab") as f:
            with open(source, "rb") as z:
                f.write(z.read())

    # this fix is not needed on Windows and it does not work on unix ...
    fix_zip(zipFile)

    with zipfile.ZipFile(zipFile) as zf:
        zf.extractall()


def fix_zip(zipFile):
    # HACK:
    #   see http://bugs.python.org/issue10694
    #   see https://stackoverflow.com/questions/3083235/unzipping-file-results-in-badzipfile-file-is-not-a-zip-file
    # The zip file generated is correct, but because of extra data after the 'central directory' section,
    # Some version of python (and some zip applications) can't read the file. By removing the extra data,
    # we ensure that all applications can read the zip without issue.
    # The ZIP format: http://www.pkware.com/documents/APPNOTE/APPNOTE-6.3.0.TXT
    # Finding the end of the central directory:
    #   http://stackoverflow.com/questions/8593904/how-to-find-the-position-of-central-directory-in-a-zip-file
    #   http://stackoverflow.com/questions/20276105/why-cant-python-execute-a-zip-archive-passed-via-stdin
    # This second link is only loosely related, but echos the first,
    # "processing a ZIP archive often requires backwards seeking"

    with open(zipFile, "r+b") as f:
        content = f.read()
        # reverse find: this string of bytes is the end of the zip's central directory.
        pos = content.rfind(b'\x50\x4b\x05\x06')
        if pos > 0:
            f.seek(pos + 20)
            f.truncate()
            f.write(b'\x00\x00')  # Zip file comment length: 0 byte length; tell zip applications to stop reading.


def delete_file(filename):
    file_target = filename
    flag = os.path.isfile(file_target)
    if flag:
        os.remove(file_target)


def splitt_file(filename, chunk_size):
    file_number = 1
    with open(filename, 'rb') as f:
        chunk = f.read(chunk_size)
        while chunk:
            with open(filename + '.' + str(file_number), 'wb') as chunk_file:
                chunk_file.write(chunk)
            file_number += 1
            chunk = f.read(chunk_size)


def merge_files(pattern, target):
    files = glob.glob(pattern)
    with open(target, 'ab') as outfile:
        for file in files:
            with open(file, 'rb') as f:
                outfile.write(f.read())

def run():
    #delete_file('voc.pth')
    #delete_file('voc.zip')
    #unzip_file()
    splitt_file('voc.pth', 50_000_000)
    #merge_files('voc.pth.*', 'voc.out')

if __name__ == '__main__':
    run()

