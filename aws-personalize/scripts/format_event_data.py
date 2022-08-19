import pandas as pd

df = pd.read_csv('../dataset/eventbrite.csv')
df = df.reset_index(drop=True)

drop_cols = ['Unnamed: 0', 'url', 'vanity_url', 'changed', 'capacity', 'capacity_is_custom', 'status',\
       'currency', 'listed', 'logo_crop_mask', 'logo', 'status_code', 'error_description', 'error',\
       'logo_crop_mask_top_left_x','logo_crop_mask_top_left_y', 'logo_crop_mask_width',\
       'logo_crop_mask_height', 'logo_original_url', 'logo_original_width', 'hide_start_date', 'hide_end_date',\
       'logo_original_height', 'logo_url', 'logo_aspect_ratio', 'resource_uri',\
       'logo_edge_color', 'logo_edge_color_set', 'name_html', 'description_html', 'show_seatmap_thumbnail', 'show_colors_in_seatmap_thumbnail',\
       'show_pick_a_seat', 'logo_id', 'created', 'version', 'end_timezone']

df = df.drop(drop_cols, axis=1)
# df =df.astype({"shareable": str, "online_event": str, 
# "locale": str, "is_locked": str,
# "privacy_setting": str,
# "is_series": str,
# "is_series_parent": str,
# "inventory_type": str,
# "is_reserved_seating": str,
# "source": str,
# "is_free": str,
# "summary": str,
# "id": str,
# "name_text": str,
# "description_text": str,
# "start_timezone": str,
# "start_local": str,
# "start_utc": str,
# "end_local": str,
# "end_utc": str,
# "is_externally_ticketed": str})

df = df.fillna(0)
df["tx_time_limit"] = df["tx_time_limit"].fillna(0)
df =df.astype({"tx_time_limit": int, "id": str})
df = df.rename(columns={'id': 'ITEM_ID'})
df = df.drop_duplicates(subset='ITEM_ID', keep="last")

print(df.columns)
print(df.dtypes)
# print(len(set(df['ITEM_ID'])))

print(df[df['ITEM_ID'].duplicated() == True])

df.reset_index(drop=True, inplace=True)
df.to_csv('../dataset/eventbrite_personalize_items.csv', index = True)




