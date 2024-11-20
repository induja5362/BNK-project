from flask import Flask,render_template,request,redirect
import sqlite3,random

app=Flask(__name__)

con=sqlite3.connect("Bank_system.db",check_same_thread=False)
cur=con.cursor()

qry=""" create table if not exists Customer_details(
    id integer PRIMARY KEY autoincrement,
    Name varchar(25),
    Gender varchar(10),
    D_O_B date,
    Age int,
    Phone_number bigint,
    Address varchar(60),
    Branch varchar(22),
    Account_Number bigint,
    Pin int,
    Amount int    
    )"""
cur.execute(qry)
con.commit()
# cur.execute(""" drop table customer_details"""

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/create",methods=["GET","POST"])
def create():

    if request.method=="POST":
        name=request.form["cusname"]
        Gender=request.form["human"]
        phone=request.form["contactnumber"]
        Age=request.form["age"]
        birth=request.form["dateofbirth"]
        address=request.form["Address"]
        branch=request.form["branch"]
        minb=request.form["iniamount"]
        pin=request.form["Pin_number"]
        c_pin=request.form["cpin"]
        if pin==c_pin:
            acc=random.randint(100000,1000000)
            acc_no="161319"+str(acc)
            cur.execute("""insert into Customer_details(Name,Gender,D_O_B,Age,Phone_number,Address,Branch,Amount,Pin,Account_number) values (?,?,?,?,?,?,?,?,?,?)""",
                        (name,Gender,birth,Age,phone,address,branch,minb,pin,acc_no))
            con.commit()
            return render_template("view 1 acc.html",Name=name,Gender=Gender,Phone_number=phone,Age=Age,D_O_B=birth,Address=address,Branch=branch,Amount=minb,Pin_number=pin,Account_number=acc_no)
        else:
            return redirect("/create")
    else:
        return render_template("create acc.html")

@app.route("/view1")
def view1():
    return render_template("view 1 acc.html")


@app.route("/view2",methods=["GET","POST"])
def view2():
    if request.method=="POST":
        acc_name=request.form["username"]
        acc_num=request.form["Accnum"]
        try:
            cur.execute("""select * from customer_details where Account_Number=?""",(acc_num,))
            userdetails=cur.fetchone()
        except Exception as e:
            return render_template("view2 acc.html")
        else:
            return render_template("cus view.html",userdetails=userdetails)
    else:
        return render_template("view2 acc.html")

@app.route("/cusview")
def cusview():
    return("")

@app.route("/viewall")
def viewall():
    cur.execute(""" select * from customer_details""")
    userdetails=cur.fetchall()
    return render_template("viewall.html",userdetails=userdetails)

@app.route("/debit",methods=["GET","POST"])
def debit():
    if request.method=="POST":
        Acno=request.form["racc"]
        amt=request.form["amount"]
        cur.execute(""" select Account_Number from Customer_details """)
        Acno_details=cur.fetchall()
        # print(Acno_details)
        
        for i in Acno_details:
            print(type(i[0]))
            # print(type(Acno))
            
            if i[0]==int(Acno):
                # print("ccc")
                cur.execute(""" select Amount from Customer_details where Account_Number=? """,(Acno,))
                dbam=cur.fetchone()
                print(type(dbam[0]))
                print(type(amt))
                namt=dbam[0]+int(amt)
                cur.execute("""update customer_details set Amount=? where Account_number=? """,(namt,Acno))
                con.commit()
                return "Amount Debited Successfully."
            else:
                # return render_template("sample.html",j=i[0],acno=Acno)  
                continue
        else:
            return render_template("sample.html")
    else:
        return render_template("debit amount.html")     


@app.route("/update",methods=["GET","POST"])
def update():
    if request.method=="POST":
        Acc=request.form["racc"]
        name=request.form["cusname"]
        Gender=request.form["human"]
        phone=request.form["contactnumber"]
        Age=request.form["age"]
        birth=request.form["dateofbirth"]
        address=request.form["Address"]
        branch=request.form["branch"]
        pin=request.form["Pin_number"]
        c_pin=request.form["cpin"]
        cur.execute(""" Select Account_number from Customer_details""")
        dbaccount=cur.fetchall()
        # print(type(dbaccount[0][0]))
        # print(type(Acc))
        for j in dbaccount:
            if str(j[0])==Acc:
                print(type(j[0]))
                print(type(Acc))
                if pin==c_pin:
                    cur.execute("""update Customer_details set Name=?,Gender=?,D_O_B=?,Age=?,Phone_Number=?,Address=?,Branch=?,Pin=? where Account_number=?""",(name,Gender,birth,Age,phone,address,branch,pin,Acc))
                    con.commit()
                    return "Updated sucessfully !"
                else:
                    continue                                                                                                                                                                                            
            else:
                continue
        else:
            return render_template("update acc.html")
    return render_template("update acc.html")

@app.route("/checkbalance",methods=["GET","POST"])
def check_balance():
    if request.method=="POST":
        Acc=request.form["racc"]
        pin=request.form["pin"]
        cur.execute(""" Select Account_number from Customer_details""")
        dbaccount=cur.fetchall()
        for j in dbaccount:
            if str(j[0])==Acc:
                cur.execute(""" select pin from Customer_details where Account_number=?""",(Acc,))
                dbpin=cur.fetchone()
                print(type(pin))
                print(type(dbpin[0]))
                if pin==str(dbpin[0]):
                    cur.execute(""" select amount from customer_details where Account_number=? """,(Acc,))
                    dbamt=cur.fetchone()
                    dbamount=dbamt[0]
                    msg="Your Account Balance is:  "
                    return render_template("check balance.html",dbamount=str(dbamount)+" Rupees/-",msg=msg)
                else:
                    return render_template("check balance.html")
        else:
            return redirect("/checkbalance")

    return render_template("check balance.html")

@app.route("/ATM",methods=["GET","POST"])
def atm():
    if request.method=="POST":
        Acc=request.form["racc"]
        pin=request.form["pin"]
        wamount=request.form["amount"]
        cur.execute(""" Select Account_number from Customer_details""")
        dbaccount=cur.fetchall()
        for j in dbaccount:
            if str(j[0])==Acc:
                cur.execute(""" select pin from Customer_details where Account_number=?""",(Acc,))
                dbpin=cur.fetchone()
                print(type(pin))
                print(type(dbpin[0]))
                if pin==str(dbpin[0]):
                    cur.execute(""" select amount from customer_details where Account_number=? """,(Acc,))
                    dbamt=cur.fetchone()
                    if int(wamount) <= dbamt[0]:
                        newamt=dbamt[0]-int(wamount)
                        cur.execute("""update customer_details set amount=? where Account_number=?""",(newamt,Acc))
                        con.commit()
                        msg="Take amount of Rupees "+str(wamount)+"/-"
                        return render_template("atm.html",msg=msg)
                    else:
                        msg="Insufficinet Balance! Check Balance!"
                        return render_template("atm.html",msg=msg)
                else:
                    return redirect("/ATM")   
        else:
            return redirect("/ATM")        
    return render_template("atm.html")

@app.route("/MoneyTransfer",methods=["GET","POST"])
def moneytransfer():
    if request.method=="POST":
        ouracout=request.form["oacc"]
        pin=request.form["pin"]
        amt=request.form["amount"]
        raacount=request.form["racc"]
        rname=request.form["rname"]
        cur.execute(""" Select Account_number from Customer_details""")
        dbaccount=cur.fetchall()
        for j in dbaccount:
            if str(j[0])==ouracout:
                cur.execute(""" select pin from Customer_details where Account_number=?""",(ouracout,))
                dbpin=cur.fetchone()
                print(type(pin))
                print(type(dbpin[0]))
                if pin==str(dbpin[0]):
                    cur.execute(""" select amount from customer_details where Account_number=? """,(ouracout,))
                    dbamt=cur.fetchone()
                    dbamount=dbamt[0]
                    for k in dbaccount:
                        if str(k[0])==raacount:
                            cur.execute(""" select amount from Customer_details where Account_number=?""",(raacount,))
                            rramt=cur.fetchone()
                            if int(amt)<=int(dbamount):
                                samt=int(dbamount)-int(amt)
                                cur.execute("""update customer_details set amount=? where Account_number=?""",(samt,ouracout))
                                con.commit()
                                newamt=int(amt)+int(rramt[0])
                                cur.execute("""update customer_details set amount=? where ACCOUNT_NUMBER=? """,(newamt,raacount))
                                con.commit()
                                return "<h2>Amount Transfered Successfully.</h2>"
                            else:
                                return "<h2>Insufficient Balance, Check balance and try again !</h2> "
                        else:
                            continue
                    else:
                        return "<h2>invalid reciever Account</h2>."
                
                else:
                    return "<h2> InValid Pin number </h2>"     
            else:
                continue   
        else:
            return redirect("/MoneyTransfer")

    else:
        return render_template("money transfer.html")

@app.route("/delete",methods=["GET","POST"])
def delete():
    if request.method=="POST":
        print("hello iam python")
        Acc=request.form["racc"]
        pin=request.form["pin"]
        cur.execute(""" Select Account_number from Customer_details""")
        dbaccount=cur.fetchall()
        print("hai")
        for j in dbaccount:
            print("hi")
            if str(j[0])==Acc:
                cur.execute(""" select pin from Customer_details where Account_number=?""",(Acc,))
                dbpin=cur.fetchone()
                print(type(pin))
                print(type(dbpin[0]))
                if pin==str(dbpin[0]):
                    cur.execute(""" delete from customer_details where Account_number=? """,(Acc,))
                    con.commit()
                    return "Acount Deleted Sucessfully."
                else:
                    return "<h2> Invalid Pin Number</h2>"
            else:
                continue
        else:
            return redirect("/delete")
            
    return render_template("delete acc.html")



app.run(debug=True)