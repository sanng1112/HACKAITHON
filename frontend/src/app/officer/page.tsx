'use client';

import { useAuth } from '@/hooks/useAuth';
import DashboardLayout from '@/components/DashboardLayout';
import { CardSkeleton } from '@/components/LoadingSpinner';

const stats = [
  {
    label: 'Hồ sơ chờ xử lý',
    value: '12',
    change: '+3 hôm nay',
    color: 'text-yellow-600 bg-yellow-100',
  },
  {
    label: 'Đang xử lý',
    value: '8',
    change: '5 hồ sơ của bạn',
    color: 'text-blue-600 bg-blue-100',
  },
  {
    label: 'Đã xử lý hôm nay',
    value: '6',
    change: 'Đạt 75% chỉ tiêu',
    color: 'text-green-600 bg-green-100',
  },
  {
    label: 'Lịch hẹn hôm nay',
    value: '4',
    change: '2 lịch chưa xác nhận',
    color: 'text-purple-600 bg-purple-100',
  },
];

export default function OfficerDashboard() {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <DashboardLayout>
        <CardSkeleton count={4} />
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <div className="page-header">
        <div>
          <h1 className="page-title">
            Xin chào, {user?.ho_ten || 'Cán bộ'}
          </h1>
          <p className="page-subtitle">Bảng điều khiển quản lý hồ sơ hành chính</p>
        </div>
      </div>

      {/* Stats grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        {stats.map((s) => (
          <div key={s.label} className="card p-6">
            <div className="flex items-center justify-between mb-4">
              <div className={`w-10 h-10 rounded-lg ${s.color} flex items-center justify-center`}>
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
            </div>
            <p className="text-2xl font-bold text-gray-900 mb-1">{s.value}</p>
            <p className="text-sm text-gray-500">{s.label}</p>
            <p className="text-xs text-gray-400 mt-1">{s.change}</p>
          </div>
        ))}
      </div>

      {/* Phân bố trạng thái */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card p-6">
          <h3 className="font-semibold text-gray-900 mb-4">Trạng thái hồ sơ</h3>
          <div className="space-y-3">
            {[
              { label: 'Chờ tiếp nhận', value: 5, color: 'bg-gray-400' },
              { label: 'Chờ xử lý', value: 7, color: 'bg-yellow-400' },
              { label: 'Đang xử lý', value: 8, color: 'bg-blue-500' },
              { label: 'Đã xử lý (tháng này)', value: 45, color: 'bg-green-500' },
              { label: 'Từ chối', value: 3, color: 'bg-red-400' },
              { label: 'Chờ bổ sung', value: 4, color: 'bg-orange-400' },
            ].map((item) => {
              const total = 72;
              const pct = (item.value / total) * 100;
              return (
                <div key={item.label}>
                  <div className="flex justify-between text-sm mb-1">
                    <span className="text-gray-600">{item.label}</span>
                    <span className="font-medium text-gray-900">{item.value}</span>
                  </div>
                  <div className="w-full bg-gray-100 rounded-full h-2">
                    <div
                      className={`h-2 rounded-full ${item.color} transition-all`}
                      style={{ width: `${pct}%` }}
                    />
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Recent activity */}
        <div className="card p-6">
          <h3 className="font-semibold text-gray-900 mb-4">Hoạt động gần đây</h3>
          <div className="space-y-4">
            {[
              { action: 'Phê duyệt hồ sơ', hs: 'HS-2026-0012', time: '5 phút trước' },
              { action: 'Yêu cầu bổ sung', hs: 'HS-2026-0009', time: '30 phút trước' },
              { action: 'Tiếp nhận hồ sơ mới', hs: 'HS-2026-0015', time: '1 giờ trước' },
              { action: 'Xác nhận lịch hẹn', hs: 'Công dân Nguyễn Văn A', time: '2 giờ trước' },
            ].map((act, i) => (
              <div key={i} className="flex items-start gap-3">
                <div className="w-2 h-2 rounded-full bg-govone-400 mt-2 flex-shrink-0" />
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-gray-900">{act.action}</p>
                  <p className="text-xs text-gray-500">{act.hs}</p>
                  <p className="text-xs text-gray-400">{act.time}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}
