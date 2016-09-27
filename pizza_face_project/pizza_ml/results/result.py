import csv, datetime, time, os
from pizza_ml.models import Pizza, Ingredient, UserProfile, PairPreferance
from django.contrib.auth.models import User
from pizza_ml.pairset.pairexp import prep_pairs, DIR_CSV 



"""
Result
are helpers functions for the views needing data from the resulst in the csv

db updates
- is_exp
- set_permission
- get_user_emails
- get_user_details
- get_all_user_details
- get_user_pairs
- get_all_users_pairs

csv updates
- save_to_csv
- save_emails
- save_user_pairs_to_csv
- get_nationality
- get_results_csv
- get_user_pairs_csv
- get_user_all_pairs
- get_user_csv

"""

def is_exp(user,exp):
    if PairPreferance.objects.filter(user=user.id, exp_no = exp):
        return True
    else:
        return False

# Set for results to db
def set_permission(user, permission):
    user_pro = UserProfile.objects.get(user=user)
    user_pro.permission = permission
    user_pro.save()

# Getters for results fomr databas
def get_user_emails(answer):
    username=[]
    mail=[]
    users = User.objects.all()
    users_p = UserProfile.objects.all()
    for user in users_p:
        print user.permission, user
        if user.permission==answer:
            username.append(user.user.username)
            mail.append(user.user.email)
        else:
            pass
    return {'username': username, 'mail' :  mail,}

def get_user_details(user):
    user_pro = UserProfile.objects.get(user=user)
    return [user.username, user_pro.dob, user_pro.gender, user_pro.allergies, user_pro.diet, user_pro.occupation, user_pro.nationality, user_pro.permission, datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S') ]

def get_all_user_details(exp):
    username=[]
    dob=[]
    gender=[]
    allergies=[]
    diet=[]
    occupation=[]
    nationality=[]
    permission=[]
    completed=[]
    users = User.objects.all()
    for u in users:
        if is_exp(u,exp) ==True:
            row = get_user_details(u)
            username.append(row[0])
            dob.append(row[1])
            gender.append(row[2])
            allergies.append(row[3])
            diet.append(row[4])
            occupation.append(row[5])
            nationality.append(row[6])
            permission.append(row[-2])
            completed.append(row[-1])
        else:
            pass
    return {
            'username': username,
            'dob' : dob,
            'gender' : gender,
            'allergies': allergies,
            'diet': diet,
            'occupation': occupation,
            'nationality': nationality,
            'permission' : permission,
            'completed time' : completed,
            }
    
def get_user_pairs(user, exp):
    print user
    pairs = PairPreferance.objects.filter(user=user.id, exp_no=exp)
    
    # returns user pairs by experiement
    res_list=[]
    index=[]
    value=[]
    pic=[]
    time=[]
    t_at=[]
    date=''
    browser=''
    scrn_h=[]
    scrn_w=[]
    scroll_x=[]
    scroll_y=[]
    
    # Check pairs for experiment
    for p in pairs:
        if p.exp_no == exp:
            index.append( p.index )
            value.append( p.value )
            pic.append( p.pic )
            time.append( p.time )
            t_at.append( p.t_at )
            date = p.date
            browser = p.browser
            scrn_h.append( p.scrn_h )
            scrn_w.append( p.scrn_w )
            scroll_x.append( p.scroll_x )
            scroll_y.append( p.scroll_y )
        else:
            pass
    pairs = {
            'exp_no': exp, 
            'index' :  index,
            'value' :  value,
            'pic': pic,
            'time':  time,
            't_at': t_at,
            'date': date,
            'browser' : browser,
            'scrn_h' :  scrn_h,
            'scrn_w':  scrn_w,
            'scroll_x' :  scroll_x,
            'scroll_y' :  scroll_y,
            }
    res_list.append(pairs)
    return { user.username : res_list}

def get_all_users_pairs(exp):
    # returns a dictionary of all users pairs from database
    users = User.objects.all()
    all_pairs = []
    for u in users:
        all_pairs.append(get_user_pairs(u, exp))
    return { 'exp_'+ str(exp) : all_pairs }

# Setters for results to CSV
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

def save_emails_csv(username, email):
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
        print p.value
        row=[p.exp_no,p.index,p.value,p.pic,p.time,p.t_at,p.date,p.browser,p.scrn_h,p.scrn_w,p.scroll_x, p.scroll_y]
        doc_new.append(row)
    name = 'users/' + user.username
    save_to_csv(doc_new, name+str(exp), True)

# Getters for results to CSV
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

def get_results_csv(name, exp):
    username=[]
    dob=[]
    gender=[]
    allergies=[]
    diet=[]
    occupation=[]
    nationality=[]
    permission=[]
    completed=[]
    file_csv = DIR_CSV + 'results/csv/'+ name + '.csv'
    
    with open(file_csv, 'rb') as res:
        reader = csv.reader(res)
        for row in reader:
            username.append(row[0])
            dob.append(row[1])
            gender.append(row[2])
            allergies.append(row[3])
            diet.append(row[4])
            occupation.append(row[5])
            nationality.append(row[6])
            permission.append(row[-2])
            completed.append(row[-1])
    res.close()
    return {
            'username': username,
            'dob' : dob,
            'gender' : gender,
            'allergies': allergies,
            'diet': diet,
            'occupation': occupation,
            'nationality': nationality,
            'permission' : permission,
            'completed time' : completed,
            }

def get_user_pairs_dict(name, exp):
    # returns user pairs by experiement
    res_list=[]
    index=[]
    value=[]
    pic=[]
    time=[]
    t_at=[]
    date=''
    browser=''
    scrn_h=[]
    scrn_w=[]
    scroll_x=[]
    scroll_y=[]
    
    file_csv = DIR_CSV + 'results/csv/users/'+ name+str(exp) + '.csv'
    
    # Check file exists
    if os.path.exists(file_csv) == True:
        with open(file_csv, 'rb') as res:
            reader = csv.reader(res)
            for row in reader:
                if int(row[0]) == exp:
                    index.append(int(row[1]))
                    value.append(int(row[2]))
                    pic.append(row[3])
                    time.append(int(row[4]))
                    t_at.append(row[5])
                    date = row[6]
                    browser = row[7]
                    scrn_h.append(int(row[8]))
                    scrn_w.append(int(row[9]))
                    scroll_x.append(int(row[10]))
                    scroll_y.append(int(row[-1]))
                else:
                    pass
            pairs = {
                    'exp_no': exp, 
                    'index' :  index,
                    'value' :  value,
                    'pic': pic,
                    'time':  time,
                    't_at': t_at,
                    'date': date,
                    'browser' : browser,
                    'scrn_h' :  scrn_h,
                    'scrn_w':  scrn_w,
                    'scroll_x' :  scroll_x,
                    'scroll_y' :  scroll_y,
                    }
            res_list.append(pairs)
        res.close()
        return { name : res_list}
    else:
        return { name : "False"}
   
def get_user_all_pairs_csv(exp):
    # returns a dictionary of all user pair details dependent on the experement
    users = User.objects.all()
    all_pairs = []
    for u in users:
        all_pairs.append(get_user_pairs_dict(u.username, exp))
    return { 'exp_'+ str(exp) : all_pairs }
    
def get_user_csv(name):
    username=[]
    mail=[]
    
    # returns user pairs by experiement
    file_csv = DIR_CSV + 'results/csv/'+ name + '.csv'
    
    with open(file_csv, 'rb') as res:
        reader = csv.reader(res)
        for row in reader:
                username.append(row[0])
                mail.append(row[-1])
    res.close()
    return {'username': username, 'mail' :  mail,}
    