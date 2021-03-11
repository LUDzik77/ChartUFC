from ChartUFC_additional import *

### FAST CHECKS ###
#print(UFC_people.columns)
#print(UFC_people)
#print(UFC_people.shape)
#print(UFC_people.info())
#print(UFC_people.shape)
#print(UFC_people[["name","fid"]])
#print(UFC_people[fid])
#print(UFC_fights.columns)      

def country_info(chosen_country):
      fig = plt.figure(figsize=(9.6, 7.2))
      fig.canvas.set_window_title(f'{chosen_country} in the UFC (part1)')
      #first page:
      perc_fighters_for(chosen_country)
      perc_victories_for(chosen_country)
      locality_for(chosen_country)
      weightclass_for(chosen_country)
         
      #second page:   
      important_fighters_for(chosen_country)     
      #third page:
      age_distribution_for(chosen_country)
      plt.show() 

if __name__== '__main__':
      query = input("Choose a country: ")
      while True:
            if query in list(UFC_people["country"]):
                  country_info(query)
                  exit()
            else: 
                  query = input("Choose an existing country: ")



