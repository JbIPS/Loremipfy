Loremipfy
=========

Transform localisation files in various way

How-To
------
```
usage: loremipfy.py [-h] [-l LOREM_OUTPUT] [-e EXCEL_OUTPUT] [-t TEMPLATE]
                    [--lang LANGUAGE]
                    input_file

Transform a localisation file

positional arguments:
  input_file            input file to transform

optional arguments:
  -h, --help            show this help message and exit
  -l LOREM_OUTPUT, --lorem LOREM_OUTPUT
                        Replace all the content by a Lorem Ipsum extract
  -e EXCEL_OUTPUT, --excel EXCEL_OUTPUT
                        Convert the XML location file into an MS Excel file
  -t TEMPLATE, --template TEMPLATE
                        Excel Template for Excel export
  --lang LANGUAGE       Language location will be translated to
```

Current transformations
-----------------------
* Loremipfy: Replace all localisation values with Lorem Ipsum extracts
* Excelify: Transform the localisation file to a valid MS Excel file 
* Automatic translation with Google Traduction

TODO
----
* Xmlify: Transform the localisation file to XML format
* Xliffy: Transform the localisation file to XLiff format


