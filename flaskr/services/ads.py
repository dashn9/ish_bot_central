import random
from flask import current_app


class AdService:
    def __init__(self):
        pass

    def insert_monetag_ads_attribs_to_identity(self, identity: dict) -> dict:
        identity["PAGE_DEPTH"] = round(
            random.uniform(
                current_app.config["PAGE_DEPTH_RANGE"][0],
                current_app.config["PAGE_DEPTH_RANGE"][1],
            ),
            2,
        )

        # Determine probability of ad click
        prob_of_ad_click = round(
            random.uniform(
                current_app.config["AD_CLICK_PROBABILITY_RANGE"][0],
                current_app.config["AD_CLICK_PROBABILITY_RANGE"][1],
            ),
            2,
        )

        identity["ADS"] = {"click_probability": prob_of_ad_click}
        identity["ADS"]["provider"] = current_app.config["AD_PROVIDER"]

        if sum(current_app.config["AD_TYPES"].values()) != 1:
            raise ValueError("Sum of ad_type weights must be equals to 1")

        ad_type_to_pick_prob = random.random()
        ad_type_to_pick_prob_cumm = 0
        for ad_type in current_app.config["AD_TYPES"].items():
            ad_type_to_pick_prob_cumm += ad_type[1]
            if ad_type_to_pick_prob <= ad_type_to_pick_prob_cumm:
                identity["ADS"]["type"] = ad_type[0]
                break

        identity["ADS"]["keywords"] = current_app.config["AD_KEYWORDS"]
        if (
            identity.get("DEVICE_TYPE") == "is_smartphone"
            and current_app.config["AD_KEYWORDS_SMARTPHONE"]
        ):
            identity["keywords"] = current_app.config["AD_KEYWORDS_SMARTPHONE"]

        identity["ADS"]["keywords_click_probability"] = round(
            random.uniform(
                current_app.config["AD_KEYWORDS_CLICK_PROBABILITY_RANGE"][0],
                current_app.config["AD_KEYWORDS_CLICK_PROBABILITY_RANGE"][1],
            ),
            2,
        )
