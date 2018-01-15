import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup 

myUrl = "https://www.webopedia.com/Top_Category.asp"
page_html = uReq(myUrl).read()
uReq(myUrl).close()

parsedPage = soup(page_html,"html.parser")
categories = parsedPage.findAll("div",{"class":"bullet_list"})

file = "terms.csv"
f = open(file, "w")

headers = "main_category_id, main_category_name, subCategory_id, subCategory_name, term_id, term_name, term_difinition\n"
f.write(headers)

for index, category in enumerate(categories):
    main_category_id = index
    main_category_name = str(category.div.span.a["href"])
    subCategories1 = category.findAll("li",{"class":"listing-item"})
    subCategories2 = category.findAll("li",{"class":"listing-item-hidden"})
    subCategories = subCategories1 + subCategories2
    for indx , subCategory in enumerate(subCategories):
        subCategory_id = indx
        subCategory_name = 	str(subCategory.a.text)
        sublink = str(subCategory.a["href"])
        link = "https://www.webopedia.com" + sublink
        terms_html = uReq(link).read()
        uReq(link).close()
        parsedTermsPage = soup(terms_html, "html.parser")
        terms1 = parsedTermsPage.findAll("li", {"class":"col-1-item"})
        terms2 = parsedTermsPage.findAll("li", {"class":"col-2-item"})
        terms = terms1 + terms2
        for inx, term in enumerate(terms):
            term_id = inx
            term_name = str(term.text)
            definistionSubUrl = str(term.a["href"])
            definistionUrl = "https://www.webopedia.com" + definistionSubUrl
            difinition_html = uReq(definistionUrl).read()
            uReq(definistionUrl).close()
            parsedDifinition = soup(difinition_html,"html.parser")
            difinition = parsedDifinition.find("div",{"class":"article_related_items"})
            textReq = ""
            for tag in difinition.next_siblings:
                if tag.name == "p":
                	break
                else:
                	textReq = textReq + str(tag)
            if str(textReq).isspace():
            	textReq = str(parsedDifinition.find("p"))
            beautifulText = str(soup(textReq, "html.parser").get_text())
            withoutCommas = beautifulText.replace(r","," ")
            elemnts = withoutCommas.splitlines()
            withoutSpaces = ""
            for elemnt in elemnts:
                if elemnt != "":
                    withoutSpaces = withoutSpaces + elemnt
            term_difinition = withoutSpaces.lstrip()
            # print ("main_category_id", main_category_id)
            # 	print ("main_category_name", main_category_name)
            # 	print ("subCategory_id", subCategory_id)
            # 	print ("term_id", term_id)
            # 	print ("subCategory_name", subCategory_name)
            # 	print ("term_name", term_name)
            # print ("term_difinition: ", term_difinition )
            f.write(str(main_category_id) + "," + main_category_name + "," + str(subCategory_id) + "," +subCategory_name + "," + str(term_id) + "," + term_name + "," + term_difinition + "\n")
f.close()

