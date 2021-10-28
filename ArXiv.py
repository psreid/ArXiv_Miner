import Mine_Tool as Mtl


class ArxivPdf:

    def __init__(self, pdf_id):
        self.id = pdf_id
        self.mention = 0
        self.year = '00'
        self.month = '00'
        self.date = '0000'
        self.get_date_from_id()
        print('Loading ArXiv ID # ' + self.id)

    def get_date_from_id(self):
        # ArXiv uses set ID format with respect to date
        # Could be form ArXiv..../hepex/yymmxxxxx.pdf
        # or of form ArXiv ....../yymm.xxxxx.pdf
        self.date = self.id.replace("hep-ex/", "")
        self.year = (self.date[0] + self.date[1])
        self.month = (self.date[2] + self.date[3])

    def retrieve_full_info(self, wordlist=None, save_plaintext=False):
        # Entire ArXiv workflow is here,
        # Takes ArXiv address and returns a boolean if the word exists within the specific PDF
        # Best Practice is to use Mine.save_local_arxiv_library() and then probe plaintext
        Mtl.get_arxiv_pdf(pdf_id=self.id)
        pdf_text = Mtl.convert_pdf_query_to_text()
        if save_plaintext:
            self.save_arxiv_plaintext(pdf_text=pdf_text)
        self.mention = Mtl.pdf_contains_word(pdf_text, wordlist)
        return self.id, self.year, self.month, self.mention

    def save_arxiv_plaintext(self, pdf_text="None", path=''):
        # Simple write function to ArXiv ID file
        text_file = open(path + "ArXiv_plaintextArXiv_" + self.date + ".txt", "w")
        text_file.write("\n\n".join(pdf_text).lower())
        text_file.close()

    def search_plaintext(self, wordlist=None, path=''):
        # Finnicky naming system makes this method less reliable
        with open(path + "ArXiv_" + self.id + ".txt", "r") as f:
            lines = f.readlines()
            if len('\n'.join(lines)) < 50:
                print("Warning, " + self.id + " may not be an ArXiv Article (too small)")
            f.close()
        self. mention = Mtl.pdf_contains_word(lines, wordlist=wordlist)
        return self.id, self.year, self.month, self.mention




