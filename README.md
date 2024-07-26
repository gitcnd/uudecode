# uudecode  (a micropython uudecoder)

Takes input from python input() aka `<stdin>` and writes it out to the file named in the uudecode "begin" header.

## How to install

1. Grab the uudecode.py file
2. Upload uudecode.py to your / or /lib folder
3. To run it, simply `import uudecode` and paste in your uudecode data to write
\*. This works nicely with either serial input, web repl input, and/or my [telnetd](https://github.com/gitcnd/telnetd)

If you're low on space, you can use the `uudecode124.mpy` (the binary format for micropython version 1.24) file instead, as follows:

     import uudecode124
