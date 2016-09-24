import csv
from pizza_ml.models import Pizza, Ingredient, UserProfile, PairPreferance

"""
Result
are helpers functions for the views needing data from the resulst in the csv
- get_results_dict
- save_to_csv
- save_emails
- get_nationality
"""

def get_results_dict(name, exp):
    res_list=[]
    #c9Testing:
    with open('pizza_ml/results/csv/'+ name +'.csv', 'rb') as res:
    #with open('pizza_face_project/pizza_ml/results/csv/'+ name +'.csv', 'rb') as res:
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
            if exp == 2:
                users['pairs']= row[7]
            else:
                users['pairs_nopics']= row[7]
                users['pairs_pics']= row[8]
                
            res_list.append(users)
    return { 'results' :res_list}

def save_to_csv(doc_new, name):
    # Saves all results on exisiting file
    doc_in = []
    #c9Testing:
    with open('pizza_ml/results/csv/'+ name + '.csv', 'rb') as inText:
    #with open('pizza_face_project/pizza_ml/results/csv/'+ name + '.csv', 'rb') as inText:
        reader = csv.reader(inText)
        for row in reader:
            doc_in.append(row)
    inText.close()
    
    for doc in doc_new:
        doc_in.append(doc)
    
    # Store all information in a csv file
    #c9Testing:
    with open('pizza_ml/results/csv/'+ name + '.csv', 'w') as outText:
    #with open('pizza_face_project/pizza_ml/results/csv/'+ name + '.csv', 'w') as outText:
        writer = csv.writer(outText, delimiter=",")
        writer.writerow(doc_in[0])
    
        for i in range(1,len(doc_in)):
            out_doc = doc_in[i]
            writer.writerow(out_doc)
    outText.close()

def save_emails(username, email):
    # save emails
    e_doc=[]
    row=[]
    row.append(username)
    row.append(email)
    e_doc.append(row)
    save_to_csv(e_doc, 'email')

def get_nationality():
    context_dict = {}
    nat_list=[]
    #c9Testing:
    with open('pizza_ml/data/nations.csv', 'rb') as nat:
    #with open('pizza_face_project/pizza_ml/data/nations.csv', 'rb') as nat:
        reader = csv.reader(nat)
        for row in reader:
            country = {
                row[0] : row[1],
                row[2] : row[3]
            }
            nat_list.append(country)
    return { 'nationality' :nat_list}
