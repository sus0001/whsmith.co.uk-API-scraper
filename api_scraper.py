import json
import requests
import pandas as pd
from time import sleep
import winsound
import logging
import time
import concurrent.futures


start_time = time.time()

api_page_numbers = 5000
time_interval = 2
# page_range = 100

database_name = "WHSMITH Books database1"


# using concurrency (multithreading) features for faster scraping:
def lightning_scraping(functions, lists):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executions = executor.map(functions, lists)
        return executions


def api_url_lists():
    api_urls = []

    for indexes in range(0, api_page_numbers, 12):
        api_urls.append(f"https://www.whsmith.co.uk/product-search?q&start={indexes}&count=12&sort=most-popular&refine_1=cgid%3DBKS00001&refine_2=price%3D(0..1000)&expand=prices")

    return api_urls


product_id = []
product_name = []
product_brand = []
product_format = []
product_contributor = []
product_price = []
product_page_url = []
product_primary_category_id = []
product_list_price = []
product_sale_price = []
product_stock_status = []
product_stock_level = []
product_image_url = []


def meet_api_endpoints(apis):     
  
    json_data = requests.get(apis).content
    json_data = json.loads(json_data)  
    
    
    for index in range(115):            
        try:       
                    
            sleep(time_interval)
                    
            try:
                id = json_data['hits'][index]['c_topPriorityVariation']['id']
            except KeyError:
                id = "N/A"
            product_id.append(id)

            try:
                name = json_data['hits'][index]['c_topPriorityVariation']['name']
            except KeyError:
                name = "N/A"
            product_name.append(name)

            try:
                brand = json_data['hits'][index]['c_topPriorityVariation']['brand']
            except KeyError:
                brand = "N/A"
            product_brand.append(brand)

            try:
                format = json_data['hits'][index]['c_topPriorityVariation']['c_productFormat']
            except KeyError:
                format = "N/A"
            product_format.append(format)
                    
            try:
                contributor = json_data['hits'][index]['c_topPriorityVariation']['c_contributor']
            except KeyError:
                contributor = "N/A"
            product_contributor.append(contributor)
                    
            try:
                price = f"£{json_data['hits'][index]['c_topPriorityVariation']['price']}"
            except KeyError:
                price = "N/A"
            product_price.append(price)

            try:
                page_url = f"https://www.whsmith.co.uk/{json_data['hits'][index]['c_topPriorityVariation']['c_page_url']}/{json_data['hits'][index]['product_id']}.html"
            except KeyError:
                page_url = "N/A"
            product_page_url.append(page_url)

            try:
                primary_category_id = json_data['hits'][index]['c_topPriorityVariation']['primary_category_id']
            except KeyError:
                primary_category_id = "N/A"
            product_primary_category_id.append(primary_category_id)
                    
            try:
                list_price = f"£{json_data['hits'][index]['c_topPriorityVariation']['listPrice']}"
            except KeyError:
                list_price = "N/A"
            product_list_price.append(list_price)

            try:
                sale_price = f"£{json_data['hits'][index]['c_topPriorityVariation']['salePrice']}"
            except KeyError:
                sale_price = "N/A"
            product_sale_price.append(sale_price)
                    
            try:
                stock_status = json_data['hits'][index]['c_topPriorityVariation']['inventory']['stock_status']
            except KeyError:
                stock_status = "N/A"
            product_stock_status.append(stock_status)

            try:
                stock_level = json_data['hits'][index]['c_topPriorityVariation']['inventory']['stock_level']
            except KeyError:
                stock_level = "N/A"
            product_stock_level.append(stock_level)

            try:
                image_url = json_data['hits'][index]['c_images'][0]['url']
            except:
                image_url = "N/A"
            product_image_url.append(image_url)

        except IndexError:
            break 
                   
 
dict_product_datas = {
                            "ID": product_id,
                            "Name": product_name,
                            "Brand": product_brand,
                            "Format": product_format,
                            "Contributor": product_contributor,
                            "Price": product_price,                            
                            "Primary Category ID": product_primary_category_id,
                            "List Price": product_list_price,
                            "Sale Price": product_sale_price,
                            "Stock Status": product_stock_status,
                            "Stock Level": product_stock_level,
                            "Product URL": product_page_url,
                            "Image URL": product_image_url

                         }

lightning_scraping(meet_api_endpoints, api_url_lists())


def output():
    df = pd.DataFrame(dict_product_datas)
    df.to_excel(f"{database_name}.xlsx", index=False)
    df.to_json(f"{database_name}.json", indent=4)
    print("Saved to Excel and Json format...")

    winsound.PlaySound('notification.mp3', winsound.SND_FILENAME)


try:
    print("Scraping.........\n")
    output()
except:
    logging.exception("Error:")
    pass

time_took = time.time() - start_time
print(f'Took {round(time_took, 2)} seconds....')