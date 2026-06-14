// ─── Enums ──────────────────────────────────────────────

export type UserRole = 'citizen' | 'officer' | 'admin';
export type TrangThaiTaiKhoan = 'active' | 'inactive' | 'locked';

export type TrangThaiHoSo =
  | 'CHO_TIEP_NHAN'
  | 'CHO_XU_LY'
  | 'DANG_XU_LY'
  | 'DA_XU_LY'
  | 'TU_CHOI'
  | 'CHO_BO_SUNG'
  | 'DA_BO_SUNG';

export type TrangThaiLichHen =
  | 'CHO_XAC_NHAN'
  | 'DA_XAC_NHAN'
  | 'DA_HUY'
  | 'HOAN_THANH';

export type LoaiThongBao = 'he_thong' | 'ho_so' | 'lich_hen';

// ─── User ───────────────────────────────────────────────

export interface User {
  id: string;
  email: string;
  ho_ten: string;
  so_cccd?: string;
  so_dien_thoai?: string;
  dia_chi?: string;
  role: UserRole;
  trang_thai: TrangThaiTaiKhoan;
  created_at: string;
  updated_at?: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
  user: User;
}

export interface RegisterRequest {
  email: string;
  password: string;
  ho_ten: string;
  so_cccd?: string;
  so_dien_thoai?: string;
}

// ─── Hồ sơ ──────────────────────────────────────────────

export interface HoSo {
  id: string;
  ma_ho_so: string;
  user_id: string;
  loai_thu_tuc: string;
  noi_dung: string;
  trang_thai: TrangThaiHoSo;
  nguoi_xu_ly_id?: string;
  ghi_chu_xu_ly?: string;
  ly_do_tu_choi?: string;
  yeu_cau_bo_sung?: string;
  ngay_nop: string;
  ngay_xu_ly?: string;
  created_at: string;
  updated_at: string;
  nguoi_nop?: Pick<User, 'id' | 'ho_ten' | 'email'>;
  nguoi_xu_ly?: Pick<User, 'id' | 'ho_ten'>;
  tai_lieu?: HoSoTaiLieu[];
  lich_su?: HoSoLichSu[];
}

export interface CreateHoSoRequest {
  loai_thu_tuc: string;
  noi_dung: string;
}

export interface HoSoTaiLieu {
  id: string;
  ho_so_id: string;
  ten_file: string;
  duong_dan: string;
  loai_file: string;
  kich_thuoc: number;
  created_at: string;
}

export interface HoSoLichSu {
  id: string;
  ho_so_id: string;
  nguoi_thuc_hien_id: string;
  hanh_dong: string;
  trang_thai_cu?: string;
  trang_thai_moi?: string;
  ghi_chu?: string;
  created_at: string;
  nguoi_thuc_hien?: Pick<User, 'ho_ten'>;
}

// ─── Lịch hẹn ───────────────────────────────────────────

export interface LichHen {
  id: string;
  user_id: string;
  can_bo_id?: string;
  tieu_de: string;
  ngay_hen: string;
  gio_hen: string;
  ghi_chu?: string;
  trang_thai: TrangThaiLichHen;
  created_at: string;
  updated_at?: string;
  can_bo?: Pick<User, 'id' | 'ho_ten'>;
}

export interface CreateLichHenRequest {
  tieu_de: string;
  ngay_hen: string;
  gio_hen: string;
  ghi_chu?: string;
}

// ─── Thông báo ──────────────────────────────────────────

export interface ThongBao {
  id: string;
  user_id?: string;
  tieu_de: string;
  noi_dung: string;
  loai: LoaiThongBao;
  da_doc: boolean;
  created_at: string;
}

export interface CreateThongBaoRequest {
  user_id?: string;
  tieu_de: string;
  noi_dung: string;
  loai: LoaiThongBao;
}

// ─── AI ─────────────────────────────────────────────────

export interface OCRResult {
  raw_text: string;
  document_type: string;
  fields: Record<string, string | null>;
  confidence: number;
  blocks: Array<{ text: string; confidence: number }>;
  source: string;
  cached: boolean;
}

export interface STTResult {
  text: string;
  language: string;
  confidence: number | null;
  source: string;
  word_count: number;
}

export interface NLPResult {
  entities: Array<{ text: string; label: string; score: number }>;
  procedure_class: string;
  procedure_score: number;
  source: string;
}

export interface AutoFillResult {
  form_data: Record<string, string>;
  uncertain_fields: string[];
  document_type: string;
  raw_text: string;
  confidence: number;
  needs_review: boolean;
  procedure_suggestion?: string;
}

export interface AIHealth {
  ocr: { loaded: boolean; model: string; version: string };
  stt: { loaded: boolean; model: string; version: string };
  nlp: { loaded: boolean; model: string; version: string };
  vnpt_api: { connected: boolean };
}

// ─── Common ─────────────────────────────────────────────

export interface ApiResponse<T> {
  success: boolean;
  data: T;
  error?: { code: string; message: string } | null;
  pagination?: Pagination;
}

export interface Pagination {
  page: number;
  limit: number;
  total: number;
  total_pages: number;
}

export interface QueryParams {
  page?: number;
  limit?: number;
  sort_by?: string;
  sort_order?: 'asc' | 'desc';
  trang_thai?: string;
  loai_thu_tuc?: string;
  from_date?: string;
  to_date?: string;
  q?: string;
  da_doc?: boolean;
  loai?: string;
}

// ─── Stats ──────────────────────────────────────────────

export interface OfficerStats {
  tong_ho_so: number;
  ho_so_moi: number;
  dang_xu_ly: number;
  da_xu_ly: number;
  tu_choi: number;
  cho_bo_sung: number;
  lich_hen_hom_nay: number;
  thong_bao_chua_doc: number;
  ho_so_theo_thang: Array<{ thang: string; so_luong: number }>;
  trang_thai_phan_bo: Array<{ trang_thai: string; so_luong: number }>;
}

export interface CitizenStats {
  tong_ho_so: number;
  dang_xu_ly: number;
  da_xu_ly: number;
  lich_hen_sap_toi: number;
  thong_bao_chua_doc: number;
}

// ─── Form ───────────────────────────────────────────────

export const LOAI_THU_TUC_OPTIONS = [
  { value: 'cap-giay-phep-xay-dung', label: 'Cấp giấy phép xây dựng' },
  { value: 'dang-ky-ho-khau', label: 'Đăng ký hộ khẩu' },
  { value: 'xac-nhan-tinh-trang-hon-nhan', label: 'Xác nhận tình trạng hôn nhân' },
  { value: 'dang-ky-khai-sinh', label: 'Đăng ký khai sinh' },
  { value: 'dang-ky-khai-tu', label: 'Đăng ký khai tử' },
  { value: 'cap-ban-sao-bang-cap', label: 'Cấp bản sao bằng cấp' },
  { value: 'xac-nhan-thu-nhap', label: 'Xác nhận thu nhập' },
  { value: 'chuyen-nhuong-quyen-su-dung-dat', label: 'Chuyển nhượng quyền sử dụng đất' },
  { value: 'xin-cap-ho-chieu', label: 'Xin cấp hộ chiếu' },
  { value: 'khac', label: 'Thủ tục khác' },
] as const;

export const TRANG_THAI_HO_SO_LABEL: Record<TrangThaiHoSo, string> = {
  CHO_TIEP_NHAN: 'Chờ tiếp nhận',
  CHO_XU_LY: 'Chờ xử lý',
  DANG_XU_LY: 'Đang xử lý',
  DA_XU_LY: 'Đã xử lý',
  TU_CHOI: 'Từ chối',
  CHO_BO_SUNG: 'Chờ bổ sung',
  DA_BO_SUNG: 'Đã bổ sung',
};

export const TRANG_THAI_LICH_HEN_LABEL: Record<TrangThaiLichHen, string> = {
  CHO_XAC_NHAN: 'Chờ xác nhận',
  DA_XAC_NHAN: 'Đã xác nhận',
  DA_HUY: 'Đã hủy',
  HOAN_THANH: 'Hoàn thành',
};

export const LOAI_THONG_BAO_LABEL: Record<LoaiThongBao, string> = {
  he_thong: 'Hệ thống',
  ho_so: 'Hồ sơ',
  lich_hen: 'Lịch hẹn',
};
