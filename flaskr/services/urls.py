import random

from flask import current_app
from cachelib import SimpleCache


class UrlService:

    cache = SimpleCache(default_timeout=600)
    _db_client = None

    def __init__(self, db_client):
        self._db_client = db_client

    def get_url_data_to_use(self, site_data):
        links_data = site_data.get(
            "LINKS", {}
        )  # Extract LINKS data or default to empty dict

        return {
            "page_url": "",
            "page_content_element": links_data.get(
                "page_content_element", current_app.config["PAGE_CONTENT_ELEMENT"]
            ),
            "related_articles_elements": links_data.get(
                "related_articles_elements",
                current_app.config["RELATED_ARTICLES_ELEMENTS"],
            ),
            "page_clicks": random.randint(
                links_data.get(
                    "page_clicks_min", current_app.config["PAGE_CLICKS_MIN"]
                ),
                links_data.get(
                    "page_clicks_max", current_app.config["PAGE_CLICKS_MAX"]
                ),
            ),
            "vignette_close_ad_elements": links_data.get(
                "vignette_close_ad_elements",
                current_app.config["VIGNETTE_CLOSE_AD_ELEMENTS"],
            ),
            "vignette_open_ad_elements": links_data.get(
                "vignette_open_ad_elements",
                current_app.config["VIGNETTE_OPEN_AD_ELEMENTS"],
            ),
            "in_page_open_ad_link_elements": links_data.get(
                "in_page_open_ad_link_elements",
                current_app.config["IN_PAGE_OPEN_AD_LINK_ELEMENTS"],
            ),
            "maximum_no_of_ads": links_data.get(
                "maximum_no_of_ads", current_app.config["MAXIMUM_NO_OF_ADS"]
            ),
            "proxy_domain_whitelists": site_data.get(
                "proxy_domain_whitelists", current_app.config["PROXY_DOMAIN_WHITELISTS"]
            ),
        }

    def precompute__weights(self):
        """
        Computes weights for URLs considering their site’s weight.
        """
        documents = list(self._db_client.ad_sites.sites.find({}))
        weighted_urls = {}
        site_weights = []

        for doc in documents:
            site = doc["HOST"]
            site_weight = doc.get("WEIGHT", 1.0)
            site_urls = doc.get("URLS", [])

            total_url_weight = sum(url[1] for url in site_urls if len(url) == 2)

            if not (total_url_weight < 1.0):
                raise ValueError(
                    "Cummulative sum of url weight can't be greater than or equal to 1"
                )
            if len(site_urls) > 0:
                site_weights.append((site, site_weight, doc))
                equal_weight = (1.0 - total_url_weight) / len(
                    [url for url in site_urls if len(url) == 1]
                )
                site_urls = [
                    (url[0], url[1] if len(url) == 2 else equal_weight)
                    for url in site_urls
                ]

                weighted_urls[site] = [(url, weight) for url, weight in site_urls]

        total_weight = sum(weight for _, weight, _ in site_weights)
        site_weights = [
            (site, (weight / total_weight), site_data)
            for site, weight, site_data in site_weights
        ]
        return weighted_urls, site_weights

    def get_weighted_data(self, use_cache=True):
        """
        Gets the weighted data from the specified collection, using cache if specified.
        """
        urls_key = "urls"
        sites_key = "sites"
        urls, sites = self.cache.get(urls_key), self.cache.get(sites_key)

        if use_cache and sites and urls:
            return urls, sites

        urls, sites = self.precompute__weights()

        if use_cache:
            self.cache.set(sites_key, sites)
            self.cache.set(urls_key, urls)

        return urls, sites

    def pick_weighted_item(self, weighted_items):
        """
        Randomly selects an item based on its weight.
        """
        random_pick = random.random()
        current = 0
        for item, weight in weighted_items:
            current += weight
            if current >= random_pick:
                return item
        return None

    def get_weighted_url(self):
        """
        Endpoint to get a URL, with optional caching.
        """

        url_weights, site_weights = self.get_weighted_data(True)
        site = self.pick_weighted_item(site_weights)

        if not site:
            return "No site available"

        urls_for_site = [(url, weight) for url, weight in url_weights[site]]
        return self.pick_weighted_item(urls_for_site), site[2]

    def fetch_random_url(self):
        link_to_use, site_data = self.get_weighted_url()
        link_data_to_use = self.get_url_data_to_use(site_data)
        link_data_to_use["page_url"] = link_to_use
        return link_to_use
