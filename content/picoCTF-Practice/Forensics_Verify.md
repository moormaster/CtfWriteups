Title: Forensics / Verify
Date: 2024-12-07

After logging in to a remote shell we find a folder `files/` containing flags and fake flags and a script `./decrypt.sh` as well to check and decrypt those files.

If we run the script on one of those files we get an output telling us whether that file contains a `fake flag` or not:

    :::bash
    $ ./decrypt.sh files/0SgkM1fC 
    bad magic number
    Error: Failed to decrypt 'files/0SgkM1fC'. This flag is fake! Keep looking!

Now all we need to do is do some bash magic to run that script [for every](https://www.man7.org/linux/man-pages/man1/bash.1.html#SHELL_GRAMMAR) single file in the `files/` directory.

Typing a loop into the bash checks to call `./decrypt.sh` on each file will give us a longer output containing the flag somewhere in between:

    :::bash
    $ for f in files/*; do ./decrypt.sh "$f"; done
    bad magic number
    Error: Failed to decrypt 'files/0SgkM1fC'. This flag is fake! Keep looking!
    bad magic number
    Error: Failed to decrypt 'files/0aer7B0J'. This flag is fake! Keep looking!
    ...

To strip off all those outputs for the fake flag we use [grep --invert-match](https://man7.org/linux/man-pages/man1/grep.1.html) or its shorthand version `grep -v` to filter out all lines containing `flag is fake`

    :::bash
    $ for f in files/*; do ./decrypt.sh "$f"; done | grep -v 'flag is fake'
    bad magic number
    bad magic number
    ...

We still get `bad magic number` outputs written to stderr which we can get rid of by [redirecting](https://www.man7.org/linux/man-pages/man1/bash.1.html#REDIRECTION) stderr to `/dev/null`


    :::bash
    $ for f in files/*; do ./decrypt.sh "$f"; done 2> /dev/null | grep -v 'flag is fake'
    picoCTF{...}