import pandas as pd
import datetime
import logging
import time
from scraperlib.utils import save_df_to_csv
from scraperlib.tokped import (
    get_tokped_category_page_data
)

# Setup the logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)

CATEGORY_ID = 3844
CATEGORY_NAME = "laptop"
DIRECTORY = "./csv"
ROWS = 60
PAGE = 100

if __name__ == "__main__":
  get_tokped_category_page_data(
      page=PAGE, 
      category_id=CATEGORY_ID, 
      rows=ROWS, 
      directory=DIRECTORY, 
      category_name=CATEGORY_NAME
  )
