'use client';

import { useState } from 'react';
import DashboardLayout from '@/components/DashboardLayout';
import StatusBadge from '@/components/StatusBadge';
import Modal from '@/components/Modal';
import { useToast } from '@/components/Toast';
import { useAuth } from '@/hooks/useAuth';
import type { LichHen, TrangThaiLichHen } from '@/types';

const MOCK_LICH_HEN: LichHen[] = [
  {
    id: '1',
    user_id: 'u1',
    tieu_de: 'Nộp hồ sơ cấp giấy phép xây dựng',
    ngay_hen: '2026-06-20',
    gio_hen: '09:00',
    trang_thai: 'DA_XAC_NHAN',
    created_at: '2026-06-12T00:00:00Z',
    can_bo: { id: 'cb1', ho_ten: 'Trần Văn B' },
  },
  {
    id: '2',
    user_id: 'u1',
    tieu_de: 'Xin xác nhận tình trạng hôn nhân',
    ngay_hen: '2026-06-25',
    gio_hen: '14:30',
    trang_thai: 'CHO_XAC_NHAN',
    created_at: '2026-06-14T00:00:00Z',
  },
  {
    id: '3',
    user_id: 'u1',
    tieu_de: 'Nộp bổ sung hồ sơ',
    ngay_hen: '2026-06-15',
    gio_hen: '10:00',
    trang_thai: 'HOAN_THANH',
    created_at: '2026-06-10T00:00:00Z',
  },
];

export default function LichHenPage() {
  const toast = useToast();
  const [lichHen, setLichHen] = useState<LichHen[]>(MOCK_LICH_HEN);
  const [showModal, setShowModal] = useState(false);
  const [form, setForm] = useState({ tieu_de: '', ngay_hen: '', gio_hen: '', ghi_chu: '' });
  const [submitting, setSubmitting] = useState(false);

  const handleCreate = async () => {
    setSubmitting(true);
    try {
      await new Promise((resolve) => setTimeout(resolve, 1000));
      const newItem: LichHen = {
        id: Math.random().toString(),
        user_id: 'u1',
        ...form,
        trang_thai: 'CHO_XAC_NHAN',
        created_at: new Date().toISOString(),
      };
      setLichHen((prev) => [newItem, ...prev]);
      toast.success('Đặt lịch hẹn thành công!');
      setShowModal(false);
      setForm({ tieu_de: '', ngay_hen: '', gio_hen: '', ghi_chu: '' });
    } catch {
      toast.error('Đặt lịch thất bại');
    } finally {
      setSubmitting(false);
    }
  };

  const handleHuy = async (id: string) => {
    setLichHen((prev) =>
      prev.map((l) => (l.id === id ? { ...l, trang_thai: 'DA_HUY' as TrangThaiLichHen } : l)),
    );
    toast.success('Đã hủy lịch hẹn');
  };

  return (
    <DashboardLayout>
      <div className="page-header">
        <div>
          <h1 className="page-title">Lịch hẹn</h1>
          <p className="page-subtitle">Quản lý lịch hẹn làm việc với cơ quan hành chính</p>
        </div>
        <button onClick={() => setShowModal(true)} className="btn-primary">
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
          </svg>
          Đặt lịch hẹn
        </button>
      </div>

      {/* List */}
      <div className="space-y-3">
        {lichHen.map((lh) => (
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
                  {lh.can_bo && (
                    <span>Cán bộ: {lh.can_bo.ho_ten}</span>
                  )}
                </div>
              </div>
              {lh.trang_thai === 'CHO_XAC_NHAN' && (
                <button
                  onClick={() => handleHuy(lh.id)}
                  className="btn-ghost btn-sm text-red-500 hover:text-red-700 hover:bg-red-50"
                >
                  Hủy
                </button>
              )}
            </div>
          </div>
        ))}
      </div>

      {/* Modal đặt lịch */}
      <Modal isOpen={showModal} onClose={() => setShowModal(false)} title="Đặt lịch hẹn mới">
        <div className="space-y-4">
          <div>
            <label className="form-label">Tiêu đề *</label>
            <input
              type="text"
              className="form-input"
              placeholder="Nộp hồ sơ..."
              value={form.tieu_de}
              onChange={(e) => setForm((prev) => ({ ...prev, tieu_de: e.target.value }))}
            />
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="form-label">Ngày *</label>
              <input
                type="date"
                className="form-input"
                value={form.ngay_hen}
                onChange={(e) => setForm((prev) => ({ ...prev, ngay_hen: e.target.value }))}
              />
            </div>
            <div>
              <label className="form-label">Giờ *</label>
              <input
                type="time"
                className="form-input"
                value={form.gio_hen}
                onChange={(e) => setForm((prev) => ({ ...prev, gio_hen: e.target.value }))}
              />
            </div>
          </div>
          <div>
            <label className="form-label">Ghi chú</label>
            <textarea
              className="form-textarea"
              rows={3}
              placeholder="Ghi chú thêm..."
              value={form.ghi_chu}
              onChange={(e) => setForm((prev) => ({ ...prev, ghi_chu: e.target.value }))}
            />
          </div>
          <div className="flex justify-end gap-3 pt-2">
            <button onClick={() => setShowModal(false)} className="btn-secondary">
              Hủy
            </button>
            <button onClick={handleCreate} className="btn-primary" disabled={submitting || !form.tieu_de || !form.ngay_hen}>
              {submitting ? 'Đang xử lý...' : 'Xác nhận đặt lịch'}
            </button>
          </div>
        </div>
      </Modal>
    </DashboardLayout>
  );
}
