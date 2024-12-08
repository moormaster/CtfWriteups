Title: Forensics / Scan Surprise
Date: 2024-12-07

We are presented a `challenge.zip` containing

    home/
        ctf-player/
            drop-in/
                flag.png

as well as a remote shell printing a qr code. The same QR code is also found in the `flag.png` inside of the `challenge.zip` and on the remote shell

    $ ls
    flag.png

To decode QR codes from an image we can use a command line tool like the [zbar bar code reader](https://zbar.sourceforge.net/). Fortunately this tool is already installed on the remote shell so we simply call it and get our flag

    $ zbarimg flag.png
    QR-Code:picoCTF{...}

