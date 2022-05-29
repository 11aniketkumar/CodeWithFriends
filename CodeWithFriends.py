import shutil
import os
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import mysql.connector
import hashlib
import csv


sno = 0

def database_check():
    try:
        conn = mysql.connector.connect(user="root", password="", host="localhost")
    except:
        s = input("Unable to connect to sql server, please start all the required services and try again.")
        return 0
    try:
        conn = mysql.connector.connect(user="root", password="", database="project", host="localhost")
        c = conn.cursor()
        print("Database found successfully.")
    except:
        conn = mysql.connector.connect(user="root", password="", host="localhost")
        c = conn.cursor()
        c.execute("CREATE DATABASE project;")
        c.execute("USE project;")
        c.execute("""CREATE TABLE acc_info(Id int(5) NOT NULL AUTO_INCREMENT PRIMARY KEY,
                    name varchar(30),
                    phone bigint(10),
                    country varchar(20),
                    Gender varchar(6));""")
        c.execute("""CREATE TABLE email(Id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
                    EmailId varchar(32));""")
        c.execute("""CREATE TABLE pin(Id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
                    password varchar(32));""")
        c.execute("""CREATE TABLE project_access(Id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
                    username varchar(32),
                    password varchar(32),
                    location varchar(80),
                    type varchar(7),
                    admin int(4));""")
        c.execute("""create view magic as select project_access.username, acc_info.name from project_access join acc_info
                    where project_access.admin=acc_info.id and project_access.type like 'Public';""")
        conn.commit()
        print("Database not found -> Creating Database -> Database created successfully.")
    finally:
        master()

############################################################################################################################

def log_in():
    def menu():
        lin.destroy()
        master()

    def key(event):
        sign_in()
        
    def sign_in():
        a = entry1.get()
        b = entry2.get()

        email_id = hashlib.md5(a.encode())
        psswrd = hashlib.md5(b.encode())
        a = str(email_id.hexdigest())
        b = str(psswrd.hexdigest())

        conn = mysql.connector.connect(user="root", password="", database="project", host="localhost")
        c = conn.cursor()
        c.execute("select emailid from email;")
        n = c.fetchall()
        l = []
        for i in n:
            for j in i:
                l.append(j)
        if a in l:
            c.execute("select id from email where emailid like '{}'".format(a))
            n = c.fetchall()
            global sno
            sno = n[0][0]
            c.execute("select password from pin where id={};".format(sno))
            n = c.fetchall()
            p_word = n[0][0]
            if b == p_word:
                r = os.path.exists("Data")
                if r == True:
                    pass
                else:
                    os.mkdir("Data")
                    
                r = os.path.exists("Data/p"+str(sno))
                if r == True:
                    pass
                else:
                    os.mkdir("Data/p"+str(sno))

                try:
                    file = open("Data/p"+str(sno)+"/active.bin", "r")
                    file.close()
                except:
                    file = open("Data/p"+str(sno)+"/active.bin", "w")
                    file.write("none")
                    file.close()
                
                lin.destroy()
                mainscreen()
            else:
                messagebox.showerror("Error", "You have typed something wrong.")
        else:
            messagebox.showerror("Error", "Unable to find a user with this Username.")
                
    lin = Tk()
    lin.title('Log-In')
    lin.geometry('600x500')
    container = Frame(lin)
    container.place(relx=0, rely=0, relheight=1, relwidth=1)
    
    label0 = Label(container, text='Sign In', font=("bold", 25))
    label1 = Label(container, text='Username')
    label2 = Label(container, text='Password')
    button = Button(container, text='Submit', bg='blue', fg='white', command=sign_in)

    entry1 = Entry(container)
    entry2 = Entry(container, show='*')
    
    label0.place(relx=0.3, rely=0.3)
    label1.place(relx=0.35, rely=0.42)
    entry1.place(relx=0.47, rely=0.42, relwidth=0.2)
    label2.place(relx=0.35, rely=0.49)
    entry2.place(relx=0.47, rely=0.49, relwidth=0.2)
    button.place(relx=0.4, rely=0.575, relheight=0.075, relwidth=0.2)

    lin.bind("<Return>", key)
    
    back = Button(container, text='Back to main menu', bg='seagreen4', fg='white', command=menu)
    back.place(relx=0, rely=0.947, relwidth=0.3)

    lin.mainloop()

############################################################################################################################

def master():

    def btn1():
        root.destroy()
        log_in()
    
    def btn2():
        root.destroy()
        sign_up()

    def qui():
        answer = messagebox.askquestion("Confirmation", "Do you really want to quit.")
        if answer == 'yes':
            root.destroy()
        else:
            pass
    
    root = Tk()
    root.title('GIT')
    root.geometry('600x500')
    container = Frame(root)
    container.place(relx=0, rely=0,relheight=1, relwidth=1)

    label1 = Label(container, text='CODE WITH FRIENDS', font=("bold", 30), bg='seagreen4', fg='white')

    button1 = Button(container, text='Log In', bg='#7F70FF', fg='white', command=btn1)
    button2 = Button(container, text='Sign Up', bg='#7F70FF', fg='white', command=btn2)
    button3 = Button(container, text='Quit', bg='#7F70FF', fg='white', command=qui)

    label1.place(relx=0, rely=0, relheight=0.2, relwidth=1)
    button1.place(relx=0.35, rely=0.3,relheight=0.09, relwidth=0.3)
    button2.place(relx=0.35, rely=0.43,relheight=0.09, relwidth=0.3)
    button3.place(relx=0.35, rely=0.56,relheight=0.09, relwidth=0.3)

    root.mainloop()

############################################################################################################################

def sign_up():
    
    def menu():
        sign.destroy()
        master()

    def d_table():
        a = entry2.get()
        b = entry3.get()

        name = StringVar()
        telephone = StringVar()
        country = StringVar()
        selection = StringVar()
        

        name = entry1.get()
        telephone = entry4.get()
        country = entry5.get()
        selection = g.get()
        
        if len(b)>=8:
            pass
        else:
            messagebox.showerror('Error','Password should be of atleast 8 characters long.')
            entry3.delete(0, END)
            return 0
        if len(telephone)>= 4:
            pass
        else:
            messagebox.showerror('Error','Please enter a valid phone number.')
            entry4.delete(0, END)
            return 0
        
        email_id = hashlib.md5(a.encode())
        psswrd = hashlib.md5(b.encode())
        a = str(email_id.hexdigest())
        b = str(psswrd.hexdigest())
        
        conn = mysql.connector.connect(user="root", password="", database="project", host="localhost")
        c = conn.cursor()
        c.execute("SELECT * FROM email;")
        n = c.fetchall()
        l = []
        for i in n:
            for j in i:
                l.append(j)
        if a in l:
            messagebox.showerror("Error!", "Sorry, this username is already taken. Please try a different username.")
            entry2.delete(0, END)
            return 0
        
        c.execute("INSERT INTO email (emailid) VALUES('{}')".format(a))
        c.execute("INSERT INTO pin (password) VALUES('{}')".format(b))

        if selection == 1:
            gender = "Male"
        else:
            gender = "Female"
        try:
            c.execute("INSERT INTO acc_info (name, phone, country, gender) VALUES('{}',{},'{}','{}');".format(name, telephone, country, gender))
            conn.commit()
        except:
            messagebox.showerror("Error!", "Please enter a valid phone number.")
            sign.destroy()
            sign_up()
        
        messagebox.showinfo("Confirmation", "Account Created Successfully.")
        
        sign.destroy()
        master()
        
    sign = Tk()
    sign.title('Sign Up Form')
    sign.geometry('420x500')

    container = Frame(sign)
    container.place(relx=0, rely=0, relheight=1, relwidth=1)

    label0 = Label(container, text='Sign Up Form', font=("bold", 25))
    label1 = Label(container, text='Full Name')
    label2 = Label(container, text='Username')
    label3 = Label(container, text='Password')
    label4 = Label(container, text='Phone Number')
    label5 = Label(container, text='Country')
    label6 = Label(container, text='Gender')

    a = StringVar()
    b = StringVar()
    g = IntVar()
    
    entry1 = Entry(container)
    entry2 = Entry(container)
    entry3 = Entry(container, show='*')
    entry4 = Entry(container)
    entry5 = Entry(container)
    entry6_0 = Radiobutton(container, text='Male', variable=g, value=1)
    entry6_1 = Radiobutton(container, text='Female', variable=g, value=2)

    button = Button(container, text='Submit', bg='blue', fg='white', command=d_table)

    label0.place(relx=0, rely=0.07, relheight=0.1, relwidth=1)
    label1.place(relx=0.128, rely=0.238)
    entry1.place(relx=0.52, rely=0.255, relwidth=0.3)
    label2.place(relx=0.128, rely=0.32)
    entry2.place(relx=0.52, rely=0.334, relwidth=0.3)
    label3.place(relx=0.128, rely=0.4)
    entry3.place(relx=0.52, rely=0.413, relwidth=0.3)
    label4.place(relx=0.128, rely=0.48)
    entry4.place(relx=0.52, rely=0.492, relwidth=0.3)
    label5.place(relx=0.128, rely=0.56)
    entry5.place(relx=0.52, rely=0.571, relwidth=0.3)
    label6.place(relx=0.128, rely=0.64)
    entry6_0.place(relx=0.45, rely=0.65)
    entry6_1.place(relx=0.7, rely=0.65)

    button.place(relx=0.3, rely=0.77, relheight=0.08, relwidth=0.33)

    back = Button(container, text='Back to main menu', bg='seagreen4', fg='white', command=menu)
    back.place(relx=0, rely=0.95, relwidth=0.35)

    sign.mainloop()

############################################################################################################################

def mainscreen():
    def logout():
        scr.destroy()
        log_in()

    #   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -

    def acc_det():
        def ch_email():
            def exi():
                r.destroy()
            
            def submit():
                conn = mysql.connector.connect(user="root", password="", database="project", host="localhost")
                c = conn.cursor()
                a = entry0.get()
                b = entry.get()
                d = entry1.get()

                email_id = hashlib.md5(a.encode())
                psswrd = hashlib.md5(d.encode())
                a = str(email_id.hexdigest())
                d = str(psswrd.hexdigest())
                email = hashlib.md5(b.encode())
                e = str(email.hexdigest())

                try:
                    c.execute("select emailid from email where emailid like '{}';".format(e))
                    n = c.fetchall()
                    if e == n[0][0]:
                        r.destroy()
                        messagebox.showerror("Error","Username already taken.")
                        return 0
                except:
                    pass
                
                c.execute("select emailid from email where id = {};".format(sno))
                n = c.fetchall()
                if n[0][0] == a:
                    c.execute("select password from pin where id = {};".format(sno))
                    n = c.fetchall()
                    if n[0][0] == d:
                        c.execute("update email set emailid='{}' where id={};".format(e,sno))
                        conn.commit()
                        messagebox.showinfo("Info","Username changed successfully.")
                        r.destroy()
                    else:
                        messagebox.showerror("Error","Wrong Password entered.")
                else:
                    messagebox.showerror("Error","Invalid username entered.")


            r = Tk()
            r.title("Change Username")
            r.geometry('330x130')
            r.resizable(0,0)
            info = Label(r, text='Please fill the details asked below to change your username.')
            label0 = Label(r, text='Enter Current Username')
            entry0 = Entry(r)
            label = Label(r, text='Enter New Username')
            entry = Entry(r)
            label1 = Label(r, text='Enter Password')
            entry1 = Entry(r, show='*')
            submit = Button(r, text='Submit', command=submit, bg='#3A6EFF', fg='white')
            cancel = Button(r, text='Cancel', command=exi, bg='#3A6EFF', fg='white')

            info.place(relx=0, rely=0)
            label0.place(relx=0, rely=0.2)
            entry0.place(relx=0.5, rely=0.2)
            label.place(relx=0, rely=0.35)
            entry.place(relx=0.5, rely=0.35)
            label1.place(relx=0, rely=0.5)
            entry1.place(relx=0.5, rely=0.5)
            submit.place(relx=0.25, rely=0.7, relwidth=0.2)
            cancel.place(relx=0.5, rely=0.7, relwidth=0.2)
            
            r.mainloop()

        def ch_pass():
            def exi():
                r.destroy()
                
            def submit():
                conn = mysql.connector.connect(user="root", password="", database="project", host="localhost")
                c = conn.cursor()
                a = entry0.get()
                b = entry.get()
                d = entry1.get()

                email_id = hashlib.md5(a.encode())
                cpsswrd = hashlib.md5(b.encode())
                npsswrd = hashlib.md5(d.encode())
                
                a = str(email_id.hexdigest())
                b = str(cpsswrd.hexdigest())
                e = str(npsswrd.hexdigest())

                c.execute("select emailid from email where id = {}".format(sno))
                n = c.fetchall()
                for i in n:
                    for j in i:
                        if j == a:
                            c.execute("select password from pin where id = {}".format(sno))
                            n = c.fetchall()
                            for i in n:
                                for j in i:
                                    if j == b:
                                        if len(d)<8:
                                            messagebox.showerror('Error','Password should be of atleast 8 characters long.')
                                            r.destroy()
                                            return 0
                                        c.execute("update pin set password='{}' where id={}".format(e,sno))
                                        conn.commit()
                                        messagebox.showinfo("Info","Password changed successfully.")
                                        r.destroy()
                                    else:
                                        messagebox.showerror("Error","Wrong Password entered.")
                        else:
                            messagebox.showerror("Error","Invalid username entered.")


            r = Tk()
            r.title("Change Password")
            r.geometry('330x130')
            r.resizable(0,0)
            info = Label(r, text='Please fill the details asked below to change your username.')
            label0 = Label(r, text='Enter Current Username')
            entry0 = Entry(r)
            label = Label(r, text='Enter Current Password')
            entry = Entry(r)
            label1 = Label(r, text='Enter New Password')
            entry1 = Entry(r, show='*')
            submit = Button(r, text='Submit', command=submit, bg='#3A6EFF', fg='white')
            cancel = Button(r, text='Cancel', command=exi, bg='#3A6EFF', fg='white')

            info.place(relx=0, rely=0)
            label0.place(relx=0, rely=0.2)
            entry0.place(relx=0.5, rely=0.2)
            label.place(relx=0, rely=0.35)
            entry.place(relx=0.5, rely=0.35)
            label1.place(relx=0, rely=0.5)
            entry1.place(relx=0.5, rely=0.5)
            submit.place(relx=0.25, rely=0.7, relwidth=0.2)
            cancel.place(relx=0.5, rely=0.7, relwidth=0.2)
            
            r.mainloop()

        
        screen = Frame(container, border=2)
        screen.place(relx=0.27, rely=0.12, relheight=1, relwidth=0.73)


        conn = mysql.connector.connect(user="root", password="", database="project", host="localhost")
        c = conn.cursor()
        
        c.execute('select * from acc_info where id={}'.format(sno))
        n = c.fetchall()
        n = n[0]
        a = n[1]
        b = n[2]
        c = n[3]
        d = n[4]
        
        title1 = Label(screen, text='ACCOUNT INFO', bg='#3b5998', fg='white', font=('bold', 25))
        name = Label(screen, text='Full Name', font=('bold',16))
        name_ = Label(screen, text=a, font=('bold',16))
        phone = Label(screen, text='Phone Number', font=('bold',16))
        phone_ = Label(screen, text=b, font=('bold',16))
        country = Label(screen, text='Country', font=('bold',16))
        country_ = Label(screen, text=c, font=('bold',16))
        gender = Label(screen, text='Gender', font=('bold',16))
        gender_ = Label(screen, text=d, font=('bold',16))
        line = Label(screen, text='______________________________________________________________________________________________________')
        email = Label(screen, text='Username', font=('bold',16))
        e_mail = Button(screen, text='Change Username', bg='#D3E6DB', command=ch_email)
        password = Label(screen, text='Password', font=('bold',16))
        pin = Button(screen, text='Change Password', bg='#D3E6DB', command=ch_pass)


        title1.place(relx=0, rely=0, relheight=0.1, relwidth=1)
        name.place(relx=0.1, rely=0.14)
        name_.place(relx=0.45, rely=0.14)
        phone.place(relx=0.1, rely=0.21)
        phone_.place(relx=0.45, rely=0.21)
        country.place(relx=0.1, rely=0.28)
        country_.place(relx=0.45, rely=0.28)
        gender.place(relx=0.1, rely=0.35)
        gender_.place(relx=0.45, rely=0.35)
        line.place(relx=0.03, rely=0.42)
        email.place(relx=0.1, rely=0.49)
        e_mail.place(relx=0.45, rely=0.49, relwidth=0.2)
        password.place(relx=0.1, rely=0.56)
        pin.place(relx=0.45, rely=0.56, relwidth=0.2)

    #   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -

    def project_():
        file = open("Data/p"+str(sno)+"/active.bin","r")
        f = file.read()
        file.close()

        conn = mysql.connector.connect(user='root', password='', database='project', host='localhost')
        c = conn.cursor()
        c.execute("select location from project_access where username like '{}';".format(f))
        n = c.fetchall()
        for i in n:
            for j in i:
                a = j
        if f=='none':
            pass
        else:
            c.execute("select admin from project_access where username like '{}';".format(f))
            n = c.fetchall()
            for i in n:
                for j in i:
                    admin_id = str(j)

            c.execute("select name from acc_info where id={};".format(admin_id))
            n = c.fetchall()
            for i in n:
                for j in i:
                    admin_name = str(j)
        
        def see_request():
            if admin_id == str(sno):
                def editing():
                    text.config(state=NORMAL)

                def opening():
                    file_path = filedialog.askopenfilename(initialdir=a+"/request", title="Select a file to open", filetype=(("python files", "*.py"),("text files","*.txt")))
                    file = open(file_path, 'r')
                    data = file.read()
                    file.close()
                    text.config(state=NORMAL)
                    text.insert(INSERT, data)
                    text.config(state=DISABLED)
                    
                def activating():
                    file = open(a+"/"+f+".py", 'w')
                    rt = text.get(1.0, END)
                    file.write(rt)
                    file.close()
                    messagebox.showinfo('Success!','Task completed successfully.')

                def adding():
                    def submit():
                        name_ = entry0.get()
                        extension = entry.get()
                        file = open(a+"/"+name_+"."+extension, 'w+')
                        rt = text.get(1.0, END)
                        file.write(rt)
                        file.close()
                        r.destroy()
                        messagebox.showinfo("Success","Code imported successfully.")
                    def exi():
                        r.destroy()
                    r = Tk()
                    r.title("Importing file to project")
                    r.geometry('330x130')
                    r.resizable(0,0)
                    label0 = Label(r, text='Filename')
                    entry0 = Entry(r)
                    label = Label(r, text='File Extension')
                    entry = Entry(r)
                    submit = Button(r, text='Submit', command=submit)
                    cancel = Button(r, text='Cancel', command=exi)

                    label0.place(relx=0.05, rely=0.17)
                    entry0.place(relx=0.5, rely=0.17)
                    label.place(relx=0.05, rely=0.4)
                    entry.place(relx=0.5, rely=0.4)
                    submit.place(relx=0.25, rely=0.7, relwidth=0.2)
                    cancel.place(relx=0.5, rely=0.7, relwidth=0.2)
                    
                    r.mainloop()
                
                green = Tk()
                green.geometry('600x500')
                see = Frame(green)
                see.place(relx=0, rely=0, relwidth=1, relheight=1)
                title1 = Label(see, text='REQUESTS', bg='#3b5998', fg='white', font=('bold', 25))
                open_ = Button(see, text='Open', command=opening)
                set_active = Button(see, text='Set as Active', command=activating)      
                add = Button(see, text='Add', command=adding)
                modify = Button(see, text='Edit', command=editing)
                text = Text(see, font=('bold', 16), padx=10, pady=5, bg='#FFE2E9')
                
                title1.place(relx=0, rely=0, relheight=0.1, relwidth=1)
                open_.place(relx=0.1, rely=0.12, relheight=0.06, relwidth=0.1)
                set_active.place(relx=0.2, rely=0.12, relheight=0.06, relwidth=0.2)
                add.place(relx=0.7, rely=0.12, relheight=0.06, relwidth=0.1)
                modify.place(relx=0.8, rely=0.12, relheight=0.06, relwidth=0.1)
                text.place(relx = 0.1, rely = 0.2, relheight=0.6, relwidth=0.8)
                text.config(state=DISABLED)

                green.mainloop()

            else:
                messagebox.showerror('Error!','Sorry you dont have permission to see this data.')
            
        def project_exit():
                file = open("Data/p"+str(sno)+"/active.bin", "w")
                f = file.write("none")
                file.close()
                messagebox.showinfo('Success!',"Project closed Successfully.")
                scr.destroy()
                mainscreen()
        
        def open_project():
            def opening():
                a = ent1.get()
                b = ent2.get()
                
                conn = mysql.connector.connect(user='root', password='', database='project', host='localhost')
                c = conn.cursor()
                c.execute('select username from project_access;')
                n = c.fetchall()
                l = []
                for i in n:
                    for j in i:
                        l.append(j)
                if a in l:
                    c.execute("select password from project_access where username like '{}';".format(a))
                    n = c.fetchall()
                    for i in n:
                        for j in i:
                            if j == b:
                                file = open("Data/p"+str(sno)+"/active.bin", "w")
                                f = file.write(a)
                                file.close()
                                messagebox.showinfo('Success!',"Project Found Successfully.")
                                scr.destroy()
                                mainscreen()
                            else:
                                messagebox.showerror('Error!','Wrong password entered.')
                else:
                    messagebox.showerror('Error!','No Project found with this name.')

                
            def create():
                a = entry1.get()
                b = entry2.get()
                c = entry3.get()
                p_type =var.get()
                
                if b == "":
                    messagebox.showerror("Error!","Please enter a password.")
                    return 0
                
                if b == c:
                    conn = mysql.connector.connect(user='root', password='', database='project', host='localhost')
                    c = conn.cursor()
                    c.execute('select username from project_access;')
                    n = c.fetchall()
                    for i in n:
                        for j in i:
                            if j==a:
                                messagebox.showerror('Error!','This Project name is already taken. Please try some other name.')
                                entry1.delete(0, END)
                                return 0
                    location = "Data/p"+str(sno)+"/"+a
                    os.mkdir("Data/p"+str(sno)+"/"+a)
                
                    if var.get()==1:
                        c.execute("insert into project_access(username, password, location, type, admin) values('{}','{}', '{}', 'Private', {});".format(a,b,location,sno))
                        conn.commit()
                    else:
                        c.execute("insert into project_access(username, password, location, type, admin) values('{}','{}', '{}', 'Public', {});".format(a,b,location,sno))
                        conn.commit()
                    os.mkdir(location+"/request")
                    entry1.delete(0, END)
                    entry2.delete(0, END)
                    entry3.delete(0, END)
                    messagebox.showinfo('Success!','Project created successfully.')
                else:
                    messagebox.showerror('Error!','Password does not match.')
                    return 0
            screen = Frame(container, border=2)
            screen.place(relx=0.27, rely=0.12, relheight=1, relwidth=0.73)

            var = IntVar()
            
            title1 = Label(screen, text='START A NEW PROJECT', bg='#3b5998', fg='white', font=('bold', 25))
            label1 = Label(screen, text='Project name')
            entry1 = Entry(screen)
            label2 = Label(screen, text='Password')
            entry2 = Entry(screen, show="*")
            label3 = Label(screen, text='Re-enter Password')
            entry3 = Entry(screen, show="*")
            private = Checkbutton(screen, text="Keep this project private", variable=var)
            start = Button(screen, text='Submit', bg='#3b5998', fg='white', command=create)
            
            title1.place(relx=0, rely=0, relheight=0.1, relwidth=1)
            label1.place(relx = 0.25, rely = 0.12)
            entry1.place(relx = 0.5, rely = 0.12, relwidth=0.2)
            label2.place(relx = 0.25, rely = 0.16)
            entry2.place(relx = 0.5, rely = 0.16, relwidth=0.2)
            label3.place(relx = 0.25, rely = 0.2)
            entry3.place(relx = 0.5, rely = 0.2, relwidth=0.2)
            private.place(relx = 0.3, rely = 0.24)
            start.place(relx = 0.35, rely = 0.3, relwidth=0.2, relheight=0.05)

            title2 = Label(screen, text='OPEN PROJECT', bg='#3b5998', fg='white', font=('bold', 25))
            lab1 = Label(screen, text='Project name')
            ent1 = Entry(screen)
            lab2 = Label(screen, text='Password')
            ent2 = Entry(screen, show="*")
            submit = Button(screen, text='Submit', bg='#3b5998', fg='white', command=opening)

            title2.place(relx=0, rely=0.44, relheight=0.1, relwidth=1)
            lab1.place(relx = 0.25, rely = 0.57)
            ent1.place(relx = 0.5, rely = 0.57, relwidth=0.2)
            lab2.place(relx = 0.25, rely = 0.61)
            ent2.place(relx = 0.5, rely = 0.61, relwidth=0.2)
            submit.place(relx = 0.35, rely = 0.69, relwidth=0.2, relheight=0.05)

        if f == "none":
            open_project()
        else:
            conn = mysql.connector.connect(user='root', password='', database='project', host='localhost')
            c = conn.cursor()
            c.execute("select type from project_access where username like '{}';".format(f))
            n = c.fetchall()
            for i in n:
                for j in i:
                    type_p = j
            
            screen = Frame(container, border=2)
            screen.place(relx=0.27, rely=0.12, relheight=1, relwidth=0.73)
            title1 = Label(screen, text='ACTIVE PROJECT', bg='#3b5998', fg='white', font=('bold', 25))
            label0 = Label(screen, text='Project Name', font=('bold', 18))
            label0_1 = Label(screen, text=f, font=('bold', 18))
            label1 = Label(screen, text='Project Type', font=('bold', 18))
            label1_1 = Label(screen, text=type_p, font=('bold', 18))
            label2 = Label(screen, text='Admin', font=('bold', 18))
            label2_1 = Label(screen, text=admin_name, font=('bold', 18))
            label3 = Label(screen, text='Requests', font=('bold', 18))
            request = Button(screen, text='See Requests', bg='#2B2BFF', fg='white', command=see_request)
            back = Button(screen, text='Exit Project', bg='red', fg='white', command=project_exit)

            title1.place(relx=0, rely=0, relheight=0.1, relwidth=1)
            label0.place(relx=0.1, rely=0.13)
            label0_1.place(relx=0.45, rely=0.13)
            label1.place(relx=0.1, rely=0.2)
            label1_1.place(relx=0.45, rely=0.2)
            label2.place(relx=0.1, rely=0.27)
            label2_1.place(relx=0.45, rely=0.27)
            label3.place(relx=0.1, rely=0.34)
            request.place(relx=0.45, rely=0.34, relheight=0.04, relwidth=0.2)
            back.place(relx=0.705, rely=0.844, relwidth=0.3)
           
    #   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -
    
    def todolist():
        screen = Frame(container, border=2)
        screen.place(relx=0.27, rely=0.12, relheight=1, relwidth=0.73)
        
        file = open("Data/p"+str(sno)+"/active.bin", 'r')
        e = file.read()
        file.close()
        
        def edit_activate():
            text.config(state=NORMAL)

        def save_changes():
            file = open("Data/p"+str(sno)+"/todo"+e+".bin", 'w')
            s = StringVar()
            s = text.get("1.0","end")
            file.write(s)
            file.close()
            text.config(state=DISABLED)
            messagebox.showinfo("List Updated", "Data updated successfully.")
            
        title1 = Label(screen, text='TO TO DO LIST', bg='#3b5998', fg='white', font=('bold', 25))
        edit = Button(screen, text='Edit', command=edit_activate)
        sv_chngs = Button(screen, text='Save Changes', command=save_changes)
        text = Text(screen, font=('bold', 22), padx=10, pady=5, bg="#FFFAC1")
        text.config(wrap=WORD)
        
        title1.place(relx=0, rely=0, relheight=0.1, relwidth=1)
        edit.place(relx=0.1, rely=0.12, relheight=0.06, relwidth=0.1)
        sv_chngs.place(relx=0.2, rely=0.12, relheight=0.06, relwidth=0.2)
        text.place(relx = 0.1, rely = 0.18, relheight=0.5, relwidth=0.8)



        try:
            file = open("Data/p"+str(sno)+"/todo"+e+".bin", 'r')
        except:
            file = open("Data/p"+str(sno)+"/todo"+e+".bin", 'w+')
            file.close()
            messagebox.showinfo("Info","Here you can write your Targets for your project.")
        finally:
            file= open("Data/p"+str(sno)+"/todo"+e+".bin", 'r')
        s = file.read()
        text.insert(INSERT, s)
        text.config(state=DISABLED)
        file.close()
        
    #   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -

    def public():
        def look():
            a = search.get()
            d = a+'%'
            conn = mysql.connector.connect(user="root", password="", database="project", host="localhost")
            c = conn.cursor()
            c.execute("select * from magic where name like '{}' or username like '{}'".format(d, d))
            n = c.fetchall()
            text.config(state=NORMAL)
            text.delete("1.0", END)
            x = " - "
            g = "\n"
            t = 1
            for i in n:
                a = 0
                s_no = str(t)+"> "
                t += 1
                for j in i:
                    a += 1
                    e = str(j) + x
                    if a==1:
                        text.insert(INSERT, s_no)
                        text.insert(INSERT, e)
                    elif a<2:
                        text.insert(INSERT, e)
                    else:
                        text.insert(INSERT, j)
                text.insert(INSERT, g)
            text.config(state=DISABLED)

        def click(event):
            look()

        screen = Frame(container, border=2)
        screen.place(relx=0.27, rely=0.12, relheight=1, relwidth=0.73)

        title1 = Label(screen, text='SEARCH PROJECT', bg='#3b5998', fg='white', font=('bold', 25))
        search = Entry(screen, justify='center', font=('bold', 16))
        search.bind("<Return>", click)
        search_button = Button(screen, text='Search', command=look)
        text = Text(screen, font=('bold', 16), padx=10, pady=5, bg='#FFE2E9')
        title1.place(relx=0, rely=0, relheight=0.1, relwidth=1)
        search.place(relx=0.1, rely=0.2, relheight=0.05, relwidth=0.5)
        search_button.place(relx=0.61, rely=0.2, relheight=0.05, relwidth=0.1)
        text.place(relx = 0.1, rely = 0.28, relheight=0.45, relwidth=0.8)
        text.config(wrap=WORD)
        text.insert(INSERT,"Search for a project name or click search to view all available open source projects with their Admin's name.")
        text.config(state=DISABLED)
        
    #   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -

    def project_notes():
        screen = Frame(container, border=2)
        screen.place(relx=0.27, rely=0.12, relheight=1, relwidth=0.73)
        
        file = open("Data/p"+str(sno)+"/active.bin", 'r')
        e = file.read()
        file.close()

        def b():
            a = page.get()
            c = int(a)
            if c>1:
                text.config(state=NORMAL)
                c = c-1
                a = str(c)
                page.delete(0, END)
                page.insert(0,a)
                try:
                    file= open("Data/p"+str(sno)+"/d"+a+"d"+e+".bin", 'r')
                except:
                    file = open("Data/p"+str(sno)+"/d"+a+"d"+e+".bin", 'w+')
                    file.write("Project Name:")
                    file.close()
                finally:
                    file= open("Data/p"+str(sno)+"/d"+a+"d"+e+".bin", 'r')
                s = file.read()
                text.delete("1.0", END)
                text.insert(INSERT, s)
                text.config(state=DISABLED)
                file.close()
        
        def n():
            a = page.get()
            c = int(a)
            c = c+1
            a = str(c)
            page.delete(0, END)
            page.insert(0,a)
            text.config(state=NORMAL)
            try:
                file= open("Data/p"+str(sno)+"/d"+a+"d"+e+".bin", 'r')
            except:
                file = open("Data/p"+str(sno)+"/d"+a+"d"+e+".bin", 'w+')
                file.write("Project Name:")
                file.close()
            finally:
                file= open("Data/p"+str(sno)+"/d"+a+"d"+e+".bin", 'r')
            s = file.read()
            text.delete("1.0", END)
            text.insert(INSERT, s)
            text.config(state=DISABLED)
            file.close()

        def p(event):
            a = page.get()
            
            if a == "":
                messagebox.showerror("Error!","Please enter a valid page number.")
                return 0
            else:
                pass
            
            text.config(state=NORMAL)
            
            try:
                file= open("Data/p"+str(sno)+"/d"+a+"d"+e+".bin", 'r')
            except:
                file = open("Data/p"+str(sno)+"/d"+a+"d"+e+".bin", 'w+')
                file.write("Project Name:")
                file.close()
            finally:
                file= open("Data/p"+str(sno)+"/d"+a+"d"+e+".bin", 'r')
            
            s = file.read()
            text.delete("1.0", END)
            text.insert(INSERT, s)
            text.config(state=DISABLED)
            file.close()


        def edit_activate():
            text.config(state=NORMAL)

        def save_changes():
            a = page.get()
            file = open("Data/p"+str(sno)+"/d"+a+"d"+e+".bin", 'w')
            s = StringVar()
            s = text.get("1.0",END)
            file.write(s)
            file.close()
            text.config(state=DISABLED)
            messagebox.showinfo("List Updated", "Data updated successfully.")

        
        title1 = Label(screen, text='NOTES', bg='#3b5998', fg='white', font=('bold', 25))
        edit = Button(screen, text='Edit', command=edit_activate)
        sv_chngs = Button(screen, text='Save Changes', command=save_changes)      
        backpage = Button(screen, text='<<', command=b)
        page = Entry(screen, font=('bold', 18), justify='center')
        page.bind("<Return>", p)
        nextpage = Button(screen, text='>>', command=n)
        text = Text(screen, font=('bold', 16), padx=10, pady=5, bg='#FFE2E9')
        text.config(wrap=WORD)
        page.insert(0,"1")
        
        title1.place(relx=0, rely=0, relheight=0.1, relwidth=1)
        edit.place(relx=0.1, rely=0.12, relheight=0.06, relwidth=0.1)
        sv_chngs.place(relx=0.2, rely=0.12, relheight=0.06, relwidth=0.2)
        backpage.place(relx=0.6, rely=0.124, relheight=0.052, relwidth=0.1)
        page.place(relx=0.71, rely=0.125, relheight=0.05, relwidth=0.08)
        nextpage.place(relx=0.8, rely=0.124, relheight=0.052, relwidth=0.1)
        text.place(relx = 0.1, rely = 0.18, relheight=0.5, relwidth=0.8)
        try:
            file = open("Data/p"+str(sno)+"/d1d"+e+".bin", 'r')
        except:
            file = open("Data/p"+str(sno)+"/d1d"+e+".bin", 'w+')
            file.write("Project Name:")
            file.close()
            file = open("Data/p"+str(sno)+"/d1d"+e+".bin", 'r')
            messagebox.showinfo("Info","Here you can write in detail about your plans(ideas,goals) regarding your project.")
        finally:
            s = file.read()
            file.close()
        text.insert(INSERT, s)
        text.config(state=DISABLED)

    #   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -

    def code():
        screen = Frame(container, border=2)
        screen.place(relx=0.27, rely=0.12, relheight=1, relwidth=0.73)
        
        file = open("Data/p"+str(sno)+"/active.bin", 'r')
        e = file.read()
        file.close()

        conn = mysql.connector.connect(user="root", password="", database="project", host="localhost")
        c = conn.cursor()
        c.execute("select location from project_access where username like '{}';".format(e))
        n = c.fetchall()
        for i in n:
            for j in i:
                a = j
        c.execute("select admin from project_access where username like '{}';".format(e))
        n = c.fetchall()
        for i in n:
            for j in i:
                admin_id = str(j)
        
        def open_file():
            if e == "none":
                text.config(state=NORMAL)
                text.insert(INSERT, "\nPlease open a project, then select a file to open.")
                text.config(state=DISABLED)
            else:
                file_path = filedialog.askopenfilename(initialdir=a, title="Select a file to open", filetype=(("python files", "*.py"),("text files","*.txt")))
                file = open(file_path, 'r')
                data = file.read()
                file.close()
                text.config(state=NORMAL)
                text.delete(1.0, END)
                text.insert(INSERT, data)
                text.config(state=DISABLED)
        
        def export_project():
            conn = mysql.connector.connect(user="root", password="", database="project", host="localhost")
            c = conn.cursor()
            c.execute("select location from project_access where username like '{}';".format(e))
            n = c.fetchall()
            for i in n:
                for j in i:
                    a = j
            if e == "none":
                text.config(state=NORMAL)
                text.insert(INSERT, "\nPlease open a project.")
                text.config(state=DISABLED)
            else:
                shutil.copytree(src=a, dst=e)
                messagebox.showinfo('Export Successful', 'Project exported to main directory successfully.')
            
        def reload():
            if e == "none":
                text.config(state=NORMAL)
                text.insert(INSERT, "\nPlease open a project.")
                text.config(state=DISABLED)
            else:
                text.config(state=NORMAL)
                text.delete(1.0, END)
                file= open(a+"/"+e+".py", 'r')
                s = file.read()
                text.insert(INSERT, s)
                text.config(state=DISABLED)
                
        def edit_prgm():
            if e == "none":
                text.config(state=NORMAL)
                text.insert(INSERT, "\nPlease open a project.")
                text.config(state=DISABLED)
            else:
                text.config(state=NORMAL)

        def edit_notepad():
            if e == "none":
                text.config(state=NORMAL)
                text.insert(INSERT, "\nPlease open a project.")
                text.config(state=DISABLED)
            else:
                os.system(a+"/"+e+".py")

        def run_prgm():
            if e == "none":
                text.config(state=NORMAL)
                text.insert(INSERT, "\nPlease open a project.")
                text.config(state=DISABLED)
            else:
                os.system("Python "+a+"/"+e+".py")

        def send_admin():
            if e == "none":
                text.config(state=NORMAL)
                text.insert(INSERT, "\nPlease open a project.")
                text.config(state=DISABLED)
            else:
                rt = text.get(1.0, END)

                conn = mysql.connector.connect(user="root", password="", database="project", host="localhost")
                c = conn.cursor()
                c.execute("select name from acc_info where id={};".format(sno))
                n = c.fetchall()
                for i in n:
                    for j in i:
                        name = j

                for i in range(10000):
                    try:
                        file = open(a+"/request/"+name+str(i)+".py", 'r')
                        file.close()
                    except:
                        file = open(a+"/request/"+name+str(i)+".py", 'w+')
                        file.write(rt)
                        file.close()
                        break

                messagebox.showinfo('Info!', 'Your program has been sent to admin.')


        def save():
            conn = mysql.connector.connect(user="root", password="", database="project", host="localhost")
            c = conn.cursor()
            c.execute("select location from project_access where username like '{}';".format(e))
            n = c.fetchall()
            for i in n:
                for j in i:
                    a = j
            if e == "none":
                text.config(state=NORMAL)
                text.insert(INSERT, "\nPlease open a project.")
                text.config(state=DISABLED)
            else:
                t = text.get(1.0, END)
                file = open(a+"/"+e+".py", 'w')
                file.write(t)
                file.close()
                messagebox.showinfo('Success!',"File Saved successfully.")


        title1 = Label(screen, text='EDITOR', bg='#3b5998', fg='white', font=('bold', 25))
        _open = Button(screen, text='Open', command=open_file)
        edit = Button(screen, text='Edit', command=edit_prgm)
        refresh = Button(screen, text='Refresh', command=reload)
        export = Button(screen, text='Export Project', command=export_project)
        text = Text(screen, font=('bold', 12), padx=10, pady=5, bg="#F1EFFF")

        title1.place(relx=0, rely=0, relheight=0.1, relwidth=1)
        _open.place(relx=0.1, rely=0.12, relheight=0.06, relwidth=0.1)
        edit.place(relx=0.2, rely=0.12, relheight=0.06, relwidth=0.1)
        refresh.place(relx=0.3, rely=0.12, relheight=0.06, relwidth=0.1)
        if e == 'none':
            send = Button(screen, text='Send to Admin', command=send_admin)
            send.place(relx=0.4, rely=0.12, relheight=0.06, relwidth=0.2)
        else:
            if sno == admin_id:
                save = Button(screen, text='Update Project', command=save)
                save.place(relx=0.4, rely=0.12, relheight=0.06, relwidth=0.2)
            else:
                send = Button(screen, text='Send to Admin', command=send_admin)
                send.place(relx=0.4, rely=0.12, relheight=0.06, relwidth=0.2)
        export.place(relx=0.6, rely=0.12, relheight=0.06, relwidth=0.2)
        text.place(relx = 0.1, rely = 0.18, relheight=0.5, relwidth=0.8)
        
        if e == "none":
            text.insert(INSERT, "Please open a project.")
            text.config(state=DISABLED)
        else:
            try:
                file = open(a+"/"+e+".py", 'r')
            except:
                file = open(a+"/"+e+".py", 'w+')
                file.close()
            finally:
                file= open(a+"/"+e+".py", 'r')
            s = file.read()
            text.insert(INSERT, s)
            text.config(state=DISABLED)
            file.close()

    #   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -

    def chat_room():
        file = open("Data/p"+str(sno)+"/active.bin", 'r')
        e = file.read()
        file.close()

        def find_user():
            def look():
                a = search.get()
                d = a+'%'
                conn = mysql.connector.connect(user="root", password="", database="project", host="localhost")
                c = conn.cursor()
                c.execute("select name from acc_info where name like '{}';".format(d))
                n = c.fetchall()
                text.config(state=NORMAL)
                text.delete("1.0", END)
                for i in n:
                    for j in i:
                        text.insert(INSERT, j)
                        text.insert(INSERT, "\n")
                text.config(state=DISABLED)
            
            def click(event):
                look()

            def export_all():
                conn = mysql.connector.connect(user="root", password="", database="project", host="localhost")
                c = conn.cursor()
                c.execute("select name from acc_info;")
                tabledata = c.fetchall()
               
                with open("users.csv", 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerows(tabledata)

                print("\nData written in users.csv file successfully.")
                print("\nPrinting Data of users.csv"," file now : \n")
                file = open("users.csv", 'r')
                for i in file:
                    print(i)
                print("Data printed successfully!")

                r.destroy()
                messagebox.showinfo("Success!","Names of all available users are exported successfully to users.csv file.")

            
            r = Tk()
            list_menu = Frame(r, border=2)
            r.geometry('700x450')
            list_menu.place(relx=0, rely=0, relheight=1, relwidth=1)

            title1 = Label(list_menu, text='FIND USER', bg='#3b5998', fg='white', font=('bold', 25))
            search = Entry(list_menu, justify='center', font=('bold', 16))
            search.bind("<Return>", click)
            search_button = Button(list_menu, text='Search', bg='#6790FF', fg='white', command=look)
            export_button = Button(list_menu, text='Download list of all users', bg='#6790FF', fg='white', command=export_all)
            text = Text(list_menu, font=('bold', 16), padx=10, pady=5, bg='#FFE2E9')
            
            title1.place(relx=0, rely=0, relheight=0.15, relwidth=1)
            search.place(relx=0.1, rely=0.2, relheight=0.07, relwidth=0.475)
            search_button.place(relx=0.58, rely=0.2, relheight=0.07, relwidth=0.1)
            export_button.place(relx=0.69, rely=0.2, relheight=0.07, relwidth=0.21)
            text.place(relx = 0.1, rely = 0.3, relheight=0.6, relwidth=0.8)
            text.config(wrap=WORD)
            text.insert(INSERT,"Search for a project name or click search to view all available open source projects with their Admin's name.")
            text.config(state=DISABLED)
        
        def msg_sending():
            del_to = to.get()
            main_msg = message.get(1.0, END)
            
            conn = mysql.connector.connect(user="root", password="", database="project", host="localhost")
            c = conn.cursor()
            
            c.execute("select id from acc_info where name like '{}%';".format(del_to))
            n = c.fetchall()
            for i in n:
                for j in i:
                    userid = str(j)

            try:
                dump = userid
            except:
                messagebox.showerror("Error!","Unable to find a user with this name.")
                return 0
            
            c.execute("select name from acc_info where name like '{}%';".format(del_to))
            n = c.fetchall()
            for i in n:
                for j in i:
                    othername = str(j)
            c.execute("select name from acc_info where id={};".format(sno))
            n = c.fetchall()
            for i in n:
                for j in i:
                    myname = str(j)
            
            try:
                file = open("Data/p"+userid+"/chat.bin", 'a')
            except:
                file = open("Data/p"+userid+"/chat.bin", 'w+')
                file.close()

            file = open("Data/p"+userid+"/chat.bin", 'a')
            file.write("\n"+myname+": "+main_msg)
            file.close()
            file = open("Data/p"+str(sno)+"/chat.bin", 'a')
            file.write("\nYou to "+othername+": "+main_msg)
            file.close()
            message.delete('1.0', END)
            
            text.config(state=NORMAL)
            file = open("Data/p"+str(sno)+"/chat.bin", 'r')
            history = file.read()
            file.close()
            text.delete('1.0', END)
            text.insert(INSERT, history)
            text.config(state=DISABLED)
            text.see('end')
            
        def del_chat():
            n = messagebox.askquestion("Delete Chat History!","Are you sure you want to do this!")
            print(n)
            if n == "yes":
                file = open("Data/p"+str(sno)+"/chat.bin", 'w')
                file.close()
                text.config(state=NORMAL)
                text.delete('1.0', END)
                text.config(state=DISABLED)
                text.see('end')
            else:
                pass

        def refresh():
            chat_data = text.get("1.0",'end-1c')
            file = open("Data/p"+str(sno)+"/chat.bin", 'r')
            history = file.read()
            file.close()
            if history == chat_data:
                screen.after(1000, refresh)
            else:
                text.config(state=NORMAL)
                text.delete('1.0', END)
                text.insert(INSERT, history)
                text.config(state=DISABLED)
                text.see('end')
                screen.after(1000, refresh)
            
        screen = Frame(container, border=2)
        screen.place(relx=0.27, rely=0.12, relheight=1, relwidth=0.73)

        title1 = Label(screen, text='CHAT ROOM', bg='#3b5998', fg='white', font=('bold', 25))
        text = Text(screen, padx=10, pady=5, bg="#FFFAC1")
        text.config(wrap=WORD)
        list_user = Button(screen, text='Find User', bg='#6790FF', fg='white', command=find_user)
        del_all = Button(screen, text='Clear Chat', bg='#6790FF', fg='white', command=del_chat)
        label0 = Label(screen, text='To')
        to = Entry(screen)
        send_msg = Button(screen, text='Send Mail', bg='#6790FF', fg='white', command=msg_sending)
        label1 = Label(screen, text='Message')
        message = Text(screen, padx=10, pady=5)
        message.config(wrap=WORD)

        title1.place(relx=0, rely=0, relheight=0.1, relwidth=1)
        text.place(relx=0.1, rely=0.15, relheight=0.38, relwidth=0.8)
        list_user.place(relx=0.1, rely=0.53, relwidth=0.18)
        del_all.place(relx=0.28, rely=0.53, relwidth=0.18)
        label0.place(relx=0.1, rely=0.6)
        to.place(relx=0.2, rely=0.6, relheight=0.04, relwidth=0.5)
        send_msg.place(relx=0.71, rely=0.6, relwidth=0.18)
        label1.place(relx=0.1, rely=0.65)
        message.place(relx=0.2, rely=0.65, relheight=0.15, relwidth=0.7)

        try:
            file = open("Data/p"+str(sno)+"/chat.bin", 'r')
            history = file.read()
        except:
            file = open("Data/p"+str(sno)+"/chat.bin", 'w+')
            messagebox.showinfo("Info",'Here you can send mail to users on this platform.')
            history = file.read()
        finally:
            file.close() 
            text.insert(INSERT, history)
            text.config(state=DISABLED)
            text.see('end')

        refresh()



    #   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -   -

    
    scr = Tk()
    scr.title('MainScreen')
    scr.geometry('900x650')
    container = Frame(scr)
    sidebar = Frame(container, border=2)
    screen = Frame(container, border=2)
    container.place(relx=0, rely=0, relheight=1, relwidth=1)
    sidebar.place(relx=0, rely=0.12, relheight=1, relwidth=0.27)
    screen.place(relx=0.27, rely=0.12, relheight=1, relwidth=0.73)


    label0 = Label(container, text="CODE  WITH  FREINDS", bg='seagreen', fg='white', font=("bold", 25))
    acc_details = Button(sidebar, text='Account', bg='#7F70FF', fg='white', font=('bold', 20), command=acc_det)
    prjct = Button(sidebar, text='Project', bg='#7F70FF', fg='white', font=('bold', 20), command=project_)
    to_do = Button(sidebar, text='To-to-do', bg='#7F70FF', fg='white', font=('bold', 20), command=todolist)
    public_project = Button(sidebar, text='Search Project', bg='#7F70FF', fg='white', font=('bold', 20), command=public)
    project_notes = Button(sidebar, text='Project Notes', bg='#7F70FF', fg='white', font=('bold', 20), command=project_notes)
    editor = Button(sidebar, text='View Code', bg='#7F70FF', fg='white', font=('bold', 20), command=code)
    messages = Button(sidebar, text='Mails', bg='#7F70FF', fg='white', font=('bold', 20), command=chat_room)
    log_out = Button(sidebar, text='Log Out', bg='#7F70FF', fg='white', font=('bold', 20), command=logout)


    label0.place(relx=0, rely=0, relheight=0.12, relwidth=1)
    acc_details.place(relx=0, rely=0, relheight=0.1, relwidth=1)
    prjct.place(relx=0, rely=0.1, relheight=0.1, relwidth=1)
    to_do.place(relx=0, rely=0.2, relheight=0.1, relwidth=1)
    public_project.place(relx=0, rely=0.3, relheight=0.1, relwidth=1)
    project_notes.place(relx=0, rely=0.4, relheight=0.1, relwidth=1)
    editor.place(relx=0, rely=0.5, relheight=0.1, relwidth=1)
    messages.place(relx=0, rely=0.6, relheight=0.1, relwidth=1)
    log_out.place(relx=0, rely=0.7, relheight=0.1, relwidth=1)

    acc_det()
    
    scr.mainloop()

database_check()
