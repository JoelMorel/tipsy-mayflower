# import gmaps
# import gmaps.datasets


# def createMap(hotspots, deadspots):
#     # updated_list contains coordinates of location if current_popularity is not None.
#     updated_list = [n['coordinates']
#                     for n in response_list if n['current_popularity'] != None]

#     # weight contains current_popularity if the value is not None
#     weight = [n['current_popularity']
#               for n in response_list if n['current_popularity'] != None]

#     gmaps.configure(api_key='AIzaSyCobJCcwLjJzFw2Iz_1R66wWXqotu2rJTM')
#     figure = gmaps.figure()
#     figure.add_layer(gmaps.heatmap_layer(
#         updated_list, weights=weight, point_radius=20))

#     return figure
