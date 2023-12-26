import requests
import pandas as pd
import datetime
import re
import logging
import time
from scraperlib.utils import standarized_columns

logging.basicConfig(#filename='./logs/keyword.log', 
                    #filemode='w', 
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)

api = "https://gql.tokopedia.com/graphql/SearchProductQueryV4"

CATEGORY_ID = 1768
FILE_NAME = "atasan wanita"
ROWS = 60
PAGE = 100

def request_with_category(category_id, rows, page):
  payload = {
    "operationName": "SearchProductQuery",
    "variables": {
        "params": f"sc={category_id}&rows={rows}&start={page*rows-60}&source=directory&device=desktop&related=true&st=product&safe_search=false",
    },
    "query": """query SearchProductQuery($params: String, $adParams: String) {
  CategoryProducts: searchProduct(params: $params) {
    count
    data: products {
      id
      url
      imageUrl: image_url
      imageUrlLarge: image_url_700
      catId: category_id
      gaKey: ga_key
      countReview: count_review
      discountPercentage: discount_percentage
      preorder: is_preorder
      name
      price
      priceInt: price_int
      original_price
      rating
      wishlist
      labels {
        title
        color
        __typename
      }
      badges {
        imageUrl: image_url
        show
        __typename
      }
      shop {
        id
        url
        name
        goldmerchant: is_power_badge
        official: is_official
        reputation
        clover
        location
        __typename
      }
      labelGroups: label_groups {
        position
        title
        type
        __typename
      }
      __typename
    }
    __typename
  }
  displayAdsV3(displayParams: $adParams) {
    data {
      id
      ad_ref_key
      redirect
      sticker_id
      sticker_image
      productWishListUrl: product_wishlist_url
      clickTrackUrl: product_click_url
      shop_click_url
      product {
        id
        name
        wishlist
        image {
          imageUrl: s_ecs
          trackerImageUrl: s_url
          __typename
        }
        url: uri
        relative_uri
        price: price_format
        campaign {
          original_price
          discountPercentage: discount_percentage
          __typename
        }
        wholeSalePrice: wholesale_price {
          quantityMin: quantity_min_format
          quantityMax: quantity_max_format
          price: price_format
          __typename
        }
        count_talk_format
        countReview: count_review_format
        category {
          id
          __typename
        }
        preorder: product_preorder
        product_wholesale
        free_return
        isNewProduct: product_new_label
        cashback: product_cashback_rate
        rating: product_rating
        top_label
        bottomLabel: bottom_label
        __typename
      }
      shop {
        image_product {
          image_url
          __typename
        }
        id
        name
        domain
        location
        city
        tagline
        goldmerchant: gold_shop
        gold_shop_badge
        official: shop_is_official
        lucky_shop
        uri
        owner_id
        is_owner
        badges {
          title
          image_url
          show
          __typename
        }
        __typename
      }
      applinks
      __typename
    }
    template {
      isAd: is_ad
      __typename
    }
    __typename
  }
}
"""
}

  headers = {
      "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
      "Referer": "https://www.tokopedia.com/search?"
  }

  return requests.request(method="POST", 
                          url=api, 
                          json=payload, 
                          headers=headers)

# response = request_with_keyword(category_id=CATEGORY_ID, rows=ROWS, page=PAGE)
# data = response.json()
# data1 = data['data']['CategoryProducts']['data']
# df1 = pd.json_normalize(data1)

# print(df1)

def flow_tokped_keyword(category_id, rows, file_name, page):
  i = 1
  while i <= page:
    try:
      response = request_with_keyword(category_id, rows, i)
      data = response.json()
      data1 = data['data']['CategoryProducts']['data']
      df1 = pd.json_normalize(data1)
      df2 = pd.DataFrame(list(map(standarized_columns, [df1]))[0])
      logging.info(f"Get the data from page {i}")
      time.sleep(5)
      df2.to_csv(f"{file_name.lower().replace(' ', '_')}.csv", index=False, mode='a')
      logging.info(f"Saved the data from the page of {i} to csv")
      i += 1
    except Exception as e:
      logging.error(e)
      pass

flow_tokped_keyword(category_id=CATEGORY_ID, 
                    rows=ROWS,
                    file_name=FILE_NAME,
                    page=PAGE)