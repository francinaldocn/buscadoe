"""Import modules."""
import os

from urllib import request

import pytesseract
import requests

from pdf2image import convert_from_path
from PIL import Image
from PyPDF2 import PdfFileReader
from PyPDF2 import PdfFileWriter
from bs4 import BeautifulSoup


def is_valid_url(url: str) -> bool:
    """
    Check if URL exists and return a boolean.

        Parameters:
            url (str): URL to check

        Return:
            boolean: True, if url exist. False if url doesn't exist
    """
    return requests.head(url).status_code == 200


def get_file_url(url: str, substring: str) -> str:
    """
    Find a full url that contains a specific substring.

    Args:
        url (str): URL to check
        substring (str): Substring to find

    Returns:
        str: full_url, if it contains the substring. None, if not contain.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    for link in soup.find_all('a'):
        full_url = str(link.get('href'))
        if substring in full_url:
            return full_url
    return None


def get_file(url: str, in_file: str) -> str:
    """
    Download a file and save in a specific path.

        Parameters:
            url (str): URL with the PDF file
            in_file (str): Input file path

        Return:
            in_file (str): Path to save the file

    """
    if not url:
        raise TypeError("URL not exist")

    request.urlretrieve(url, in_file)
    return in_file


def verify_if_pdf_is_text_or_image(temp_folder: str, in_file: str) -> bool:
    """
    Verify if PDF is text or image.

        Parametes:
            in_file (str): Source file name
        Return:
            True (bolean): if text
            False (bolean): if image
    """
    pdfReader = PdfFileReader(open(f"{temp_folder}/{in_file}.pdf", "rb"))
    page = pdfReader.getPage(0)
    text = page.extractText()

    if text == "":
        return False
    else:
        return True


def split_pdf(temp_folder: str, in_file: str) -> list:
    """
    Split PDF files in pages.

        Parametes:
            temp_folder (str): Path to the temp folder
            in_file (str): Source file name
        Return:
        list_of_files (list): List with the splitted files
    """
    input_file = PdfFileReader(open(in_file, "rb"))
    list_of_files = []

    for i in range(input_file.numPages):
        output = PdfFileWriter()
        output.addPage(input_file.getPage(i))
        with open(f"{temp_folder}/{i+1}.pdf", "wb") as output_stream:
            output.write(output_stream)
        list_of_files.append(i + 1)

    os.remove(in_file)

    return list_of_files


def convert_pdf_to_text(temp_folder: str, in_file: str) -> str:
    """
    Convert PDF to text and return text.

        Parameters:
            tmp_folder (st): Temporary folder do save parcial files
            in_file (str): PDF file path to be converted
        Return:
            text (str): Coverted text

    """
    pdfReader = PdfFileReader(open(f"{temp_folder}/{in_file}.pdf", "rb"))
    page = pdfReader.getPage(0)
    text = page.extractText()
    text = text.replace("-\n", "")

    os.remove(f"{temp_folder}/{in_file}.pdf")

    return text


def convert_pdf_to_image(tmp_folder: str, pdf_file: str, dpi: int = 150) -> None:
    """
    Convert PDF file to images.

        Parameters:
            tmp_folder (st): Temporary folder do save parcial files
            pdf_file (str): PDF file path to be converted
    """
    file = convert_from_path(f"{tmp_folder}/{pdf_file}.pdf", dpi=dpi)

    for i in range(len(file)):
        file[i].save(f"{tmp_folder}/{pdf_file}.jpg", "JPEG")

    os.remove(f"{tmp_folder}/{pdf_file}.pdf")


def convert_img_to_text(tmp_folder: str, img_file: str) -> str:
    """
    Convert Images to text and return text.

        Parameters:
            tmp_folder (st): Temporary folder do save parcial files
            img_file (str): Image file path to be converted
        Return:
            text (str): Coverted text

    """
    filename = f"{tmp_folder}/{img_file}.jpg"
    text = str(((pytesseract.image_to_string(
        Image.open(filename), config="-l por --oem 3 --psm 3"))))
    text = text.replace("-\n", "")
    os.remove(f"{tmp_folder}/{img_file}.jpg")

    return text


def search_in_text(text: str, terms: str, term_search: dict, page: str) -> str:
    """
    Search terms in text.

        Parameters:
            text (str): Text to search the terms
            terms (str): Terms to find
            term_search (dict): Empty dictionary to store search data
            page (str): File path
        Return:
            term_serach (dict): Return a dictionary with the terms found
    """
    lines = text.split("\n")

    for term in terms:
        term_count = 0

        for line in lines:
            if line.lower().find(term.lower()) != -1:
                term_count += 1

        if term_count > 0:
            term_search[term].append(page)

    return term_search


if __name__ == "__main__":
    pass
