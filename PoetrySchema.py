
# coding: utf-8

# In[3]:

import numpy as np
import schemabank as sb 


def GenPoetryReadingSchema():
   

   
   #GENERATE THE PEOPLE ORDER
   arr_people = np.arange(sb.SchemaBank("howmany_people"))
   np.random.shuffle(arr_people)
   #GENERATE THE DRINK ORDER
   arr_drink = np.arange(sb.SchemaBank("howmany_drink"))
   np.random.shuffle(arr_drink)
   #GENERATE THE DESSERT ORDER
   arr_dessert = np.arange(sb.SchemaBank("howmany_dessert"))
   np.random.shuffle(arr_dessert)
   
   
   #DETERMINE ROLES
   roles = {
           "Subject": sb.SchemaBank("person" + str(arr_people[0])),
           "Friend": sb.SchemaBank("person" + str(arr_people[1])),
           "Emcee": sb.SchemaBank("person" + str(arr_people[2])),
           "Poet": sb.SchemaBank("person" + str(arr_people[3])),
           "Drink_bought": sb.SchemaBank("drink" + str(arr_drink[0])),
           "Dessert_bought": sb.SchemaBank("dessert" + str(arr_dessert[0]))
       }
   
   #SET THE STATES
   states = {
       "Begin": 1,
       "Order_drink": 0,
       "Too_expensive": 0,
       "Sit_down": 0,
       "Stand_up": 0,
       "Emcee_intro": 0,
       "Poet_performs": 0,
       "Subject_performs": 0,
       "Subject_declines": 0,
       "Say_goodbye": 0,
       "Order_dessert": 0,
       "End":0,

   }
   
   #SET THE NARRATIVE STRING
   NARRATIVE = ""
   ORDER_OF_EVENTS = ""
   
   #GENERATE THE NARRATIVE STRING WITH CONDITIONALS
   while states["End"] == 0:
       
       #BEGIN
       if states["Begin"] == 1:
           NARRATIVE = NARRATIVE + roles["Subject"].name + " walked into the coffee shop on poetry night."
           ORDER_OF_EVENTS = ORDER_OF_EVENTS + "BEGIN => "
           states["Begin"] = 0
           dice = np.random.uniform()
           if roles["Subject"].hungry == "yes":
               if dice < .8:
                   states["Order_drink"] = 1
               else:
                   states["Sit_down"] = 1
           else:
               if dice < .4:
                   states["Order_drink"] = 1
               else:
                   states["Sit_down"] = 1
                   
       #ORDER_DRINK            
       elif states["Order_drink"] == 1:
           NARRATIVE = NARRATIVE + roles["Subject"].pronoun_u +  " walked up to the counter and decided on a " + roles["Drink_bought"].name + "."
           ORDER_OF_EVENTS = ORDER_OF_EVENTS + "ORDER DRINK => "
           states["Order_drink"] = 0
           dice = np.random.uniform()
           if roles["Drink_bought"].price > 4:
               if dice < .8:
                   states["Too_expensive"] = 1
               elif dice < .9:
                   states["Sit_down"] = 1
               else:
                   states["Stand_up"] = 1
           else:
               if dice < .4:
                   states["Sit_down"] = 1
               else:
                   states["Stand_up"] = 1
                   
       #TOO_EXPENSIVE
       elif states["Too_expensive"] == 1:
           NARRATIVE = NARRATIVE + " But after hearing how expensive it was, " +  roles["Subject"].pronoun_l +\
           " cancelled the order."
           ORDER_OF_EVENTS = ORDER_OF_EVENTS + "TOO EXPENSIVE => "
           states["Too_expensive"] = 0
           dice = np.random.uniform()
           if dice < .5:
               states["Sit_down"] = 1
           else:
               states["Stand_up"] = 1
                  
       #SIT_DOWN
       elif states["Sit_down"] == 1:
           NARRATIVE = NARRATIVE + roles["Subject"].pronoun_u +" found an empty chair next to " +\
           roles["Friend"].name + ". '" + roles["Friend"].greeting + ", " + roles["Subject"].name + "!' said " +\
           roles["Friend"].name + ". '" + roles["Subject"].greeting + ", " + roles["Friend"].name + "!' " +\
           roles["Subject"].name + " replied."  
           ORDER_OF_EVENTS = ORDER_OF_EVENTS + "SIT DOWN => "
           states["Sit_down"] = 0
           states["Listen_to_poetry"] = 1   
           dice = np.random.uniform()
           if dice < .5:
               states["Emcee_intro"] = 1
           else:
               states["Poet_performs"] = 1
               
       #STAND_UP
       elif states["Stand_up"] == 1:
           NARRATIVE = NARRATIVE + roles["Subject"].pronoun_u + " saw " + roles["Friend"].name + " standing in"\
           " the back and walked over to them. '" + roles["Friend"].greeting + ", " + roles["Subject"].name + "!' said " +\
           roles["Friend"].name + ". '" + roles["Subject"].greeting + ", " + roles["Friend"].name + "!' " +\
           roles["Subject"].name + " replied." 
           ORDER_OF_EVENTS = ORDER_OF_EVENTS + "STAND UP => "
           states["Stand_up"] = 0
           dice = np.random.uniform()
           if dice < .7:
               states["Emcee_intro"] = 1
           else:
               states["Poet_performs"] = 1
               
       
       #EMCEE_INTRO
       elif states["Emcee_intro"] == 1:
           NARRATIVE = NARRATIVE + " " + roles["Emcee"].name + ", who was the emcee for tonight, walked "\
           "to the front of the room and introduced the first poet, " + roles["Poet"].name + "."
           ORDER_OF_EVENTS = ORDER_OF_EVENTS + "EMCEE INTRO => "
           states["Emcee_intro"] = 0
           states["Poet_performs"] = 1
           
       #POET_PERFORMS
       elif states["Poet_performs"] == 1:
           NARRATIVE = NARRATIVE + " " + roles["Poet"].name +  " stepped up to the microphone and read "\
            "the poem that " + roles["Poet"].pronoun_l +  " had written: '" + roles["Poet"].poem + "' The crowd snapped their fingers politely."
           ORDER_OF_EVENTS = ORDER_OF_EVENTS + "POET PERFORMS => "
           states["Poet_performs"] = 0
           dice = np.random.uniform()
           if roles["Subject"].mood == "nervous":
               if dice < .8:
                   states["Subject_declines"] = 1
               else:
                   states["Subject_performs"] = 1
           elif roles["Subject"].mood == "happy":
               if dice < .1:
                   states["Subject_declines"] = 1
               else:
                   states["Subject_performs"] = 1
           else:
               if dice < .3:
                   states["Subject_declines"] = 1
               else:
                   states["Subject_performs"] = 1
                   
               
       #SUBJECT_DECLINES
       elif states["Subject_declines"] == 1:
           NARRATIVE = NARRATIVE + " " + roles["Subject"].name +  " had also written a poem, but "\
                      "decided that " + roles["Subject"].pronoun_l +  " wasn't in the mood to share it today."
           ORDER_OF_EVENTS = ORDER_OF_EVENTS + "SUBJECT DECLINES => "
           states["Subject_declines"] = 0
           states["Say_goodbye"] = 1
           
       #SUBJECT_PERFORMS
       elif states["Subject_performs"] == 1:
           NARRATIVE = NARRATIVE + " " + roles["Subject"].name +  " then took at turn at the microphone:'" +\
                      roles["Subject"].poem + "' When " + roles["Subject"].pronoun_l +  " sat back down, " + \
                                roles["Friend"].name +  " said that " + roles["Friend"].pronoun_l +  " loved the poem."
           ORDER_OF_EVENTS = ORDER_OF_EVENTS + "SUBJECT PERFORMS => "
           states["Subject_performs"] = 0
           states["Say_goodbye"] = 1
           
       #SAY_GOODBYE
       elif states["Say_goodbye"] == 1:
           NARRATIVE = NARRATIVE + " After all the poets had performed, " + roles["Subject"].name +\
           " and " + roles["Friend"].name +  " said their goodbyes and walked toward the door."
           ORDER_OF_EVENTS = ORDER_OF_EVENTS + "SAY GOODBYE => "
           states["Say_goodbye"] = 0
           dice = np.random.uniform()
           if roles["Subject"].hungry == "yes":
               if dice < .7:
                   states["Order_dessert"] = 1
               else:
                   states["End"] = 1
           else:
               if dice < .1:
                   states["Order_dessert"] = 1
               else:
                   states["End"] = 1
                   
       #ORDER_DESSERT
       elif states["Order_dessert"] == 1:
           NARRATIVE = NARRATIVE + " On the way out, " + roles["Subject"].name + " ordered a " +\
           roles["Dessert_bought"].name +  " to take home. The barista took one from the " + roles["Dessert_bought"].location +\
           " and wrapped it up to go."
           ORDER_OF_EVENTS = ORDER_OF_EVENTS + "ORDER DESSERT => "
           states["Order_dessert"] = 0
           states["End"] = 1 
           
       
               
   #END
   NARRATIVE = NARRATIVE + " " + roles["Subject"].name +  " made a mental note to come back again next week."
   ORDER_OF_EVENTS = ORDER_OF_EVENTS + "END"

           
       
               
       
       
   
   #print(ORDER_OF_EVENTS)
   return NARRATIVE
       
       

   


# In[ ]:



