'use client';

import { useState } from 'react';
import DashboardLayout from '@/components/DashboardLayout';
import Modal from '@/components/Modal';
import { useToast } from '@/components/Toast';
import type { ThongBao, LoaiThongBao } from '@/types';
import { LOAI_THONG_BAO_LABEL } from '@/types';

const MOCK_THONG_BAO: ThongBao[] = [
  {
    id: '1', tieu_de: 'Thông báo lịch nghỉ lễ 30/4',
    noi_dung: 'UBND phường thông báo lịch nghỉ lễ...',
    loai: 'he_thong', da_doc: false,
    created_at: '2026-06-14T08:00:00Z',
  },
  {
    id: '2', tieu_de: 'Nhắc nhở: Hồ sơ tồn đọng',
    noi_dung: 'Hiện còn 5 hồ sơ chờ xử lý quá hạn 3 ngày.',
    loai: 'he_thong', da_doc: false,
    created_at: '2026-06-13T09:00:00Z',
  },
  {
    id: '3', tieu_de: 'Cập nhật quy trình xử lý hồ sơ',
    noi_dung: 'Quy trình xử lý hồ sơ cấp phép xây dựng đã được cập nhật.',
    loai: 'he_thong', da_doc: true,
    created_at: '2026-06-10T10:00:00Z',
  },
];

export default function OfficerThongBaoPage() {
  const toast = useToast();
  const [thongBaos, setThongBaos] = useState(MOCK_THONG_BAO);
  const [showModal, setShowModal] = useState(false);
  const [form, setForm] = useState({ tieu_de: '', noi_dung: '', loai: 'he_thong' as LoaiThongBao });
  const [submitting, setSubmitting] = useState(false);

  const handleCreate = async () => {
    setSubmitting(true);
    try {
      await new Promise((resolve) => setTimeout(resolve, 800));
      const newTB: ThongBao = {
        id: Math.random().toString(),
        ...form,
        da_doc: false,
        created_at: new Date().toISOString(),
      };
      setThongBaos((prev) => [newTB, ...prev]);
      toast.success('Đã gửi thông báo');
      setShowModal(false);
      setForm({ tieu_de: '', noi_dung: '', loai: 'he_thong' });
    } catch {
      toast.error('Gửi thông báo thất bại');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <DashboardLayout>
      <div className="page-header">
        <div>
          <h1 className="page-title">Quản lý thông báo</h1>
          <p className="page-subtitle">Gửi thông báo đến công dân</p>
        </div>
        <button onClick={() => setShowModal(true)} className="btn-primary">
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
          </svg>
          Tạo thông báo
        </button>
      </div>

      <div className="space-y-3">
        {thongBaos.map((tb) => (
          <div key={tb.id} className={`card-hover p-5 ${!tb.da_doc ? 'border-l-4 border-l-govone-500' : ''}`}>
            <div className="flex items-start justify-between gap-4">
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 mb-1">
                  {!tb.da_doc && <span className="w-2 h-2 rounded-full bg-govone-600 flex-shrink-0" />}
                  <h3 className="text-sm font-semibold text-gray-900">{tb.tieu_de}</h3>
                  <span className="px-2 py-0.5 text-xs rounded-full bg-gray-100 text-gray-600">
                    {LOAI_THONG_BAO_LABEL[tb.loai]}
                  </span>
                </div>
                <p className="text-sm text-gray-500 line-clamp-2">{tb.noi_dung}</p>
                <p className="text-xs text-gray-400 mt-1">
                  {new Date(tb.created_at).toLocaleDateString('vi-VN', {
                    hour: '2-digit', minute: '2-digit', day: 'numeric', month: 'numeric',
                  })}
                </p>
              </div>
            </div>
          </div>
        ))}
      </div>

      <Modal isOpen={showModal} onClose={() => setShowModal(false)} title="Tạo thông báo mới">
        <div className="space-y-4">
          <div>
            <label className="form-label">Tiêu đề *</label>
            <input type="text" className="form-input" placeholder="Tiêu đề thông báo"
              value={form.tieu_de}
              onChange={(e) => setForm((prev) => ({ ...prev, tieu_de: e.target.value }))}
            />
          </div>
          <div>
            <label className="form-label">Loại</label>
            <select className="form-select"
              value={form.loai}
              onChange={(e) => setForm((prev) => ({ ...prev, loai: e.target.value as LoaiThongBao }))}
            >
              <option value="he_thong">Hệ thống</option>
              <option value="ho_so">Hồ sơ</option>
              <option value="lich_hen">Lịch hẹn</option>
            </select>
          </div>
          <div>
            <label className="form-label">Nội dung *</label>
            <textarea className="form-textarea" rows={5} placeholder="Nội dung thông báo..."
              value={form.noi_dung}
              onChange={(e) => setForm((prev) => ({ ...prev, noi_dung: e.target.value }))}
            />
          </div>
          <div className="flex justify-end gap-3 pt-2">
            <button onClick={() => setShowModal(false)} className="btn-secondary">Hủy</button>
            <button onClick={handleCreate} className="btn-primary" disabled={submitting || !form.tieu_de || !form.noi_dung}>
              {submitting ? 'Đang gửi...' : 'Gửi thông báo'}
            </button>
          </div>
        </div>
      </Modal>
    </DashboardLayout>
  );
}
