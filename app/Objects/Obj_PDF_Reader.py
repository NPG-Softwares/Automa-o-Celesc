import os
import re

import fitz


class PDFReader:
    def __init__(self, file: str | bytes, path: str = None) -> None:
        if isinstance(file, str):
            self.file = file
            self.path = path or os.getcwd()

        elif isinstance(file, bytes):
            self.file = file

    def read_pdf(self):
        if isinstance(self.file, str):
            self._pdf_obj = fitz.open(os.path.join(self.path, self.file))
        elif isinstance(self.file, bytes):
            self._pdf_obj = fitz.open('pdf', self.file)
        return self._pdf_obj

    def get_text(self, pdf: fitz.Document, page: int) -> str:
        return pdf.load_page(page).get_text().encode().decode()

    def find_element(self, line: str, element: str, index: int = -1,
                     sep: str = None, debug_line: bool = False,
                     regex: bool = None) -> str:
        if regex:
            result = re.findall(element, line)
            if len(result) > 0:
                return result

        if element in line:
            if debug_line:
                print(line)
                print(line.split(sep))

            found_element = line.split(sep)[index].strip()
            return found_element

    def get_pages(self) -> int:
        return range(self._pdf_obj.page_count)

    def close_pdf(self):
        self._pdf_obj.close()

    def extract_specific_pages(self, output_file, pages_to_extract):
        with fitz.open() as new_pdf:
            for page_number in pages_to_extract:
                self._pdf_obj.load_page(page_number)
                new_pdf.insert_pdf(self._pdf_obj,
                                   from_page=page_number,
                                   to_page=page_number)
            new_pdf.save(output_file)
