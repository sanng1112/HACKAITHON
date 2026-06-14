'use client';

import { useState, useEffect } from 'react';
import DashboardLayout from '@/components/DashboardLayout';
import DataTable, { Column } from '@/components/DataTable';
import StatusBadge from '@/components/StatusBadge';
import Modal from '@/components/Modal';
import { useToast } from '@/components/Toast';
import type { HoSo, TrangThaiHoSo } from '@/types';

const MOCK_HO_SO: (HoSo & { nguoi_nop_ten?: string })[] = [
  {
    id: '1',
    ma_ho_so: 'HS-2026-0001',
    user_id: 'u1',
    loai_thu_tuc: 'Cấp giấy phép xây dựng',
    noi_dung: 'Xin cấp giấy phép xây dựng nhà ở tại 123 Lê Lợi, Q1',
    trang_thai: 'CHO_XU_LY',
    ngay_nop: '2026-06-10T08:30:00Z',
    created_at: '2026-06-10T08:30:00Z',
    updated_at: '2026-06-10T08:30:00Z',
    nguoi_nop: { id: 'u1', ho_ten: 'Nguyễn Văn A', email: 'a@gmail.com' },
  },
  {
    id: '2',
    ma_ho_so: 'HS-2026-0002',
    user_id: 'u2',
    loai_thu_tuc: 'Đăng ký hộ khẩu',
    noi_dung: 'Đăng ký hộ khẩu thường trú',
    trang_thai: 'DANG_XU_LY',
    ngay_nop: '2026-06-09T10:00:00Z',
    created_at: '2026-06-09T10:00:00Z',
    updated_at: '2026-06-12T09:00:00Z',
    nguoi_nop: { id: 'u2', ho_ten: 'Trần Thị C', email: 'c@gmail.com' },
    nguoi_xu_ly: { id: 'cb1', ho_ten: 'Trần Văn B' },
  },
  {
    id: '3',
    ma_ho_so: 'HS-2026-0003',
    user_id: 'u3',
    loai_thu_tuc: 'Xác nhận tình trạng hôn nhân',
    noi_dung: 'Xin xác nhận tình trạng hôn nhân',
    trang_thai: 'CHO_TIEP_NHAN',
    ngay_nop: '2026-06-13T07:30:00Z',
    created_at: '2026-06-13T07:30:00Z',
    updated_at: '2026-06-13T07:30:00Z',
    nguoi_nop: { id: 'u3', ho_ten: 'Lê Văn D', email: 'd@gmail.com' },
  },
  {
    id: '4',
    ma_ho_so: 'HS-2026-0004',
    user_id: 'u4',
    loai_thu_tuc: 'Cấp bản sao bằng cấp',
    noi_dung: 'Xin cấp bản sao bằng tốt nghiệp ĐH',
    trang_thai: 'DA_XU_LY',
    ngay_nop: '2026-06-05T14:00:00Z',
    ngay_xu_ly: '2026-06-08T16:00:00Z',
    created_at: '2026-06-05T14:00:00Z',
    updated_at: '2026-06-08T16:00:00Z',
    nguoi_nop: { id: 'u4', ho_ten: 'Phạm Thị E', email: 'e@gmail.com' },
  },
  {
    id: '5',
    ma_ho_so: 'HS-2026-0005',
    user_id: 'u5',
    loai_thu_tuc: 'Cấp giấy phép xây dựng',
    noi_dung: 'Xin cấp phép sửa chữa nhà',
    trang_thai: 'CHO_BO_SUNG',
    ngay_nop: '2026-06-03T09:00:00Z',
    yeu_cau_bo_sung: 'Cần bổ sung sơ đồ mặt bằng',
    created_at: '2026-06-03T09:00:00Z',
    updated_at: '2026-06-06T11:00:00Z',
    nguoi_nop: { id: 'u5', ho_ten: 'Hoàng Văn F', email: 'f@gmail.com' },
  },
  {
    id: '6',
    ma_ho_so: 'HS-2026-0006',
    user_id: 'u6',
    loai_thu_tuc: 'Đăng ký khai sinh',
    noi_dung: 'Đăng ký khai sinh cho con',
    trang_thai: 'TU_CHOI',
    ngay_nop: '2026-06-01T10:00:00Z',
    ly_do_tu_choi: 'Thiếu giấy chứng sinh',
    created_at: '2026-06-01T10:00:00Z',
    updated_at: '2026-06-02T15:00:00Z',
    nguoi_nop: { id: 'u6', ho_ten: 'Vũ Thị G', email: 'g@gmail.com' },
  },
];

const filterTabs: Array<{ value: TrangThaiHoSo | 'ALL'; label: string }> = [
  { value: 'ALL', label: 'Tất cả' },
  { value: 'CHO_TIEP_NHAN', label: 'Chờ tiếp nhận' },
  { value: 'CHO_XU_LY', label: 'Chờ xử lý' },
  { value: 'DANG_XU_LY', label: 'Đang xử lý' },
  { value: 'CHO_BO_SUNG', label: 'Chờ bổ sung' },
  { value: 'DA_XU_LY', label: 'Đã xử lý' },
];

const columns: Column<HoSo & { nguoi_nop_ten?: string }>[] = [
  {
    key: 'ma_ho_so',
    header: 'Mã HS',
    render: (item) => (
      <span className="font-medium text-gray-900">{item.ma_ho_so}</span>
    ),
  },
  {
    key: 'nguoi_nop_ten',
    header: 'Người nộp',
    render: (item) => (
      <span className="text-gray-700">{item.nguoi_nop?.ho_ten}</span>
    ),
  },
  {
    key: 'loai_thu_tuc',
    header: 'Thủ tục',
    className: 'min-w-[150px] hidden sm:table-cell',
    hideOnMobile: true,
  },
  {
    key: 'trang_thai',
    header: 'Trạng thái',
    render: (item) => <StatusBadge status={item.trang_thai} />,
  },
  {
    key: 'ngay_nop',
    header: 'Ngày nộp',
    render: (item) => (
      <span className="text-gray-500 text-xs">
        {new Date(item.ngay_nop).toLocaleDateString('vi-VN')}
      </span>
    ),
    hideOnMobile: true,
  },
];

export default function OfficerHoSoPage() {
  const toast = useToast();
  const [data, setData] = useState(MOCK_HO_SO);
  const [filter, setFilter] = useState<TrangThaiHoSo | 'ALL'>('ALL');
  const [selected, setSelected] = useState<(HoSo & { nguoi_nop_ten?: string }) | null>(null);
  const [showDetail, setShowDetail] = useState(false);
  const [actionNote, setActionNote] = useState('');

  const filtered = filter === 'ALL' ? data : data.filter((h) => h.trang_thai === filter);

  const handleAction = async (action: string) => {
    if (!selected) return;
    try {
      await new Promise((resolve) => setTimeout(resolve, 800));
      let newStatus: TrangThaiHoSo = 'DANG_XU_LY';
      let msg = '';

      switch (action) {
        case 'tiep-nhan':
          newStatus = 'CHO_XU_LY';
          msg = 'Đã tiếp nhận hồ sơ';
          break;
        case 'nhan-xu-ly':
          newStatus = 'DANG_XU_LY';
          msg = 'Đã nhận xử lý hồ sơ';
          break;
        case 'phe-duyet':
          newStatus = 'DA_XU_LY';
          msg = 'Đã phê duyệt hồ sơ';
          break;
        case 'tu-choi':
          if (!actionNote) {
            toast.warning('Vui lòng nhập lý do từ chối');
            return;
          }
          newStatus = 'TU_CHOI';
          msg = 'Đã từ chối hồ sơ';
          break;
        case 'yeu-cau-bo-sung':
          if (!actionNote) {
            toast.warning('Vui lòng nhập yêu cầu bổ sung');
            return;
          }
          newStatus = 'CHO_BO_SUNG';
          msg = 'Đã yêu cầu bổ sung';
          break;
      }

      setData((prev) =>
        prev.map((h) =>
          h.id === selected.id
            ? { ...h, trang_thai: newStatus, ghi_chu_xu_ly: actionNote }
            : h,
        ),
      );
      toast.success(msg);
      setShowDetail(false);
      setSelected(null);
      setActionNote('');
    } catch {
      toast.error('Thao tác thất bại');
    }
  };

  return (
    <DashboardLayout>
      <div className="page-header">
        <div>
          <h1 className="page-title">Quản lý hồ sơ</h1>
          <p className="page-subtitle">Tiếp nhận và xử lý hồ sơ hành chính</p>
        </div>
      </div>

      {/* Status tabs */}
      <div className="flex gap-2 mb-6 overflow-x-auto pb-2">
        {filterTabs.map((f) => (
          <button
            key={f.value}
            onClick={() => setFilter(f.value)}
            className={`px-4 py-1.5 rounded-full text-sm font-medium whitespace-nowrap transition-colors ${
              filter === f.value
                ? 'bg-govone-600 text-white'
                : 'bg-white text-gray-600 border border-gray-200 hover:bg-gray-50'
            }`}
          >
            {f.label}
            <span className="ml-1.5 text-xs opacity-70">
              ({filter === 'ALL' ? data.length : data.filter((h) => h.trang_thai === f.value).length})
            </span>
          </button>
        ))}
      </div>

      {/* Table */}
      <DataTable
        columns={columns}
        data={filtered}
        loading={false}
        emptyTitle="Không có hồ sơ nào"
        onRowClick={(item) => {
          setSelected(item);
          setShowDetail(true);
          setActionNote('');
        }}
        keyExtractor={(item) => item.id}
      />

      {/* Detail modal */}
      <Modal
        isOpen={showDetail}
        onClose={() => setShowDetail(false)}
        title={`Hồ sơ ${selected?.ma_ho_so || ''}`}
        size="lg"
      >
        {selected && (
          <div className="space-y-6">
            {/* Info */}
            <div className="grid grid-cols-2 gap-4">
              <div>
                <p className="text-xs text-gray-500 uppercase">Người nộp</p>
                <p className="text-sm font-medium">{selected.nguoi_nop?.ho_ten}</p>
              </div>
              <div>
                <p className="text-xs text-gray-500 uppercase">Trạng thái</p>
                <StatusBadge status={selected.trang_thai} size="md" />
              </div>
              <div>
                <p className="text-xs text-gray-500 uppercase">Loại thủ tục</p>
                <p className="text-sm font-medium">{selected.loai_thu_tuc}</p>
              </div>
              <div>
                <p className="text-xs text-gray-500 uppercase">Ngày nộp</p>
                <p className="text-sm font-medium">
                  {new Date(selected.ngay_nop).toLocaleDateString('vi-VN')}
                </p>
              </div>
            </div>

            {/* Nội dung */}
            <div>
              <p className="text-xs text-gray-500 uppercase mb-1">Nội dung</p>
              <p className="text-sm text-gray-700 bg-gray-50 rounded-lg p-3">{selected.noi_dung}</p>
            </div>

            {/* Actions */}
            <div className="border-t pt-4">
              <p className="text-xs text-gray-500 uppercase mb-3">Thao tác</p>
              <div className="flex flex-wrap gap-2 mb-3">
                {(selected.trang_thai === 'CHO_TIEP_NHAN' || selected.trang_thai === 'CHO_XU_LY') && (
                  <button
                    onClick={() => handleAction('tiep-nhan')}
                    className="btn-primary btn-sm"
                  >
                    Tiếp nhận
                  </button>
                )}
                {selected.trang_thai === 'CHO_XU_LY' && (
                  <button
                    onClick={() => handleAction('nhan-xu-ly')}
                    className="btn-primary btn-sm"
                  >
                    Nhận xử lý
                  </button>
                )}
                {selected.trang_thai === 'DANG_XU_LY' && (
                  <>
                    <button
                      onClick={() => handleAction('phe-duyet')}
                      className="btn-primary btn-sm"
                    >
                      Phê duyệt
                    </button>
                    <button
                      onClick={() => handleAction('yeu-cau-bo-sung')}
                      className="btn-secondary btn-sm"
                    >
                      Yêu cầu bổ sung
                    </button>
                    <button
                      onClick={() => handleAction('tu-choi')}
                      className="btn-danger btn-sm"
                    >
                      Từ chối
                    </button>
                  </>
                )}
              </div>
              {(selected.trang_thai === 'DANG_XU_LY') && (
                <textarea
                  className="form-textarea mt-2"
                  rows={3}
                  placeholder="Ghi chú / Lý do từ chối / Yêu cầu bổ sung..."
                  value={actionNote}
                  onChange={(e) => setActionNote(e.target.value)}
                />
              )}
            </div>
          </div>
        )}
      </Modal>
    </DashboardLayout>
  );
}
