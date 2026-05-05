from pypdf import PdfReader


def extract_pages_from_pdf(pdf_path: str):
    """
    Extract text per page from a PDF.

    Returns:
        List of dicts: [{"page": int, "text": str}, ...]
    """
    reader = PdfReader(pdf_path)

    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text()

        if text:
            pages.append({
                "page": page_number,
                "text": text
            })

    return pages



