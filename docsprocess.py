from pypdf import PdfReader
def loadpdf():
    reader = PdfReader("AIML SYLLABUS.PDF")
    print(f"Number of pages in pdf: {len(reader.pages)}")
    if len(reader.pages) > 0:
        page = reader.pages[0]
        text = page.extract_text()
        return text
    else: 
        print("pdf has no pages. Please try again!")
        return None
text = loadpdf()
print(text)