# python_002
Demo with zipFile

Create ZIP from zip-parts
```
    zipFile = "voc.zip"
    zips = glob.glob('vox.zip.*')
    for source in zips:
        with open(zipFile, "ab") as f:
            with open(source, "rb") as z:
                f.write(z.read())
```

Try to fix the resulting zip

```
   with open(zipFile, "r+b") as f:
        content = f.read()
        pos = content.rfind(b'\x50\x4b\x05\x06')
        if pos > 0:
            f.seek(pos + 20)
            f.truncate()
            f.write(b'\x00\x00')
```

And now do unzip

```
    with zipfile.ZipFile(zipFile) as zf:
        zf.extractall()
```

Error is thrown

```
    OSError: [Errno 22] Invalid argument
```