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

KEYWORD = "susu bayi"
FILE_NAME = ""
ROWS = 60
SORT = 4
PAGE = 100

def request_with_keyword(keyword, rows, sort, page):
  payload = {
      "operationName": "SearchProductQueryV4",
      "variables": {"params":  f"device=desktop&ob={sort}&q={keyword}&rows={rows}&safe_search=false&show_adult=true&source=search&start={page*rows-60}&unique_id=41c9119fd5fb4151a8123aed4c8097ac"},
      "query": """query SearchProductQueryV4($params: String!) {
                    ace_search_product_v4(params: $params) {
                      header {
                        totalData
                        totalDataText
                        processTime
                        responseCode
                        errorMessage
                        additionalParams
                        keywordProcess
                        componentId
                        __typename
                      }
                      data {
                        banner {
                          position
                          text
                          imageUrl
                          url
                          componentId
                          trackingOption
                          __typename
                        }
                        backendFilters
                        isQuerySafe
                        ticker {
                          text
                          query
                          typeId
                          componentId
                          trackingOption
                          __typename
                        }
                        redirection {
                          redirectUrl
                          departmentId
                          __typename
                        }
                        related {
                          position
                          trackingOption
                          relatedKeyword
                          otherRelated {
                            keyword
                            url
                            product {
                              id
                              name
                              price
                              imageUrl
                              rating
                              countReview
                              url
                              priceStr
                              wishlist
                              shop {
                                shopId: id
                                city
                                isOfficial
                                isPowerBadge
                                __typename
                              }
                              ads {
                                adsId: id
                                productClickUrl
                                productWishlistUrl
                                shopClickUrl
                                productViewUrl
                                __typename
                              }
                              badges {
                                title
                                imageUrl
                                show
                                __typename
                              }
                              ratingAverage
                              labelGroups {
                                position
                                type
                                title
                                url
                                __typename
                              }
                              componentId
                              warehouseIdDefault
                              __typename
                            }
                            componentId
                            __typename
                          }
                          __typename
                        }
                        suggestion {
                          currentKeyword
                          suggestion
                          suggestionCount
                          instead
                          insteadCount
                          query
                          text
                          componentId
                          trackingOption
                          __typename
                        }
                        products {
                          id
                          name
                          ads {
                            adsId: id
                            productClickUrl
                            productWishlistUrl
                            productViewUrl
                            __typename
                          }
                          badges {
                            title
                            imageUrl
                            show
                            __typename
                          }
                          category: departmentId
                          categoryBreadcrumb
                          categoryId
                          categoryName
                          countReview
                          customVideoURL
                          discountPercentage
                          gaKey
                          imageUrl
                          labelGroups {
                            position
                            title
                            type
                            url
                            __typename
                          }
                          originalPrice
                          price
                          priceRange
                          rating
                          ratingAverage
                          shop {
                            shopId: id
                            name
                            url
                            city
                            isOfficial
                            isPowerBadge
                            __typename
                          }
                          url
                          wishlist
                          sourceEngine: source_engine
                          warehouseIdDefault
                          __typename
                        }
                        violation {
                          headerText
                          descriptionText
                          imageURL
                          ctaURL
                          ctaApplink
                          buttonText
                          buttonType
                          __typename
                        }
                        __typename
                      }
                      __typename
                    }
                  }"""
                }

  headers = {
      "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
      "Referer": "https://www.tokopedia.com/search?"
  }

  return requests.request(method="POST", 
                          url=api, 
                          json=payload, 
                          headers=headers)

def flow_tokped_keyword(keyword, rows, sort, page):
  i = 1
  while i <= page:
    try:
      response = request_with_keyword(keyword, rows, sort, i)
      data = response.json()
      data1 = data['data']['ace_search_product_v4']['data']['products']
      df1 = pd.json_normalize(data1)
      df2 = pd.DataFrame(list(map(standarized_columns, [df1]))[0])
      logging.info(f"Get the data from page {i}")
      time.sleep(5)
      df2.to_csv(f"{KEYWORD.lower().replace(' ', '_')}.csv", index=False, mode='a')
      logging.info(f"Saved the data from the page of {i} to csv")
      i += 1
    except Exception as e:
      logging.error(e)
      pass

flow_tokped_keyword(keyword=KEYWORD, 
                    rows=ROWS, 
                    sort=SORT, 
                    page=PAGE)