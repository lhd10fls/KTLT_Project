import tkinter as tk
import csv
from tkinter import ttk, messagebox
from models import Sach, BanDoc
from business_logic import (
    xoa_sach, xoa_ban_doc,
    xu_ly_muon_sach, xu_ly_tra_sach, liet_ke_sach_qua_han
)

class LibraryApp(tk.Tk):
    def doc_bandoc_csv(filename):
        ds = []
        with open(filename, mode='r', newline='', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                ds.append(BanDoc(
                    row['MSSV'],
                    row['HoTen'],
                    row['GioiTinh'],
                    row['NgaySinh']
                ))
        return ds

    def luu_bandoc_csv(filename, ds_bd):
        with open(filename, mode='w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=['MSSV','HoTen','GioiTinh','NgaySinh'])
            writer.writeheader()
            for b in ds_bd:
                writer.writerow(b.__dict__)

    def doc_muontra_csv(filename):
        ds = []
        with open(filename, mode='r', newline='', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                ds.append(MuonTra)(
                    row['MaPhieuMuon'],
                    row['MSSV'],
                    row['MaSach'],
                    row['NgayMuon'],
                    row['NgayHenTra'],
                    row.get('NgayTraThucTe', ''),
                    row.get('TinhTrangMuon', '')
                )
        return ds

    def luu_muontra_csv(filename, ds_muon):
        with open(filename, mode='w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=['MaPhieuMuon','MSSV','MaSach','NgayMuon','NgayHenTra','NgayTraThucTe','TinhTrangMuon'])
            writer.writeheader()
            for m in ds_muon:
                writer.writerow(m.__dict__)

    def __init__(self, ds_sach, ds_bd, ds_muon):
        super().__init__()
        self.title("Quản Lý Thư Viện")
        self.geometry("900x600")
        main_frame = tk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)

        self.frm_menu = tk.Frame(main_frame, width=150, bg="#f0f0f0")
        self.frm_menu.pack(side=tk.LEFT, fill=tk.Y)
        self.container = tk.Frame(main_frame)
        self.container.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.ds_sach = ds_sach
        self.ds_bd = ds_bd
        self.ds_muon = ds_muon

        self.frames = {}
        self.create_menu()
        self.create_frames()
        self.show_frame("sach")

    def create_menu(self):
        frm_menu = tk.Frame(self.frm_menu, bg="#f0f0f0")
        frm_menu.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        ttk.Label(frm_menu, text="MENU", font=("Arial", 16, "bold")).pack(pady=10)
        ttk.Button(frm_menu, text="Quản lý sách", width=20, command=lambda: self.show_frame("sach")).pack(pady=5)
        ttk.Button(frm_menu, text="Quản lý bạn đọc", width=20, command=lambda: self.show_frame("bandoc")).pack(pady=5)
        ttk.Button(frm_menu, text="Mượn - Trả sách", width=20, command=lambda: self.show_frame("muontra")).pack(pady=5)
        ttk.Button(frm_menu, text="Danh sách đang mượn", command=lambda: self.show_frame("dangmuon")).pack(pady=5)
        ttk.Button(frm_menu, text="Danh sách quá hạn", width=20, command=self.liet_ke_qua_han_ui).pack(pady=5)
        ttk.Button(frm_menu, text="Thoát", width=20, command=self.quit).pack(pady=5)

    def create_frames(self):
        # Quản lý sách
        frm_sach = ttk.Frame(self.container)
        self.frames["sach"] = frm_sach
        self.create_sach_frame(frm_sach)

        # Danh sách đang mượn
        frm_dangmuon = ttk.Frame(self.container)
        self.frames["dangmuon"] = frm_dangmuon
        self.create_dangmuon_frame(frm_dangmuon)
        
        # Quản lý bạn đọc
        frm_bd = ttk.Frame(self.container)
        self.frames["bandoc"] = frm_bd
        self.create_bandoc_frame(frm_bd)

        # Mượn trả sách
        frm_muontra = ttk.Frame(self.container)
        self.frames["muontra"] = frm_muontra
        self.create_muontra_frame(frm_muontra)

        for f in self.frames.values():
            f.pack_forget()

    def show_frame(self, name):
        for f in self.frames.values():
            f.pack_forget()
        self.frames[name].pack(fill=tk.BOTH, expand=True)
        if name == "sach":
            self.load_ds_sach()
        elif name == "bandoc":
            self.load_ds_bd()

    # --- Quản lý sách ---
    def create_sach_frame(self, parent):
        # Thanh tìm kiếm
        search_frame = ttk.LabelFrame(parent, text="Tìm kiếm sách")
        search_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(search_frame, text="Mã sách:").grid(row=0, column=0, padx=5, pady=2)
        self.search_ma = ttk.Entry(search_frame)
        self.search_ma.grid(row=0, column=1, padx=5)

        ttk.Label(search_frame, text="Tác giả:").grid(row=0, column=2, padx=5)
        self.search_tacgia = ttk.Entry(search_frame)
        self.search_tacgia.grid(row=0, column=3, padx=5)

        ttk.Label(search_frame, text="Thể loại:").grid(row=0, column=4, padx=5)
        self.search_theloai = ttk.Entry(search_frame)
        self.search_theloai.grid(row=0, column=5, padx=5)

        ttk.Button(search_frame, text="Tìm kiếm", command=self.tim_kiem_sach_ui).grid(row=0, column=6, padx=10)
        ttk.Button(search_frame, text="Hiện tất cả", command=self.load_ds_sach).grid(row=0, column=7, padx=10)

        ttk.Label(parent, text="Quản lý sách", font=("Arial", 18, "bold")).pack(pady=10)

        columns = ("Mã Sách", "Tên Sách", "Tác Giả", "Thể Loại", "Số Lượng", "Tình Trạng")
        self.tree_sach = ttk.Treeview(parent, columns=columns, show="headings")
        for col in columns:
            self.tree_sach.heading(col, text=col)
            self.tree_sach.column(col, width=120)
        self.tree_sach.pack(fill=tk.BOTH, expand=True, pady=0.5, padx=10)

        frm_btn = ttk.Frame(parent)
        frm_btn.pack(pady=5)

        ttk.Button(frm_btn, text="Thêm sách", command=self.them_sach_ui).pack(side=tk.LEFT, padx=5)
        ttk.Button(frm_btn, text="Xóa sách", command=self.xoa_sach_ui).pack(side=tk.LEFT, padx=5)
        ttk.Button(frm_btn, text="Cập nhật sách", command=self.cap_nhat_sach_ui).pack(side=tk.LEFT, padx=5)
        ttk.Button(frm_btn, text="Tải lại", command=self.load_ds_sach).pack(side=tk.LEFT, padx=5)

    def load_ds_sach(self):
        self.tree_sach.delete(*self.tree_sach.get_children())
        for s in self.ds_sach:
            self.tree_sach.insert("", tk.END, values=(s.MaSach, s.TenSach, s.TacGia, s.TheLoai, s.SoLuong, s.TinhTrang))

    def tim_kiem_sach_ui(self):
        ma = self.search_ma.get().strip().lower()
        tacgia = self.search_tacgia.get().strip().lower()
        theloai = self.search_theloai.get().strip().lower()

        ket_qua = []
        for s in self.ds_sach:
            if (ma in s.MaSach.lower() or not ma) and \
            (tacgia in s.TacGia.lower() or not tacgia) and \
            (theloai in s.TheLoai.lower() or not theloai):
                ket_qua.append(s)

        self.tree_sach.delete(*self.tree_sach.get_children())
        for s in ket_qua:
            self.tree_sach.insert("", tk.END, values=(s.MaSach, s.TenSach, s.TacGia, s.TheLoai, s.SoLuong, s.TinhTrang))

    def them_sach_ui(self):
        dialog = ThemSachDialog(self, self.ds_sach)
        self.wait_window(dialog)
        self.load_ds_sach()

    def xoa_sach_ui(self):
        selected = self.tree_sach.selection()
        if not selected:
            messagebox.showwarning("Chú ý", "Vui lòng chọn sách để xóa")
            return
        ma_sach = self.tree_sach.item(selected[0])['values'][0]
        if messagebox.askyesno("Xác nhận", f"Xóa sách mã {ma_sach}?"):
            if xoa_sach(ma_sach, self.ds_sach):
                messagebox.showinfo("Thành công", "Xóa thành công")
                self.load_ds_sach()
            else:
                messagebox.showerror("Lỗi", "Xóa thất bại")

    def cap_nhat_sach_ui(self):
        selected = self.tree_sach.selection()
        if not selected:
            messagebox.showwarning("Chú ý", "Vui lòng chọn sách để cập nhật")
            return
        ma_sach = self.tree_sach.item(selected[0])['values'][0]
        dialog = CapNhatSachDialog(self, self.ds_sach, ma_sach)
        self.wait_window(dialog)
        self.load_ds_sach()

    def create_dangmuon_frame(self, parent):
        ttk.Label(parent, text="Danh sách đang mượn", font=("Arial", 14, "bold")).pack(pady=10)

        columns = ("Mã Phiếu Mượn", "MSSV", "Mã Sách", "Ngày Mượn", "Ngày Hẹn Trả", "Tình Trạng Mượn")
        self.tree_dangmuon = ttk.Treeview(parent, columns=columns, show="headings")
        for col in columns:
            self.tree_dangmuon.heading(col, text=col)
            self.tree_dangmuon.column(col, width=120)
        self.tree_dangmuon.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        ttk.Button(parent, text="Làm mới", command=self.load_ds_dang_muon).pack(pady=5)
        self.load_ds_dang_muon()

    def load_ds_dang_muon(self):
        self.tree_dangmuon.delete(*self.tree_dangmuon.get_children())
        for m in self.ds_muon:
            ngay_tra = (m.NgayTraThucTe or "").strip().lower()
            if ngay_tra in ["", "chưa trả", "none", "null"]:
                self.tree_dangmuon.insert("", tk.END, values=(
                    m.MaPhieuMuon, m.MSSV, m.MaSach, m.NgayMuon, m.NgayHenTra, m.TinhTrangMuon
                ))

    # --- Quản lý bạn đọc ---
    def create_bandoc_frame(self, parent):
        ttk.Label(parent, text="Quản lý bạn đọc", font=("Arial", 18, "bold")).pack(pady=10)

        columns = ("MSSV", "Họ Tên", "Giới Tính", "Ngày Sinh")
        self.tree_bd = ttk.Treeview(parent, columns=columns, show="headings")
        for col in columns:
            self.tree_bd.heading(col, text=col)
            self.tree_bd.column(col, width=150)
        self.tree_bd.pack(fill=tk.BOTH, expand=True, pady=10)

        frm_btn = ttk.Frame(parent)
        frm_btn.pack(pady=5)

        ttk.Button(frm_btn, text="Thêm bạn đọc", command=self.them_bandoc_ui).pack(side=tk.LEFT, padx=5)
        ttk.Button(frm_btn, text="Xóa bạn đọc", command=self.xoa_bandoc_ui).pack(side=tk.LEFT, padx=5)
        ttk.Button(frm_btn, text="Tải lại", command=self.load_ds_bd).pack(side=tk.LEFT, padx=5)

    def load_ds_bd(self):
        self.tree_bd.delete(*self.tree_bd.get_children())
        for b in self.ds_bd:
            self.tree_bd.insert("", tk.END, values=(b.MSSV, b.HoTen, b.GioiTinh, b.NgaySinh))

    def them_bandoc_ui(self):
        dialog = ThemBanDocDialog(self, self.ds_bd)
        self.wait_window(dialog)
        self.load_ds_bd()

    def xoa_bandoc_ui(self):
        selected = self.tree_bd.selection()
        if not selected:
            messagebox.showwarning("Chú ý", "Vui lòng chọn bạn đọc để xóa")
            return
        mssv = self.tree_bd.item(selected[0])['values'][0]
        if messagebox.askyesno("Xác nhận", f"Xóa bạn đọc MSSV {mssv}?"):
            if xoa_ban_doc(mssv, self.ds_bd):
                messagebox.showinfo("Thành công", "Xóa thành công")
                self.load_ds_bd()
            else:
                messagebox.showerror("Lỗi", "Xóa thất bại")

    # --- Mượn trả sách ---
    def create_muontra_frame(self, parent):
        ttk.Label(parent, text="Mượn - Trả sách", font=("Arial", 18, "bold")).pack(pady=10)

        frm_btn = ttk.Frame(parent)
        frm_btn.pack(pady=20)

        ttk.Button(frm_btn, text="Mượn sách", width=20, command=self.muon_sach_ui).pack(pady=5)
        ttk.Button(frm_btn, text="Trả sách", width=20, command=self.tra_sach_ui).pack(pady=5)
        ttk.Button(frm_btn, text="Liệt kê sách quá hạn", width=20, command=self.liet_ke_qua_han_ui).pack(pady=5)

    def muon_sach_ui(self):
        dialog = MuonSachDialog(self, self.ds_sach, self.ds_bd, self.ds_muon)
        self.wait_window(dialog)

    def tra_sach_ui(self):
        dialog = TraSachDialog(self, self.ds_sach, self.ds_muon)
        self.wait_window(dialog)

    def liet_ke_qua_han_ui(self):
        dialog = LietKeQuaHanDialog(self, self.ds_muon)
        self.wait_window(dialog)

# -------- Dialogs ----------
class ThemSachDialog(tk.Toplevel):
    def __init__(self, parent, ds_sach):
        super().__init__(parent)
        self.title("Thêm sách mới")
        self.ds_sach = ds_sach
        self.create_widgets()

    def create_widgets(self):
        labels = ["Mã sách", "Tên sách", "Tác giả", "Thể loại", "Số lượng", "Tình trạng (Con/Het)"]
        self.entries = {}
        for i, text in enumerate(labels):
            ttk.Label(self, text=text).grid(row=i, column=0, sticky=tk.W, pady=2, padx=5)
            entry = ttk.Entry(self)
            entry.grid(row=i, column=1, pady=2, padx=5)
            self.entries[text] = entry
        ttk.Button(self, text="Thêm", command=self.them_sach).grid(row=len(labels), column=0, columnspan=2, pady=10)

    def them_sach(self):
        try:
            ma_sach = self.entries["Mã sách"].get().strip()
            if any(s.MaSach == ma_sach for s in self.ds_sach):
                messagebox.showerror("Lỗi", "Mã sách đã tồn tại!")
                return
            ten_sach = self.entries["Tên sách"].get().strip()
            tac_gia = self.entries["Tác giả"].get().strip()
            the_loai = self.entries["Thể loại"].get().strip()
            so_luong = int(self.entries["Số lượng"].get().strip())
            tinh_trang = self.entries["Tình trạng (Con/Het)"].get().strip()
            self.ds_sach.append(Sach(ma_sach, ten_sach, tac_gia, the_loai, so_luong, tinh_trang))
            messagebox.showinfo("Thành công", "Thêm sách thành công!")
            self.destroy()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Nhập liệu không hợp lệ: {e}")


class CapNhatSachDialog(tk.Toplevel):
    def __init__(self, parent, ds_sach, ma_sach):
        super().__init__(parent)
        self.title(f"Cập nhật sách {ma_sach}")
        self.ds_sach = ds_sach
        self.ma_sach = ma_sach
        self.sach = next((s for s in ds_sach if s.MaSach == ma_sach), None)
        if not self.sach:
            messagebox.showerror("Lỗi", "Không tìm thấy sách cần cập nhật!")
            self.destroy()
            return
        self.create_widgets()

    def create_widgets(self):
        labels = ["Tên sách", "Tác giả", "Thể loại", "Số lượng", "Tình trạng (Con/Het)"]
        self.entries = {}
        vals = [self.sach.TenSach, self.sach.TacGia, self.sach.TheLoai, str(self.sach.SoLuong), self.sach.TinhTrang]
        for i, (text, val) in enumerate(zip(labels, vals)):
            ttk.Label(self, text=text).grid(row=i, column=0, sticky=tk.W, pady=2, padx=5)
            entry = ttk.Entry(self)
            entry.insert(0, val)
            entry.grid(row=i, column=1, pady=2, padx=5)
            self.entries[text] = entry
        ttk.Button(self, text="Cập nhật", command=self.cap_nhat_sach).grid(row=len(labels), column=0, columnspan=2, pady=10)

    def cap_nhat_sach(self):
        try:
            self.sach.TenSach = self.entries["Tên sách"].get().strip()
            self.sach.TacGia = self.entries["Tác giả"].get().strip()
            self.sach.TheLoai = self.entries["Thể loại"].get().strip()
            self.sach.SoLuong = int(self.entries["Số lượng"].get().strip())
            self.sach.TinhTrang = self.entries["Tình trạng (Con/Het)"].get().strip()
            messagebox.showinfo("Thành công", "Cập nhật sách thành công!")
            self.destroy()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Nhập liệu không hợp lệ: {e}")


class ThemBanDocDialog(tk.Toplevel):
    def __init__(self, parent, ds_bd):
        super().__init__(parent)
        self.title("Thêm bạn đọc mới")
        self.ds_bd = ds_bd
        self.create_widgets()

    def create_widgets(self):
        labels = ["MSSV", "Họ tên", "Giới tính", "Ngày sinh (dd/mm/yyyy)"]
        self.entries = {}
        for i, text in enumerate(labels):
            ttk.Label(self, text=text).grid(row=i, column=0, sticky=tk.W, pady=2, padx=5)
            entry = ttk.Entry(self)
            entry.grid(row=i, column=1, pady=2, padx=5)
            self.entries[text] = entry
        ttk.Button(self, text="Thêm", command=self.them_bandoc).grid(row=len(labels), column=0, columnspan=2, pady=10)

    def them_bandoc(self):
        try:
            mssv = self.entries["MSSV"].get().strip()
            if any(b.MSSV == mssv for b in self.ds_bd):
                messagebox.showerror("Lỗi", "Mã bạn đọc đã tồn tại!")
                return
            ho_ten = self.entries["Họ tên"].get().strip()
            gioi_tinh = self.entries["Giới tính"].get().strip()
            ngay_sinh = self.entries["Ngày sinh (dd/mm/yyyy)"].get().strip()
            self.ds_bd.append(BanDoc(mssv, ho_ten, gioi_tinh, ngay_sinh))
            messagebox.showinfo("Thành công", "Thêm bạn đọc thành công!")
            self.destroy()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Nhập liệu không hợp lệ: {e}")


class MuonSachDialog(tk.Toplevel):
    def __init__(self, parent, ds_sach, ds_bd, ds_muon):
        super().__init__(parent)
        self.title("Mượn sách")
        self.ds_sach = ds_sach
        self.ds_bd = ds_bd
        self.ds_muon = ds_muon
        self.create_widgets()

    def create_widgets(self):
        labels = ["MSSV bạn đọc", "Mã sách", "Mã phiếu mượn", "Ngày mượn (yyyy-mm-dd)", "Ngày hẹn trả (yyyy-mm-dd)"]
        self.entries = {}
        for i, text in enumerate(labels):
            ttk.Label(self, text=text).grid(row=i, column=0, sticky=tk.W, pady=2, padx=5)
            entry = ttk.Entry(self)
            entry.grid(row=i, column=1, pady=2, padx=5)
            self.entries[text] = entry
        ttk.Button(self, text="Mượn sách", command=self.muon_sach).grid(row=len(labels), column=0, columnspan=2, pady=10)

    def muon_sach(self):
        try:
            mssv = self.entries["MSSV bạn đọc"].get().strip()
            ma_sach = self.entries["Mã sách"].get().strip()
            ma_phieu = self.entries["Mã phiếu mượn"].get().strip()
            ngay_muon = self.entries["Ngày mượn (yyyy-mm-dd)"].get().strip()
            ngay_hen_tra = self.entries["Ngày hẹn trả (yyyy-mm-dd)"].get().strip()

            if not any(b.MSSV == mssv for b in self.ds_bd):
                messagebox.showerror("Lỗi", f"Không tìm thấy bạn đọc MSSV {mssv}")
                return
            ma_sach = ma_sach.strip().lower()
            sach = next((s for s in self.ds_sach if s.MaSach.strip().lower() == ma_sach), None)

            if not sach:
                messagebox.showerror("Lỗi", f"Không tìm thấy sách mã {ma_sach}")
                return
            if sach.SoLuong <= 0:
                messagebox.showerror("Lỗi", "Sách đã hết")
                return

            from business_logic import muon_sach as muon_sach_bl
            if muon_sach_bl(mssv, ma_sach, self.ds_sach, self.ds_muon, ma_phieu, ngay_muon, ngay_hen_tra):
                messagebox.showinfo("Thành công", "Mượn sách thành công!")
                self.destroy()
            else:
                messagebox.showerror("Lỗi", "Mượn sách thất bại")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Nhập liệu không hợp lệ: {e}")


class TraSachDialog(tk.Toplevel):
    def __init__(self, parent, ds_sach, ds_muon):
        super().__init__(parent)
        self.title("Trả sách")
        self.ds_sach = ds_sach
        self.ds_muon = ds_muon
        self.create_widgets()

    def create_widgets(self):
        labels = ["MSSV bạn đọc", "Mã sách", "Ngày trả thực tế (yyyy-mm-dd)"]
        self.entries = {}
        for i, text in enumerate(labels):
            ttk.Label(self, text=text).grid(row=i, column=0, sticky=tk.W, pady=2, padx=5)
            entry = ttk.Entry(self)
            entry.grid(row=i, column=1, pady=2, padx=5)
            self.entries[text] = entry
        ttk.Button(self, text="Trả sách", command=self.tra_sach).grid(row=len(labels), column=0, columnspan=2, pady=10)

    def tra_sach(self):
        try:
            mssv = self.entries["MSSV bạn đọc"].get().strip()
            ma_sach = self.entries["Mã sách"].get().strip()
            ngay_tra = self.entries["Ngày trả thực tế (yyyy-mm-dd)"].get().strip()

            from business_logic import tra_sach as tra_sach_bl
            if tra_sach_bl(mssv, ma_sach, self.ds_sach, self.ds_muon, ngay_tra):
                messagebox.showinfo("Thành công", "Trả sách thành công!")
                self.destroy()
            else:
                messagebox.showerror("Lỗi", "Trả sách thất bại hoặc chưa từng mượn sách này.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Nhập liệu không hợp lệ: {e}")


class LietKeQuaHanDialog(tk.Toplevel):
    def __init__(self, parent, ds_muon):
        super().__init__(parent)
        self.title("Danh sách sách quá hạn")
        self.ds_muon = ds_muon
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self, text="Nhập ngày hiện tại (yyyy-mm-dd):").pack(padx=10, pady=5)
        self.entry_ngay = ttk.Entry(self)
        self.entry_ngay.pack(padx=10, pady=5)
        ttk.Button(self, text="Tìm", command=self.tim_qua_han).pack(padx=10, pady=5)

        columns = ("MaPhieuMuon", "MSSV", "MaSach", "NgayMuon", "NgayHenTra", "NgayTraThucTe", "TinhTrangMuon")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def tim_qua_han(self):
        ngay_hien_tai = self.entry_ngay.get().strip()
        try:
            from business_logic import liet_ke_sach_qua_han as liet_ke_bl
            ds_qua_han = liet_ke_bl(self.ds_muon, ngay_hien_tai)
            self.tree.delete(*self.tree.get_children())
            if ds_qua_han:
                for phieu in ds_qua_han:
                    self.tree.insert("", tk.END, values=(
                        phieu.MaPhieuMuon, phieu.MSSV, phieu.MaSach, phieu.NgayMuon,
                        phieu.NgayHenTra, phieu.NgayTraThucTe or "Chưa trả", phieu.TinhTrangMuon))
            else:
                messagebox.showinfo("Kết quả", "Không có sách nào quá hạn.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Ngày nhập không hợp lệ: {e}")

    