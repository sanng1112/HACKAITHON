'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import DashboardLayout from '@/components/DashboardLayout';
import DataTable, { Column } from '@/components/DataTable';
import StatusBadge from '@/components/StatusBadge';
import LoadingSpinner from '@/components/LoadingSpinner';
import type { HoSo, TrangThaiHoSo, QueryParams } from '@/types';
import { TRANG_THAI_HO_SO_LABEL } from '@/types';
import { hoSoService } from '@/services/ho-so';

// Mock data để demo
const MOCK_HO_SO: HoSo[] = [
  {
    id: '1',
    ma_ho_so: 'HS-2026-0001',
    user_id: 'u1',
    loai_thu_tuc: 'Cấp giấy phép xây dựng',
    noi_dung: 'Xin cấp giấy phép xây dựng nhà ở tại 123 Lê Lợi, Q1',
    trang_thai: 'DANG_XU_LY',
    ngay_nop: '2026-06-10T08:30:00Z',
    created_at: '2026-06-10T08:30:00Z',
    updated_at: '2026-06-12T10:00:00Z',
    nguoi_nop: { id: 'u1', ho_ten: 'Nguyễn Văn A', email: 'a@gmail.com' },
  },
  {
    id: '2',
    ma_ho_so: 'HS-2026-0002',
    user_id: 'u1',
    loai_thu_tuc: 'Xác nhận tình trạng hôn nhân',
    noi_dung: 'Xin xác nhận tình trạng hôn nhân để làm hộ chiếu',
    trang_thai: 'DA_XU_LY',
    ngay_nop: '2026-06-08T14:00:00Z',
    ngay_xu_ly: '2026-06-11T09:00:00Z',
    created_at: '2026-06-08T14:00:00Z',
    updated_at: '2026-06-11T09:00:00Z',
    nguoi_nop: { id: 'u1', ho_ten: 'Nguyễn Văn A', email: 'a@gmail.com' },
  },
  {
    id: '3',
    ma_ho_so: 'HS-2026-0003',
    user_id: 'u1',
    loai_thu_tuc: 'Đăng ký hộ khẩu',
    noi_dung: 'Đăng ký hộ khẩu thường trú tại phường Bến Nghé',
    trang_thai: 'CHO_BO_SUNG',
    ngay_nop: '2026-06-05T10:00:00Z',
    yeu_cau_bo_sung: 'Cần bổ sung giấy tờ chứng minh chỗ ở hợp pháp',
    created_at: '2026-06-05T10:00:00Z',
    updated_at: '2026-06-09T15:00:00Z',
    nguoi_nop: { id: 'u1', ho_ten: 'Nguyễn Văn A', email: 'a@gmail.com' },
  },
  {
    id: '4',
    ma_ho_so: 'HS-2026-0004',
    user_id: 'u1',
    loai_thu_tuc: 'Cấp bản sao bằng cấp',
    noi_dung: 'Xin cấp bản sao bằng tốt nghiệp THPT',
    trang_thai: 'CHO_TIEP_NHAN',
    ngay_nop: '2026-06-13T07:00:00Z',
    created_at: '2026-06-13T07:00:00Z',
    updated_at: '2026-06-13T07:00:00Z',
    nguoi_nop: { id: 'u1', ho_ten: 'Nguyễn Văn A', email: 'a@gmail.com' },
  },
  {
    id: '5',
    ma_ho_so: 'HS-2026-0005',
    user_id: 'u1',
    loai_thu_tuc: 'Đăng ký khai sinh',
    noi_dung: 'Đăng ký khai sinh cho cháu Nguyễn Văn B',
    trang_thai: 'TU_CHOI',
    ngay_nop: '2026-06-01T09:00:00Z',
    ly_do_tu_choi: 'Thiếu giấy chứng sinh từ bệnh viện',
    created_at: '2026-06-01T09:00:00Z',
    updated_at: '2026-06-03T11:00:00Z',
    nguoi_nop: { id: 'u1', ho_ten: 'Nguyễn Văn A', email: 'a@gmail.com' },
  },
];

const allStatusFilters: Array<{ value: TrangThaiHoSo | 'ALL'; label: string }> = [
  { value: 'ALL', label: 'Tất cả' },
  { value: 'CHO_TIEP_NHAN', label: 'Chờ tiếp nhận' },
  { value: 'DANG_XU_LY', label: 'Đang xử lý' },
  { value: 'DA_XU_LY', label: 'Đã xử lý' },
  { value: 'CHO_BO_SUNG', label: 'Chờ bổ sung' },
  { value: 'TU_CHOI', label: 'Từ chối' },
];

const columns: Column<HoSo>[] = [
  {
    key: 'ma_ho_so',
    header: 'Mã hồ sơ',
    render: (item) => (
      <span className="font-medium text-gray-900">{item.ma_ho_so}</span>
    ),
  },
  {
    key: 'loai_thu_tuc',
    header: 'Loại thủ tục',
    className: 'min-w-[180px]',
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
      <span className="text-gray-500">
        {new Date(item.ngay_nop).toLocaleDateString('vi-VN')}
      </span>
    ),
    hideOnMobile: true,
  },
  {
    key: 'actions',
    header: '',
    render: (item) => (
      <span
        className="text-govone-600 hover:text-govone-700 font-medium text-sm cursor-pointer"
        onClick={(e) => {
          e.stopPropagation();
          window.location.href = `/citizen/ho-so/${item.id}`;
        }}
      >
        Chi tiết
      </span>
    ),
    className: 'text-right',
  },
];

export default function HoSoPage() {
  const router = useRouter();
  const [data, setData] = useState<HoSo[]>([]);
  const [loading, setLoading] = useState(true);
  const [statusFilter, setStatusFilter] = useState<TrangThaiHoSo | 'ALL'>('ALL');

  useEffect(() => {
    // Dùng mock data vì backend chưa có API
    setLoading(true);
    setTimeout(() => {
      setData(
        statusFilter === 'ALL'
          ? MOCK_HO_SO
          : MOCK_HO_SO.filter((h) => h.trang_thai === statusFilter),
      );
      setLoading(false);
    }, 500);
  }, [statusFilter]);

  return (
    <DashboardLayout>
      <div className="page-header">
        <div>
          <h1 className="page-title">Hồ sơ của tôi</h1>
          <p className="page-subtitle">
            Quản lý và theo dõi trạng thái các hồ sơ hành chính
          </p>
        </div>
        <button
          onClick={() => router.push('/citizen/nop-ho-so')}
          className="btn-primary"
        >
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
          </svg>
          Nộp hồ sơ mới
        </button>
      </div>

      {/* Filter tabs */}
      <div className="flex gap-2 mb-6 overflow-x-auto pb-2">
        {allStatusFilters.map((f) => (
          <button
            key={f.value}
            onClick={() => setStatusFilter(f.value)}
            className={`px-4 py-1.5 rounded-full text-sm font-medium whitespace-nowrap transition-colors ${
              statusFilter === f.value
                ? 'bg-govone-600 text-white'
                : 'bg-white text-gray-600 border border-gray-200 hover:bg-gray-50'
            }`}
          >
            {f.label}
          </button>
        ))}
      </div>

      <DataTable<HoSo>
        columns={columns}
        data={data}
        loading={loading}
        emptyTitle="Chưa có hồ sơ nào"
        emptyDescription="Bắt đầu nộp hồ sơ hành chính trực tuyến ngay!"
        onRowClick={(item) => router.push(`/citizen/ho-so/${item.id}`)}
        keyExtractor={(item) => item.id}
      />
    </DashboardLayout>
  );
}
