'use client';

import type { TrangThaiHoSo, TrangThaiLichHen } from '@/types';
import { TRANG_THAI_HO_SO_LABEL, TRANG_THAI_LICH_HEN_LABEL } from '@/types';

interface StatusBadgeProps {
  status: TrangThaiHoSo | TrangThaiLichHen;
  type?: 'ho-so' | 'lich-hen';
  size?: 'sm' | 'md';
}

const statusClassMap: Record<string, string> = {
  CHO_TIEP_NHAN: 'badge-cho-tiep-nhan',
  CHO_XU_LY: 'badge-cho-xu-ly',
  DANG_XU_LY: 'badge-dang-xu-ly',
  DA_XU_LY: 'badge-da-xu-ly',
  TU_CHOI: 'badge-tu-choi',
  CHO_BO_SUNG: 'badge-cho-bo-sung',
  DA_BO_SUNG: 'badge-da-bo-sung',
  CHO_XAC_NHAN: 'badge-cho-xu-ly',
  DA_XAC_NHAN: 'badge-dang-xu-ly',
  DA_HUY: 'badge-tu-choi',
  HOAN_THANH: 'badge-da-xu-ly',
};

export default function StatusBadge({
  status,
  type = 'ho-so',
  size = 'sm',
}: StatusBadgeProps) {
  const label =
    type === 'ho-so'
      ? TRANG_THAI_HO_SO_LABEL[status as TrangThaiHoSo] || status
      : TRANG_THAI_LICH_HEN_LABEL[status as TrangThaiLichHen] || status;

  const sizeClass = size === 'sm' ? 'px-2 py-0.5 text-xs' : 'px-3 py-1 text-sm';

  return (
    <span
      className={`inline-flex items-center font-medium rounded-full ${statusClassMap[status] || 'badge-cho-tiep-nhan'} ${sizeClass}`}
    >
      {label}
    </span>
  );
}
