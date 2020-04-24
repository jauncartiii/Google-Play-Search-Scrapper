import requests

config = {
    "manual_data_scrap": False, # When False, max result are 50
    "search_word": "dating",
    "country_code": "es",
    "number_downloads": False # Increase significantly the time of the data gathery
}



if config["manual_data_scrap"]:
    r = open("manual_data_scrap", "r", encoding="utf8").read()
else:
    r = requests.get(f"https://play.google.com/store/search?q={config['search_word']}&c=apps&gl={config['country_code']}").text

r = r.replace(" >", ">")
item_app_holder = r.split("<div class=\"Vpfmgd\">")

if len(item_app_holder) < 2:
    print("No results")
    exit(0)

item_app_holder.pop(0)

count_div_start = item_app_holder[0].count("<div")
count_div_end = item_app_holder[0].count("</div>")

index = 0
for i in range(count_div_end):
    index = item_app_holder[-1].find("</div>", index) + 6

last_item_app_holder = item_app_holder.pop(-1)
item_app_holder.append(last_item_app_holder[0:index])

data_holder_item_holder = {}
authors = 0
apps = 0
rating_sum = 0
total_users = 0
for item in item_app_holder:
    temp_data_split = item.split("<div class=\"kCSSQe\">")

    temp2_data_split = temp_data_split[1].split("<a ")
    app_name = temp2_data_split[1].split("title=\"")[1].split("\"")[0].replace("\n", "")
    app_link = "https://play.google.com" + temp2_data_split[1].split("href=\"")[1].split("\"")[0].replace("\n", "")

    author_name = temp2_data_split[2].split("<div class=\"KoLSrc\">")[1].split("</div>")[0].replace("\n", "")
    author_link = "https://play.google.com" + temp2_data_split[2].split("href=\"")[1].split("\"")[0].replace("\n", "")

    try:
        rating = temp_data_split[2].split("Rated ")[1].split(" ")[0]
        rating_sum += float(rating.replace(",", "."))
    except:
        try:
            rating = temp_data_split[2].split("Valoración: ")[1].split(" ")[0]
            rating_sum += float(rating.replace(",", "."))
        except:
            rating = "N/A"

    if not data_holder_item_holder.get(author_name):
        data_holder_item_holder[author_name] = {}
        data_holder_item_holder[author_name]["href"] = author_link
        authors += 1
    
    if not data_holder_item_holder[author_name].get("apps"):
        data_holder_item_holder[author_name]["apps"] = []

    downloads = "N/A"
    if config["number_downloads"]:
        app_data = requests.get(app_link).text
        
        try:
            downloads = app_data.split("<span class=\"htlgb\">")[6].split("</span>")[0]
            total_users += int(downloads.replace(".", "").replace(",", "").replace("+", ""))
        except:
            downloads = "N/A"

        pass

    data_holder_item_holder[author_name]["apps"].append((app_name, app_link, rating, downloads))
    apps += 1


print(
    f'''General Data:
    \tOffline: {config['manual_data_scrap']}
    \tQuery Term: {config['search_word']}\n
    \t- Authors: {authors}
    \t- Apps: {apps}
    \t- Average Rating: {'{:.4f}'.format(rating_sum/apps)}
    \t- Total users all results sum: {f'{total_users:,}' if config['number_downloads'] else 'N/A'}\n'''
)

for (author, data) in data_holder_item_holder.items():
    print(f"\n{author}")
    for app in data["apps"]:
        print(f"\t{app[2]} {f'{app[3]} ' if config['number_downloads'] else ''}- {app[0]}")

