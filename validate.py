#
# validate.py
#
import os
import glob
import zipfile


def create_weights():
    #
    zips = glob.glob('vox.zip.*')
    zipFile = os.path.relpath("voc.zip")
    for zipName in zips:
        source = zipName
        with open(zipFile, "ab") as f:
            with open(source, "rb") as z:
                f.write(z.read())

    with open(zipFile, "rb") as f:
        print("OK")

    # this fix is not needed on Windows and does not work on unix ...
    fix_zip(zipFile)
    # fix_zip_2(zipFile)

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
    # This second link is only losely related, but echos the first,
    # "processing a ZIP archive often requires backwards seeking"

    with open(zipFile, "r+b") as f:
        content = f.read()
        # reverse find: this string of bytes is the end of the zip's central directory.
        pos = content.rfind(b'\x50\x4b\x05\x06')
        if pos > 0:
            f.seek(pos + 20)  # +20: see secion V.I in 'ZIP format' link above.
            f.truncate()
            f.write(b'\x00\x00')  # Zip file comment length: 0 byte length; tell zip applications to stop reading.


def fix_zip_2(zipFile):
    with open(zipFile, "r+b") as f:
        content = f.read()
        pos = content.rfind(b'\x50\x4b\x05\x06')
        if pos > 0:
            f.seek(pos + 22)
            f.truncate()


def fix_zip_show_checkpoints(zipFile):
    # https://python-list.python.narkive.com/BkZgCEiq/badzipfile-file-is-not-a-zip-file
    # import sys
    points = [
        # ("FileHeader", b'\x03\x04'),  # magic number for file header
        # ("DataDescriptor", b'\x07\x08'),  # see PKZIP APPNOTE (V) (C)
        # ("CentralDir", b'\x01\x02'),  # magic number for central  directory
        # ("EndArchive", b'\x05\x06'),  # magic number for end of archive record
        # ("EndArchive64", b'\x06\x06'),  # magic token for Zip64 header
        # ("EndArchive64Locator", b'\x06\x07'),  # magic token for locator header
        # ("ArchiveExtraData", b'PK\x06\x08'),  # APPNOTE (V) (E)
        # ("DigitalSignature", b'\x05\x05'),  # APPNOTE (V) (F)
        ("End of CentralDir", b'\x50\x4b\x05\x06')
    ]
    with open(zipFile, "rb") as f:
        buff = f.read()
        f.close()
        blen = len(buff)
        print("archive size is", blen)
        for point_name, point_value in points:
            print("search for", point_name, point_value)
            pos = 0
            while pos < blen:
                pos = buff.find(point_value, pos)
                if pos < 0:
                    break
                print("%s at %d" % (point_name, pos))
                pos += 4


def run():
    #
    file_target = 'voc.pth'
    flag = os.path.isfile(file_target)
    if flag:
        os.remove(file_target)

    file_zip = 'voc.zip'
    flag = os.path.isfile(file_zip)
    if flag:
        os.remove(file_zip)

    create_weights()


if __name__ == '__main__':
    run()
