from docling.document_converter import DocumentConverter
import os

# Create a DocumentConverter object
dc = DocumentConverter()

# Source file path
source = os.path.join(os.path.dirname(__file__), 'assets', 'sample.pdf')

# Convert the source file to a text file
result = dc.convert(source)

# Print the result
print(result.document.export_to_markdown())
