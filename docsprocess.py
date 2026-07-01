from pypdf import PdfReader
reader = PdfReader("AIML SYLLABUS.PDF")
print(len(reader.pages))