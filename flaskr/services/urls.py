import json
import random


class UrlService:
    main_urls = []
    old_urls = []
    active_url_to_use = {
        "page_url": "",
        "page_content_element_type": "id",
        "page_content_element_name": "ouuzc",
        "related_articles_elements_type": "class",
        "related_articles_elements_name": "nav-links",
        "page_clicks": random.randint(3, 5),
        "vignette_close_ad_elements_type": "xpath",
        "vignette_close_ad_elements_name": "//iframe//span[text() = 'Close']",
        "vignette_open_ad_elements_type": "xpath",
        "vignette_open_ad_elements_name": "//iframe//span[count(ancestor::div) = 5]",
        "in_page_ad_link_elements_type": "xpath",
        "in_page_ad_link_elements_name": '//iframe//div[@style="display: flex !important;"]',
        "maximum_no_of_ads": 2,
        "proxy_domain_whitelists": [
            "whouseem.com",
            "gloaphoo.net",
            "dudialgator.com",
            "highrevenuegate.com",
            "bedrapiona.com",
            "fleraprt.com",
            "gggtrenks.com",
            "x2tsa.com",
            "poufaini.com",
            "maltrk.com",
            "trknex.com",
        ],
    }

    def __init__(self):
        with open("./flaskr/files/webpages_to_visit.json", "r") as f:
            urls_data = json.load(f)
            self.main_urls = urls_data["url_mains"]
            self.old_urls = urls_data["old_urls"]

    def fetch_random_url(self):
        link_pick_prob = random.random()
        link_pick_prob_cumm = 0
        if random.random() <= 0.7:
            for url in self.main_urls:
                link_pick_prob_cumm += url[1]
                if link_pick_prob <= link_pick_prob_cumm:
                    link_to_use = self.active_url_to_use.copy()
                    link_to_use["page_url"] = url[0]
                    return link_to_use
        else:
            link_to_use = self.active_url_to_use.copy()
            if random.random() <= 0.7:
                link_to_use["page_url"] = random.choice(
                    self.old_urls[: int(len(self.old_urls) // 2.5)]
                )
            else:
                link_to_use["page_url"] = random.choice(
                    self.old_urls[int(len(self.old_urls) // 2.5) :]
                )
            return link_to_use
