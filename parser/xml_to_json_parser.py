from bs4 import BeautifulSoup
import requests
import json


class XmlToJsonParser:
    """
        Main class responsible to parse the given XML to JSON.
    """

    def __init__(self, url):
        self.url = url

        self.json = {"feed": []}

        self.main_parser()

    def api_call(self) -> requests.request:
        call = requests.get(self.url)
        return call

    def xml_content_parser(self):
        return BeautifulSoup(self.api_call().content, "html5lib")
    def as_json(self):
        return json.dumps(self.json)

    def as_dict(self):
        return self.json

    def serialize_inner_description_item(self, type: str, content) -> dict:
        return {"type": type, "content": content}

    def remove_ctags(self, text: str) -> str:
        if text[:9] == "<![CDATA[" and text[:3] == "<![":
            return text[9:-3]
        else:
            return text

    def main_parser(self):
        content = self.xml_content_parser()

        xml_itens = content.find_all("item")

        for xml_item in xml_itens:
            main_json = {"title": "", "link": "", "description": []}

            main_json["title"] = self.remove_ctags(text=xml_item.title.get_text())
            main_json["link"] = xml_item.contents[-5].rstrip()

            description_tags = xml_item.description

            for tag in description_tags:

                if tag.name == "p":
                    try:
                        p_text = tag.text
                        if p_text and p_text != "\n\t\xa0":
                            main_json["description"].append(
                                self.serialize_inner_description_item(
                                    type="text", content=p_text.replace("\n\t", "")
                                )
                            )
                    except:
                        continue

                elif (
                    tag.name == "div"
                ):  # Mind div elements could contains either image or links

                    images = tag.find("img")
                    html_list_itens = tag.find_all("li")

                    if images:
                        if hasattr(images, "attrs"):
                            main_json["description"].append(
                                self.serialize_inner_description_item(
                                    type="image", content=images.attrs.get("src", None),
                                )
                            )

                    if html_list_itens:

                        list_with_links_href = []

                        for li_element in html_list_itens:
                            if hasattr(li_element, "a") and hasattr(
                                li_element.a, "attrs"
                            ):
                                list_with_links_href.append(
                                    li_element.a.attrs.get("href", None)
                                )
                        main_json["description"].append(
                            self.serialize_inner_description_item(
                                type="links", content=list_with_links_href
                            )
                        )

            self.json["feed"].append({"item": main_json})