import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import matplotlib.image as mpimg
from datetime import datetime
import matplotlib.cbook as cbook


UFC_fights = pd.read_csv("ALL UFC FIGHTS 2_23_2016 SHERDOG.COM - Sheet1.csv")
UFC_people = pd.read_csv("ALL UFC FIGHTERS 2_23_2016 SHERDOG.COM - Sheet1.csv")
UFC_people.drop_duplicates(subset ="fid", keep = "first", inplace = True)


def ratio(wins, defeats):
    if wins== 0: return(0)
    elif defeats==0: return(100)
    else: return (int((wins/(wins+defeats))*100))

wins = dict(UFC_fights["f1fid"].value_counts())
defeats = dict(UFC_fights["f2fid"].value_counts())

row_list_dict = list()
for fid in UFC_people["fid"]:
    W = wins.get(fid, 0) 
    D = defeats.get(fid, 0)
    S = W+D
    R = ratio(W,D)
    row_list_dict.append({"fid": fid,
                            "wins": W,
                            "defeats": D,
                            "fights": S,
                            "ratio": R
                            })
fighters_records = pd.DataFrame(row_list_dict)
fighters_records.set_index("fid", inplace=True)

def weightclass_for(chosen_country):
    my_fighters = UFC_people[UFC_people["country"] == chosen_country]
    my_fighters2 = my_fighters["class"].value_counts()
    w_label = (f"weightclasses for {chosen_country}")

    plt.subplot(2,2,1)
    plt.bar([(x[0:6]+"\n"+x[6:12]) for x in my_fighters2.index.values], my_fighters2.values, color="green", 
              edgecolor="blue", label=w_label)
    plt.yticks(my_fighters2.values, my_fighters2.values)
    plt.legend()

def perc_fighters_for(chosen_country):
    my_data = UFC_people[UFC_people["country"] == chosen_country]
    chosen_country_fighters = (len(my_data))
    all_fighters = (len(UFC_people))

    country_slices = [chosen_country_fighters, all_fighters]
    country_labels = [chosen_country, "Rest of the world"]
    country_colors = ["orange", "yellow"]
    explode = [0.1, 0]

    plt.subplot(2,2,2)
    plt.pie(country_slices, labels=country_labels, explode=explode,
              colors=country_colors,
              shadow=True, startangle=200, autopct='%1.1f%%')

    plt.title(f"percentage of fighters from {chosen_country} in the UFC")
    plt.tight_layout()


def perc_victories_for(chosen_country):     
    my_fighters = UFC_people[UFC_people["country"] == chosen_country]
    my_fighters2 = fighters_records.loc[my_fighters["fid"]]
    Wins = my_fighters2["wins"].sum()
    Defeats = my_fighters2["defeats"].sum()

    country_slices = [Wins, Defeats]
    country_labels = ["Wins", "Defeats"]
    country_colors = ["Green", "Red"]
    explode = [0.1, 0]

    plt.subplot(2,2,3)
    plt.pie(country_slices, labels=country_labels, explode=explode,
              colors=country_colors, wedgeprops={'edgecolor': 'black'},
              shadow=True, startangle=120, autopct='%1.1f%%')
    #plt.title(f"Win ratio for fighter from {chosen_country}")


def Locality_special_case_low_nr_localities(my_fighters, list_of_all_localities ):
    locality_slices = list_of_all_localities.values
    locality_labels = list_of_all_localities.index.values
    return(locality_slices, locality_labels)

def locality_main_engine(my_fighters, list_of_all_localities):
    unimportant_localities = []
    booleans = []

    if (sum([x>2 for x in list_of_all_localities.values])) >5: threshold=2
    else: threshold=1

    for locality_ in list_of_all_localities:
        if locality_>threshold:booleans.append(True)
        else:booleans.append(False)

    locality_slices = []
    locality_labels = []
    zipped_ = zip(booleans, (zip(list_of_all_localities.index.values, list_of_all_localities.values)))
    for loc_rec in zipped_:
        if loc_rec[0]:
            locality_slices.append(loc_rec[1][1])
            locality_labels.append(loc_rec[1][0])
        else: 
            unimportant_localities.append(loc_rec[1][1])

    if len(unimportant_localities)!=0:
        locality_slices.append(sum(unimportant_localities))
        if len(locality_labels)>0: locality_labels.append(f"other locations ({sum(unimportant_localities)})") 
        else: locality_labels.append(f"{sum(unimportant_localities)} various locations")       
    return(locality_slices, locality_labels)

def locality_for(chosen_country):
    my_fighters = UFC_people[UFC_people["country"] == chosen_country]
    list_of_all_localities = my_fighters["locality"].value_counts()    

    if (len(list_of_all_localities.values)) < 9:
        locality_slices, locality_labels = Locality_special_case_low_nr_localities(my_fighters, list_of_all_localities)
    else: 
        locality_slices, locality_labels = locality_main_engine(my_fighters, list_of_all_localities)

    plt.subplot(2,2,4)
    plt.pie(locality_slices, labels=locality_labels, wedgeprops={'edgecolor': 'black'},
              shadow=True, startangle=200, autopct='%1.1f%%')

    plt.title(f"Cities of origin of the fighters from {chosen_country}")


def important_fighters_for(chosen_country):
    
    #fig = plt.figure(figsize=(9.6, 7.2))
    #fig.canvas.set_window_title(f'{chosen_country} in the UFC (part1)')    
    
    my_fighters = UFC_people[UFC_people["country"] == chosen_country]
    my_fighters2 = fighters_records.loc[my_fighters["fid"]]
    my_fighters3 = my_fighters2.loc[(my_fighters2["fights"] > 1) & (my_fighters2["ratio"] >49)]
    if(len(my_fighters3 ))>7:
        my_fighters3 = my_fighters2.loc[(my_fighters2["fights"] > 5) & (my_fighters2["ratio"] >49)]
        if(len(my_fighters3 ))>7:
            my_fighters3 = my_fighters2.loc[(my_fighters2["fights"] > 9) & (my_fighters2["ratio"] >60)]
            if(len(my_fighters3 ))>7:
                my_fighters3 = my_fighters2.loc[(my_fighters2["fights"] > 14) & (my_fighters2["ratio"] >65)]                  

    data = {}
    for i in range(len(my_fighters3)):
        fighter_idd_ = my_fighters3.loc[:,["wins","defeats"]].index.values[i]
        fighter_name_ = list(UFC_people[UFC_people["fid"] == fighter_idd_].name)[0]
        name_2lines = fighter_name_.replace(" ","\n")  
        data[name_2lines] = my_fighters3.loc[:,["wins","defeats"]].values[i]

    plt.plot()
    data_for_hbar = pd.DataFrame(data)      

    data_transposed = data_for_hbar.transpose()
    data_transposed.plot(kind="barh", stacked=False, legend=None)
    plt.title(f"Notable fighters from {chosen_country}")

    blue_patch = mpatches.Patch(color='tab:blue', label='wins')
    orange_patch = mpatches.Patch(color='tab:orange', label='defeats')
    plt.legend(handles=[orange_patch, blue_patch])    
    plt.show()
 
def age_distribution_for(chosen_country):
    now = datetime.now()
    this_year = int(now.strftime("%Y"))      
       
    #for country population
    my_fighters = UFC_people[UFC_people["country"] == chosen_country]
    my_fighters2 = my_fighters["birth_date"]
    my_fighters3 = my_fighters2[my_fighters2.notna()]
    
    my_fighters_bdates = my_fighters3.str.slice(start=-4)
    my_fighters_bdates2 = list(map(int, my_fighters_bdates.values))         
    my_fighters_bdates3 = list(map((lambda x: this_year-x), my_fighters_bdates2))
    
    plt.subplot(1,2,1)
    plt.hist(my_fighters_bdates3, color ="blue")
    plt.xlabel("AGE (at the moment)")
    plt.ylabel("FIGHTERS")
    plt.title(f"Age of fighters from {chosen_country}")
    blue_patch = mpatches.Patch(color="blue", label=(f"{chosen_country}"))
    plt.legend(handles=[blue_patch]) 
    
    #for all population
    all_fighters = UFC_people["birth_date"]
    all_fighters2 = all_fighters[all_fighters.notna()]
    
    all_fighters_bdates = all_fighters2.str.slice(start=-4)
    all_fighters_bdates2 = list(map(int, all_fighters_bdates.values))         
    all_fighters_bdates3 = list(map((lambda x: this_year-x), all_fighters_bdates2))
    plt.subplot(1,2,2)
    
    plt.hist(all_fighters_bdates3, color ="grey")
    plt.xlabel("AGE (at the moment)")
    plt.title(f"Age of UFC fighters")
    grey_patch = mpatches.Patch(color="grey", label="world")
    plt.legend(handles=[grey_patch]) 
    #plt.show() 
    #https://www.youtube.com/watch?v=XDv6T4a0RNc&t=824s


#for later use
def get_photo():
    img = mpimg.imread("UFC_LOGO.png")
    fig, ax = plt.subplots()
    my_image = ax.imshow(img)
    patch = mpatches.Circle((260, 200), radius=200, transform=ax.transData)
    my_image.set_clip_path(patch)    
    plt.axis("off")
    plt.show()
    

#for later use
def country_(query_country):
    return (UFC_people["country"] == query_country)

def weightclass_(query_weightclass):
    return (UFC_people["weight"] == query_weightclass)

def height_(query_height):
    return (UFC_people["height"] == query_height)

def search_top_ratio(number, filter_):
    return(UFC_people.loc[filter_, "name"].head(number))

#x = search_top_ratio(15, country_("Poland"))    