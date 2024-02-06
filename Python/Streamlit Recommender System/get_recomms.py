import pandas as pd
import numpy as np
import glob
import os
from numpy.linalg import norm
import matplotlib.pyplot as plt
from sklearn.cluster import AgglomerativeClustering
import authenticate as a


users = pd.read_csv('all_picked.csv', sep = ',', index_col = 0)
shows = pd.read_csv('BBC_merged1.csv')


def recomm(user_picked):
#username = a.authenticate().name


    #Get the average value for the show/series and apply it to all


    def apply_mean(shows, users):
        tags_explore = shows.tags.str.split(", ", expand=True)
        shows['tag1'] = tags_explore[3]

        #merge user data with tags to do the groupby
        users['id'] = users.index


        #also merge with the titles because they overlap
        users_tags = users.merge(shows[['tag1', 'id', 'title']], on='id', how='left')

        users = users.drop(columns='id')

        #assign the mean value per show, should add it only if value missing

        for column in users_tags.iloc[:,:-3].columns:
            users_tags[column] = np.where(users_tags[column].isna(), users_tags.groupby(['tag1'])[column].transform('mean'), users_tags[column])
        
        #Apply the same rating per user for all movies/shows with the same title if value is missing

        for column in users_tags.iloc[:,:-3].columns:
            users_tags[column] = np.where(users_tags[column].isna(), users_tags.groupby(['title'])[column].transform('mean'), users_tags[column])
        
        return users_tags.iloc[:,:-3]


    # Apply mean function
    users_applied = apply_mean(shows, users)

    users_applied.mean()

    # Remove mean of user per review to normalise reviews
    users_normalised = users_applied - users_applied.mean()



    def cosine_similarity(a, b):
        return np.dot(a,b)/(norm(a)*norm(b))



    def create_similarity(users_normalised):
        # Fillna to make sure cosine works
        users_normalised = users_normalised.fillna(0)
        n_users = len(users_normalised.columns)
        #Calculate similarity for all users

        similarity_list = []

        for previous_column in users_normalised:
            for current_column in users_normalised:
                similarity_list.append(cosine_similarity(users_normalised[previous_column], users_normalised[current_column]))
        #Turn into 2d array 25 users by 25 users
        similarity_array = np.array(similarity_list).reshape(n_users,n_users)

        #Create dataframe, because I love dataframes
        df_similarities = pd.DataFrame(similarity_array, index= users_normalised.columns, columns = users_normalised.columns)

        return similarity_array, df_similarities



    # Apply similarity function
    similarity_array, df_similarities = create_similarity(users_normalised)

    df_similarities

    #hierarchical clustering
    def do_hierarchical(similarity_array, users_normalised):

        users_normalised_clusters = users_normalised.T

        #Change similarity into distance
        distance_matrix = 1 - similarity_array
        np.fill_diagonal(distance_matrix, 0)
        
        clustering = AgglomerativeClustering(n_clusters= 4, affinity = 'precomputed', linkage='complete', compute_distances = True).fit(distance_matrix)
        users_normalised_clusters['cluster'] = clustering.labels_
        return users_normalised_clusters

    users_normalised_clusters = do_hierarchical(similarity_array, users_normalised)
    users_normalised_clusters.head()

    #nearest cluster
    cluster_pivot = users_normalised_clusters.pivot_table(columns='cluster', aggfunc='mean')
    sim_array, df_sim = create_similarity(cluster_pivot)
    df_sim


    # users_normalised_clusters[users_normalised_clusters['cluster'] == 3]

    # users_normalised_clusters['cluster']


    # users_normalised_clusters[users_normalised_clusters['cluster'] == 0]]

    df_sim[0].drop(0).nlargest(1).index[0]
    # df_sim[1].drop(1).nlargest(1)
    # df_sim[3].drop(3).nlargest(1)



    #change 0's to missing values for all except k-means column
    users_normalised_clusters.iloc[:, :-1] = users_normalised_clusters.iloc[:, :-1].replace(to_replace=0.0, value=np.NaN)

    #Get similar users baseed on the same cluster
    def get_similar_users_reviews_same(user,clusters):
        cluster = clusters.loc[clusters['cluster'] == clusters.loc[user,'cluster']] #pick columns that are in the same cluster as the user
        cluster = cluster.drop(columns = ['cluster']).T #drop k_means column
        not_user = cluster[cluster[user].isna()].drop(columns = [user]) #keep only rows that user didn't rate and drop the column with the user and 
        return not_user
        # return cluster.index

    #Get similar users based on random other cluster

    import random

    def get_similar_users_reviews_different(user,clusters):
        #randomly pick the new cluster
        # no_clusters = clusters['cluster'].max()
        # numbers = list(range(0, no_clusters + 1))
        # numbers.remove(clusters.loc[user,'cluster']) #creates list of integers for each cluster except the one of user1
        # other_cluster = random.choice(numbers) #pick random number from those clusters
        
        user_cluster = clusters.loc[user,'cluster']
        cluster_pivot = clusters.pivot_table(columns='cluster', aggfunc='mean')
        sim_array, df_sim = create_similarity(cluster_pivot)
        other_cluster = df_sim[user_cluster].drop(0).nlargest(1).index[0]
        
        
        #create df with the new cluster
        cluster = clusters.T #transpose df -> users as columns
        not_user = cluster[cluster[user].isna() | (cluster.index == 'cluster')] #keep only rows that user didn't rate, already need to do this here, but exclude k-means
        not_user = not_user.T #transpose again; users as rows, k-means as column
        not_user = not_user.loc[not_user['cluster'] == other_cluster] #pick columns that are in the cluster chosen randomly    return not_user
        return not_user.T

    def recommend_movies(user,clusters,shows, df_similarities, get_similar_users_reviews): #choose get_similar_users_reviews_different to get different recommendations
        similar_users = get_similar_users_reviews(user, clusters)
        similarities = df_similarities.loc[user,similar_users.columns]
        #multiply by the similarities scores only if returning the recommendations from the same cluster
        if get_similar_users_reviews == get_similar_users_reviews_same:
            return similar_users * similarities
        else:
            return similar_users

    #Example: user2
    #set the user to user based on session state
    recommendations_same_cluster = recommend_movies(user_picked, users_normalised_clusters, shows, df_similarities, get_similar_users_reviews_same).mean(axis = 1).nlargest(100)
    recommendations_other_cluster = recommend_movies(user_picked, users_normalised_clusters, shows, df_similarities, get_similar_users_reviews_different).mean(axis = 1).nlargest(100)

    #retrieve the title, genre and image for the recommendations
    #These are partly random episodes -> might be best to recommend the first episode
    recommendations_same_cluster_df = pd.DataFrame(recommendations_same_cluster, columns = ['similarity_score'])
    recommendations_other_cluster_df = pd.DataFrame(recommendations_other_cluster, columns = ['similarity_score'])

    recommendations_same_cluster_info = pd.merge(recommendations_same_cluster_df, shows, left_index = True, right_on = 'id').groupby('tag1').first().sort_values('similarity_score', ascending=False)
    recommendations_other_cluster_info = pd.merge(recommendations_other_cluster_df, shows, left_index = True, right_on = 'id').groupby('tag1').first().sort_values('similarity_score', ascending=False)

    recommendations_same_cluster_info.to_csv('same_cluster.csv')
    recommendations_other_cluster_info.to_csv('other_cluster.csv')

