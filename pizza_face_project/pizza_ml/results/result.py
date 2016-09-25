import csv, datetime, time, os
from pizza_ml.models import Pizza, Ingredient, UserProfile, PairPreferance
from django.contrib.auth.models import User
from pizza_ml.pairset.pairexp import prep_pairs, DIR_CSV 



"""
Result
are helpers functions for the views needing data from the resulst in the csv

- save_to_csv
- save_emails
- save_user_pairs_to_csv
- get_nationality
- get_results_dict
- get_user_pairs_dict
- get_user_all_pairs

"""

def save_to_csv(doc_new, name, new):
    # Saves all results on exisiting file
    doc_in = []
    file_csv = DIR_CSV + 'results/csv/'+ name + '.csv'
    
    # Check file exists
    if os.path.exists(file_csv) == True:
        if new == False:
            with open(file_csv, 'rb') as inText:
                reader = csv.reader(inText)
                for row in reader:
                    doc_in.append(row)
                inText.close()
        else:
            os.remove(file_csv)
            
    for doc in doc_new:
        doc_in.append(doc)
   
    
    
    # Store all information in a csv file
    with open(file_csv, 'w') as outText:
        writer = csv.writer(outText, delimiter=",")
        writer.writerow(doc_in[0])
    
        for i in range(1,len(doc_in)):
            writer.writerow(doc_in[i])
    outText.close()

def save_emails(username, email):
    # save emails
    e_doc=[]
    row=[]
    row.append(username)
    row.append(email)
    e_doc.append(row)
    save_to_csv(e_doc, 'email', False)

def save_user_to_csv(user, name, answer):
    user_pro = UserProfile.objects.get(user=user)
    
    doc_new=[]
    row=[]
    row.append(user.username)
    row.append(user_pro.dob)
    row.append(user_pro.gender)
    row.append(user_pro.allergies)
    row.append(user_pro.diet)
    row.append(user_pro.occupation)
    row.append(user_pro.nationality)
    row.append(answer)
    row.append(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
    
    # save all info to a csv file
    doc_new.append(row)
    
    save_to_csv(doc_new, name, False)

def save_user_pairs_to_csv(user, exp):
    # formats and then saves a users pair preferances to a csv file
    doc_new = []
    row =[]
    pairs = PairPreferance.objects.all()
    pairs = pairs.filter(user=user.id, exp_no=exp)
    for p in pairs:
        row=[p.exp_no,p.index,p.value,p.pic,p.time,p.t_at,p.date,p.browser,p.scrn_h,p.scrn_w,p.scroll_x, p.scroll_y]
        doc_new.append(row)
    name = 'users/' + user.username
    save_to_csv(doc_new, name+str(exp), True)

def get_nationality():
    context_dict = {}
    nat_list=[]
    file_csv = DIR_CSV + '/data/nations.csv'

    with open(file_csv, 'rb') as nat:
        reader = csv.reader(nat)
        for row in reader:
            country = {
                row[0] : row[1],
                row[2] : row[3]
            }
            nat_list.append(country)
    return { 'nationality' :nat_list}

def get_results_dict(name, exp):
    res_list=[]
    file_csv = DIR_CSV + 'results/csv/'+ name + '.csv'
    
    with open(file_csv, 'rb') as res:
        reader = csv.reader(res)
        for row in reader:
            users = {
                'username': row[0],
                'dob' : row[1],
                'gender' : row[2],
                'allergies': row[3],
                'diet': row[4],
                'occupation': row[5],
                'nationality': row[6],
                'permission' : row[-2],
                'completed time' : row[-1],
            }
                
            res_list.append(users)
    return { 'results' :res_list}

def get_user_pairs_dict(name, exp):
    # returns user pairs by experiement
    res_list=[]
    file_csv = DIR_CSV + 'results/csv/users/'+ name+str(exp) + '.csv'
    
    # Check file exists
    if os.path.exists(file_csv) == True:
        with open(file_csv, 'rb') as res:
            reader = csv.reader(res)
            for row in reader:
                if int(row[0]) == exp:
                    pairs = {
                        'exp_no': int(row[0]), 
                        'index' :  int(row[1]),
                        'value' :  int(row[2]),
                        'pic': row[3],
                        'time':  int(row[4]),
                        't_at': row[5],
                        'date': row[6],
                        'browser' : row[7],
                        'scrn_h' :  int(row[8]),
                        'scrn_w':  int(row[9]),
                        'scroll_x' :  int(row[10]),
                        'scroll_y' :  int(row[-1]),
                    }
                    res_list.append(pairs)
                else:
                    pass
        return { name : res_list}
    else:
        return { name : "False"}
   
def get_user_all_pairs(exp):
    # returns a dictionary of all user pair details dependent on the experement
    users = User.objects.all()
    all_pairs = []
    for u in users:
        all_pairs.append(get_user_pairs_dict(u.username, exp))
    return { 'exp_'+ str(exp) : all_pairs }