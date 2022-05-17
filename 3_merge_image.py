from tkinter import *
import tkinter.ttk as ttk
import tkinter.filedialog as filedialog
import tkinter.messagebox as msgbox
import os
from turtle import delay
from urllib.parse import MAX_CACHE_SIZE
from PIL import Image

# 파일추가
def add_file():
    filenames = filedialog.askopenfilenames(initialdir="Downloads", \
        title="이미지 선택", \
        filetypes=(("png", "*.png"), ("jpg", "*.jpg"), ("eme", "*.eme")))
    
    for i in filenames:
        listbox.insert(END, i) # gui 리스트 박스에 파일 추가

# 선택삭제
def delete_file():
    print(reversed(listbox.curselection()))
    for i in reversed(listbox.curselection()):
        listbox.delete(i)   # gui 리스트 박스에 파일 삭제

# 저장경로
def find_file():
    dirname = filedialog.askdirectory(initialdir="/", title="저장경로를 지정하세요.")
    if dirname == "":
        return
    path_entry.delete(0, END)
    path_entry.insert(0, dirname)
    print("저장경로 :", dirname)

# 이미지 통합 완료 후 입력 값 초기화
def sucess():
    listbox.delete(0, END)
    p_var.set(0)
    progressbar.update()

# 이미지 통합
def merge_image():
    try:
        ####################### 옵션처리 ########################

        # 가로넓이
        img_width = width_option.get()
        if img_width == "원본유지":
            img_width = -1
        else:
            img_width = int(img_width)

        # 간격
        img_space = room_option.get()
        if img_space == "좁게":
            img_space = 30
        elif img_space == "보통":
            img_space = 60
        elif img_space == "넓게":
            img_space = 90
        else:
            img_space = 0
        
        #포멧
        img_format = format_option.get().lower()

        #######################################################

        images = [Image.open(x) for x in listbox.get(0, END)]

        if img_width > -1 :
            # 선택된 가로 길이에 비율에 맞는 세로 길이 구하기
            image_sizes = [(int(img_width), int(img_width * x.size[1] / x.size[0])) for x in images]
        else:
            # 원본사이즈
            image_sizes = [(int(x.size[0]) , int(x.size[1])) for x in images]

        widths, heights = list(zip(*image_sizes)) #zip을 이용하여 튜플 리스트 unzip하기

        # size -> size[0] : width, size[1] : height

        #widths = [x.size[0] for x in images]
        #heights = [x.size[1] for x in images]

        print("widths :", widths)
        print("heights :", heights)

        # 가로길이 가장 긴 값, 총 이미지의 높이 합 (설정한 간격까지 height에 추가해주기)
        max_width, total_height = max(widths), sum(heights) + (img_space * (len(images) - 1))
        #print("max widths :", max_width)
        #print("total height :", total_height)

        # 스케치북 준비
        result_img = Image.new("RGB", (max_width, total_height), (255, 255, 255)) #배경색 지정
        y_offset = 0 # 이미지를 추가할 y위치 지정

        # 이미지 붙히기
        for idx, img in enumerate(images):

            # 이미지 width가 원본유지가 아닐 경우
            if img_width > -1 :
                img = img.resize(image_sizes[idx])

            result_img.paste(img, (0,y_offset))
            y_offset += img.size[1] + img_space   #이미지 높이값 만큼 더해주기 + 이미지 간격 

            #프로그래스 바(현재 퍼센트 구하기)
            progress = (idx + 1) / len(images) * 100
            p_var.set(progress)
            progressbar.update()


        # 최종 이미지 경로에 이미지 저장
        image_path = "merge images." + img_format
        dest_path = os.path.join(path_entry.get(), image_path)
        result_img.save(dest_path)
        if os.path.isfile(dest_path) :
            msgbox.showinfo("알림", "작업이 완료되었습니다.")
        else:
            msgbox.showerror("에러", "알 수 없는 오류가 발생하였습니다.")
    
    except Exception as err:
        msgbox.showerror("에러", err)

    sucess()

# 시작
def start():    

    #이미지 파일 체크
    print(listbox.size())
    if listbox.size() == 0 :
        msgbox.showwarning("경고", "이미지 파일을 추가하세요.")
        return
    #저장경로 체크
    if not os.path.isdir(path_entry.get()):
        msgbox.showwarning("오류","저장경로를 찾을 수 없습니다.")
        return

    merge_image()
            



root = Tk()
root.title("이미지 합치기 (python project)")
root.geometry("+1200+600")  #크기지정 + 위치지정 ("가로x세로+x측+y측")
root.resizable(False, False)


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
progressbar = ttk.Progressbar(frame_status_lable, maximum=100, length=525, variable=p_var)
progressbar.pack(pady=5)


# 시작/닫기 버튼
frame_btn = Frame(root)
frame_btn.pack(fill="x", expand=False, pady=3)
addBtn = Button(frame_btn, text="닫기", command=root.quit, width=12, pady=5)
addBtn.pack(side="right", padx=3)
deleteBtn = Button(frame_btn, text="시작", command=start, width=12, pady=5)
deleteBtn.pack(side="right", padx=3)



root.mainloop()