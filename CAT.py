# %%
import requests
from bs4 import BeautifulSoup

def get_norkyst_files():
    # Base catalog URL
    catalog_url = "https://thredds.met.no/thredds/catalog/fou-hi/norkyst800m-1h/catalog.html"
    
    # Get the catalog page
    response = requests.get(catalog_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all dataset links (they typically end with .nc)
    datasets = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and href.endswith('.nc'):
            # Convert catalog link to OPeNDAP URL
            file_name = href.split('/')[-1]
            opendap_url = f"https://thredds.met.no/thredds/dodsC/fou-hi/norkyst800m-1h/{file_name}"
            datasets.append(opendap_url)
    
    return datasets


def get_nora3_files():
    pass


#%%
if __name__ == "__main__":
    datasets = get_norkyst_files()
    print("\n" + "-"*50)
    print("Available Norkyst-800m datasets:")
    for i, url in enumerate(datasets):
        print(f"{i:3d} : {url}")
    print("-"*50)




# %%
