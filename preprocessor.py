import pandas as pd

def preprocess(df, region_df):
    """
    Preprocess the Olympic data by filtering for Summer Olympics, 
    merging with region data, removing duplicates, and encoding medals.
    
    Parameters:
        df (pd.DataFrame): The main Olympics dataset.
        region_df (pd.DataFrame): The dataset containing region (NOC) mappings.
    
    Returns:
        pd.DataFrame: The preprocessed dataset.
    """

    # Filtering for Summer Olympics
    df = df[df['Season'] == 'Summer'].copy()

    # Merging with region dataset using 'NOC'
    df = df.merge(region_df, on='NOC', how='left')

    # Dropping duplicates to avoid redundant entries
    df.drop_duplicates(inplace=True)

    # One-hot encoding the 'Medal' column (Gold, Silver, Bronze)
    df = df.join(pd.get_dummies(df['Medal'], dtype=int))

    return df
