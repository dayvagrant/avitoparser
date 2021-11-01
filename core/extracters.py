import re
import dateparser
from datetime import timedelta
from core.utils import update_params
from loguru import logger


def title_func(item_of_frame, debug):
    """Extract title name."""
    try:
        return item_of_frame.find(attrs={"data-marker": "item-title"}).get("title")
    except Exception as ex:
        if debug:
            logger.error(ex)
        return None


def priceCurrency_func(item_of_frame, debug):
    """Extract price currency."""
    try:
        return item_of_frame.find(attrs={"itemprop": "priceCurrency"}).get("content")
    except Exception as ex:
        if debug:
            logger.error(ex)
        return None


def price_func(item_of_frame, debug):
    """Extract price value."""
    try:
        return item_of_frame.find(attrs={"itemprop": "price"}).get("content")
    except Exception as ex:
        if debug:
            logger.error(ex)
        return None


def name_func(item_of_frame, debug):
    """Extract name of sale."""
    try:
        return item_of_frame.find(attrs={"itemprop": "name"}).get_text()
    except Exception as ex:
        if debug:
            logger.error(ex)
        return None


def item_specific_params_func(item_of_frame, debug):
    """Extract item specific params."""
    try:
        return item_of_frame.find(
            attrs={"data-marker": "item-specific-params"}
        ).get_text()
    except Exception as ex:
        if debug:
            logger.error(ex)
        return None


def text_func(item_of_frame, debug):
    """Extract text."""
    try:
        return (
            item_of_frame.find(
                "div", attrs={"class": re.compile("iva-item-descriptionStep")}
            )
            .find_next("div")
            .get_text()
        )
    except Exception as ex:
        if debug:
            logger.error(ex)
        return None


def city_func(item_of_frame, debug):
    """Extract city."""
    try:
        return (
            item_of_frame.find("div", attrs={"class": re.compile("geo-georeferences")})
            .find_next("span")
            .get_text()
        )
    except Exception as ex:
        try:
            return (
                item_of_frame.find("span", attrs={"class": re.compile("geo-address")})
                .find_next("span")
                .get_text()
            )
        except Exception as ex2:
            if debug:
                logger.error(ex, ex2)
                return None


def description_func(item_of_frame, debug):
    """Extract description_func of sale."""
    try:
        return item_of_frame.find("meta", attrs={"itemprop": "description"}).get(
            "content"
        )
    except Exception as ex:
        if debug:
            logger.error(ex)
        return None


def created_item_func(item_of_frame, debug):
    """Extract created date."""
    try:
        text_date = item_of_frame.find(
            "div", attrs={"data-marker": "item-date", "class": re.compile("date-text-")}
        ).text
        pyDate = dateparser.parse(text_date) + timedelta(hours=3)
        return pyDate.strftime("%Y/%m/%d, %H:%M")
    except Exception as ex:
        if debug:
            logger.error(ex)
        return None


def link_func(item_of_frame, debug):
    """Extract link."""
    try:
        return item_of_frame.find(
            "a", attrs={"class": re.compile("iva-item-sliderLink-")}
        ).get("href")
    except Exception as ex:
        if debug:
            logger.error(ex)
        return None


def user_func(item_of_frame, debug):
    """Extract user name."""
    try:
        return item_of_frame.find(
            "a", attrs={"data-marker": re.compile("item-link")}
        ).get_text()
    except Exception as ex:
        if debug:
            logger.error(ex)
        return None


def id_func(item_of_frame, debug):
    """Extract item id."""
    try:
        return item_of_frame.attrs.get("data-item-id", None)
    except Exception as ex:
        if debug:
            logger.error(ex)
        return None


def parse_items(item_of_frame, debug=False, **add_params):
    """Run all parse keys."""
    try:
        item_for_sold = dict(
            title=title_func(item_of_frame, debug),
            priceCurrency=priceCurrency_func(item_of_frame, debug),
            price=price_func(item_of_frame, debug),
            name=name_func(item_of_frame, debug),
            item_specific_params=item_specific_params_func(item_of_frame, debug),
            text=text_func(item_of_frame, debug),
            city=city_func(item_of_frame, debug),
            created_item=created_item_func(item_of_frame, debug),
            link=link_func(item_of_frame, debug),
            user=user_func(item_of_frame, debug),
            id=id_func(item_of_frame, debug),
        )
        if item_for_sold:
            result_dict = update_params(item_for_sold, add_params)
            return result_dict
    except Exception as ex:
        logger.error("have except")
        logger.error(ex)
        pass


def extract_data_from_page(
    html_soup,
    items_for_sold: list = list(),
    with_recomendations: bool = True,
    debug: bool = True,
):
    """Main extracter.
    Separate direct_search and recomendations results and extraxt keys thems.
    """
    direct_search_items, recomendations_items = None, None
    body_of_items = html_soup.find_all(
        "div", attrs={"class": re.compile("items-items-")}
    )
    for i in body_of_items:
        if i.attrs.get("data-marker", False) == "catalog-serp":
            direct_search_items = i.find_all("div", attrs={"data-marker": "item"})
        if not i.attrs.get("data-marker", False) == "catalog-serp":
            recomendations_items = i.find_all("div", attrs={"data-marker": "item"})
    if direct_search_items:
        # collect direct sold items
        for i in direct_search_items:
            item_for_sold = parse_items(i, debug, type_of_serach="direct_search")
            items_for_sold.append(item_for_sold)
    if not direct_search_items and not with_recomendations:
        pass
    if recomendations_items is not None and with_recomendations:
        # collect recomendations sold items
        for i in recomendations_items:
            item_for_sold = parse_items(i, debug, type_of_serach="recomendations")
            items_for_sold.append(item_for_sold)
    if items_for_sold:
        return items_for_sold
    else:
        logger.error(f"Can not find items")
        pass
