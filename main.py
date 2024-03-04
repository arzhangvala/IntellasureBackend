import pandas as pd
import psycopg2
from datetime import datetime
import os
path_variable = os.getenv('PATH')
print(path_variable)
networks = [ "BCBS", "CIGNA", "HUMANA", "UNITED HEALTH CARE"]
from dotenv import load_dotenv, dotenv_values

load_dotenv()

financials_dict = {
"charge_code":[],
"claim_id":[],
"status":[],
"state":[],
"charged":[],
"paid":[],
"policy_id":[],
"insurance":[],
"facility": [],
"date":[]

}
DB_NAME = os.getenv("DB_NAME")
def update_financials_database(file_name):
    data = pd.read_csv(file_name)

    DB_NAME = os.getenv("DB_NAME")
    DB_HOST = os.getenv("DB_HOST")
    DB_PASSWORD= os.getenv("DB_PASSWORD")
    DB_USER= os.getenv("DB_USER")


    #charged => charge balanced
    #charged_to_date, charged_from_date
    #charged_insurance_payments => paid
    #add Primary Payed Amount

    #charged_balance = balance
    #charged_insurance_payments = paid
    #primary_allowed_amount
    #charged_debit_amount = charged
    # patient birthday
    # fu note

    connection = psycopg2.connect(
         host = DB_HOST,
         database = DB_NAME,
        user = DB_USER,
        password = DB_PASSWORD)
    curr = connection.cursor()


    for i, row in data.iterrows():


        claim_id = row[1]
        status =  row[0]
        patient_id = row[2]  #charge patient id
        paid = row[-3] #charged_insurancepayment
        print(paid)

        policy_id = row[3]
        facility_name = row[4]
        insurance = row[5].split('(')[0]
        date = row[8]
        reason = "Nan"
        charge_code = row[9]  # CPT CODE
        if type(row[11]) == float:
            primary_pay_amount = row[11]
        else:
            primary_pay_amount = float(row[11].split('$')[1].replace(',', ''))

        if type(row[10]) == float:
             charged= row[10]
        else:
            charged = float(row[10].split('$')[1].replace(',', ''))
        balance = float(row[13].split('$')[1].replace(',', ''))  # Charge Balance
        patient_birthday = row[14]  # patient birthday
        paid = float(row[15].split('$')[1].replace(',', ''))  # Charged_insurance_payments
        fu_note = row[-1]


        date_object = datetime.strptime(date, "%m/%d/%Y").date()
        patient_birthday = datetime.strptime(patient_birthday, "%m/%d/%Y").date()
        #if balance due patient closed else open this means
        if status == "BALANCE DUE PATIENT":
            state = "ClOSED"
            print("BALANCE DUE")
        else:
            state = "OPEN"

        try:
            insert_query = '''INSERT INTO Financials_Patient_Beachside(charge_code, Patient_ID,reason,  claim_ID, Status, State, Charged, Paid, Policy_ID, Insurance, Facility, Primary_pay_amount, Balance, FU_Note, Patient_Birthday, Date)
            VALUES (%s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,CAST(%s as date), CAST(%s as date) )'''
            data_to_insert = (charge_code, patient_id, reason, claim_id, status, state, charged, paid, policy_id, insurance, facility_name, primary_pay_amount, balance, fu_note, patient_birthday, date)
            curr.execute(insert_query, data_to_insert)
            connection.commit()
        except Exception as e:
            print("This error here is: " + str(e))
            continue
            # commit the transaction

        #store in Financials csv and dict for potential use later
            financials_dict["charge_code"].append(charge_code)
            financials_dict["claim_id"].append(claim_id)
            financials_dict["status"].append(status)
            financials_dict["state"].append(state)
            financials_dict["charged"].append(charged)
            financials_dict["paid"].append(paid)
            financials_dict["policy_id"].append(policy_id)
            financials_dict["insurance"].append(insurance)
            financials_dict["date"].append(date)
            financials_dict["facility"].append(facility_name)


    df = pd.DataFrame.from_dict(financials_dict)
    df.to_csv('Financials_Patient_Test')
    curr.close()

    return data
#everything csv 3
def update_financials_database_everything3(file_name):
    data = pd.read_csv(file_name)

    DB_NAME = os.getenv("DB_NAME")
    DB_HOST = os.getenv("DB_HOST")
    DB_PASSWORD= os.getenv("DB_PASSWORD")
    DB_USER= os.getenv("DB_USER")


    #charged => charge balanced
    #charged_to_date, charged_from_date
    #charged_insurance_payments => paid
    #add Primary Payed Amount

    #charged_balance = balance
    #charged_insurance_payments = paid
    #primary_allowed_amount
    #charged_debit_amount = charged
    # patient birthday
    # fu note

    connection = psycopg2.connect(
         host = DB_HOST,
         database = DB_NAME,
        user = DB_USER,
        password = DB_PASSWORD)
    curr = connection.cursor()


    for i, row in data.iterrows():

        balance = float(row[13].split('$')[1].replace(',', '')) #Charge Balance
        paid =  float(row[16].split('$')[1].replace(',', '')) # Charged_insurance_payments
        charge_code = row[9] #CPT CODE
        claim_id = row[1]
        status =  row[0]
        if type(row[11]) == float:
            primary_pay_amount = row[11]
        else:
            primary_pay_amount = float(row[11].split('$')[1].replace(',', ''))

        if type(row[10]) == float:
             charged= row[10]
        else:
            charged = float(row[10].split('$')[1].replace(',', ''))
        policy_id = row[4]
        insurance = row[5].split('(')[0]
        date = row[8]
        facility_name = row[4]
        reason = "Nan"
        fu_note = row[-1]
        patient_birthday = row[14] #patient birthday
        patient_id = row[2]  #charge patient id



        date_object = datetime.strptime(date, "%m/%d/%Y").date()
        patient_birthday = datetime.strptime(patient_birthday, "%m/%d/%Y").date()
        #if balance due patient closed else open this means
        if status == "BALANCE DUE PATIENT":
            state = "ClOSED"
            print("BALANCE DUE")
        else:
            state = "OPEN"

        try:
            insert_query = '''INSERT INTO Financials_Patient_test3(charge_code, Patient_ID,reason,  claim_ID, Status, State, Charged, Paid, Policy_ID, Insurance, Facility, Primary_pay_amount, Balance, FU_Note, Patient_Birthday, Date)
            VALUES (%s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,CAST(%s as date), CAST(%s as date) )'''
            data_to_insert = (charge_code, patient_id, reason, claim_id, status, state, charged, paid, policy_id, insurance, facility_name, primary_pay_amount, balance, fu_note, patient_birthday, date)
            curr.execute(insert_query, data_to_insert)
            connection.commit()
        except Exception as e:
            print("This error here is: " + str(e))
            continue
            # commit the transaction

        #store in Financials csv and dict for potential use later
            financials_dict["charge_code"].append(charge_code)
            financials_dict["claim_id"].append(claim_id)
            financials_dict["status"].append(status)
            financials_dict["state"].append(state)
            financials_dict["charged"].append(charged)
            financials_dict["paid"].append(paid)
            financials_dict["policy_id"].append(policy_id)
            financials_dict["insurance"].append(insurance)
            financials_dict["date"].append(date)
            financials_dict["facility"].append(facility_name)


    df = pd.DataFrame.from_dict(financials_dict)
    df.to_csv('Financials_Patient_Test')
    curr.close()

    return data




if __name__ == '__main__':
    file_name = "Everything - Nasim 2.csv"
    update_financials_database(file_name)
