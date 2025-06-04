from typing import List
from data_handler import (
    tao_sach, kiem_tra_trung_ma_sach, tim_sach_theo_ma,
    cap_nhat_thong_tin_sach, xoa_sach, tim_kiem_sach,
    tao_ban_doc, kiem_tra_trung_ma_bd, xoa_ban_doc,
    muon_sach, tra_sach, sach_qua_han
)
from models import Sach, BanDoc, MuonTra
from datetime import datetime


# --- Quản lý sách ---

def them_sach(ds_sach: List[Sach]):
    s = tao_sach()
    if kiem_tra_trung_ma_sach(s.MaSach, ds_sach):
        print(f"Lỗi: Mã sách {s.MaSach} đã tồn tại, không thể thêm.")
        return False
    ds_sach.append(s)
    print(f"Thêm sách [{s.MaSach}] thành công.")
    return True


def xoa_sach_theo_ma(ds_sach: List[Sach]):
    ma_sach = input("Nhập mã sách cần xóa: ").strip()
    if xoa_sach(ma_sach, ds_sach):
        print(f"Xóa sách [{ma_sach}] thành công.")
        return True
    else:
        print(f"Lỗi: Không tìm thấy sách có mã [{ma_sach}].")
        return False


def cap_nhat_sach(ds_sach: List[Sach]):
    ma_sach = input("Nhập mã sách cần cập nhật: ").strip()
    if cap_nhat_thong_tin_sach(ma_sach, ds_sach):
        print("Cập nhật thành công.")
        return True
    else:
        print(f"Lỗi: Không tìm thấy sách có mã [{ma_sach}].")
        return False


def tim_kiem_sach_theo_tieu_chi(ds_sach: List[Sach]):
    print("Nhập tiêu chí tìm kiếm (bỏ trống để bỏ qua):")
    ten_sach = input("Tên sách: ").strip()
    tac_gia = input("Tác giả: ").strip()
    the_loai = input("Thể loại: ").strip()

    tieu_chi = {}
    if ten_sach:
        tieu_chi['TenSach'] = ten_sach
    if tac_gia:
        tieu_chi['TacGia'] = tac_gia
    if the_loai:
        tieu_chi['TheLoai'] = the_loai

    ket_qua = tim_kiem_sach(ds_sach, tieu_chi)
    if ket_qua:
        print(f"Tìm thấy {len(ket_qua)} sách:")
        for s in ket_qua:
            print(s)
    else:
        print("Không tìm thấy sách phù hợp.")


# --- Quản lý bạn đọc ---

def them_ban_doc(ds_bd: List[BanDoc]):
    b = tao_ban_doc()
    if kiem_tra_trung_ma_bd(b.MSSV, ds_bd):
        print(f"Lỗi: Mã bạn đọc {b.MSSV} đã tồn tại, không thể thêm.")
        return False
    ds_bd.append(b)
    print(f"Thêm bạn đọc [{b.MSSV}] thành công.")
    return True


def xoa_ban_doc_theo_ma(ds_bd: List[BanDoc]):
    mssv = input("Nhập mã bạn đọc cần xóa: ").strip()
    if xoa_ban_doc(mssv, ds_bd):
        print(f"Xóa bạn đọc [{mssv}] thành công.")
        return True
    else:
        print(f"Lỗi: Không tìm thấy bạn đọc có mã [{mssv}].")
        return False


def hien_thi_ban_doc(ds_bd: List[BanDoc]):
    if not ds_bd:
        print("Danh sách bạn đọc trống.")
    else:
        print(f"Danh sách bạn đọc ({len(ds_bd)} người):")
        for b in ds_bd:
            print(b)

# --- Quản lý mượn trả sách ---
def xu_ly_muon_sach(ds_sach: List[Sach], ds_bd: List[BanDoc], ds_muon: List[MuonTra]):
    mssv = input("Nhập MSSV bạn đọc: ").strip()
    if not any(b.MSSV == mssv for b in ds_bd):
        print(f"Lỗi: Không tìm thấy bạn đọc MSSV {mssv}.")
        return False

    ma_sach = input("Nhập mã sách cần mượn: ").strip()
    sach = tim_sach_theo_ma(ma_sach, ds_sach)
    if sach is None:
        print(f"Lỗi: Không tìm thấy sách mã {ma_sach}.")
        return False
    if sach.SoLuong <= 0:
        print(f"Lỗi: Sách [{ma_sach}] đã hết.")
        return False

    ma_phieu = input("Nhập mã phiếu mượn: ").strip()
    ngay_muon = input("Nhập ngày mượn (yyyy-mm-dd): ").strip()
    ngay_hen_tra = input("Nhập ngày hẹn trả (yyyy-mm-dd): ").strip()

    if muon_sach(mssv, ma_sach, ds_sach, ds_muon, ma_phieu, ngay_muon, ngay_hen_tra):
        print("Mượn sách thành công.")
        return True
    else:
        print("Mượn sách thất bại.")
        return False


def xu_ly_tra_sach(ds_sach: List[Sach], ds_muon: List[MuonTra]):
    mssv = input("Nhập MSSV bạn đọc: ").strip()
    ma_sach = input("Nhập mã sách trả: ").strip()
    ngay_tra = input("Nhập ngày trả thực tế (yyyy-mm-dd): ").strip()

    if tra_sach(mssv, ma_sach, ds_sach, ds_muon, ngay_tra):
        print("Trả sách thành công.")
        return True
    else:
        print("Trả sách thất bại hoặc chưa từng mượn sách này.")
        return False


def liet_ke_sach_qua_han(ds_muon: List[MuonTra]):
    ngay_hien_tai = input("Nhập ngày hiện tại (yyyy-mm-dd): ").strip()
    ds_qua_han = sach_qua_han(ds_muon, ngay_hien_tai)
    if ds_qua_han:
        print(f"Có {len(ds_qua_han)} sách quá hạn:")
        for phieu in ds_qua_han:
            print(phieu)
    else:
        print("Không có sách nào quá hạn.")
