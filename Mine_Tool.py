import urllib.request as libreq
import pandas as pd
import os
import pdftotext
import urllib.request


def get_arxiv_pdf(pdf_id, target='Target.pdf'):
    # Attempts to locate an ArXiv pdf with a specific id
    flag = 0
    while flag < 2:
        try:
            urllib.request.urlretrieve('https://export.arxiv.org/pdf/' + pdf_id + '.pdf', target)
            flag += 1
            return None
        except:
            print('ArXiv PDF not present at address')

            try:
                pdf_id.replace("hep-ex/", "")
                urllib.request.urlretrieve('https://export.arxiv.org/pdf/' + pdf_id + '.pdf', target)
                flag += 1
                return None
            except:
                print('still failed to find PDF with replaced hep-ex prefix')
                flag += 1


def convert_pdf_query_to_text(target='Target.pdf'):
    # Warning: Current version must be used directly after get_arxiv_pdf because requiring to save
    # PDF in order to get plaintext is awful badness.
    # Takes the saved PDF file and returns a plaintext string
    try:
        with open(target, "rb") as f:
            try:
                pdf = pdftotext.PDF(f)
                if os.path.exists(target):
                    os.remove(target)  # Remove PDF to sort any memory leakage
            except:
                pdf = 'nullpdf'
                print('PDF not found')
        return pdf
    except FileNotFoundError:
        return 'Dummy string'


def load_plaintext_file(target='Target.pdf'):
    try:
        with open(target, "rb") as f:

            pdf = f.read()

        return pdf
    except FileNotFoundError:
        return 'Dummy string'


def pdf_contains_word(pdf_text, wordlist, lower=True):

    # Boolean expression checking entire word list versus arXiv plaintext
    # First checks if you care about case sensitivity
    print(pdf_text)
    if lower:
        sentence = "\n\n".join(pdf_text).lower()
    else:
        sentence = "\n\n".join(pdf_text)
    # Returns if word exists within plaintext
    if any(word in sentence for word in wordlist):
        return 1
    else:
        return 0


def prep_plotting(target_pdf='arXiv_mention_boosteddecisiontree.csv'):
    #TODO this is just a notebook shortcut. Delete later
    df = pd.read_csv(target_pdf)
    df = df[['year', 'mention']]
    print(df)
    return df
