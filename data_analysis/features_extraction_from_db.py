#!/usr/bin/python

# This code is a compliment to "Covert lie detection using keyboard dynamics".
# Copyright (C) 2017  Riccardo Spolaor
# See GNU General Public Licence v.3 for more details.
# NO WARRANTY EXPRESSED OR IMPLIED. USE AT YOUR OWN RISK.

import MySQLdb
import json
import ast
import pandas as pd
from apsw import main
from numpy import mean, std
from copy import deepcopy



mobile_=0
N=5 #keystrokes


db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     port=13306,
                     user="???", # your username
                      passwd="????", # your password
                      db="??????") # name of the data base

# you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor() 

queryNOmobile="""
SELECT
            S.participant_id,
            A1.question_id,
            A1.text_answer, 
            A1.keystroke,
            A1.timestamp_prompted,
            A1.timestamp_first_digit,
            A1.timestamp_enter, 
            A1.timestamp_tap,
            A2.text_answer,
            A2.keystroke, 
            A2.timestamp_prompted,
            A2.timestamp_first_digit,
            A2.timestamp_enter,
            A2.timestamp_tap,
            S.session_id,
            S.mobile,
            P.first_name,
            P.last_name,
            P.email,
            P.birthday,
            P.education,
            P.job,
            P.visual_disease,
            P.lensorglass,
            P.mother_language,
            Q.text_short
            
            
FROM 
            participants as P,
            session as S,
            answers as A1, 
            answers as A2,
            questions as Q
WHERE 
            P.participant_id = S.participant_id AND
            S.session_id = A1.session_id AND 
            S.session_id = A2.session_id AND 
            A1.question_id = A2.question_id AND  
            S.mobile = %s AND
            Q.question_id=A1.question_id AND Q.language="italian" and
            S.current_question_index = 105 AND 
            A1.mind_condition = 1 AND 
            A2.mind_condition = 0 AND 
            P.participant_id>=34
ORDER BY S.participant_id, A1.question_id
#LIMIT 200
"""%mobile_


                
# Use all the SQL you like
print "query executing...",
cur.execute(queryNOmobile)
print "End"

def string_to_list_of_dict(st):
    #print st 
    st=st.replace("},{","}|{")
    st=st.replace("[","")
    st=st.replace("]","")
    st=st.replace(":\",\"",":\"comma\"")
    st=st.replace(":\":\"",":\"colon\"")
    st=st.replace(":\";\"",":\"period\"")
    st=st.replace(":\"\r\"",":\"ENTER\"")
    
    st=st.replace(":\',\'",":\'comma\'")
    st=st.replace(":\':\'",":\'colon\'")
    st=st.replace(":\';\'",":\'period\'")
    st=st.replace(":\'\r\'",":\'ENTER\'")
    
    #list of dictionaries
    st_l = st.split("|")
    st_list_dict=[]
    for elem in st_l:
        elem=elem.replace("{","")
        elem=elem.replace("}","")
        #just in case
        
        tmp=elem.split(",")
        tmp=[t.replace("\"","") for t in tmp]
        
        dict_tmp={}
        for t in tmp:
            k=t.split(":")
            #print k
            k1=k[1]
            if k[0] == "tn": # or k[0] == "t": #timestamp
                k1=float(k1)
            elif k[0]== "cod": #key code
                k1=int(k1)
            else:
                k1="%s"%k1  #character or UP/DOWN
            dict_tmp["%s"%k[0]]=k1
        st_list_dict.append(dict_tmp)
    st_final=sorted(st_list_dict, key=lambda k: k['tn']) 
    
#     tmp=0
#     for i in st_final:
#         print i["tn"]-tmp,
#         tmp=i["tn"]
#     print ""
#     
    
    return st_final


def keyrepetition_check(list_keys):
    
    keys=[]
    for keys_ in list_keys:
        for key_ in keys_:
            
            character=key_["character"]
            verse=key_["k"]
            if verse=="DOWN":
                keys.append(character)
            #timestamp=key_["tn"]
    
    consecutive=[]
    repetition_consecutive=0
    num_keys={}
    
    for i,III in enumerate(keys):
    
        if III not in num_keys.keys() :
            num_keys[III]=0
        num_keys[III]+=1
           
        if len(consecutive)>=1 and consecutive[-1] == III:
            consecutive.append(III)
            if len(consecutive)>repetition_consecutive:
                repetition_consecutive=len(consecutive)
            
        else:
            consecutive=[III]
    
    max_keys=0 ###the most repeated key
    for k in num_keys:
        if num_keys[k]>max_keys:
            max_keys=num_keys[k]
        
    return {"max_key_repeated":max_keys, "max_consecutive_key":repetition_consecutive}

def first_n_events(list_keys,n):
     
    used_shift=0
    count=0
    tmp_list_n=[]
    
    ##########TODO    
    
    
    for i,key_ in enumerate(list_keys):
        
        character=key_["character"]
        verse=key_["k"]
        key_code=key_["cod"]
        timestamp=key_["tn"]
        
        
        #Icount all the keystrokes
        
        if character=="u0010" or key_code==16:  #filter shift
            #current_sequence=sequence_interupted(current_sequence)
            if verse=="DOWN":
                used_shift+=1
            continue
        
        elif key_code==8:  #filter del
            continue
        
        #elif key_code==32:  #filter space
            #sequence_interupted() TODO is it interupted?
            #continue

        elif key_code==46:  #filter canc
            continue
        
        elif key_code>=112 and key_code<=122:  #filter f1 to f11
            continue
        
        elif key_code>=33 and key_code<=40:  #filter arrow and pagup
            continue
        
        elif key_code==13:  #filter ENTER
            continue 
            #End of digits!
        
        elif key_code==9 and key_code==225 and key_code==188 and key_code==18 and key_code==45 and key_code==17:  #filter tab, 
            continue
        
        else:
            tmp_list_n.append(key_)

    #list_n_keys=[None for i in range(n*2)] #N*2 sia up che down
    list_keys_verse=[]
    list_keys_delay=[]
    list_keys_up=[]
    list_keys_down=[]
    list_flight=[]
    list_press=[]
    
    
    previous=None
    previous_up=None
    previous_down=None
    for i,key_ in enumerate(tmp_list_n[:(n*2 + 1)]):
        if previous is None:
            previous=key_
        else:
            list_keys_verse.append(1.0 if key_["k"]=="UP" else 0.0)
            list_keys_delay.append(float(key_["tn"])-float(previous["tn"]))
            
        if key_["k"]=="UP":
            if previous_up is None:
                previous_up=key_
            else:
                list_keys_up.append(float(key_["tn"])-float(previous_up["tn"]))
            
            if previous_down is not None:
                list_flight.append(float(key_["tn"])-float(previous_down["tn"]))                             
        else:
            if previous_down is None:
                previous_down=key_
            else:
                list_keys_down.append(float(key_["tn"])-float(previous_down["tn"]))
            
            if previous_up is not None:
                list_press.append(float(key_["tn"])-float(previous_up["tn"]))
    
    
    features_n={"firstN_used_shift":used_shift,
                "firstN_both_mean":mean(list_keys_delay),    "firstN_both_std":std(list_keys_delay),  
                "firstN_up_mean":mean(list_keys_up),    "firstN_up_std":std(list_keys_up), 
                "firstN_down_mean":mean(list_keys_down),    "firstN_down_std":std(list_keys_down), 
                "firstN_flight_mean":mean(list_flight),    "firstN_flight_std":std(list_flight), 
                "firstN_press_mean":mean(list_press),       "firstN_press_std":std(list_press), 
                
                }
    
    
    listN_keys_verse=[0.5 for i in range(n*2)]
    listN_keys_delay=[-10000.0 for i in range(n*2)]
    listN_keys_up=[-10000.0 for i in range(n)]
    listN_keys_down=[-10000.0 for i in range(n)]
    listN_flight=[-10000.0 for i in range(n)]
    listN_press=[-10000.0 for i in range(n)]    
    
    for i,datum in enumerate(list_keys_verse[:(n*2)]):
        listN_keys_verse[i]=datum
        
    for i,datum in enumerate(list_keys_delay[:(n*2)]):
        listN_keys_delay[i]=datum
        
    for i,datum in enumerate(list_keys_up[:n]):
        listN_keys_up[i]=datum
        
    for i,datum in enumerate(list_keys_down[:n]):
        listN_keys_down[i]=datum
        
    for i,datum in enumerate(list_flight[:n]):
        listN_flight[i]=datum
        
    for i,datum in enumerate(list_press[:n]):
        listN_press[i]=datum
        
    ###################    
    
    for i,datum in enumerate(listN_keys_verse):
        features_n["firstN_verse_%s"%i]=datum
        
    for i,datum in enumerate(listN_keys_delay):
        features_n["firstN_both_%s"%i]=datum
        
    for i,datum in enumerate(listN_keys_up):
        features_n["firstN_up_%s"%i]=datum
        
    for i,datum in enumerate(listN_keys_down):
        features_n["firstN_down_%s"%i]=datum
        
    for i,datum in enumerate(listN_flight):
        features_n["firstN_fligth_%s"%i]=datum
        
    for i,datum in enumerate(listN_press):
        features_n["firstN_press_%s"%i]=datum
        
        
    return features_n


def first_n_events_labels(n):
     
    
        
    features_n_labels=["firstN_used_shift","firstN_both_mean","firstN_both_std",  
                "firstN_up_mean",    "firstN_up_std", 
                "firstN_down_mean",    "firstN_down_std", 
                "firstN_flight_mean",    "firstN_flight_std", 
                "firstN_press_mean",       "firstN_press_std", 
                
                ]
    
    
    listN_keys_verse=[0.5 for i in range(n*2)]
    listN_keys_delay=[-10000.0 for i in range(n*2)]
    listN_keys_up=[-10000.0 for i in range(n)]
    listN_keys_down=[-10000.0 for i in range(n)]
    listN_flight=[-10000.0 for i in range(n)]
    listN_press=[-10000.0 for i in range(n)]    
        
    ###################    
    
    for i,datum in enumerate(listN_keys_verse):
        features_n_labels.append("firstN_verse_%s"%i)
        
    for i,datum in enumerate(listN_keys_delay):
        features_n_labels.append("firstN_both_%s"%i)
        
    for i,datum in enumerate(listN_keys_up):
        features_n_labels.append("firstN_up_%s"%i)
        
    for i,datum in enumerate(listN_keys_down):
        features_n_labels.append("firstN_down_%s"%i)
        
    for i,datum in enumerate(listN_flight):
        features_n_labels.append("firstN_fligth_%s"%i)
        
    for i,datum in enumerate(listN_press):
        features_n_labels.append("firstN_press_%s"%i)
        
        
    return features_n_labels


def filter_unwanted_and_count(list_keys):
    tmp_list=[]
    
    #full_sequence=[]
    consecutive_press=[] #list of list
    
    current_sequence=[]
    
    def sequence_interupted(current_sequence):
        consecutive_press.append(current_sequence)
        return []
    #down only
    
    number_shift=0
    number_del=0
    number_canc=0
    number_arrow=0
    number_space=0
    
    time_key_before_enter_down=0.
    time_key_before_enter_up=0.
    time_key_before_enter_flight=0.
    
    
    previous_key_down=None
    previous_key_up=None
    
    time_key_before_enter_down_raw=0.
    time_key_before_enter_up_raw=0.
    time_key_before_enter_flight_raw=0.
    
    
    previous_key_down_raw=None
    previous_key_up_raw=None
    
    
    
    for i_, key_ in enumerate(list_keys):
        character=key_["character"]
        verse=key_["k"]
        key_code=key_["cod"]
        timestamp=float(key_["tn"])
        
        
        if character=="u0010" or key_code==16:  #filter shift
            #current_sequence=sequence_interupted(current_sequence)
            if verse=="DOWN":
                number_shift+=1
            continue
        
        elif key_code==8:  #filter del
            current_sequence=sequence_interupted(current_sequence)
            if verse=="DOWN":
                number_del+=1
            continue
        
        elif key_code==32:  #filter space
            #sequence_interupted() TODO is it interupted?
            if verse=="DOWN":
                number_space+=1
            #continue #now I consider the spaces too
        
        elif key_code==46:  #filter canc
            current_sequence=sequence_interupted(current_sequence)
            if verse=="DOWN":
                number_canc+=1
            continue
        
        elif key_code>=112 and key_code<=122:  #filter f1 to f11
            current_sequence=sequence_interupted(current_sequence)
            
            continue
        
        elif key_code>=33 and key_code<=40:  #filter arrow and pagup
            current_sequence=sequence_interupted(current_sequence)
            if verse=="DOWN":
                number_arrow+=1
            continue
        
        elif key_code==13:  #filter ENTER
            current_sequence=sequence_interupted(current_sequence)
            #filtered
            if previous_key_down is not None and verse=="DOWN":
                time_key_before_enter_down=timestamp - float(previous_key_down["tn"])                
            if previous_key_up is not None and verse=="UP":
                time_key_before_enter_up=timestamp - float(previous_key_up["tn"])
            if previous_key_up is not None and verse=="DOWN":
                time_key_before_enter_flight= timestamp - float(previous_key_up["tn"])
            
            #raw
            if previous_key_down_raw is not None and verse=="DOWN":
                time_key_before_enter_down_raw =timestamp - float(previous_key_down_raw["tn"])                
            if previous_key_up is not None and verse=="UP":
                time_key_before_enter_up_raw = timestamp - float(previous_key_up_raw["tn"])
            if previous_key_up is not None and verse=="DOWN":
                time_key_before_enter_flight_raw = timestamp - float(previous_key_up_raw["tn"])
                
            continue 
            #End of digits!
        
        elif key_code==9 and key_code==225 and key_code==188 and key_code==18 and key_code==45 and key_code==17:  #filter tab, 
            current_sequence=sequence_interupted(current_sequence)
            continue
        
        else:
            if verse=="DOWN":
                previous_key_down=key_
            elif verse=="UP":
                previous_key_up=key_
                
            current_sequence.append(key_)
        
        if verse=="DOWN":
                previous_key_down_raw=key_
        elif verse=="UP":
            previous_key_up_raw=key_
            
        #Icount all the keystrokes
        tmp_list.append(key_)
        
        
            
    #sequence_interupted()
    
    return {"number_shift":number_shift,
            "number_del":number_del,
            "number_canc":number_canc,
            "number_arrow":number_arrow,
            "number_space":number_space,
            "consecutive_press":consecutive_press,
            "consecutive_raw":[tmp_list],
            "time_key_before_enter_down":time_key_before_enter_down,
            "time_key_before_enter_up":time_key_before_enter_up,
            "time_key_before_enter_flight":time_key_before_enter_flight,
            "time_key_before_enter_down_raw":time_key_before_enter_down_raw,
            "time_key_before_enter_up_raw":time_key_before_enter_up_raw,
            "time_key_before_enter_flight_raw":time_key_before_enter_flight_raw,
            }

def series_statistics_extraction(label,series_):
    serie = pd.Series(series_)
         
    stats={}
    methods=["max","min","median","mad","std","kurt","var","mean","skew"]
    def get_value(pkts, method, params=None):   
            #print('get value %s on obj count %s ' % (method, pkts.count())
            try:
                res = getattr(pkts, method)() if params is None else getattr(pkts, method)(params) 
            except ZeroDivisionError:
                return 0.0
            is_nul=not pd.notnull(res)
            if res is None or is_nul:
                return 0.0
            else:
                return res 
            
    for method in methods:
        tmp=get_value(serie, method)
        stats[label+"_"+method]= tmp
            
            
        #quantile
    
    for i in range(1,10,1):
        stats[label+"_quantile%s"%(i*10)]=get_value(serie, "quantile",i/10.0)
                
    #number of packets
    stats[label+"_length"]=len(serie)

    """
    for w in range(int(max_length/(window_size/2))):
        for serie in [pkt_total_sizes, pkt_in_sizes,  pkt_out_sizes]:
            serie_w=serie[w*(window_size/2):w*(window_size/2)+window_size]
            for method in methods:
                stats.append(get_value(serie_w, method)) 
                
            #quantile
              
                for i in range(1,10,1):
                    stats.append(get_value(serie_w, "quantile",i/10.0))
                    
                #number of packets
                stats.append(len(serie_w))
    """    
    
    
    return stats

def series_statistics_labels(label=None):
    
         
    labels=["max","min","median","mad","std","kurt","var","mean","skew"]
            
            
        #quantile
          
    for i in range(1,10,1):
        labels.append("quantile%s"%(i*10))
            
        #number of packets
    labels.append("length")

    """
    for w in range(int(max_length/(window_size/2))):
        for serie in [pkt_total_sizes, pkt_in_sizes,  pkt_out_sizes]:
            serie_w=serie[w*(window_size/2):w*(window_size/2)+window_size]
            for method in methods:
                stats.append(get_value(serie_w, method)) 
                
            #quantile
              
                for i in range(1,10,1):
                    stats.append(get_value(serie_w, "quantile",i/10.0))
                    
                #number of packets
                stats.append(len(serie_w))
    """    
    
    
    return labels


def series_keystrokes_consecutive(list_dict_consecutive):
    series2_up=[]
    series2_down=[]
    series2_flight=[]
    series2_press=[]
    series2_both=[]
    
    series3_up=[]
    series3_down=[]
    series3_both=[]
    
    breakers=0 #down before up
    
    #list of consecutive keystrokes
    for keystrokes_ in list_dict_consecutive:
        #consecutive keystrokes
        previous_up=None
        previous_down=None
        
        previous_key=None
    
        #for TRIGRAPH
        previous2_up=None
        previous2_down=None
        
        previous2_key=None
    
    
        #I ignore the sequence of only 1 element
        if len(keystrokes_)<=1:
            continue
        
        
        for key_ in keystrokes_:
            
            character=key_["character"]
            verse=key_["k"]
            key_code=key_["cod"]
            timestamp=key_["tn"]
            
            
            #there are 2 consecutive down or 2 up
            if previous_key is not None and previous_key["k"]==verse:
                breakers+=1 
                #print previous_key["character"], key_["character"] #
            
            if verse=="UP":
                #DIGRAPH
                if previous_up is not None:
                    series2_up.append( timestamp - previous_up["tn"] )
                
                if previous_down is not None and previous_down["cod"]==key_code:
                    series2_press.append(timestamp - previous_down["tn"])
                
                #TRIGRAPH
                if previous2_up is not None:
                    series3_up.append( timestamp - previous2_up["tn"] )
                
                if previous2_down is not None:
                    series3_both.append( timestamp - previous2_down["tn"] )
                
                
                
                previous2_up=previous_up
                previous_up=key_
                
                
            elif verse=="DOWN":
                #DIGRAPH
                if previous_down is not None:
                    series2_down.append( timestamp - previous_down["tn"] )
                if previous_up is not None: 
                    series2_flight.append(timestamp - previous_up["tn"])
                
                #TRIGRAPH
                if previous2_down is not None:
                    series3_down.append( timestamp - previous2_down["tn"] )
                
                
                previous2_down=previous_down
                previous_down=key_
                
            #both
            if previous_key is not None:
                series2_both.append(timestamp - previous_key["tn"])
                    
            previous2_key=previous_key
            previous_key=key_
#     
#     if breakers>6:
#         for elem in list_dict_consecutive:
#             for i in elem :
#                 print i
#             print "-----------------------"
#             
#         print "############################"
#     
    return {"series_di_both":series2_both,
            "series_di_up":series2_up,
            "series_di_down":series2_down,
            "series_di_flight":series2_flight,
            "series_di_press":series2_press,
            "series_tri_up":series3_up,
            "series_tri_down":series3_down,
            "series_tri_both":series3_both,
            "breakers":breakers #significant only on UP and DOWN   
            } 


###################################################################
####################### main ######################################
###################################################################
only_down_sessions=[]
all_sessions=[]

DATA_only_down={}
DATA_UPandDOWN={}
data={}

users_unreliable=[]
std_sex=None

# print all the first cell of all the rows
for row in cur.fetchall() :
    """
    0    S.participant_id,
    1    A1.question_id,
    2    A1.text_answer, 
    3    A1.keystroke,
    4    A1.timestamp_prompted,
    5    A1.timestamp_first_digit,
    6    A1.timestamp_enter, 
    7    A1.timestamp_tap,
    8    A2.text_answer,
    9    A2.keystroke, 
    10   A2.timestamp_prompted,
    11   A2.timestamp_first_digit,
    12   A2.timestamp_enter,
    13   A2.timestamp_tap,
    14   S.session_id
    15   S.mobile
    16    P.first_name,
    17   P.last_name,
    18   P.email,
    19   P.birthday,
    20   P.education,
    21   P.job
    22   P.visual_disease,
    23   P.lensorglass,
    24   P.mother_language,
    25    A1.text_short
    
    - P.sex
    """    
    participant_id = row[0]
    question_id = row[1]
    answer_true = row[2]
    json_keystroke_true = row[3]
    answer_false = row[8]
    json_keystroke_false = row[9]
    session_id=row[14]
    mobile=row[15]
    first_name=row[16]
    last_name=row[17]
    email=row[18]
    birthday=row[19]
    education=row[20]
    job=row[21]
    visual_disease="No" if row[22]=="" else row[22]
    lensorglass=row[23]
    mother_language=row[24]
    text_short=row[25]
    
        
    
    
    if participant_id in users_unreliable:
        continue
    
    if participant_id not in data.keys():
        data[participant_id]=[]
        #get the sex of the participant
        cur1 = db.cursor() 
        query_sex="""
            SELECT A.text_answer
            FROM answers A, session S
            WHERE A.question_id=0 and A.mind_condition=1 and A.session_id=S.session_id and S.participant_id=%s
            """%(participant_id)
        cur1.execute(query_sex)


        femminile=["d",
            "donna",
            "f",
            "fammina",
            "female",
            "femmile",
            "femmin",
            "Femmina",
            "femmina",
            "femminikle",
            "femminile",
            "femmo",]

        maschile=[
            "m",
            "machile",
            "marchile",
            "maschike",
            "maschile",
            "maschio",
            "uomo",
        ]    

        """
        unreliables
        Spesso
        tanto
        Tito
        kdoihebwkdo
        """
        
        sex_=cur1.fetchall()
        
        sex_=sex_[0][0].strip().lower()
        if sex_ in maschile:
            std_sex="M"
        elif sex_ in femminile or "femmina" in sex_:
            std_sex="F"

        else:
            users_unreliable.append(participant_id)
            continue
        



    
    
    #some filtering
    if answer_true.strip().lower()==answer_false.strip().lower():
        #the answer is the same
        continue #skip
    elif len(answer_true.strip().lower())<=2 or len(answer_false.strip().lower())<=2:
        #one of the two answer is shorter than 2 char
        continue
    elif "it" not in mother_language.lower() or "tali" not in mother_language.lower(): #lingua italiana 
        continue
    
    tmp={"participant_id":participant_id,"mobile":mobile,"question_id":question_id, "session_id":session_id, "true_answer":answer_true,"false_answer":answer_false }
    
    tmp["true_prompted-firstdigit"]=float(row[5])-float(row[4])
    tmp["true_firstdigit-enter"]=float(row[6])-float(row[5])
    tmp["true_prompted-enter"]=float(row[6])-float(row[4])
    tmp
    
    tmp["false_prompted-firstdigit"]=float(row[11])-float(row[10])
    tmp["false_firstdigit-enter"]=float(row[12])-float(row[11])
    tmp["false_prompted-enter"]=float(row[12])-float(row[10])
    
    tmp["true_answer_length"]=len(answer_true.strip())
    tmp["false_answer_length"]=len(answer_false.strip())
    
    tmp["first_name"]=first_name
    tmp["last_name"]=last_name
    tmp["email"]=email
    tmp["birthday"]=birthday
    tmp["age"]= 2015 - int(("%s"%birthday)[:4])
    
    education_=None
    if education=="0":
        education_="medium"
    elif education=="1":
        education_="high"
    elif education=="2":
        education_="Bachelor"
    elif education=="3":
        education_="Master"
    elif education=="4":
        education_="PhD"
    
    tmp["education"]=education_
    tmp["job"]=job
    tmp["visual_disease"]=visual_disease
    tmp["lens_or_glass"]=lensorglass
    tmp["mother_language"]=mother_language
    tmp["question_text"]=text_short
    tmp["sex"]=std_sex
    
    obj_true=string_to_list_of_dict(json_keystroke_true)
    features_N_true=first_n_events(obj_true,N)
    features_true = filter_unwanted_and_count(obj_true)
    series_true = series_keystrokes_consecutive(features_true["consecutive_press"])
    series_true_raw = series_keystrokes_consecutive(features_true["consecutive_raw"])
    
    repetitions_true=keyrepetition_check(features_true["consecutive_press"])
    tmp["true_max_key_repetition"]=repetitions_true["max_key_repeated"]
    tmp["true_max_key_consecutive"]=repetitions_true["max_consecutive_key"]
    
    
    tmp["true_number_shift"]=features_true["number_shift"]
    tmp["true_number_del"]=features_true["number_del"]
    tmp["true_number_canc"]=features_true["number_canc"]
    tmp["true_number_arrow"]=features_true["number_arrow"]
    tmp["true_number_shift"]=features_true["number_shift"]
    tmp["true_number_shift"]=features_true["number_shift"]
    tmp["true_number_space"]=features_true["number_space"]
    tmp["true_number_delcanc"]=features_true["number_del"]+features_true["number_canc"]
    
    tmp["true_time_key_before_enter_down"]=features_true["time_key_before_enter_down"]
    tmp["true_time_key_before_enter_up"]=features_true["time_key_before_enter_up"]
    tmp["true_time_key_before_enter_flight"]=features_true["time_key_before_enter_flight"]
    tmp["true_time_key_before_enter_down_raw"]=features_true["time_key_before_enter_down_raw"]
    tmp["true_time_key_before_enter_up_raw"]=features_true["time_key_before_enter_up_raw"]
    tmp["true_time_key_before_enter_flight_raw"]=features_true["time_key_before_enter_flight_raw"]
    
    tmp["true_breakers"]=series_true["breakers"]        
    
    for lab in first_n_events_labels(N):
        tmp["true_%s"%(lab)]=features_N_true[lab]
    
    
    
    obj_false=string_to_list_of_dict(json_keystroke_false)
    features_N_false=first_n_events(obj_false,N)
    features_false = filter_unwanted_and_count(obj_false)
    series_false = series_keystrokes_consecutive(features_false["consecutive_press"])
    series_false_raw = series_keystrokes_consecutive(features_false["consecutive_raw"])
    
    repetitions_false=keyrepetition_check(features_false["consecutive_press"])
    tmp["false_max_key_repetition"]=repetitions_false["max_key_repeated"]
    tmp["false_max_key_consecutive"]=repetitions_false["max_consecutive_key"]
    
    tmp["false_number_shift"]=features_false["number_shift"]
    tmp["false_number_del"]=features_false["number_del"]
    tmp["false_number_canc"]=features_false["number_canc"]
    tmp["false_number_arrow"]=features_false["number_arrow"]
    tmp["false_number_shift"]=features_false["number_shift"]
    tmp["false_number_shift"]=features_false["number_shift"]
    tmp["false_number_space"]=features_false["number_space"]
    tmp["false_number_delcanc"]=features_false["number_del"]+features_false["number_canc"]
    tmp["false_time_key_before_enter_down"]=features_false["time_key_before_enter_down"]
    tmp["false_time_key_before_enter_up"]=features_false["time_key_before_enter_up"]
    tmp["false_time_key_before_enter_flight"]=features_false["time_key_before_enter_flight"]
    tmp["false_time_key_before_enter_down_raw"]=features_false["time_key_before_enter_down_raw"]
    tmp["false_time_key_before_enter_up_raw"]=features_false["time_key_before_enter_up_raw"]
    tmp["false_time_key_before_enter_flight_raw"]=features_false["time_key_before_enter_flight_raw"]
    tmp["false_breakers"]=series_false["breakers"]
    for lab in first_n_events_labels(N):
        tmp["false_%s"%(lab)]=features_N_false[lab]
    
    
    series_stats={}
    
    for mode in ["filtered","raw"]:
        
        for  mind in ["true","false"]:
            
            if mind =="true":   
                serie = series_true if mode=="filtered" else series_true_raw
            else:
                serie = series_false if mode=="filtered" else series_false_raw
                    
            for label in serie:
                if label =="breakers":
                    continue
                
                series_stats[label]=series_statistics_extraction("%s_%s_"%(mind,mode)+label, serie[label])
                for label_1 in  series_stats:
                    for label_2 in series_stats[label_1]:
                        tmp[label_2]=series_stats[label_1][label_2]
            
        
    
                
    #print tmp
    #print "-------------------------------------------"
    
    #for i,label in enumerate(tmp):
    #    print i,label
    #answer_true,features_true
    
    #print json_keystroke_true
    #print json.load(json_keystroke_true)
    #data[participant_id]["keystroke_true"]=json.load(json_keystroke_true)
    #data[participant_id]["keystroke_false"]=json.load(json_keystroke_false)
    
    tmp["DOWN_only"]=0
    #finally
    for l in tmp:
        if tmp[l] == 0  and "up_length" in l: #and "kurt" not in l and "skew" not in l and l!="question id":
            #HAS only DOWN
            tmp["DOWN_only"]=1
            
            if tmp["session_id"] not in only_down_sessions:
                only_down_sessions.append(tmp["session_id"])
            break
        
            
    
    if tmp["session_id"] not in all_sessions:
        all_sessions.append(tmp["session_id"])
        
    #, #tmp["answer_true"], tmp["answer_false"], l, tmp
    
    ####inserting in the right dict
    if tmp["DOWN_only"]==1:
        if participant_id not in DATA_only_down.keys():
            DATA_only_down[participant_id]=[]
        DATA_only_down[participant_id].append(tmp)
        
    else:       
        if participant_id not in DATA_UPandDOWN.keys():
            DATA_UPandDOWN[participant_id]=[]
        DATA_UPandDOWN[participant_id].append(tmp)
        
    data[participant_id].append(tmp)

    
    
#creazione labels
labels_data_base=["participant_id","first_name","last_name","email","age","mother_language","sex","education","job","visual_disease","lens_or_glass","mobile","DOWN_only","question_id","question_text","session_id","true_answer","false_answer","birthday"]
labels_data=deepcopy(labels_data_base)    

#data_distinct=[]


for mind in ["true","false"]:
    labels_data.append("%s_answer_length"%mind)
    labels_data.append("%s_breakers"%mind)
    
    
    
    times=["prompted-firstdigit","firstdigit-enter","prompted-enter"]
    for time_ in times:
        labels_data.append("%s_%s"%(mind,time_))
    
    labels_data.append("%s_max_key_repetition"%mind)
    labels_data.append("%s_max_key_consecutive"%mind)
        
        
    series_=["series_di_both", "series_di_up","series_di_down","series_di_flight","series_di_press","series_tri_both", "series_tri_up","series_tri_down"]
    stats_labels=series_statistics_labels()#label)
    
    for mode in ["filtered","raw"]:
        for serie_type in series_:
            for stat in stats_labels:
                labels_data.append("%s_%s_%s_%s"%(mind,mode,serie_type,stat))
    
    
    
    number_=["shift", "del","canc","shift","space","delcanc","arrow",]
    
    for num in number_:
        labels_data.append("%s_number_%s"%(mind,num))
    
    time_=["time_key_before_enter_down","time_key_before_enter_up","time_key_before_enter_flight","time_key_before_enter_down_raw","time_key_before_enter_up_raw","time_key_before_enter_flight_raw"]
    for time in time_:
        labels_data.append("%s_%s"%(mind,time))
        
    for lab in first_n_events_labels(N):
        labels_data.append("%s_%s"%(mind,lab))
        
    
    

file_o=open("list_features.txt","w")    
print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
for i,lab in enumerate(labels_data):
    file_o.write("\"%s\",\n"%(lab))
    print lab  
    

    

print "only_down_sessions=", len(only_down_sessions), " and all_sessions=", len(all_sessions)



import csv,gzip


file_="data_NOMobile_" if mobile==0 else "data_Mobile_"
marker_= "_filter7"


with open(file_+"all"+marker_+".csv", 'wb') as f:  # Just use 'w' mode in 3.x
    w = csv.DictWriter(f, labels_data)
    w.writeheader()
    for part in sorted(data):
        for row in data[part]:
            w.writerow(row)
    
with open(file_+"DOWNonly"+marker_+".csv", 'wb') as f:  # Just use 'w' mode in 3.x
    w = csv.DictWriter(f, labels_data)
    w.writeheader()
    for part in sorted(DATA_only_down):
        for row in DATA_only_down[part]:
            w.writerow(row)
            
with open(file_+"UPandDOWN"+marker_+".csv", 'wb') as f:  # Just use 'w' mode in 3.x
    w = csv.DictWriter(f, labels_data)
    w.writeheader()
    for part in sorted(DATA_UPandDOWN):
        for row in DATA_UPandDOWN[part]:
            w.writerow(row)
            
