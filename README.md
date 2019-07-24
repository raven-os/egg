# Egg

The installer of Raven-OS

First you need to install Python development for the command msgfmt3

At the racine of the repository launch:
``` find ./locales -name "*.po" | while read f; do msgfmt3.py -o ${f%.po}.mo $f; done ``` 