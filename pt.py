import tkinter
import numpy, os
from time import strftime
from save_txt import data_time
from tkinter.filedialog import askdirectory
from tkinter.messagebox import showinfo

window = tkinter.Tk()
window.iconbitmap('1.ico')
window.geometry('440x340+740+300')
window.resizable(0, 0)
window.title('Pt thermistor converter')

hello = ['hello', 'Hello', 'HELLO', '你好', '您好', 'hi', 'Hi', 'HI']
times = strftime("%Y%m%d_%H")[3:]


def quit_win():
    with open('ptc_setting', 'w', encoding='utf-8')as g:
        g.write(str(dict_win))
    window.destroy()


try:
    with open(r'ptc_setting', 'r', encoding='utf-8')as f:
        dict_win = eval(f.read())
except:
    dict_win = {'filepath': '', 're_type': 1, 'co_mode': 1}
re_type = dict_win['re_type']
co_mode = dict_win['co_mode']


def mu_file():
    dict_win['filepath'] = askdirectory()


def history():
    if dict_win['filepath'] == '':
        showinfo(title='history', message='当前未选择历史记录的保存路径！')
    else:
        path_his = dict_win['filepath'].replace('/', '\\')
        os.system('explorer.exe %s' % path_his)


def help_win():
    showinfo(title='Help', message='1. 在输入框中输入相应值，点击转换按钮,下方显示转换后的值；'
                                   '\n2. 默认工作目录是此软件的安装目录；\n3. 电阻值的默认单位是Ω，温度值的默认单位是℃；\n4. 转换方式依据《JJG229-2010》标准文件。')


def help_log():
    showinfo(title='Update log', message='1.改变了设置的存储方式，由两个配置文件变为一个；\n2.历史记录可以直接打开文件夹。')


def about_win():
    showinfo(title='About', message='Pt thermistor converter\n\n版本号：#1.0.0 正式版\n开发者：散人杨某\n发布日期：2021/4/3')


def setting():
    global re_type, co_mode

    def exit_setting():
        global re_type, co_mode
        dict_win['re_type'] = re_type
        dict_win['co_mode'] = co_mode
        window_setting.destroy()

    def ptht():
        global re_type
        # print(var_pt.get())
        re_type = int(var_pt.get())

    def ptdc():
        global co_mode
        # print(var_ct.get())
        co_mode = int(var_ct.get())

    var_pt = tkinter.StringVar()
    var_pt.set(re_type)
    var_ct = tkinter.StringVar()
    var_ct.set(co_mode)
    window_setting = tkinter.Toplevel(window)
    window_setting.title('Setting')
    window_setting.resizable(0, 0)
    window_setting.geometry('360x280+780+350')
    window_setting.iconbitmap('1.ico')
    tkinter.Label(window_setting, text='铂电阻类型', fg='#333333', font=('微软雅黑', 14)).place(x=180, y=50, anchor='center')
    tkinter.Label(window_setting, text='转换方式', fg='#333333', font=('微软雅黑', 14)).place(x=180, y=150, anchor='center')
    tkinter.Button(window_setting, text=' OK ', font=('微软雅黑', 10),
                   bg='#cccccc', fg='#333333', activebackground='#dddddd', activeforeground='#666666',
                   relief='sunken', bd=0, padx=20, pady=2,
                   command=exit_setting).place(x=340, y=260, anchor='se')
    tkinter.Radiobutton(window_setting, text='Pt1000', font=('微软雅黑', 13), bg='#ffffff', fg='#333333',
                        width=12, indicatoron=False, bd=0, selectcolor='#9BCD9B', activebackground='#dddddd',
                        variable=var_pt, value=1, command=ptht).place(x=180, y=90, anchor='e')
    tkinter.Radiobutton(window_setting, text='Pt100', font=('微软雅黑', 13), bg='#ffffff', fg='#333333',
                        width=12, indicatoron=False, bd=0, selectcolor='#9BCD9B', activebackground='#dddddd',
                        variable=var_pt, value=2, command=ptht).place(x=180, y=90, anchor='w')
    tkinter.Radiobutton(window_setting, text='Ω → ℃', font=('微软雅黑', 13), bg='#ffffff', fg='#333333',
                        width=12, indicatoron=False, bd=0, selectcolor='#9BCD9B', activebackground='#dddddd',
                        variable=var_ct, value=1, command=ptdc).place(x=180, y=190, anchor='e')
    tkinter.Radiobutton(window_setting, text='℃ → Ω', font=('微软雅黑', 13), bg='#ffffff', fg='#333333',
                        width=12, indicatoron=False, bd=0, selectcolor='#9BCD9B', activebackground='#dddddd',
                        variable=var_ct, value=2, command=ptdc).place(x=180, y=190, anchor='w')
    window_setting.protocol('WM_DELETE_WINDOW', exit_setting)


def entry(num):
    global re_type, co_mode
    global dict_win
    # print(re_type, co_mode)
    try:
        if num in hello:
            result = '你好，欢迎使用此脚本\n 详情请查看帮助页面！'
        else:
            num = float(num)
            A = 3.9083 * 10 ** (-3)
            B = -5.775 * 10 ** (-7)
            C = -4.183 * 10 ** (-12)
            if re_type == 1 and co_mode == 1:
                R0 = 1000
                if 3905.1 > num >= 1000:
                    a = B
                    b = A
                    c = 1 - num / R0
                    arg = [a, b, c]
                    root = numpy.roots(arg)
                    temperature = root[1]
                elif 184.7 < num < 1000:
                    a = C
                    b = -100 * C
                    c = B
                    d = A
                    e = 1 - num / R0
                    arg = [a, b, c, d, e]
                    root = numpy.roots(arg)
                    temperature = root[3].real
                else:
                    temperature = '人生苦短，我用python'
                result = '%.5f ℃' % temperature
            elif re_type == 1 and co_mode == 2:
                R0 = 1000
                if -200.1 < num < 0:
                    temperature = R0 * (1 + A * num + B * num ** 2 + C * (num - 100) * num ** 3)
                elif 0 <= num < 850.1:
                    temperature = R0 * (1 + A * num + B * num ** 2)
                else:
                    pass
                result = '%.5f Ω' % temperature
            elif re_type == 2 and co_mode == 1:
                R0 = 100
                if 390.51 > num >= 100:
                    a = B
                    b = A
                    c = 1 - num / R0
                    arg = [a, b, c]
                    root = numpy.roots(arg)
                    temperature = root[1]
                elif 18.47 < num < 100:
                    a = C
                    b = -100 * C
                    c = B
                    d = A
                    e = 1 - num / R0
                    arg = [a, b, c, d, e]
                    root = numpy.roots(arg)
                    temperature = root[3].real
                else:
                    pass
                result = '%.5f ℃' % temperature
            elif re_type == 2 and co_mode == 2:
                R0 = 100
                if -200.1 < num < 0:
                    temperature = R0 * (1 + A * num + B * num ** 2 + C * (num - 100) * num ** 3)
                elif 0 <= num < 850.1:
                    temperature = R0 * (1 + A * num + B * num ** 2)
                else:
                    pass
                result = '%.5f Ω' % temperature
            else:
                pass
            data_time(num, result, times, dict_win['filepath'])
    except:
        result = '输入错误'
    return result


def transformation():
    lb2.config(text=entry(et.get()))


def ret(self):
    transformation()


tkinter.Label(window, text='输入值', font=('微软雅黑', 14), bg='#eeeeee', fg='#333333',
              height=2).place(x=220, y=40, anchor='center')
et = tkinter.Entry(window, show=None, width=14, justify='center', relief='flat', fg='#333333', font=('微软雅黑', 16))
et.place(x=220, y=80, anchor='center')
et.bind('<Return>', ret)
bt = tkinter.Button(window, text=' ⇵ ', bg='#cccccc', fg='#333333', activebackground='#dddddd',
                    activeforeground='#666666', relief='sunken', bd=0,
                    padx=20, pady=2,
                    command=transformation, font=('微软雅黑', 12))
bt.place(x=220, y=130, anchor='center')
lb2 = tkinter.Label(window, text='', width=20, height=2, font=('微软雅黑', 20), bg='#eeeeee', fg='#333333')
lb2.place(x=220, y=230, anchor='center')

menu_bar = tkinter.Menu(window)

file_menu = tkinter.Menu(menu_bar, tearoff=0, activeforeground='#000000', activebackground='#91c9f7')
menu_bar.add_cascade(label='File', menu=file_menu)
file_menu.add_command(label='Working path', command=mu_file)
file_menu.add_command(label='History', command=history)
file_menu.add_separator()
file_menu.add_command(label='Exit', command=quit_win)

setting_menu = tkinter.Menu(menu_bar, tearoff=0, activeforeground='#000000', activebackground='#91c9f7')
menu_bar.add_cascade(label='Configure', menu=setting_menu)
setting_menu.add_command(label='Setting', command=setting)

help_menu = tkinter.Menu(menu_bar, tearoff=0, activeforeground='#000000', activebackground='#91c9f7')
menu_bar.add_cascade(label='Help', menu=help_menu)
help_menu.add_command(label='Help', command=help_win)
help_menu.add_command(label='Update log', command=help_log)
help_menu.add_command(label='About', command=about_win)

window.config(menu=menu_bar)

window.protocol('WM_DELETE_WINDOW', quit_win)
window.mainloop()
