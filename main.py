# main.py

from tkinter import Tk
from models import Sach, BanDoc, MuonTra
from data_handler import doc_file_csv, luu_file_csv
from gui import LibraryApp

FILE_SACH = "data/Sach.csv"
FILE_SV = "data/BanDoc.csv"
FILE_MUONTRA = "data/Muon_Tra.csv"

def doc_du_lieu():
    ds_sach = doc_file_csv(FILE_SACH, Sach)
    ds_bd = doc_file_csv(FILE_SV, BanDoc)
    ds_muon = doc_file_csv(FILE_MUONTRA, MuonTra)
    return ds_sach, ds_bd, ds_muon

def luu_du_lieu(ds_sach, ds_bd, ds_muon):
    luu_file_csv(ds_sach, FILE_SACH, Sach)
    luu_file_csv(ds_bd, FILE_SV, BanDoc)
    luu_file_csv(ds_muon, FILE_MUONTRA, MuonTra)
    print("Lưu dữ liệu thành công!")

def main():
    ds_sach, ds_bd, ds_muon = doc_du_lieu()

    app = LibraryApp(ds_sach, ds_bd, ds_muon)
    app.mainloop()

    # Ghi dữ liệu khi đóng cửa sổ
    def on_closing():
        if app.ds_sach or app.ds_bd or app.ds_muon:
            if Tk.messagebox.askyesno("Thoát", "Bạn có muốn lưu dữ liệu trước khi thoát?"):
                luu_du_lieu(app.ds_sach, app.ds_bd, app.ds_muon)
        app.destroy()

    app.protocol("WM_DELETE_WINDOW", on_closing)
    app.mainloop()

if __name__ == "__main__":
    main()
