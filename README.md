# Egg

The intaller of Raven-OS	The installer of Raven-OS

First you need to install gettext for the command msgfmt

## Dependencies

Install the package `gettext` to use the command `msgfmt`. Depending on your distribution, it may be called `msgfmt`, `msgfmt3` or `msgfmt3.py`.

```bash
find ./locales -name "*.po" | while read f; do msgfmt -o ${f%.po}.mo $f; done
``` 
You may need to adapt this command depending on the alternative name `msgfmt` might have on your system.

## Running the intaller

To run Egg, type 
```bash
python3 ./egg.py
```
Note that only the root user is able to use Egg.
