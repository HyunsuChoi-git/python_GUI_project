from tkinter import *
import tkinter.ttk as ttk
import tkinter.filedialog as filedialog

root = Tk()
root.title("이미지 합치기 (python project)")
root.geometry("+1200+600")  #크기지정 + 위치지정 ("가로x세로+x측+y측")
root.resizable(False, False)

def add_file():
    print("** 파일추가 **")
    filename = filedialog.askopenfilename(initialdir="", title="이미지 선택", filetypes=(("png", "*.png"), ("jpg", "*.jpg"), ("eme", "*.eme")))
    listbox.insert(END, filename) # gui 리스트 박스에 파일 추가

def delete_file():
    print("** 선택삭제 **")
    print(reversed(listbox.curselection()))
    for i in reversed(listbox.curselection()):
        listbox.delete(i)   # gui 리스트 박스에 파일 삭제

def find_file():
    print("** 찾아보기 **")
    dirname = filedialog.askdirectory(initialdir="/", title="저장경로를 지정하세요.")
    path_entry.delete(0, END)
    path_entry.insert(0, dirname)
    print("저장경로 :", dirname)


def selectFile():
    print("이미지 선택")

def start():
    print("** 시작 **")

    #저장경로 체크
    if not os.path.isdir(path_entry.get()):
        msgbox.showerror("오류","저장경로를 찾을 수 없습니다.")
        return
        
    print(width_option.get())
    print(room_option.get())
    print(format_option.get())
    print(path_entry.get())
    print(listbox.get(0, END))


# 추가/삭제 버튼
frame_btn = Frame(root)
frame_btn.pack(fill="x", expand=False, pady=3)
addBtn = Button(frame_btn, text="파일추가", command=add_file, width=12, pady=5)
addBtn.pack(side="left", padx=3)
deleteBtn = Button(frame_btn, text="파일삭제", command=delete_file, width=12, pady=5)
deleteBtn.pack(side="right", padx=3)



# 추가/삭제 버튼
frame_btn = Frame(root)
frame_btn.pack(fill="x", expand=False, pady=3)
addBtn = Button(frame_btn, text="파일추가", command=add_file, width=12, pady=5)
addBtn.pack(side="left", padx=3)
deleteBtn = Button(frame_btn, text="파일삭제", command=delete_file, width=12, pady=5)
deleteBtn.pack(side="right", padx=3)

#스크롤 / 파일업로드 공간
frame_room = Frame(root)
frame_room.pack(fill="x", expand=False, pady=3)

scrollbar = Scrollbar(frame_room)
scrollbar.pack(side="right", fill="y")

listbox = Listbox(frame_room, selectmode="multiple", height=15, yscrollcommand=scrollbar.set)
listbox.pack(fill="both", side="left", padx=3, expand=True)
#txt = Text(frame_room, yscrollcommand=scrollbar.set, width=45)
#txt.pack(side="left", fill="both", expand=True, padx=3)

scrollbar.config(command=listbox.yview)


#저장경로 (경로text박스, 찾아보기 버튼)
frame_save_lable = LabelFrame(root, text="저장경로")
frame_save_lable.pack(fill="x", expand="False", padx=3)

path_entry = Entry(frame_save_lable, width=63)
path_entry.pack(side="left", fill="x", expand=True, ipady=4 )
find_btn = Button(frame_save_lable, text="찾아보기", pady=1, padx=10, command=find_file)
find_btn.pack(side="right", pady=5, padx=3)


#옵션 (가로넓이, 간격, 포맷)
frame_option_label = LabelFrame(root, text="옵션")
frame_option_label.pack(fill="x", expand="False", padx=3, pady=3)

width = Label(frame_option_label, text="가로넓이", width=10)
width.grid(row=0, column=0)
width_option_group = ["원본유지", "1024", "800", "640"]
width_option = ttk.Combobox(frame_option_label, value=width_option_group, state="readonly", width=10)
width_option.current(0)
width_option.grid(row=0, column=1, pady=5, padx=3)

room = Label(frame_option_label, text="간격", width=10)
room.grid(row=0, column=2)
room_option_group = ["없음", "보통", "넓게", "좁게"]
room_option = ttk.Combobox(frame_option_label, value=room_option_group, state="readonly", width=10)
room_option.current(0)
room_option.grid(row=0, column=3, pady=5, padx=3)

format = Label(frame_option_label, text="포맷", width=10)
format.grid(row=0, column=4)
format_option_group = ["PNG", "JPG", "BMP"]
format_option = ttk.Combobox(frame_option_label, value=format_option_group, state="readonly", width=10)
format_option.current(0)
format_option.grid(row=0, column=5, pady=5, padx=3)

#진행상황 (프로그레스 바)
frame_status_lable = LabelFrame(root, text="진행상황")
frame_status_lable.pack(fill="x", expand="False", padx=3)

p_var = DoubleVar()
progressbar = ttk.Progressbar(frame_status_lable, maximum=100, variable=p_var)
progressbar.pack(fill="x", pady=5, padx=3)

# 시작/닫기 버튼
frame_btn = Frame(root)
frame_btn.pack(fill="x", expand=False, pady=3)
addBtn = Button(frame_btn, text="닫기", command=root.quit, width=12, pady=5)
addBtn.pack(side="right", padx=3)
deleteBtn = Button(frame_btn, text="시작", command=start, width=12, pady=5)
deleteBtn.pack(side="right", padx=3)


root.mainloop()