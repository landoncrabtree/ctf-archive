# nocaml

## Description

How to read files without the standard library? 🐪🤔

For weird infra reasons unrelated to actual solve, here's the gnarly command to test your solution:

`(base64 -w0 your-solution.ml; echo) | ncat --no-shutdown --ssl nocaml.chal.uiuc.tf 1337`

**author**: n8


## Files

* [nocaml.ml](files/nocaml.ml)

* [Dockerfile](files/Dockerfile)

* [nsjail.cfg](files/nsjail.cfg)

* [go.sh](files/go.sh)

