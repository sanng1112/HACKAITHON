'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import DashboardLayout from '@/components/DashboardLayout';
import StatusBadge from '@/components/StatusBadge';
import type { ThongBao } from '@/types';
import { LOAI_THONG_BAO_LABEL } from '@/types';

const MOCK_THONG_BAO: ThongBao[] = [
  {
    id: '1',
    tieu_de: 'Hồ sơ HS-2026-0001 đã được tiếp nhận',
    noi_dung: 'Hồ sơ cấp giấy phép xây dựng của bạn đã được cán bộ Trần Văn B tiếp nhận và đang xử lý.',
    loai: 'ho_so',
    da_doc: false,
    created_at: '2026-06-12T10:30:00Z',
  },
  {
    id: '2',
    tieu_de: 'Yêu cầu bổ sung hồ sơ',
    noi_dung: 'Hồ sơ HS-2026-0003 cần bổ sung: Giấy tờ chứng minh chỗ ở hợp pháp. Vui lòng bổ sung trong vòng 7 ngày.',
    loai: 'ho_so',
    da_doc: false,
    created_at: '2026-06-11T15:00:00Z',
  },
  {
    id: '3',
    tieu_de: 'Lịch nghỉ lễ 30/4 - 1/5',
    noi_dung: 'UBND phường thông báo lịch nghỉ lễ từ ngày 30/4 đến hết ngày 3/5. Các hoạt động hành chính sẽ tạm dừng trong thời gian này.',
    loai: 'he_thong',
    da_doc: true,
    created_at: '2026-06-10T08:00:00Z',
  },
  {
    id: '4',
    tieu_de: 'Lịch hẹn đã được xác nhận',
    noi_dung: 'Lịch hẹn "Nộp hồ sơ cấp giấy phép xây dựng" vào 09:00 ngày 20/06/2026 đã được cán bộ Trần Văn B xác nhận.',
    loai: 'lich_hen',
    da_doc: true,
    created_at: '2026-06-09T14:00:00Z',
  },
  {
    id: '5',
    tieu_de: 'Hồ sơ HS-2026-0002 đã được phê duyệt',
    noi_dung: 'Hồ sơ xác nhận tình trạng hôn nhân của bạn đã được phê duyệt. Vui lòng đến UBND để nhận kết quả.',
    loai: 'ho_so',
    da_doc: true,
    created_at: '2026-06-08T11:00:00Z',
  },
];

const loaiFilters = [
  { value: 'ALL', label: 'Tất cả' },
  { value: 'ho_so', label: 'Hồ sơ' },
  { value: 'lich_hen', label: 'Lịch hẹn' },
  { value: 'he_thong', label: 'Hệ thống' },
] as const;

export default function ThongBaoPage() {
  const router = useRouter();
  const [thongBaos, setThongBaos] = useState<ThongBao[]>(MOCK_THONG_BAO);
  const [filter, setFilter] = useState<string>('ALL');

  const filtered = filter === 'ALL' ? thongBaos : thongBaos.filter((tb) => tb.loai === filter);
  const unreadCount = thongBaos.filter((tb) => !tb.da_doc).length;

  const handleMarkAsRead = (id: string) => {
    setThongBaos((prev) => prev.map((tb) => (tb.id === id ? { ...tb, da_doc: true } : tb)));
  };

  return (
    <DashboardLayout>
      <div className="page-header">
        <div>
          <h1 className="page-title">
            Thông báo
            {unreadCount > 0 && (
              <span className="ml-2 px-2 py-0.5 text-sm bg-red-100 text-red-600 rounded-full">
                {unreadCount} chưa đọc
              </span>
            )}
          </h1>
          <p className="page-subtitle">Cập nhật thông tin về hồ sơ và lịch hẹn của bạn</p>
        </div>
      </div>

      {/* Loại filter */}
      <div className="flex gap-2 mb-6">
        {loaiFilters.map((f) => (
          <button
            key={f.value}
            onClick={() => setFilter(f.value)}
            className={`px-4 py-1.5 rounded-full text-sm font-medium transition-colors ${
              filter === f.value
                ? 'bg-govone-600 text-white'
                : 'bg-white text-gray-600 border border-gray-200 hover:bg-gray-50'
            }`}
          >
            {f.label}
          </button>
        ))}
      </div>

      {/* List */}
      <div className="space-y-3">
        {filtered.map((tb) => (
          <div
            key={tb.id}
            className={`card-hover p-5 cursor-pointer ${!tb.da_doc ? 'border-l-4 border-l-govone-500 bg-govone-50/30' : ''}`}
            onClick={() => handleMarkAsRead(tb.id)}
          >
            <div className="flex items-start justify-between gap-4">
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 mb-1">
                  {!tb.da_doc && (
                    <span className="w-2 h-2 rounded-full bg-govone-600 flex-shrink-0" />
                  )}
                  <h3 className={`text-sm ${!tb.da_doc ? 'font-semibold text-gray-900' : 'font-medium text-gray-700'}`}>
                    {tb.tieu_de}
                  </h3>
                  <span className="px-2 py-0.5 text-xs rounded-full bg-gray-100 text-gray-600">
                    {LOAI_THONG_BAO_LABEL[tb.loai]}
                  </span>
                </div>
                <p className={`text-sm ${!tb.da_doc ? 'text-gray-600' : 'text-gray-400'} line-clamp-2`}>
                  {tb.noi_dung}
                </p>
                <p className="text-xs text-gray-400 mt-1">
                  {new Date(tb.created_at).toLocaleDateString('vi-VN', {
                    hour: '2-digit',
                    minute: '2-digit',
                    day: 'numeric',
                    month: 'numeric',
                    year: 'numeric',
                  })}
                </p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </DashboardLayout>
  );
}
