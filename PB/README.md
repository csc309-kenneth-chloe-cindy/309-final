# Generating Documentation

1. Run `pip install -r requirements.txt`
2. Run `python3 manage.py generateschema --format openapi-json --file FILE_NAME`
3. Use [swdoc](https://www.swdoc.org/) to generate a PDF. Paste in the JSON contents from the file
   you created in the last step. Be sure to **check the OpenAPI 3.0 checkbox**!! Then press
   generate. Then press download.
4. Save the PDF into the **PB** directory as **docs.pdf**
