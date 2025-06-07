# data_handler.py

import csv
from typing import List, Type, Any
from models import Sach, BanDoc, MuonTra


def doc_file_csv(ten_file: str, lop: Type) -> List[Any]:
    ds = []
    try:
        with open(ten_file, mode='r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if lop == Sach:
                    obj = Sach(
                        ma_sach=row['MaSach'],
                        ten_sach=row['TenSach'],
                        tac_gia=row['TacGia'],
                        the_loai=row['TheLoai'],
                        so_luong=int(row['SoLuong']),
                        tinh_trang=row['TinhTrang']
                    )
                elif lop == BanDoc:
                    obj = BanDoc(
                        mssv=row['MSSV'],
                        ho_ten=row['HoTen'],

                        gioi_tinh=row['GioiTinh'],
                        ngay_sinh=row['NgaySinh']
                    )
                elif lop == MuonTra:
                    ngay_tra = row.get('NgayTraThucTe', '').strip()
                    tinh_trang_muon = "Đang mượn" if not ngay_tra else "Đã trả"

                    obj = MuonTra(
                        ma_phieu=row['MaPhieuMuon'],
                        mssv=row['MSSV'],
                        ma_sach=row['MaSach'],
                        ngay_muon=row['NgayMuon'],
                        ngay_hen_tra=row['NgayHenTra'],
                        ngay_tra_thuc_te=ngay_tra,
                        tinh_trang_muon=tinh_trang_muon
                    )
                else:
                    raise ValueError("Lớp không hợp lệ")
                ds.append(obj)
    except FileNotFoundError:
        print(f"File {ten_file} không tồn tại, trả về danh sách rỗng.")
    except Exception as e:
        print(f"Lỗi đọc file {ten_file}: {e}")
    return ds


def luu_file_csv(ds: List[Any], ten_file: str, lop: Type):
    if lop == Sach:
        fieldnames = ['MaSach', 'TenSach', 'TacGia', 'TheLoai', 'SoLuong', 'TinhTrang']
    elif lop == BanDoc:
        fieldnames = ['MSSV', 'HoTen', 'GioiTinh', 'NgaySinh']
    elif lop == MuonTra:
        fieldnames = ['MaPhieuMuon', 'MSSV', 'MaSach', 'NgayMuon', 'NgayHenTra', 'NgayTraThucTe', 'TinhTrangMuon']
    else:
        raise ValueError("Lớp không hợp lệ")

    try:
        with open(ten_file, mode='w', encoding='utf-8-sig', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for obj in ds:
                if lop == Sach:
                    writer.writerow({
                        'MaSach': obj.MaSach,
                        'TenSach': obj.TenSach,
                        'TacGia': obj.TacGia,
                        'TheLoai': obj.TheLoai,
                        'SoLuong': obj.SoLuong,
                        'TinhTrang': obj.TinhTrang
                    })
                elif lop == BanDoc:
                    writer.writerow({
                        'MSSV': obj.MSSV,
                        'HoTen': obj.HoTen,
                        'GioiTinh': obj.GioiTinh,
                        'NgaySinh': obj.NgaySinh
                    })
                elif lop == MuonTra:
                    writer.writerow({
                        'MaPhieuMuon': obj.MaPhieuMuon,
                        'MSSV': obj.MSSV,
                        'MaSach': obj.MaSach,
                        'NgayMuon': obj.NgayMuon,
                        'NgayHenTra': obj.NgayHenTra,
                        'NgayTraThucTe': obj.NgayTraThucTe,
                        'TinhTrangMuon': obj.TinhTrangMuon
                    })
    except Exception as e:
        print(f"Lỗi ghi file {ten_file}: {e}")


# Các hàm xử lý tầng 1 - sách
def tao_sach() -> Sach:
    print("Nhập thông tin sách mới:")
    ma_sach = input("Mã sách: ").strip().lower()
    ten_sach = input("Tên sách: ").strip().lower()
    tac_gia = input("Tác giả: ").strip().lower()
    the_loai = input("Thể loại: ").strip().lower()
    so_luong = int(input("Số lượng: ").strip())
    tinh_trang = input("Tình trạng: ").strip().lower() or "con"  
    return Sach(ma_sach, ten_sach, tac_gia, the_loai, so_luong, tinh_trang)

def kiem_tra_trung_ma_sach(ma_sach: str, ds_sach: List[Sach]) -> bool:
    return any(s.MaSach == ma_sach for s in ds_sach)

def tim_sach_theo_ma(ma_sach: str, ds_sach: List[Sach]) -> Sach | None:
    ma_sach = ma_sach.strip().lower()
    for s in ds_sach:
        if s.MaSach.strip().lower() == ma_sach:
            return s
    return None

def cap_nhat_thong_tin_sach(ma_sach: str, ds_sach: List[Sach]) -> bool:
    s = tim_sach_theo_ma(ma_sach, ds_sach)
    if s is None:
        return False
    print(f"Cập nhật thông tin sách [{ma_sach}]:")
    s.TenSach = input(f"Tên sách ({s.TenSach}): ") or s.TenSach
    s.TacGia = input(f"Tác giả ({s.TacGia}): ") or s.TacGia
    s.TheLoai = input(f"Thể loại ({s.TheLoai}): ") or s.TheLoai
    try:
        so_luong = input(f"Số lượng ({s.SoLuong}): ")
        if so_luong:
            s.SoLuong = int(so_luong)
    except ValueError:
        pass
    tinh_trang = input(f"Tình trạng ({s.TinhTrang}): ")
    if tinh_trang:
        s.TinhTrang = tinh_trang
    return True

def xoa_sach(ma_sach: str, ds_sach: List[Sach]) -> bool:
    for i, s in enumerate(ds_sach):
        if s.MaSach.strip().lower() == ma_sach:
            del ds_sach[i]
            return True
    return False

def tim_kiem_sach(ds_sach: List[Sach], tieu_chi: dict) -> List[Sach]:
    ket_qua = ds_sach
    for key, val in tieu_chi.items():
        ket_qua = [s for s in ket_qua if val.lower() in str(getattr(s, key, '')).lower()]
    return ket_qua

# Các hàm xử lý tầng 1 - bạn đọc
def tao_ban_doc() -> BanDoc:
    print("Nhập thông tin bạn đọc mới:")
    mssv = input("MSSV: ").strip()
    ho_ten = input("Họ tên: ").strip()
    gioi_tinh = input("Giới tính: ").strip()
    ngay_sinh = input("Ngày sinh (dd/mm/yyyy): ").strip()
    return BanDoc(mssv, ho_ten, gioi_tinh, ngay_sinh)

def kiem_tra_trung_ma_bd(mssv: str, ds_bd: List[BanDoc]) -> bool:
    return any(b.MSSV == mssv for b in ds_bd)

def xoa_ban_doc(mssv: str, ds_bd: List[BanDoc]) -> bool:
    for i, b in enumerate(ds_bd):
        if b.MSSV == mssv:
            del ds_bd[i]
            return True
    return False

# Các hàm xử lý tầng 1 - mượn trả
def muon_sach(mssv: str, ma_sach: str, ds_sach: List[Sach], ds_muon: List[MuonTra], ma_phieu: str,
              ngay_muon: str, ngay_hen_tra: str) -> bool:
    ma_sach = ma_sach.strip().lower()
    sach = next((s for s in ds_sach if s.MaSach.strip().lower() == ma_sach), None)
    if sach is None or sach.SoLuong <= 0:
        return False
    sach.SoLuong -= 1
    sach.TinhTrang = "Het" if sach.SoLuong == 0 else "Con"
    muon = MuonTra(ma_phieu, mssv, ma_sach, ngay_muon, ngay_hen_tra)
    ds_muon.append(muon)
    return True

def tra_sach(mssv: str, ma_sach: str, ds_sach: List[Sach], ds_muon: List[MuonTra], ngay_tra_thuc_te: str) -> bool:
    for muon in ds_muon:
        if muon.MSSV == mssv and muon.MaSach == ma_sach and muon.TinhTrangMuon.lower() == "dang muon":
            muon.NgayTraThucTe = ngay_tra_thuc_te
            muon.TinhTrangMuon = "Da tra"
            sach = tim_sach_theo_ma(ma_sach, ds_sach)
            if sach:
                sach.SoLuong += 1
                sach.TinhTrang = "Con"
            return True
    return False

def sach_qua_han(ds_muon: List[MuonTra], ngay_hien_tai: str) -> List[MuonTra]:
    return [m for m in ds_muon if m.da_qua_han(ngay_hien_tai)]
