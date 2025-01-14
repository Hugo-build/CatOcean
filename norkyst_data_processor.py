# %% Import libraries and define functions
import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

def load_netcdf(url):
    return nc.Dataset(url)

def extract_variables(dataset, var_names):
    return {name: dataset.variables[name][:] for name in var_names}

def plot_variable(data, lat, lon, title, cmap='viridis'):
    plt.figure(figsize=(10, 8))
    plt.imshow(data, extent=[lon.min(), lon.max(), lat.min(), lat.max()], 
               cmap=cmap, origin='lower')
    plt.colorbar(label=title)
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title(title)
    plt.show()

def fit_weibull(data):
    # Flatten and remove NaNs
    flat_data = data.flatten()
    flat_data = flat_data[~np.isnan(flat_data)]
    # Fit Weibull distribution
    params = stats.weibull_min.fit(flat_data)
    return params

def process_netcdf_files(urls, variables):
    all_data = []
    for url in urls:
        dataset = load_netcdf(url)
        data = extract_variables(dataset, variables)
        all_data.append(data)
        
        # Plot each variable
        for var_name, var_data in data.items():
            if var_data.ndim == 2:
                plot_variable(var_data, data['lat'], data['lon'], f'{var_name} at surface')
            elif var_data.ndim == 4:
                plot_variable(var_data[0, 0], data['lat'], data['lon'], f'{var_name} at surface (first time step)')
        
        # Fit Weibull for 'u'
        if 'u' in data:
            u_data = data['u']
            if u_data.ndim == 4:
                u_data = u_data[0, 0]  # First time step, surface level
            weibull_params = fit_weibull(u_data)
            print(f"Weibull parameters for 'u': c={weibull_params[0]:.2f}, loc={weibull_params[1]:.2f}, scale={weibull_params[2]:.2f}")
        
        dataset.close()
    
    return all_data


# %% Test as main
if __name__ == "__main__":
    # Usage
    urls = [
        'https://thredds.met.no/thredds/dodsC/fou-hi/norkyst800m-1h/NorKyst-800m_ZDEPTHS_his.an.2024090400.nc',
        # Add more URLs here
    ]
    
    dataset = load_netcdf(urls[0])

    # Print the available variables
    print("Available variables:")
    for var in dataset.variables.keys():
        print(f"- {var}")

    variables = ['u', 'v', 'temp', 'salt', 'lat', 'lon']

    data  = extract_variables(dataset, variables)
    print(data)

    
# %%
