# Rebug 1

## Description

Can't seem to print out the flag :( 
Can you figure out how to get the flag with this binary?

Author: `Mahmoud Shabana`

## Files

* [test.out](files/test.out)

## Solution

Taking a look in Ghidra and doing some basic cleanup:

![main](https://i.imgur.com/2OcHw5q.png)

The only condition for "that's correct" is for the length of the user-supplied input to be 12. All we need to do to get the flag is provide a 12 character string.

`csawctf{c20ad4d76fe97759aa27a0c99bff6710}`

