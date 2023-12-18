import requests

url = "https://gql.tokopedia.com/graphql/SearchProductQuery"

payload = {
    "operationName": "SearchProductQuery",
    "variables": {
        "params": "page=2&ob=&identifier=ibu-bayi_susu-bayi-anak&sc=5506&user_id=0&rows=60&start=61&source=directory&device=desktop&page=2&related=true&st=product&safe_search=false",
        "adParams": "page=2&page=2&dep_id=5506&ob=&ep=product&item=15&src=directory&device=desktop&user_id=0&minimum_item=15&start=61&no_autofill_range=5-14"
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
    "cookie": "_abck=CC03FE56A4A2B8964189E6FFB02C363C~-1~YAAQjVA7FxYqk3WMAQAAkQ8heAvkOXfXSwSiVslVbMiXZ5XYqz%2Flzw2TcaQPNjKWB7WwDKfqRCT0GxFvTUtlPWdOtNBALnjMAmeF2PapAuDSWuF4NzI6QATwP9pfNplD2IZlQoU4m5EP4fapzmgoU%2FieKmbCJ4aF40W%2Bk4EtbkfPG7VuiixsKbuRY63r481Xhqhn0iEJ4qQ4E5cQ7Cq%2Fb6n3nBIlXCm%2Fn92vlgbX3FhjgyapoxArbbGU%2BpNouCYB895ndlPnWjO7WdaJtIG%2Bm0BxGde6BHAE2nIWlPwoozsRt185R5M7%2BYnR0EYjg%2BLB1fe1R%2FvEnYBJ4CcgsAowE5Y6C58N%2BPqZF4BurTfKnIIBI8v3v8lXxMB%2B9%2F5t4RbvBEg7IsXpHmj1ySho~-1~-1~-1",
    "sec-ch-ua": ""Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"",
    "Tkpd-UserId": "0",
    "X-Version": "f80b5df",
    "sec-ch-ua-mobile": "?0",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "iris_session_id": "d3d3LnRva29wZWRpYS5jb20=.82447e4514a1142989d2f1a4f2d31484.1702820838175",
    "content-type": "application/json",
    "accept": "*/*",
    "Referer": "https://www.tokopedia.com/p/ibu-bayi/susu-bayi-anak?page=2",
    "X-Source": "tokopedia-lite",
    "x-device": "desktop-0.0",
    "X-Tkpd-Lite-Service": "zeus",
    "sec-ch-ua-platform": ""Linux""
}

response = requests.request("POST", url, json=payload, headers=headers)

print(response.text)