import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, simpledialog
import os, json, shutil

#kHỞI TẠO FILE SETTING
setting = {
	'launcher_path':''
}
file = 'settings.json'
path = os.getcwd() + "\\"
extention_path = '/game/'
if 'version' not in os.listdir():
	os.makedirs(path + '/version')
if 'mods' not in os.listdir():
	os.makedirs(path + '/mods')
mod_folder = [item for item in os.listdir(path + '/mods') if '.' not in item]
mods = [item for item in os.listdir(path + '/mods') if '.jar' in item]
for folder in mod_folder:
	for item in os.listdir(path + '\\mods\\' + folder):
		if '.jar' in item:
			mods.append(folder + '/' + item)
def save_setting():
	global path, file, setting
	with open(path + file, 'w') as f:
		setting = json.dumps(setting)
		f.write(setting)
	f.close()
if file not in os.listdir():
	save_setting()
else:
	with open(path + file, 'r') as f:
		setting = dict(json.load(f))
	f.close()

#CỬA SỔ
window = tk.Tk()
window.geometry('500x320')
window.minsize(500,320)
# print(filedialog.askopenfilename())
# window.resizable(False, False)
window.rowconfigure(0, weight=1)
window.columnconfigure([0,1],weight=1)
window.title('Mod Installer for LegacyLauncher')
# print(simpledialog.askstring(' ', 'Version Name'))
#KHUNG CHÍNH
def update_mod_select():
	global mods
	mod_select.delete(0,tk.END)
	for i, item in enumerate(mods):
		mod_select.insert(i, item)
def browse_file():
	global setting
	path = filedialog.askopenfilename(title='Open Launcher Exe', filetypes=(('Exe', '*.exe'), ('All file', '*.*')))
	if path:
		setting['launcher_path'] = path
		save_setting()
		launcher.config(state='normal')
		launcher.delete(0,tk.END)
		launcher.insert(0,path)
		launcher.config(state='disabled')
def install_mod():
	global setting, extention_path, mods
	try:
		version = version_select.curselection()[0]
		index = mod_select.curselection()[0]
		if mods[index] not in os.listdir(path + '/version/' + version_select.get(version)):
			shutil.copy(path + 'mods/' + mods[index], path + '/version/' + version_select.get(version))
			status.config(text='Cài đặt thành công!')
		else:
			status.config(text='Xin lỗi bạn đã cài đặt mod này rồi!')
		
	except:
		status.config(text='Có lỗi xảy ra, đảm bảo thực hiện đúng.')
	status.after(2500, lambda: status.config(text='Trạng thái: Không xác định.'))
def remove_mod():
	global setting, extention_path, mods
	try:
		version = version_select.curselection()[0]
		index = mod_select.curselection()[0]
		item_path = ''
		if '/' not in mods[index]:
			item_path = path + '/version/' + version_select.get(version) + '/' + mods[index]
		else:
			item_path = path + '/version/' + version_select.get(version) + '/' + mods[index].split('/')[-1]

		if item_path.split('/')[-1] in os.listdir(path + '/version/' + version_select.get(version)):
			os.remove(item_path)
			status.config(text='Xoá bỏ thành công!')
		else:
			status.config(text='Xin lỗi mod không tồn tại trong thư mục')
	except:
		status.config(text='Có lỗi xảy ra, đảm bảo thực hiện đúng.')
	status.after(2500, lambda: status.config(text='Trạng thái: Không xác định.'))

def add_mod():
	global path
	custom = filedialog.askopenfilename(title='Choose your custom mod', filetypes=(('Java', '*.jar'),('Java 8','*.jar')))
	if custom:
		shutil.copy(custom, path + '/mods/' + custom.split('/')[-1])


main = tk.Frame(window, relief=tk.RIDGE,borderwidth=4)
logo = tk.Label(main,text='Mod Installer', font=('Calibri Light', 24))
credit = tk.Label(main, text='Made by thiendev. Ver1.0', font=('Fixedsys', 8))

launcher = tk.Entry(main, relief='sunken', width=35)
if file not in os.listdir():
	launcher.insert(0,'Vui lòng chọn thư mục chứa file exe của Launcher (chỉ cần chọn 1 lần, đường dẫn sẽ được lưu trữ)')
else:
	launcher.insert(0,str(setting['launcher_path']))
launcher.config(state='disabled')
browse = ttk.Button(main, text='Duyệt',command=browse_file)
add_mod = ttk.Button(main, text='Thêm mod...', command=add_mod)
install = ttk.Button(main, text='Cài đặt',command=install_mod)
remove = ttk.Button(main, text='Xoá bỏ', command=remove_mod)
status = tk.Message(main, text='Trạng thái: Không xác định.',width=200)
infomation = tk.Message(main, text='Đường dẫn: ',width=200)


logo.grid(row=0,column=0)
credit.grid(row=1,column=0)
launcher.grid(row=2,column=0,padx=10,pady=40)
browse.grid(row=2,column=1,padx=10)
add_mod.grid(row=3,column=0,sticky='w',padx=10)
install.grid(row=3,column=1,padx=10)
status.grid(row=4,column=0,sticky='w',padx=10,pady=5)
remove.grid(row=4, column=1,padx=10)
infomation.grid(row=5,column=0,sticky='w',padx=10)
#KHUNG MOD, DANH SÁCH MOD
def path_version_info(event):
	global path
	text = 'Đường dẫn: '
	try:
		version = version_select.get(version_select.curselection())
		text += '/version/' + version + '\n'
		for item in os.listdir(path + '/version/' + version):
			text += item + '\n'
		if os.listdir(path + '/version/' + version) == []:
			text += '(Trống)'
	except:
		pass
	infomation.config(text=text)
def path_mod_info(event):
	global path
	text = 'Đường dẫn: /mods\n'
	try:
		text += mod_select.get(mod_select.curselection())
	except:
		pass
	infomation.config(text=text)
def update_version_select():
	global path
	version_select.delete(0,tk.END)
	for i, item in enumerate(os.listdir(path + '/version')):
		version_select.insert(i, item)
def create_version_folder():
	global path
	name = simpledialog.askstring(' ', 'Enter Version Name')
	try:
		os.makedirs(path + '/version/' + name)
	except:
		pass
	update_version_select()
def delete_version_folder():
	global path
	try:
		version = version_select.curselection()[0]
		shutil.rmtree(path + '/version/' + os.listdir(path + '/version')[version])
	except:
		pass
	update_version_select()

def apply_mod():
	global setting, path, extention_path
	launcher_path = setting['launcher_path'].split('/')
	launcher_path.pop(-1)
	launcher_path = '/'.join(launcher_path) + extention_path
	
	try:
		version = version_select.get(version_select.curselection())

		if os.listdir(path + '/version/' + version) == []:
			status.config(text='Không thể áp dụng do chưa có mod trong thư mục')
		else:
			if 'mods' in os.listdir(launcher_path):
				shutil.rmtree(launcher_path + 'mods')
			shutil.copytree(path + '/version/' + version, launcher_path + version)
			os.rename(launcher_path + version, launcher_path + 'mods')

			
	except:
		status.config(text='Có lỗi xảy ra, đảm bảo thực hiện đúng.')
	status.after(2500, lambda: status.config(text='Trạng thái: Không xác định.'))

mod_frame = tk.Frame(window)
mod_frame.rowconfigure(1, weight=1)
mod_frame.columnconfigure(0,weight=1)

text = tk.Label(mod_frame,text='Mod có sẵn', font=('Calibri Light', 17))
mod_select = tk.Listbox(mod_frame,width = 26, height = 20, activestyle='none', selectmode=tk.SINGLE, exportselection=0)
text2 = tk.Label(mod_frame, text='Phiên bản', font=('Calibri Light', 14))
version_select = tk.Listbox(mod_frame,width=26, height=4, activestyle='none', selectmode=tk.SINGLE, exportselection=0)
delete = ttk.Button(mod_frame, text='Xoá', command=delete_version_folder)
add_version = ttk.Button(mod_frame, text='Thêm', command=create_version_folder)
applied = ttk.Button(mod_frame, text='Áp dụng', command=apply_mod)

mod_select.bind('<<ListboxSelect>>', path_mod_info)
version_select.bind('<<ListboxSelect>>',path_version_info)
for i, item in enumerate(mods):
	mod_select.insert(i, item)
for i, item in enumerate(os.listdir(path + '/version')):
	version_select.insert(i, item)

text.grid(sticky='news')
mod_select.grid(sticky='news')
text2.grid(sticky='news')
version_select.grid(sticky='news')
add_version.grid(sticky='news',pady=2)
delete.grid(sticky='news',pady=2)
applied.grid(sticky='news',pady=2)
#ĐẶT KHUNG
mod_frame.grid(row=0,column=0, sticky='news')
main.grid(row=0,column=1, sticky='news')

#VÒNG LẶP
window.mainloop()