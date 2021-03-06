from operator import itemgetter
import math
import string

#import preprocessor as p
#import internet as i
from django.conf import settings
from googlesearch import search
import requests
import os
import PreprocessingComponent.views as p
from urllib.request import urlopen,Request
from bs4 import BeautifulSoup
from ScrapeSearchEngine.ScrapeSearchEngine import Google
from ScrapeSearchEngine.ScrapeSearchEngine import Duckduckgo
from ScrapeSearchEngine.ScrapeSearchEngine import Givewater
from ScrapeSearchEngine.ScrapeSearchEngine import Bing
from ScrapeSearchEngine.ScrapeSearchEngine import Yahoo
from ScrapeSearchEngine.ScrapeSearchEngine import Ecosia

userAgent = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
             ' Chrome/89.0.4389.114 Safari/537.36 Edg/89.0.774.68')
#search on google "my user agent"

#check a url can be doawnloaded as a file?
def is_downloadable(url):
    """
    Does the url contain a downloadable resource
    """
    h = requests.head(url, allow_redirects=True)
    header = h.headers
    content_type = header.get('content-type')
    if 'text' in content_type.lower():
        return False
    if 'html' in content_type.lower():
        return False
    return True
# search keyword from multiple search engine include
def search_keyword(search):
    list_url = []
    list_url.extend(Google(search, userAgent))
    list_url.extend(Bing(search, userAgent))
    list_url.extend( Yahoo(search, userAgent))
    list_url.extend(Duckduckgo(search, userAgent))
    list_url.extend(Givewater(search, userAgent))
    # list_url.extend (Ecosia(search, userAgent))
    return list(dict.fromkeys(list_url))

# download file downloadable such as: pdf, docx,...
def download_document(url):
    if (is_downloadable(url)):
        name = os.path.basename(url)
        r = requests.get(url, allow_redirects=True)
        open("file_downloaded\\" + name, 'wb').write(r.content)
        return "file_downloaded\\" + name

# crawl text from html website then preprocess and give output: list sentence after preprocessing.
def crawl_web(url):
    import platform
    import ssl

    # ...

    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    ssl_context.verify_mode = ssl.CERT_REQUIRED
    ssl_context.check_hostname = True
    ssl_context.load_default_certs()

    if platform.system().lower() == 'darwin':
        import certifi
        ssl_context.load_verify_locations(
            cafile=os.path.relpath(certifi.where()),
            capath=None,
            cadata=None)

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
             ' Chrome/89.0.4389.114 Safari/537.36 Edg/89.0.774.68'}
    req=Request(url,headers=headers)
    html = urlopen(req).read()
    soup = BeautifulSoup(html, features="html.parser", from_encoding="iso-8859-1")

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()  # rip it out
    # get text
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))

    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    temp = p.list_para2txt(text.split("\n"))
    res  = p.convert2listsentence(temp)
    return res #list sentence
# vncorenlp_file = 'D:\DH\TotNghiep\core\preprocessing\VnCoreNLP\VnCoreNLP-1.1.1.jar'
# from vncorenlp import VnCoreNLP
# vncorenlp = VnCoreNLP(vncorenlp_file)

def get_path():
    return os.getcwd()

# C??ch ch???y ch????ng tr??nh:
# S???a path c???a c??c file v?? th???c thi ch????ng tr??nh 

#DOC_FILE_PATH = 'baocao.docx'
STOPWORD_FILE_PATH = 'stopword.txt'
ALPHABET_FILE_PATH = 'alphabet.txt'


# Th???ng k?? t??? lo???i c???a m???t t???. Xem t??? ???? ????ng vai tr?? bao nhi??u t??? lo???i, m???i t??? lo???i bao nhi??u l???n.
# Input:
#    + word: t??? c???n th???ng k??
#    + vncorenlp_postag: postag c???a vncorenlp
# Output: list c??c tuple ???? s???p x???p gi???m d???n theo s??? l?????ng t??? lo???i
# V?? d???: [('V', 10), ('N', 6), ('Np', 2)]
def tag_statistic(word, vncorenlp_postag):
    word_tag_dict = {}

    for sen_lst in vncorenlp_postag:
        for w_tpl in sen_lst:
            w = w_tpl[0].lower()
            if word == w:
                if w_tpl[1] in word_tag_dict:
                    word_tag_dict[w_tpl[1]] += 1
                else:
                    word_tag_dict[w_tpl[1]] = 1

    return sorted(word_tag_dict.items(), key = itemgetter(1), reverse = True)


# T??m v??? tr?? c??u ch???a m???t t??? n??o ???? ???ng v???i tag (cho tr?????c) c???a t??? ???? trong c??u. 
# V?? d???: T??m c??c c??u ch???a t??? 'qu??n' c?? tag l?? 'Np'
# Input:
#    + word: t??? c???n th???ng k??
#    + tag: tag ???ng v???i word
#    + vncorenlp_postag: postag c???a vncorenlp
# Output: list v??? tr?? c???a c??c c??u th???a ??i???u ki???n (word, tag) trong vncorenlp_postag
def find_sentence_index(word, tag, vncorenlp_postag):
    index = []

    for i in range(len(vncorenlp_postag)):
        for w_tpl in vncorenlp_postag[i]:
            w = w_tpl[0].lower()
            if word == w and w_tpl[1] == tag[0][0]:
                index.append(i)
                break

    return index


# T??ch d??ng c???a text v?? l??u v??o m???ng
# Input: file .txt
# Output: danh s??ch c??c ph???n t??? (list)
def preprocess_text_file(txt_file):
    f = open(txt_file, 'r', encoding='utf-8')
    elements = f.readlines()
    for i in range(len(elements)):
        elements[i] = elements[i].replace('\n', '')
    f.close()

    return elements


# Ki???m tra trong 1 chu???i c?? h???p l??? ????? s??? d???ng cho thu???t to??n TF-IDF hay kh??ng?
# V?? d???:
#    + Chu???i h???p l???: Nguy???n_??nh, ?????ng_minh, l??nh_th???,...
#    + Chu???i kh??ng h???p l???: 1972, ??, ??(x),...
# Input: chu???i b???t k??? (string)
# Output: 
#    + True: h???p l???
#    + False: kh??ng h???p l???  
def check(string):
    result = True
    if len(string) == 1:
        result = False
    else:
        for char in string:
            if char not in alphabet:
                result = False
                break
            
    return result
    

# T??m t???t c??? t??? ph??n bi???t v?? ti???n x??? l?? c??c t???
# Input: list ???? t??ch t??? t??ch c??u c???a vncore, stop word
# Output:  
#    + Dictionary c???a t???t c??? t??? ph??n bi???t kh??ng bao g???m stop word, d???u c??u v???i 
#      key l?? t??? A, value l?? s??? l?????ng t??? A c?? trong v??n b???n (dict). VD: {h??i_h?????c: 3, 'B???o_?????i': 5} 
#    + T???ng s??? t??? c???a v??n b???n (int)
def total_words_and_len(vncorenlp_postag):
    words = dict()
    doc_len = 0

    for s in vncorenlp_postag:
        for w in s:
            w_temp = w[0].lower()
            doc_len += 1
            if w_temp not in stopwords and check(w_temp) == True:
                if w_temp in words:
                    words[w_temp] += 1
                else:
                    words[w_temp] = 1

    return words, doc_len


# ?????m s??? c??u ch???a t??? c???n check
# Input: t??? c???n check v?? list c??u c???a vncore
# Output: s??? c??u ch???a t??? c???n check (int)
def check_word_in_sent(word, vncorenlp_postag):
    count = 0
    for s in vncorenlp_postag:
        if word in s:
            count += 1

    return count


# L???y n gi?? tr??? cao nh???t s???p x???p theo th??? t??? gi???m d???n c???a m???t dictionary
# Input: Dictionary c?? ch???a gi?? tr??? ki???u s??? ????? c?? th??? so s??nh
# Output: n gi?? tr??? cao nh???t ???? ???????c s???p gi???m d???n
def get_top(dic, n):
    result = dict(sorted(dic.items(), key = itemgetter(1), reverse = True)[:n]) 
    return result


# T??nh gi?? tr??? TF c???a t???t c??? t???
# Input: Dictionary c???a t???t c??? c??c t??? ???? t??nh ??? h??m total_word_and_len v?? t???ng s??? t??? c???a v??n b???n (???? lo???i b??? stopword)
# Output: Gi?? tr??? TF c???a t???ng t??? (dict). VD: {h??i_h?????c: 0.4, 'B???o_?????i': 0.2} 
def TF(total_words_dict, doc_len):
    tf = dict()
    for key, val in total_words_dict.items():
        tf[key] = val / doc_len
    
    return tf


# T??nh gi?? tr??? IDF c???a t???t c??? t???
# Input: Dictionary c???a t???t c??? c??c t??? ???? t??nh ??? h??m total_word_and_len v?? list ???? t??ch t??? t??ch c??u c???a vncore
# Output: Gi?? tr??? IDF c???a t???ng t??? (dict). VD: {h??i_h?????c: 0.01297742362, 'B???o_?????i': 0.0643231124}
def IDF(total_words_dict, vncorenlp_postag):
    idf = dict()

    for key, val in total_words_dict.items():
        idf[key] = math.log(len(vncorenlp_postag) / (1 + check_word_in_sent(key, vncorenlp_postag)))

    return idf


# T??nh gi?? tr??? TF-IDF c???a t???t c??? t???
# Input: TF (dict) v?? IDF (dict)
# Output: gi?? tr??? TF-IDF (dict)
def TFIDF(tf, idf):
    tfidf = dict()
    tfidf = {key: tf[key] * idf.get(key, 0) for key in tf.keys()}

    return tfidf



# stopwords: Danh s??ch c??c stop word. VD: v??, l??, c??c, trong, ngo??i, c???a,........
# alphabet: c??c k?? t??? h???p l??? nh??: ??, ??, ??, b, j, ??, A, ??, Z, ...... v?? '_'
stopwords = preprocess_text_file(STOPWORD_FILE_PATH)
alphabet = preprocess_text_file(ALPHABET_FILE_PATH)


def get_link(postag, filename, sentences, numofwords):
    
    words, length = total_words_and_len(postag)

    tf = TF(words, length)
    idf = IDF(words, postag)
    tfidf = TFIDF(tf, idf)
    
    #N gi?? tr??? cao nh???t
    N = 20
    N_keywords = get_top(tfidf, N)
    print(N_keywords, '\n')

    kw_index = 0
    keyword_list = list(N_keywords.keys())
    testdata = tag_statistic(keyword_list[kw_index], postag)
    print(testdata)
    tag = tag_statistic(keyword_list[kw_index], postag)[0][0]

    sentences_index = find_sentence_index(keyword_list[kw_index], tag, postag)

    index = 0
    link = search_keyword(sentences[sentences_index[index]])

    return link

if __name__=='__main__':
    #list_link=p.preprocess_link('docFile_test/bacho.docx')
    a,b,c,d = p.preprocess_link('D:/example.docx')
    l = get_link(a, b, c,d)
    print(l)
