from tkinter import *
import tkinter.messagebox
import sqlite3
from PIL import Image, ImageTk
import time
import calendar
import datetime


def Clock():
    current_time = time.strftime("%H:%M:%S")
    clock.config(text = current_time)
    clock.after(100, Clock)


'''
    QUIT BUTTON
        IF CLICKED, ASKIND USER TO CONFIRM QUITING
        IF USER CLICK 'YES', WINDOW CLOSES
'''
def exitApp():
    opt_ex = tkinter.messagebox.askquestion('Exit application', 'Are you sure?')
    if opt_ex == 'yes':
        root.destroy()

def about():
    tkinter.messagebox.showinfo("About page", "This is a registration page")




''' 
    THIRD WINDOW - CHECK-OUT PASSWORD
        CONNECTING TO DATABASE, SELECT ALL FROM USER
        IF ENTRED EMAIL IS EQUAL TO SOME EMAIL IN DATABASE, WRITE THAT PASSWORD TO 'YOUR PASSWORD.TXT' FILE
        ELSE SEND A MESSAGE 'EMAIL NOT FOUND' AND ASK USER IF HE WANTS TO TRY AGAIN
        IF USER SAY 'NO', WINDOW CLOSES
'''
def third_window():
    window2 = Toplevel()
    window2.geometry('300x100')
    window2.title('Password Recovery')
    photo = PhotoImage(file = 'wallpaper.png')
    label = Label(window2, image = photo)
    label.pack()

    ent_rec = StringVar()

    def recover():

        rec = ent_rec.get()

        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM user")
        read = cur.fetchall()

        for i in read:
            if rec == i[2]:
                tkinter.messagebox.showinfo("Success", "Successfully sent! Password saved in 'your_password.txt' file")
                with open('your_password.txt','w') as file:
                    file.write(i[3])
                    window2.destroy()
                    break

            elif len(rec) == 0:
                tkinter.messagebox.showinfo('Not found', 'Empty field, please enter email')
                break

        else:
            mail_n_f = tkinter.messagebox.askquestion('Not found', 'Email not found, do you want to try again?')
            if mail_n_f == 'no':
                window2.destroy()


    label_rc = Label(window2, text = ' Enter email ', bg = '#004038', fg = 'white', relief = 'raised', width = 11, font = ('arial', 12, 'bold'))
    label_rc.place(x = 10, y = 28)
    entry_rec = Entry(window2, textvar = ent_rec)
    entry_rec.place(x = 140, y = 30)
    button_rec = Button(window2, text = 'Send', bg = 'red', fg = 'white', width = 13, relief = 'raised', font = ('arial', 10, 'bold'), command = recover)
    button_rec.place(x = 145, y = 60)

    window2.mainloop()



''' 
    SECOND WINDOW - LOGIN
        GETTING EMAIL AND PASSWORD FROM LOGIN FIELDS
        CONNECTING TO DATABASE, SELECT ALL FROM USER
        CHECKING IF EMAIL AND PASSWORD EXIST IN DATABASE
        IF THEY EXIST, USER-DATA ARE WRITED IN RESULT.TXT FILE
        IF LENGHT OF EMAIL OR PASSWORD ARE 0, SEND A MESSAGE TO USER
'''
def second_window():
    window = Toplevel()
    window.geometry('410x400')
    window.title('Login Page')
    photo = PhotoImage(file = 'wallpaper.png')
    label = Label(window, image = photo)
    label.pack()

    ent_lg_em = StringVar()
    ent_lg_pass = StringVar()

    def login():

        e_mail = ent_lg_em.get()
        password = ent_lg_pass.get()

        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM user")
        read = cur.fetchall()

        for i in read:
            if e_mail == i[2] and password == i[3]:
                tkinter.messagebox.showinfo("Success", "Login successfull, check 'result.txt' file")
                with open('result.txt','w') as file:
                    file.write(str(i))
                    window.destroy()
                    break
        else:
            if len(e_mail) == 0 or len(password) == 0:
                tkinter.messagebox.showwarning("Failed", "Please fill up required fields")
            else:
                tkinter.messagebox.showwarning("Failed", "Wrong email or password")


    label_w2 = Label(window, text= ' Enter your email and password ', bg = '#004038', fg = 'white', relief = 'raised', font = ('arial', 14, 'bold'))
    label_w2.place(x = 20, y = 100)
    label_w3 = Label(window, text = ' Email ', bg = '#004038', fg = 'white', relief = 'raised', width = 9, font = ('arial', 11, 'bold'))
    label_w3.place(x = 30, y = 200)
    label_w4 = Label(window, text = ' Password ', bg = '#004038', fg = 'white', relief = 'raised', width = 9, font = ('arial', 11, 'bold'))
    label_w4.place(x = 30, y = 250)
    label_rec = Label(window, text = "Password forgotten? ", bg = '#004038', fg = 'white', relief = 'raised', font = ('arial',10))
    label_rec.place(x = 210, y = 370)
    
    entry_w3 = Entry(window ,textvar = ent_lg_em)
    entry_w3.place(x = 130, y = 202)
    entry_w4 = Entry(window, show = "*", textvar = ent_lg_pass)
    entry_w4.place(x = 130, y = 252)
    
    btn_login = Button(window, text = 'Login', bg = 'red', fg = 'white', width = 7, font = ('bold',10, 'bold'), command = login)
    btn_login.place(x = 125, y = 300)
    btn_cancel = Button(window, text = 'Cancel', bg = 'red', fg = 'white', width = 7, font = ('bold',10, 'bold'), command = window.destroy)
    btn_cancel.place(x = 190, y = 300)
    btn_rec = Button(window, text = 'Click here', bg = 'red', fg = 'white', relief = 'raised', font = ('arial', 9, 'bold'), command = third_window)
    btn_rec.place(x = 335 , y = 370)

    window.mainloop()



''' 
    FIRST WINDOW - MAIN WINDOW FOR REGISTRATION
        IF FIELDS ARE EMPTY, ASK USER TO FILL UP ALL FIELDS
        IF EMAIL DONT CONTAINS '@' OR '.', EMAIL IS NOT GOOD
        CHECK IF PASSWORDS ARE THE SAME
        CONNECTING TO DATABASE, SELECT ALL FROM USER
        CHECK IF EMAIL ALREADY EXIST IN DATABASE
        IF EMAIL DONT EXIST, DATAS ARE WRITED IN
'''
root = Tk()
root.geometry('600x580')
root.title('Register Page')
photo = PhotoImage(file = 'wallpaper.png')
label = Label(root, image=photo)
label.pack()

# OPTIONS AT THE TOP OF THE PAGE (NOT IMPORTANT)

menu = Menu(root)
root.config(menu = menu)
submenu1 = Menu(menu)
menu.add_cascade(label = 'File', menu = submenu1)
submenu1.add_command(label = 'Exit', command = root.destroy)
submenu2 = Menu(menu)
menu.add_cascade(label = 'Options', menu = submenu2)
submenu2.add_command(label = 'About', command = about)

def database():
    firstname = ent_fn.get()
    lastname = ent_ln.get()
    email = ent_em.get()
    password = ent_pass.get()
    password2 = ent_pass2.get()
    state = var.get()
    gendr = rb1.get()
    d = var1.get()
    m = var2.get()
    y = var3.get()


    if len(firstname) == 0 or len(lastname) == 0 or len(email) == 0 or len(password) == 0 \
     or len(state) == 0 or len(gendr) == 0 or len(d) == 0 or len(m) == 0 or len(y) == 0:
        tkinter.messagebox.showwarning('Failed', 'Please fill up all required fields')

    elif '@' not in email or '.' not in email:
        tkinter.messagebox.showwarning('Error', 'Email not entered correctly')

    elif password2 != password:
        tkinter.messagebox.showwarning('Error', 'Passwords not equal')

    else:
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM user")
        read = cur.fetchall()

        for i in read:
            if i[2] == email:
                tkinter.messagebox.showwarning('Registration failed', 'Email already exist')
                break
        else:
            cur.execute('CREATE TABLE IF NOT EXISTS user \
                (firstName TEXT, lastName TEXT, mail TEXT, password TEXT, state TEXT, gendre TEXT, day TEXT, month TEXT, year TEXT)')
            cur.execute('INSERT INTO user \
                (firstName, lastName, mail, password, state, gendre, day, month, year) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',\
                (firstname, lastname, email, password, state, gendr, d, m, y,))
            conn.commit()
            conn.close()

ent_fn = StringVar()
ent_ln = StringVar()
ent_em = StringVar()
ent_pass = StringVar()
ent_pass2 = StringVar()
var = StringVar()
rb1 = StringVar()
var1 = StringVar()
var2 = StringVar()
var3 = StringVar()


label = Label(root, text = ' Registration ', bg = '#004038', fg = 'white', width = 11, relief = 'ridge', font = ('Times', 30, 'bold'))
label.place(x = 50, y = 80)
label2 = Label(root, text = ' First name ', bg = '#004038', fg = 'white', width = 11, relief = 'raised', font = ('arial', 12, 'bold'))
label2.place(x = 80, y = 200)
label3 = Label(root, text = ' Last name ', bg = '#004038', fg = 'white', width = 11, relief = 'raised', font = ('arial', 12, 'bold'))
label3.place(x = 80, y = 230)
label4 = Label(root, text = ' E-mail ', bg = '#004038', fg = 'white', width = 11, relief = 'raised', font = ('arial', 12, 'bold'))
label4.place(x = 80, y = 260)
label_pw = Label(root, text = ' Password ', bg = '#004038', fg = 'white', width = 11, relief = 'raised', font = ('arial', 12, 'bold'))
label_pw.place(x = 80, y = 290)
label5 = Label(root, text = ' Country ', bg = '#004038', fg = 'white', width = 11, relief = 'raised', font = ('arial', 12, 'bold'))
label5.place(x = 80, y = 325)
b_d = Label(root, text = ' Date of birth ', bg = '#004038', fg = 'white', width = 11, relief = 'raised', font = ('arial', 12, 'bold'))
b_d.place(x = 80, y = 360)
label7 = Label(root, text = ' Gendre ', bg = '#004038', fg = 'white', width = 11, relief = 'raised', font = ('arial', 12, 'bold'))
label7.place(x = 80, y = 400)


entry2 = Entry(root, font = ('arial', 10, 'bold'), textvar = ent_fn)
entry2.place(x = 210, y = 200)
entry3 = Entry(root, font = ('arial', 10, 'bold'), textvar = ent_ln)
entry3.place(x = 210, y = 230)
entry4 = Entry(root, font = ('arial', 10, 'bold'), textvar = ent_em)
entry4.place(x = 210, y = 260)
entry_pw = Entry(root, font = ('arial', 10, 'bold'), show = '*', textvar = ent_pass)
entry_pw.place(x = 210, y = 290)
entry_pw2 = Entry(root, font = ('arial', 10, 'bold'), show = '*', textvar = ent_pass2)
entry_pw2.place(x = 355, y = 290)

# DROP-DOWN MENUS

list_country = ['Serbia', 'Croatia', 'Bulgaria', 'Bosnia and Herzegovina', 'Romania', 'Montenegro', 'Albanija', 'Macedonia']
droplist = OptionMenu(root, var, *list_country)
var.set('Select Country')
droplist.config(width = 14, bg = '#004038', fg = 'grey', font = ('arial', 9, 'bold'))
droplist.place(x = 210, y = 325)

day = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31']
droplist = OptionMenu (root, var1, *day)
var1.set('Select Day')
droplist.config(width = 10, bg = '#004038', fg = 'grey', font = ('arial', 9, 'bold'))
droplist.place(x = 210, y = 360)

month = ['January', 'February', 'March', 'April', 'May', 'July', 'Jul', 'August', 'September', 'October', 'November', 'December']
droplist = OptionMenu(root, var2, *month)
var2.set('Select Month')
droplist.config(width = 12, bg = '#004038', fg = 'grey', font = ('arial', 9, 'bold'))
droplist.place(x = 300, y = 360)

year = ['1980', '1981', '1982', '1983', '1984', '1985', '1986', '1987', '1988', '1989', '1990', '1991', '1992', '1993', '1994', '1995', '1996', '1997' ,'1998', '1999', '2000']
droplist = OptionMenu(root, var3, *year)
var3.set('Select Year')
droplist.config(width = 10, bg = '#004038', fg = 'grey', font = ('arial', 9, 'bold'))
droplist.place(x = 400, y = 360)


rbtn1 = Radiobutton(root, text = 'Male', value = 'Male', variable = rb1, bg = '#004038', fg = 'grey', width = 7, relief = 'raised', font = ('arial', 10, 'bold'))
rbtn1.place(x = 210, y = 400)
rbtn2 = Radiobutton(root, text = 'Female', value = 'Female', variable = rb1, bg = '#004038', fg = 'grey', width = 7, relief = 'raised', font = ('arial', 10, 'bold'))
rbtn2.place(x = 295, y = 400)


login_button = Button(root, text = 'Login', bg = 'red', fg = 'white', width = 23, relief ='raised', font = ('arial', 11, 'bold'), command = second_window)
login_button.place(x = 210, y = 520)
register_button = Button(root, text = 'Register', bg = 'red', fg = 'white', width = 10, font = ('arial', 12, 'bold'), command = database)
register_button.place(x = 210, y = 470)
quit_button = Button(root, text = 'Quit', bg = 'red', fg = 'white', width = 10, font = ('arial', 12, 'bold'), command = exitApp)
quit_button.place(x = 320, y = 470)


clock = Label(root, bg = '#004038', fg = 'white', relief = 'raised', font = ('arial', 20, 'bold'))
clock.place(x = 450, y = 20)
date = Label(root, text=f"{datetime.datetime.now():%a, %b %d %Y}", fg="white", bg="#004038", relief = 'raised', font=("arial", 10, 'bold'))
date.place(x = 450, y = 60)



if __name__ == '__main__':
    Clock()
    root.mainloop()