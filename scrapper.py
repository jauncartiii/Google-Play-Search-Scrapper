import requests
import json

config = {
    "manual_data_scrap": False,
    "search_word": "dating",
    "country_code": "es"
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
for item in item_app_holder:
    temp_data_split = item.split("<div class=\"kCSSQe\">")

    temp2_data_split = temp_data_split[1].split("<a ")
    title_name = temp2_data_split[1].split("title=\"")[1].split("\"")[0].replace("\n", "")
    title_link = temp2_data_split[1].split("href=\"")[1].split("\"")[0].replace("\n", "")

    author_name = temp2_data_split[2].split("<div class=\"KoLSrc\">")[1].split("</div>")[0].replace("\n", "")
    author_link = temp2_data_split[2].split("href=\"")[1].split("\"")[0].replace("\n", "")

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

    data_holder_item_holder[author_name]["apps"].append((title_name, title_link, rating))
    apps += 1


print(f"General Data:\n\tOffline: {config['manual_data_scrap']}\n\tAuthors: {authors}\n\tApps: {apps}\n\tAverage Rating: {rating_sum/apps}\n\n\n")
for (author, data) in data_holder_item_holder.items():
    print(f"\n{author}")
    for app in data["apps"]:
        print(f"\t{app[2]} {app[0]}")

