# Egg

The installer of Raven-OS

First you need to install gettext for the command msgfmt3.py

At the root of the repository, run:
``` find ./locales -name "*.po" | while read f; do msgfmt3.py -o ${f%.po}.mo $f; done ``` 