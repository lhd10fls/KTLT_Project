from datetime import datetime

class Sach:
    def __init__(self, ma_sach: str, ten_sach: str, tac_gia: str, the_loai: str, so_luong: int, tinh_trang: str):
        # Tên thuộc tính giống hệt tên cột CSV để dễ map
        self.MaSach = ma_sach
        self.TenSach = ten_sach
        self.TacGia = tac_gia
        self.TheLoai = the_loai
        self.SoLuong = so_luong
        self.TinhTrang = tinh_trang  # "Con" hoặc "Het"

    def __str__(self):
        return (f"[{self.MaSach}] {self.TenSach} - Tác giả: {self.TacGia}, Thể loại: {self.TheLoai}, "
                f"Số lượng: {self.SoLuong}, Tình trạng: {self.TinhTrang}")


class BanDoc:
    def __init__(self, mssv: str, ho_ten: str, gioi_tinh: str, ngay_sinh: str):
        self.MSSV = mssv
        self.HoTen = ho_ten
        self.GioiTinh = gioi_tinh

        # Chuẩn hóa định dạng ngày sinh thành yyyy-mm-dd
        try:
            ns = datetime.strptime(ngay_sinh, "%d/%m/%Y")  # hoặc thêm các format khác nếu cần
            self.NgaySinh = ns.strftime("%Y-%m-%d")
        except:
            self.NgaySinh = ngay_sinh  # fallback nếu không parse được

    def __str__(self):
        return f"[{self.MSSV}] {self.HoTen} - Giới tính: {self.GioiTinh}, Ngày sinh: {self.NgaySinh}"


class MuonTra:
    def __init__(self, ma_phieu: str, mssv: str, ma_sach: str,
                 ngay_muon: str, ngay_hen_tra: str, ngay_tra_thuc_te: str = "",
                 tinh_trang_muon: str = "Dang muon"):
        # Tên thuộc tính trùng tên cột CSV
        self.MaPhieuMuon = ma_phieu
        self.MSSV = mssv
        self.MaSach = ma_sach
        self.NgayMuon = ngay_muon          # Dạng chuỗi "yyyy-mm-dd"
        self.NgayHenTra = ngay_hen_tra    # Dạng chuỗi "yyyy-mm-dd"
        self.NgayTraThucTe = ngay_tra_thuc_te  # "" nếu chưa trả
        self.TinhTrangMuon = tinh_trang_muon    # "Dang muon" hoặc "Da tra"

    def __str__(self):
        return (f"Phiếu {self.MaPhieuMuon}: MSSV {self.MSSV} mượn sách {self.MaSach} "
                f"ngày mượn {self.NgayMuon}, hẹn trả {self.NgayHenTra}, "
                f"ngày trả thực tế: {self.NgayTraThucTe or 'Chưa trả'}, "
                f"tình trạng: {self.TinhTrangMuon}")

    def da_qua_han(self, ngay_hien_tai: str) -> bool:
        if self.TinhTrangMuon.lower() == "da tra":
            return False
        date_format = "%Y-%m-%d"
        ngay_hen_tra_dt = datetime.strptime(self.NgayHenTra, date_format)
        ngay_hien_tai_dt = datetime.strptime(ngay_hien_tai, date_format)
        return ngay_hien_tai_dt > ngay_hen_tra_dt
