import pandas as pd
import Mine_Tool as Mtl
import ArXiv as ArX
from os import listdir
from os.path import isfile, join


class Mine:
    # Mine is the Overarching container for all the ArXiv PDF ID's, Potential words that need queried,
    # and high level search/API query commands to be conducted from the lower ArXivPDF class
    def __init__(self, id_list=None, wordlist=None):
        self.mine_data = pd.DataFrame(columns=['id', 'year', 'month', 'mention'])
        self.id_list = id_list
        self.wordlist = wordlist
        self.temp_row = pd.DataFrame(columns=['id', 'year', 'month', 'mention'])
        if self.wordlist is None:
            print('Warning: you are attempting build a arXiv word searcher without search words!')
        assert self.id_list is not None, 'Empty arXiv IDs, id_list must not be None'

    def save_local_arxiv_lib(self, path=''):
        # If we want to download the library separate from analysis
        for index, ids in enumerate(self.id_list):
            pdf = ArX.ArxivPdf(pdf_id=ids[0])
            Mtl.get_arxiv_pdf(pdf_id=ids[0], target='TMP_ARXIV_SAVE_FILE.PDF')
            pdf.save_arxiv_plaintext(pdf_text=Mtl.convert_pdf_query_to_text(target='TMP_ARXIV_SAVE_FILE.PDF'), path=path)
        return None

    def query_local_arxiv_lib(self, to_csv=True, path=''):
        for index, ids in enumerate(self.id_list):
            pdf = ArX.ArxivPdf(pdf_id=ids[0])

            # search_plaintext returns 4 parameters
            temp_id, temp_year, temp_month, temp_mention = pdf.search_plaintext(wordlist=self.wordlist, path='')
            temp_data = {'id': [temp_id], 'year': [temp_year], 'month': [temp_month], 'mention': [temp_mention]}
            self.temp_row = pd.DataFrame(data=temp_data,
                                        columns=['id', 'year', 'month', 'mention'])
            self.mine_data.loc[index] = temp_id, temp_year, temp_month, temp_mention

            # Save the data every attempt
            if to_csv:
                self.temp_row.to_csv('arXiv_mention_' + self.wordlist[0] + '.csv', mode='a', header=False)

        if to_csv:
            self.mine_data.to_csv('arXiv_mention_' + self.wordlist[0] + 'full.csv', mode='a')

        return None

    def compile_remote_arxiv_lib(self, to_csv=True, save_plaintext=False):
        # Full workflow, iterates over all pdfs on remote arXiv server without saving locally,
        # retrieves plaintext and determines if specified words in the wordlist are within the plaintext
        # Not recommended to use this function alone. Best practice is:
        # save_local_arxiv_lib --> query_local_arxiv_lib

        for index, ids in enumerate(self.id_list):
            pdf = ArX.ArxivPdf(pdf_id=ids[0])

            # Retrieve_info returns 4 parameters
            temp_id, temp_year, temp_month, temp_mention = pdf.retrieve_full_info(wordlist=self.wordlist, save_plaintext=save_plaintext)
            temp_data = {'id': [temp_id], 'year': [temp_year], 'month': [temp_month], 'mention': [temp_mention]}
            self.temp_row = pd.DataFrame(data=temp_data,
                                        columns=['id', 'year', 'month', 'mention'])
            self.mine_data.loc[index] = temp_id, temp_year, temp_month, temp_mention


            # Save the data every attempt
            if to_csv:
                self.temp_row.to_csv('arXiv_mention_' + self.wordlist[0] + '.csv', mode='a', header=False)

        if to_csv:
            self.mine_data.to_csv('arXiv_mention_' + self.wordlist[0] + 'full.csv', mode='a')

    def load_mine_from_dir(self, path=''):
        # Generates a mine from a directory consisting of nothing but plaintext folders.
        files = [f for f in listdir(path) if isfile(join(path, f))]
        for file in files:
            return


def clean_empty_files(path=''):
    # a second pass checking saved files for "nullpdf".
    # FIXME clean this. There are a ton of redundancies so that it works.
    files = [f for f in listdir(path) if isfile(join(path, f))]
    for file in files:
        print(join(path, file))
        print(Mtl.load_plaintext_file(target=str(join(path, file))))
        #flag = Mtl.pdf_contains_word(pdf_text=str(Mtl.load_plaintext_file(target=join(path, file))),
        #                             wordlist=str('b' + 'n\nu\nl\nl\np\nd\nf'))
        flag = Mtl.load_plaintext_file(target=str(join(path, file)))
        print(len(flag))
        if len(str(flag)) < 50:
            print("File contains" + str(Mtl.load_plaintext_file(join(path, file))))
            dummy_flag = str(Mtl.load_plaintext_file(join(path, file)))
            if dummy_flag != 'Dummy string':
                # Now test both ArXiv URL formats
                file_id = file.replace("ArXiv_plaintextArXiv_", "hep-ex/")
                file_id = file_id.replace(".txt", "")
                Mtl.get_arxiv_pdf(pdf_id=file_id)
                pdf_text = Mtl.convert_pdf_query_to_text()
                file_arx = ArX.ArxivPdf(pdf_id=file_id)
                file_arx.save_arxiv_plaintext(pdf_text=pdf_text)
            else:
                print("File contains Dummy string")
        else:
            print("Filename" + file + "is not empty")



