import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import tkinter.messagebox
import csv

class QuanLyDonHangApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quản Lý Đơn Hàng")
        self.cua_so_them_san_pham = None
        self.du_lieu_san_pham = []
        self.tao_giao_dien()
        
    def tao_giao_dien(self):
        columns = ["Tên Sản Phẩm", "Giá Nhập", "Giá Bán", "Số Lượng Đã Bán", "Số Lượng Tồn Kho"]
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings")
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
            style = ttk.Style()
            style.configure("Treeview", rowheight=40)
        self.tree.heading(col, text=col, anchor=tk.CENTER)
        y_scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.tree.yview)
        y_scrollbar.grid(row=0, column=1, sticky="ns")

        x_scrollbar = ttk.Scrollbar(self.root, orient="horizontal", command=self.tree.xview)
        x_scrollbar.grid(row=1, column=0, sticky="ew")

        self.tree.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)

        self.tree.grid(row=0, column=0, pady=10, sticky="nsew")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        btn_them_san_pham = tk.Button(self.root, text="Thêm Sản Phẩm", command=self.mo_cua_so_them_san_pham)
        btn_them_san_pham.grid(row=6, column=0, padx=5, pady=10)
        btn_sua_san_pham = tk.Button(self.root, text="Sửa Sản Phẩm", command=self.mo_cua_so_sua_san_pham)
        btn_sua_san_pham.grid(row=6, column=1, padx=5, pady=10)
        btn_xoa_san_pham = tk.Button(self.root, text="Xóa Sản Phẩm", command=self.xoa_san_pham)
        btn_xoa_san_pham.grid(row=6, column=2, padx=5, pady=10)

        btn_import = tk.Button(self.root, text="Import", command=self.import_csv)
        btn_import.grid(row=6, column=3, padx=5, pady=10)

        self.doc_du_lieu_tu_csv()

    def mo_cua_so_them_san_pham(self):
        self.cua_so_them_san_pham = tk.Toplevel(self.root)
        self.cua_so_them_san_pham.title("Thêm Sản Phẩm")

        lbl_ten_san_pham = tk.Label(self.cua_so_them_san_pham, text="Tên Sản Phẩm:")
        lbl_ten_san_pham.grid(row=0, column=0, padx=10, pady=5)

        ent_ten_san_pham = tk.Entry(self.cua_so_them_san_pham)
        ent_ten_san_pham.grid(row=0, column=1, padx=10, pady=5)

        lbl_gia_ban = tk.Label(self.cua_so_them_san_pham, text="Giá Bán:")
        lbl_gia_ban.grid(row=2, column=0, padx=10, pady=5)

        ent_gia_ban = tk.Entry(self.cua_so_them_san_pham)
        ent_gia_ban.grid(row=2, column=1, padx=10, pady=5)

        lbl_so_luong_ban = tk.Label(self.cua_so_them_san_pham, text="Số Lượng Đã Bán:")
        lbl_so_luong_ban.grid(row=4, column=0, padx=10, pady=5)

        ent_so_luong_ban = tk.Entry(self.cua_so_them_san_pham)
        ent_so_luong_ban.grid(row=4, column=1, padx=10, pady=5)

        lbl_so_luong_ton_kho = tk.Label(self.cua_so_them_san_pham, text="Số Lượng Tồn Kho:")
        lbl_so_luong_ton_kho.grid(row=3, column=0, padx=10, pady=5)

        ent_so_luong_ton_kho = tk.Entry(self.cua_so_them_san_pham)
        ent_so_luong_ton_kho.grid(row=3, column=1, padx=10, pady=5)

        lbl_gia_nhap = tk.Label(self.cua_so_them_san_pham, text="Giá Nhập:")
        lbl_gia_nhap.grid(row=1, column=0, padx=10, pady=5)

        ent_gia_nhap = tk.Entry(self.cua_so_them_san_pham)
        ent_gia_nhap.grid(row=1, column=1, padx=10, pady=5)


        btn_luu = tk.Button(self.cua_so_them_san_pham, text="Lưu", command=lambda: self.luu_san_pham(
            ent_ten_san_pham.get(),
            ent_gia_nhap.get(),
            ent_gia_ban.get(),
            ent_so_luong_ban.get(),
            ent_so_luong_ton_kho.get()
        ))
        btn_luu.grid(row=5, column=0, columnspan=2, pady=10)
        
    def mo_cua_so_sua_san_pham(self):
        chon_sp = self.tree.selection()
        if not chon_sp:
            tk.messagebox.showinfo("Thông báo", "Vui lòng chọn sản phẩm cần sửa.")
            return

        selected_index = int(self.tree.index(chon_sp[0]))
        selected_sp = self.du_lieu_san_pham[selected_index]

        self.cua_so_sua_san_pham = tk.Toplevel(self.root)
        self.cua_so_sua_san_pham.title("Sửa Sản Phẩm")

        lbl_ten_san_pham = tk.Label(self.cua_so_sua_san_pham, text="Tên Sản Phẩm:")
        lbl_ten_san_pham.grid(row=0, column=0, padx=10, pady=5)

        ent_ten_san_pham = tk.Entry(self.cua_so_sua_san_pham)
        ent_ten_san_pham.grid(row=0, column=1, padx=10, pady=5)
        ent_ten_san_pham.insert(0, selected_sp[0])

        lbl_gia_ban = tk.Label(self.cua_so_sua_san_pham, text="Giá Bán:")
        lbl_gia_ban.grid(row=2, column=0, padx=10, pady=5)

        ent_gia_ban = tk.Entry(self.cua_so_sua_san_pham)
        ent_gia_ban.grid(row=2, column=1, padx=10, pady=5)
        ent_gia_ban.insert(0, selected_sp[1])

        lbl_so_luong_ban = tk.Label(self.cua_so_sua_san_pham, text="Số Lượng Đã Bán:")
        lbl_so_luong_ban.grid(row=4, column=0, padx=10, pady=5)

        ent_so_luong_ban = tk.Entry(self.cua_so_sua_san_pham)
        ent_so_luong_ban.grid(row=4, column=1, padx=10, pady=5)
        ent_so_luong_ban.insert(0, selected_sp[2])

        lbl_so_luong_ton_kho = tk.Label(self.cua_so_sua_san_pham, text="Số Lượng Tồn Kho:")
        lbl_so_luong_ton_kho.grid(row=3, column=0, padx=10, pady=5)

        ent_so_luong_ton_kho = tk.Entry(self.cua_so_sua_san_pham)
        ent_so_luong_ton_kho.grid(row=3, column=1, padx=10, pady=5)
        ent_so_luong_ton_kho.insert(0, selected_sp[3])

        lbl_gia_nhap = tk.Label(self.cua_so_sua_san_pham, text="Giá Nhập:")
        lbl_gia_nhap.grid(row=1, column=0, padx=10, pady=5)

        ent_gia_nhap = tk.Entry(self.cua_so_sua_san_pham)
        ent_gia_nhap.grid(row=1, column=1, padx=10, pady=5)
        ent_gia_nhap.insert(0, selected_sp[4])

        btn_luu_sua = tk.Button(self.cua_so_sua_san_pham, text="Lưu Sửa", command=lambda: self.luu_sua_san_pham(
            selected_index,
            ent_ten_san_pham.get(),
            ent_gia_ban.get(),
            ent_so_luong_ban.get(),
            ent_so_luong_ton_kho.get(),
            ent_gia_nhap.get()
        ))
        btn_luu_sua.grid(row=5, column=0, columnspan=2, pady=10)
    def luu_san_pham(self, ten_san_pham, gia_nhap, gia_ban, so_luong_ban, so_luong_ton_kho):
        if ten_san_pham and gia_ban and so_luong_ban and so_luong_ton_kho and gia_nhap:
            san_pham = [ten_san_pham, gia_nhap, gia_ban, so_luong_ban, so_luong_ton_kho]
            self.du_lieu_san_pham.append(san_pham)
            self.tree.insert("", "end", values=san_pham)
            
            self.ghi_du_lieu_vao_csv()
            self.cua_so_them_san_pham.destroy()
        else:
            tk.messagebox.showerror("Lỗi", "Vui lòng điền đầy đủ thông tin sản phẩm.")
    def luu_sua_san_pham(self, selected_index, ten_san_pham, gia_nhap, gia_ban, so_luong_ban, so_luong_ton_kho):
        if ten_san_pham and gia_ban and so_luong_ban and so_luong_ton_kho and gia_nhap:
            san_pham = [ten_san_pham, gia_nhap, gia_ban, so_luong_ban, so_luong_ton_kho]
            self.du_lieu_san_pham[selected_index] = san_pham
            self.tree.item(self.tree.selection(), values=san_pham)
            self.ghi_du_lieu_vao_csv()
            self.cua_so_sua_san_pham.destroy()
        else:
            tk.messagebox.showerror("Lỗi", "Vui lòng điền đầy đủ thông tin sản phẩm khi sửa.")
    def doc_du_lieu_tu_csv(self):
        try:
            with open('du_lieu_san_pham.csv', newline='', encoding='utf-8') as file_csv:
                doc_gia = csv.reader(file_csv)
                next(doc_gia)
                for row in doc_gia:
                    self.du_lieu_san_pham.append(row)
                    self.tree.insert("", "end", values=row)
        except FileNotFoundError:
            tk.messagebox.showwarning("Cảnh Báo", "File CSV không tồn tại. Sẽ tạo mới khi lưu dữ liệu.")
    def ghi_du_lieu_vao_csv(self):
        with open('du_lieu_san_pham.csv', 'w', newline='', encoding='utf-8') as file_csv:
            ghi_gia = csv.writer(file_csv)
            ghi_gia.writerow(["Tên Sản Phẩm", "Giá Bán", "Số Lượng Đã Bán", "Số Lượng Tồn Kho", "Giá Nhập"])
            for san_pham in self.du_lieu_san_pham:
                ghi_gia.writerow(san_pham)
    def import_csv(self):
        try:
            file_path = filedialog.askopenfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
            if file_path:
                with open(file_path, newline='', encoding='utf-8') as file_csv:
                    doc_file_moi = list(csv.reader(file_csv))[1:]  
            self.du_lieu_san_pham.extend(doc_file_moi)

            '''
            for item in self.tree.get_children():
                self.tree.delete(item)
            '''
            
            for row in self.du_lieu_san_pham:
                self.tree.insert("", "end", values=row)
                self.ghi_du_lieu_vao_csv()
            tk.messagebox.showinfo("Thông báo", "Import dữ liệu từ CSV thành công.")
        except Exception as e:
            tk.messagebox.showerror("Lỗi", f"Không thể import từ CSV: {e}")
    def xoa_san_pham(self):
        chon_item = self.tree.selection()
        if not chon_item:
            tk.messagebox.showinfo("Thông báo", "Vui lòng chọn sản phẩm cần xóa.")
            return

        confirmation = tk.messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa sản phẩm này?")
        if confirmation:
            for item in chon_item:
                index = int(self.tree.index(item))
                del self.du_lieu_san_pham[index]
                self.tree.delete(item)
            self.ghi_du_lieu_vao_csv()

    
    
app = QuanLyDonHangApp(root=tk.Tk())
app.root.mainloop()