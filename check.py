def api_url_lists():
    api_urls = []

    for indexes in range(1, 100, 12):
        api_urls.append(f"https://www.whsmith.co.uk/product-search?q&start={indexes}&count=12&sort=most-popular&refine_1=cgid%3DBKS00001&refine_2=price%3D(0..1000)&expand=prices")

    return api_urls


print(api_url_lists())

for i in range(0, 36, 12):
    print(i)