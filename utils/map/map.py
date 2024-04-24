import os
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

def genMap():

    # file acsess
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, "stations.csv")
    image_path = os.path.join(current_dir, "map.jpg")



    # read the csv 
    df = pd.read_csv(data_path, skiprows=1, names=['x', 'y', 'objectid', 'uri', 'name', 'feature_date', 'feature_source', 'attribute_date', 'attribute_source', 'source_ufi', 'source_jurisdiction', 'custodian_agency', 'custodian_licensing', 'loading_date', 'building_id', 'operationalstatus', 'height', 'significance', 'address', 'suburb', 'site_class', 'local_construction_type', 'local_year_built', 'state', 'source_supply_date', 'featuresubtype'])
    print(df.head())

    filtered_df = df

    # thing to filter the data
    state = 'VIC'
    status = 'Operational'
    filtered_df = df[df['state'] == state]
    filtered_df = filtered_df[filtered_df['operationalstatus'] == status]


    # plot graph
    smallerdf = filtered_df[['x', 'y', 'state', 'operationalstatus']]
    sns.scatterplot(data=smallerdf, x="x", y="y", hue="state", style="operationalstatus")
    bg_image = plt.imread(image_path)
    plt.imshow(bg_image, extent=[114.694, 153.611, -43.45, -12.475], aspect='auto')

    # settings
    plt.xlim(141.163, 147.383)  
    plt.ylim(-39.353, -33.878) 
    plt.legend([], frameon=False)
    plt.axis('off')

    # Save the specific area of the plot as an image
    plt.savefig(os.path.join(current_dir, "gen.png"), bbox_inches='tight', pad_inches=0.0)
genMap()