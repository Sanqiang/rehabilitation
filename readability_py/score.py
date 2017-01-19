from readability.feature import text
from math import sqrt
import urllib.request
from bs4 import BeautifulSoup


def flesch_reading_ease_score(txt):
    txt_model = text(txt)
    return 206.835-0.846*txt_model.wl()-1.015*txt_model.sl()

def flesch_kincaid_reading_grade_level(txt):
    txt_model = text(txt)
    return 0.39*txt_model.sl()+11.8*txt_model.spw()-15.59

def fog_index(txt):
    txt_model = text(txt)
    return 0.4*(txt_model.sl() + txt_model.lw())

def smog_rgl(txt):
    txt_model = text(txt)
    return 3+sqrt(txt_model.lw())

txt1 = ""
txt2 = ""
if False:
    txt1 = "Once upon a time there was an old woman who loved baking gingerbread. She would bake gingerbread cookies, cakes, houses and gingerbread people, all decorated with chocolate and peppermint, caramel candies and colored frosting."
    txt2 = "The aim of the study was to examine interactive relations of race and socioeconomic status (SES) to magnetic resonance imaging (MRI)-assessed global brain outcomes with previously demonstrated prognostic significance for stroke, dementia, and mortality."
else:
    url1 = "http://www.magickeys.com/BOOKS/GINGERBREAD/INDEX.HTML"
    url2 = "https://www.nih.gov/news-events/news-releases/new-method-performing-aortic-valve-replacement-proves-successful-high-risk-patients"
    with urllib.request.urlopen(url1) as response:
        html1 = response.read()
        obj1 = BeautifulSoup(html1, 'html.parser')
        txt1 = obj1.getText()
    with urllib.request.urlopen(url2) as response:
        html2 = response.read()
        txt2 = BeautifulSoup(html2, 'html.parser').getText()


print("flesch_reading_ease_score")
print(flesch_reading_ease_score(txt1))
print("\t")
print(flesch_reading_ease_score(txt2))
print("\n")

print("flesch_kincaid_reading_grade_level")
print(flesch_kincaid_reading_grade_level(txt1))
print("\t")
print(flesch_kincaid_reading_grade_level(txt2))
print("\n")

print("fog_index")
print(fog_index(txt1))
print("\t")
print(fog_index(txt2))
print("\n")

print("smog_rgl")
print(smog_rgl(txt1))
print("\t")
print(smog_rgl(txt2))
print("\n")
