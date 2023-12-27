import requests
import pandas as pd
import datetime
import re
import logging
import time
from scraperlib.utils import (
   standarized_columns, 
   save_df_to_csv
)

# Setup the logging
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)

def request_category_page(category_id, rows, page):
    endpoint = "https://gql.tokopedia.com/graphql/SearchProductQueryV4"

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

    return requests.request(
        method="POST", 
        url=endpoint, 
        json=payload, 
        headers=headers
    )

def request_product_page(shop_domain, product_key):
    endpoint = "https://gql.tokopedia.com/graphql/PDPGetLayoutQuery"


    payload ={"operationName": "PDPGetLayoutQuery",
            "variables": {
                "shopDomain": f"{shop_domain}",
                "productKey": f"{product_key}",
                "apiVersion": 1,
            },
            "query": """fragment ProductVariant on pdpDataProductVariant {
                        errorCode
                        parentID
                        defaultChild
                        sizeChart
                        totalStockFmt
                        variants {
                            productVariantID
                            variantID
                            name
                            identifier
                            option {
                            picture {
                                urlOriginal: url
                                urlThumbnail: url100
                                __typename
                            }
                            productVariantOptionID
                            variantUnitValueID
                            value
                            hex
                            stock
                            __typename
                            }
                            __typename
                        }
                        children {
                            productID
                            price
                            priceFmt
                            slashPriceFmt
                            discPercentage
                            optionID
                            optionName
                            productName
                            productURL
                            picture {
                            urlOriginal: url
                            urlThumbnail: url100
                            __typename
                            }
                            stock {
                            stock
                            isBuyable
                            stockWordingHTML
                            minimumOrder
                            maximumOrder
                            __typename
                            }
                            isCOD
                            isWishlist
                            campaignInfo {
                            campaignID
                            campaignType
                            campaignTypeName
                            campaignIdentifier
                            background
                            discountPercentage
                            originalPrice
                            discountPrice
                            stock
                            stockSoldPercentage
                            startDate
                            endDate
                            endDateUnix
                            appLinks
                            isAppsOnly
                            isActive
                            hideGimmick
                            isCheckImei
                            minOrder
                            __typename
                            }
                            thematicCampaign {
                            additionalInfo
                            background
                            campaignName
                            icon
                            __typename
                            }
                            __typename
                        }
                        __typename
                        }

                        fragment ProductMedia on pdpDataProductMedia {
                        media {
                            type
                            urlOriginal: URLOriginal
                            urlThumbnail: URLThumbnail
                            urlMaxRes: URLMaxRes
                            videoUrl: videoURLAndroid
                            prefix
                            suffix
                            description
                            variantOptionID
                            __typename
                        }
                        videos {
                            source
                            url
                            __typename
                        }
                        __typename
                        }

                        fragment ProductCategoryCarousel on pdpDataCategoryCarousel {
                        linkText
                        titleCarousel
                        applink
                        list {
                            categoryID
                            icon
                            title
                            isApplink
                            applink
                            __typename
                        }
                        __typename
                        }

                        fragment ProductHighlight on pdpDataProductContent {
                        name
                        price {
                            value
                            currency
                            priceFmt
                            slashPriceFmt
                            discPercentage
                            __typename
                        }
                        campaign {
                            campaignID
                            campaignType
                            campaignTypeName
                            campaignIdentifier
                            background
                            percentageAmount
                            originalPrice
                            discountedPrice
                            originalStock
                            stock
                            stockSoldPercentage
                            threshold
                            startDate
                            endDate
                            endDateUnix
                            appLinks
                            isAppsOnly
                            isActive
                            hideGimmick
                            __typename
                        }
                        thematicCampaign {
                            additionalInfo
                            background
                            campaignName
                            icon
                            __typename
                        }
                        stock {
                            useStock
                            value
                            stockWording
                            __typename
                        }
                        variant {
                            isVariant
                            parentID
                            __typename
                        }
                        wholesale {
                            minQty
                            price {
                            value
                            currency
                            __typename
                            }
                            __typename
                        }
                        isCashback {
                            percentage
                            __typename
                        }
                        isTradeIn
                        isOS
                        isPowerMerchant
                        isWishlist
                        isCOD
                        preorder {
                            duration
                            timeUnit
                            isActive
                            preorderInDays
                            __typename
                        }
                        __typename
                        }

                        fragment ProductCustomInfo on pdpDataCustomInfo {
                        icon
                        title
                        isApplink
                        applink
                        separator
                        description
                        __typename
                        }

                        fragment ProductInfo on pdpDataProductInfo {
                        row
                        content {
                            title
                            subtitle
                            applink
                            __typename
                        }
                        __typename
                        }

                        fragment ProductDetail on pdpDataProductDetail {
                        content {
                            title
                            subtitle
                            applink
                            showAtFront
                            isAnnotation
                            __typename
                        }
                        __typename
                        }

                        fragment ProductDataInfo on pdpDataInfo {
                        icon
                        title
                        isApplink
                        applink
                        content {
                            icon
                            text
                            __typename
                        }
                        __typename
                        }

                        fragment ProductSocial on pdpDataSocialProof {
                        row
                        content {
                            icon
                            title
                            subtitle
                            applink
                            type
                            rating
                            __typename
                        }
                        __typename
                        }

                        fragment ProductDetailMediaComponent on pdpDataProductDetailMediaComponent {
                        title
                        description
                        contentMedia {
                            url
                            ratio
                            type
                            __typename
                        }
                        show
                        ctaText
                        __typename
                        }

                        query PDPGetLayoutQuery($shopDomain: String, $productKey: String, $layoutID: String, $apiVersion: Float, $userLocation: pdpUserLocation, $extParam: String, $tokonow: pdpTokoNow, $deviceID: String) {
                        pdpGetLayout(shopDomain: $shopDomain, productKey: $productKey, layoutID: $layoutID, apiVersion: $apiVersion, userLocation: $userLocation, extParam: $extParam, tokonow: $tokonow, deviceID: $deviceID) {
                            requestID
                            name
                            pdpSession
                            basicInfo {
                            alias
                            createdAt
                            isQA
                            id: productID
                            shopID
                            shopName
                            minOrder
                            maxOrder
                            weight
                            weightUnit
                            condition
                            status
                            url
                            needPrescription
                            catalogID
                            isLeasing
                            isBlacklisted
                            isTokoNow
                            menu {
                                id
                                name
                                url
                                __typename
                            }
                            category {
                                id
                                name
                                title
                                breadcrumbURL
                                isAdult
                                isKyc
                                minAge
                                detail {
                                id
                                name
                                breadcrumbURL
                                isAdult
                                __typename
                                }
                                __typename
                            }
                            txStats {
                                transactionSuccess
                                transactionReject
                                countSold
                                paymentVerified
                                itemSoldFmt
                                __typename
                            }
                            stats {
                                countView
                                countReview
                                countTalk
                                rating
                                __typename
                            }
                            __typename
                            }
                            components {
                            name
                            type
                            position
                            data {
                                ...ProductMedia
                                ...ProductHighlight
                                ...ProductInfo
                                ...ProductDetail
                                ...ProductSocial
                                ...ProductDataInfo
                                ...ProductCustomInfo
                                ...ProductVariant
                                ...ProductCategoryCarousel
                                ...ProductDetailMediaComponent
                                __typename
                            }
                            __typename
                            }
                            __typename
                        }
                        }
                        """
                            }
        
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
        "Referer": "https://www.tokopedia.com",
        "X-TKPD-AKAMAI": "pdpGetLayout"
    }

    return requests.request(
        method="POST", 
        url=endpoint, 
        json=payload, 
        headers=headers
    )

def get_the_data_category_page(category_id, rows, page):
  response = request_category_page(category_id, rows, page)
  data = response.json()
  data1 = data['data']['CategoryProducts']['data']
  df1 = pd.json_normalize(data1)
  return pd.DataFrame(list(map(standarized_columns, [df1]))[0])

def get_the_data_product_page(shop_name, product_url):
    response = request_product_page(
            shop_domain=shop_name, 
            product_key=product_url
    )
    data = response.json()["data"]["pdpGetLayout"]["basicInfo"]
    return pd.json_normalize(data)

def iterate_column(df, column, index_list):
  prod = []
  for i in df[column]:
    split1 = i.replace("?", "/")
    split2 = split1.split('/'); del split1
    prod.append(split2[index_list])
  return prod

def iterate_product_page(
    df, column_shop_name, column_product_url, index_list_shop_name, index_list_product_url):

    shop_name = iterate_column(
            df=df, 
            column=column_shop_name, 
            index_list=index_list_shop_name
    )

    product_url = iterate_column(
            df=df, 
            column=column_product_url, 
            index_list=index_list_product_url
    )

    if len(shop_name) == len(product_url):
        prod = []
        for i in range(len(shop_name)):
            time.sleep(1)
            logging.info(f"Get the data from product page of shop {shop_name[i]} and product {product_url[i]}")
            prod1 = get_the_data_product_page(
                shop_name = shop_name[i], 
                product_url = product_url[i]
            )
            prod.append(prod1)
        return prod
    else:
        logging.info("Error on extract the shop name and product url")

def get_tokped_category_page_data(
      page, category_id, rows, directory, category_name):
  
    i = 1
    while i <= page:
        try:
            df2 = get_the_data_category_page(
                category_id=category_id, 
                rows=rows, 
                page=i
            )

            logging.info(f"Get the data from page {i}")

            df_prod = iterate_product_page(
                df=df2,
                column_shop_name="url",
                column_product_url="url",
                index_list_shop_name=3,
                index_list_product_url=4
            )
            
            concat_df_prod = pd.concat(df_prod)

            # manipulate the data
            df2['id'] = df2['id'].astype(int)
            concat_df_prod['id'] = concat_df_prod['id'].astype(int)
            concat_df_prod = concat_df_prod.drop('url', axis=1)

            df_merge = pd.merge(
                df2, 
                concat_df_prod, 
                left_on=['id'], 
                right_on=['id'], 
                how='left'
            )

            print(df_merge)

            time.sleep(4)
            if i == 1:
                save_df_to_csv(
                    df=df_merge,
                    dir=directory,
                    file_name=category_name, 
                    header=True
                )
            else:
                save_df_to_csv(
                    df=df_merge,
                    dir=directory,
                    file_name=category_name, 
                    header=False
                )
            
            logging.info(f"Saved the data from the page of {i} to csv")

            i += 1

            # return df_merge
        
        except Exception as e:
            logging.error(e)
            pass