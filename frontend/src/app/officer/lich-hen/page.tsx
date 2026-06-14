'use client';

import { useState } from 'react';
import DashboardLayout from '@/components/DashboardLayout';
import StatusBadge from '@/components/StatusBadge';
import Modal from '@/components/Modal';
import { useToast } from '@/components/Toast';
import type { LichHen, TrangThaiLichHen } from '@/types';

const MOCK_LICH_HEN: LichHen[] = [
  {
    id: '1', user_id: 'u1', tieu_de: 'Nộp hồ sơ cấp phép xây dựng',
    ngay_hen: '2026-06-20', gio_hen: '09:00', trang_thai: 'CHO_XAC_NHAN',
    created_at: '2026-06-12T00:00:00Z',
    can_bo: { id: 'cb1', ho_ten: 'Trần Văn B' },
  },
  {
    id: '2', user_id: 'u2', tieu_de: 'Xin xác nhận tình trạng hôn nhân',
    ngay_hen: '2026-06-20', gio_hen: '10:30', trang_thai: 'CHO_XAC_NHAN',
    created_at: '2026-06-13T00:00:00Z',
  },
  {
    id: '3', user_id: 'u3', tieu_de: 'Nộp bổ sung hồ sơ HS-2026-0005',
    ngay_hen: '2026-06-20', gio_hen: '14:00', trang_thai: 'DA_XAC_NHAN',
    created_at: '2026-06-11T00:00:00Z',
    can_bo: { id: 'cb1', ho_ten: 'Trần Văn B' },
  },
  {
    id: '4', user_id: 'u4', tieu_de: 'Nộp hồ sơ đăng ký hộ khẩu',
    ngay_hen: '2026-06-21', gio_hen: '08:00', trang_thai: 'HOAN_THANH',
    created_at: '2026-06-10T00:00:00Z',
    can_bo: { id: 'cb1', ho_ten: 'Trần Văn B' },
  },
  {
    id: '5', user_id: 'u5', tieu_de: 'Hỏi về thủ tục cấp hộ chiếu',
    ngay_hen: '2026-06-19', gio_hen: '15:00', trang_thai: 'DA_HUY',
    created_at: '2026-06-08T00:00:00Z',
  },
];

const filterTabs = [
  { value: 'ALL', label: 'Tất cả' },
  { value: 'CHO_XAC_NHAN', label: 'Chờ xác nhận' },
  { value: 'DA_XAC_NHAN', label: 'Đã xác nhận' },
  { value: 'HOAN_THANH', label: 'Hoàn thành' },
];

export default function OfficerLichHenPage() {
  const toast = useToast();
  const [lichHen, setLichHen] = useState(MOCK_LICH_HEN);
  const [filter, setFilter] = useState('ALL');

  const filtered = filter === 'ALL' ? lichHen : lichHen.filter((l) => l.trang_thai === filter);

  const handleXacNhan = async (id: string) => {
    setLichHen((prev) =>
      prev.map((l) => (l.id === id ? { ...l, trang_thai: 'DA_XAC_NHAN' as TrangThaiLichHen } : l)),
    );
    toast.success('Đã xác nhận lịch hẹn');
  };

  const handleHoanThanh = async (id: string) => {
    setLichHen((prev) =>
      prev.map((l) => (l.id === id ? { ...l, trang_thai: 'HOAN_THANH' as TrangThaiLichHen } : l)),
    );
    toast.success('Đã hoàn thành lịch hẹn');
  };

  return (
    <DashboardLayout>
      <div className="page-header">
        <div>
          <h1 className="page-title">Quản lý lịch hẹn</h1>
          <p className="page-subtitle">Xác nhận và quản lý lịch hẹn công dân</p>
        </div>
      </div>

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
          </button>
        ))}
      </div>

      <div className="space-y-3">
        {filtered.map((lh) => (
          <div key={lh.id} className="card-hover p-5">
            <div className="flex items-start justify-between gap-4">
              <div className="flex-1">
                <div className="flex items-center gap-3 mb-2">
                  <h3 className="font-medium text-gray-900">{lh.tieu_de}</h3>
                  <StatusBadge status={lh.trang_thai} type="lich-hen" />
                </div>
                <div className="flex flex-wrap gap-4 text-sm text-gray-500">
                  <span className="flex items-center gap-1">
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                    {new Date(lh.ngay_hen).toLocaleDateString('vi-VN')}
                  </span>
                  <span className="flex items-center gap-1">
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    {lh.gio_hen}
                  </span>
                </div>
              </div>
              {lh.trang_thai === 'CHO_XAC_NHAN' && (
                <button onClick={() => handleXacNhan(lh.id)} className="btn-primary btn-sm">
                  Xác nhận
                </button>
              )}
              {lh.trang_thai === 'DA_XAC_NHAN' && (
                <button onClick={() => handleHoanThanh(lh.id)} className="btn-secondary btn-sm">
                  Hoàn thành
                </button>
              )}
            </div>
          </div>
        ))}
      </div>
    </DashboardLayout>
  );
}
