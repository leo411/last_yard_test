import argparse
import json
from collections import namedtuple

PreferenceMatch = namedtuple("PreferenceMatch", ["product_name", "product_codes"])

def update_dict_key(old_key, new_key, products):
    for product in products:
        if new_key not in product:
           product[new_key] = product.pop(old_key)

def remove_dict_key(key, products):
    for product in products:
        product.pop(key)

def main(product_data, include_tags, exclude_tags):
    """The implementation of the pipeline test."""
    include_tags_products = []
    for product in product_data:
        for tag in args.include:
            if product['tags'].count(tag) > 0:
                include_tags_products.append(product)
    
    unique_include_tags_products= []

    for product in include_tags_products:
        if product not in unique_include_tags_products:
            unique_include_tags_products.append(product)
    
    for product in unique_include_tags_products:
       for tag in args.exclude:
           if tag in product['tags']:
              unique_include_tags_products.remove(product)
    
    update_dict_key('name', 'product_name', unique_include_tags_products)
    update_dict_key('code', 'product_codes', unique_include_tags_products)
    remove_dict_key('tags', unique_include_tags_products)
    
    preference_match_list = [PreferenceMatch(**product) for product in unique_include_tags_products]
    return preference_match_list

if __name__ == "__main__":

    def parse_tags(tags):
        return [tag for tag in tags.split(",") if tag]

    parser = argparse.ArgumentParser(
        description="Extracts unique product names matching given tags."
    )
    parser.add_argument(
        "product_data",
        help="a JSON file containing tagged product data",
    )
    parser.add_argument(
        "--include",
        type=parse_tags,
        help="a comma-separated list of tags whose products should be included",
        default="",
    )
    parser.add_argument(
        "--exclude",
        type=parse_tags,
        help="a comma-separated list of tags whose matching products should be excluded",
        default="",
    )

    args = parser.parse_args()

    with open(args.product_data) as f:
        product_data = json.load(f)
    
    order_items = main(product_data, args.include, args.exclude)
    print("order_items", order_items)

    for item in order_items:
        print("%s:\n%s\n" % (item.product_name, "\n".join(item.product_codes.split('\n'))))
