'use client';

import DashboardLayout from '@/components/DashboardLayout';
import { useAuth } from '@/hooks/useAuth';

export default function ProfilePage() {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <DashboardLayout>
        <div className="flex justify-center py-12">
          <div className="h-8 w-8 border-2 border-govone-200 border-t-govone-600 rounded-full animate-spin" />
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <div className="max-w-2xl mx-auto">
        <div className="page-header">
          <div>
            <h1 className="page-title">Thông tin cá nhân</h1>
            <p className="page-subtitle">Quản lý thông tin tài khoản của bạn</p>
          </div>
        </div>

        {/* Avatar & Name */}
        <div className="card p-8 mb-6 text-center">
          <div className="w-20 h-20 rounded-full bg-govone-100 flex items-center justify-center text-govone-600 text-2xl font-bold mx-auto mb-4">
            {user?.ho_ten?.charAt(0) || 'U'}
          </div>
          <h2 className="text-xl font-bold text-gray-900">{user?.ho_ten}</h2>
          <p className="text-sm text-gray-500">{user?.email}</p>
          <span className="inline-flex mt-2 px-3 py-1 rounded-full text-xs font-medium bg-govone-100 text-govone-700">
            {user?.role === 'citizen' ? 'Công dân' : user?.role === 'officer' ? 'Cán bộ' : 'Quản trị viên'}
          </span>
        </div>

        {/* Chi tiết */}
        <div className="card divide-y divide-gray-100">
          <div className="px-6 py-4">
            <p className="text-xs text-gray-500 uppercase">Họ và tên</p>
            <p className="text-sm font-medium text-gray-900 mt-1">{user?.ho_ten}</p>
          </div>
          <div className="px-6 py-4">
            <p className="text-xs text-gray-500 uppercase">Email</p>
            <p className="text-sm font-medium text-gray-900 mt-1">{user?.email}</p>
          </div>
          <div className="px-6 py-4">
            <p className="text-xs text-gray-500 uppercase">Số CCCD</p>
            <p className="text-sm font-medium text-gray-900 mt-1">{user?.so_cccd || 'Chưa cập nhật'}</p>
          </div>
          <div className="px-6 py-4">
            <p className="text-xs text-gray-500 uppercase">Số điện thoại</p>
            <p className="text-sm font-medium text-gray-900 mt-1">{user?.so_dien_thoai || 'Chưa cập nhật'}</p>
          </div>
          <div className="px-6 py-4">
            <p className="text-xs text-gray-500 uppercase">Địa chỉ</p>
            <p className="text-sm font-medium text-gray-900 mt-1">{user?.dia_chi || 'Chưa cập nhật'}</p>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}
