from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
from TYtkinter import TrendyolData
from tkinter import messagebox
import time
import threading
import smtplib
class TRendYouAll(Frame):
    def __init__(self, main_screen):
        Frame.__init__(self, main_screen, padx=30, pady=30)

        self.window = main_screen
        self.width = 570
        self.height = 900
        self.window.wm_iconbitmap('tyicon.ico')
        self.window.title("WebScraping")
        self.window.minsize(width=570, height=900)
        self.window.maxsize(width=570, height=900)
        self.window.geometry("570x900+50+50")
        self.window.configure(bg='gray69')
        self.pack()

        self.counter_file = 0

        self.bg_img = Image.open('bg.png')
        self.bg_img = self.bg_img.resize((570, 900))
        self.image_bg = ImageTk.PhotoImage(self.bg_img)
        self.bg_img_Label = Label(self.window, image=self.image_bg)
        self.bg_img_Label.place(x=0, y=0)

        self.product_var = StringVar()
        self.search_Label = Label(self.window, relief=FLAT, text='Entry Product', bg='VioletRed1', font=('Bauhaus 93', 10, 'normal'))
        self.search_Label.place(x=130, y=300, width=100, height=30)
        self.product_entry = Entry(self.window, textvariable=self.product_var, font=('calibre', 10, 'normal'))
        self.product_entry.place(x=230, y=300, width=170, height=30)


        self.option_order = StringVar()
        self.option_order.set('Choose One')
        self.Order_label = Label(self.window, relief=FLAT, text='Order By', bg='yellow3', font=('Bauhaus 93', 10, 'normal'))
        self.Order_label.place(x=130, y=400, width=100, height=30)

        self.option_menu = OptionMenu(self.window, self.option_order, "Recommended", "Best Sellers", "Newest Arrivals",
                                      "Price: Low to High", "Price: High to Low", "Most Liked", "Most Commented")
        self.option_menu.place(x=230, y=400, width=170, height=30)

        self.amountData = Label(self.window, relief=FLAT, text='Amount of Data %50', bg='OrangeRed2',
                                font=('Bauhaus 93', 10, 'normal'))
        self.amountData.place(x=130, y=500, width=150, height=30)
        self.slider = ttk.Scale(self.window, from_=1, to=99, orient="horizontal", command=self.scale_move)
        self.slider.set(50)
        self.slider.place(x=280, y=500, width=200, height=30)


        self.file_name = StringVar()
        self.file_Label = Label(self.window, relief=FLAT, text='Entry File Name', bg='cyan',
                                  font=('Bauhaus 93', 10, 'normal'))
        self.file_Label.place(x=130, y=600, width=100, height=30)
        self.file_name_entry = Entry(self.window, textvariable=self.file_name, font=('calibre', 10, 'normal'))
        self.file_name_entry.place(x=230, y=600, width=170, height=30)


        self.start_Button = Button(self.window, text='Start', command=self.kaos, bg='orange')
        self.start_Button.place(x=400, y=700, width=80, height=30)

        self.mail_ = StringVar(value='user@mail.com')
        self.mail_Label = Label(self.window, relief=FLAT, text='Let me know after the data is ready.', bg='gray', fg='white', font=('calibre', 10, 'normal'))
        self.mail_Label.place(x=150, y=780, width=300, height=30)
        self.mail_entry = Entry(self.window, textvariable=self.mail_, font=('calibre', 10, 'normal'), bg='gray64')
        self.mail_entry.place(x=150, y=810, width=300, height=30)


    def scale_move(self, value):
        self.amountData.configure(text='Amount of Data %'+str(value[:2]))


    def kaos(self):
        if self.counter_file <= 4:
            self.counter_file += 1
            amountData = self.slider.get()
            product = self.product_var.get().replace(' ', '%20')
            OrderBy = self.option_order.get()
            FileName = self.file_name.get()
            mail = self.mail_.get()
            dict_order = {"Recommended": 'SCORE', "Best Sellers": 'BEST_SELLER', "Newest Arrivals": 'MOST_RECENT',
                                          "Price: Low to High": 'PRICE_BY_ASC', "Price: High to Low" : 'PRICE_BY_DESC', "Most Liked": 'MOST_FAVOURITE', "Most Commented": 'MOST_RATED'}

            OrderBy = dict_order[str(OrderBy)]
            loading_finish = Label(self.window, relief=FLAT, text='Preparing ' + str(FileName) + ' file ...', bg='snow3',
                                   font=('Bauhaus 93', 10, 'normal'))
            loading_finish.place(x=130, y=(self.counter_file * 30) + 700, width=150, height=30)

            f = TrendyolData(str(product), int(amountData), OrderBy, str(FileName))
            t = threading.Thread(target=f.changePage)
            t.start()

            while t.is_alive():
                self.window.update()
                time.sleep(0.1)

            loading_finish.configure(text="The " + str(FileName) + " file is ready.")
            color_list = ['grey60', 'grey55', 'grey50', 'grey45', 'grey40', 'grey35', 'grey30', 'grey25',
                          'grey20',
                          'grey15', 'grey10', 'grey5', 'grey1']
            for i in color_list:
                self.window.update()
                time.sleep(0.5)
                loading_finish.configure(bg=i)
            loading_finish.destroy()
            self.counter_file -= 1
            if mail != 'user@mail.com':
                send = threading.Thread(target=self.send_mail, args=(str(mail), ))
                send.start()

        else:
            messagebox.showerror('WebScraping Error', 'Warning: It is not recommended to scrape data from more than four '
                                               'websites simultaneously. Scraping large amounts of data can slow down '
                                               'your system and overload the websites you are scraping. Please limit '
                                               'your requests to four or fewer at a time.')

    @staticmethod
    def send_mail(mail):

        gmail_user = "pythontestinfo@gmail.com"
        gmail_password = "umfilxybhvdccjqm"

        smtp_server = 'smtp.gmail.com'
        smtp_port = 587

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(gmail_user, gmail_password)

        to = mail
        subject = "Python Test"
        body = "Hi, User; Process finished."
        message = f"Subject: {subject}\n\n{body}"
        try:
            server.sendmail(gmail_user, to, message)
        except:
            messagebox.showerror('WebScraping Error',
                                 'Warning: Message could not be delivered to user')
        server.quit()


root = Tk()
a = TRendYouAll(root)
a.mainloop()
