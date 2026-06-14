'use client';

import { useAuth } from '@/hooks/useAuth';
import { CardSkeleton } from '@/components/LoadingSpinner';
import Link from 'next/link';

const statsCards = [
  {
    label: 'Hồ sơ đang xử lý',
    value: '3',
    icon: 'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z',
    color: 'text-blue-600 bg-blue-100',
    href: '/citizen/ho-so',
  },
  {
    label: 'Lịch hẹn sắp tới',
    value: '1',
    icon: 'M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z',
    color: 'text-green-600 bg-green-100',
    href: '/citizen/lich-hen',
  },
  {
    label: 'Thông báo chưa đọc',
    value: '2',
    icon: 'M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9',
    color: 'text-yellow-600 bg-yellow-100',
    href: '/citizen/thong-bao',
  },
];

export default function CitizenDashboard() {
  const { user, loading } = useAuth();

  if (loading) {
    return <CardSkeleton count={3} />;
  }

  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title">
            Xin chào, {user?.ho_ten || 'Quý công dân'}
          </h1>
          <p className="page-subtitle">
            Chào mừng bạn đến với GovOne — Hệ thống hành chính công thông minh
          </p>
        </div>
        <Link href="/citizen/nop-ho-so" className="btn-primary">
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
          </svg>
          Nộp hồ sơ mới
        </Link>
      </div>

      {/* Stats grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
        {statsCards.map((card) => (
          <Link key={card.label} href={card.href} className="card-hover p-6 block">
            <div className="flex items-center justify-between mb-4">
              <div className={`w-10 h-10 rounded-lg ${card.color} flex items-center justify-center`}>
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d={card.icon} />
                </svg>
              </div>
            </div>
            <p className="text-2xl font-bold text-gray-900 mb-1">{card.value}</p>
            <p className="text-sm text-gray-500">{card.label}</p>
          </Link>
        ))}
      </div>

      {/* Quick actions */}
      <h2 className="text-lg font-semibold text-gray-900 mb-4">Tiện ích nhanh</h2>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <QuickActionCard
          title="Tra cứu hồ sơ"
          description="Xem trạng thái hồ sơ của bạn"
          href="/citizen/ho-so"
          icon="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
        />
        <QuickActionCard
          title="Đặt lịch hẹn"
          description="Đặt lịch làm việc với cán bộ"
          href="/citizen/lich-hen"
          icon="M12 6v6m0 0v6m0-6h6m-6 0H6"
        />
        <QuickActionCard
          title="Nộp hồ sơ"
          description="Nộp hồ sơ hành chính trực tuyến"
          href="/citizen/nop-ho-so"
          icon="M12 4v16m8-8H4"
        />
        <QuickActionCard
          title="Hỗ trợ AI"
          description="Trợ lý ảo thông minh"
          href="/citizen/ai-assistant"
          icon="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"
        />
      </div>

      {/* Recent activity */}
      <div className="card mt-8">
        <div className="px-6 py-4 border-b border-gray-100">
          <h3 className="font-semibold text-gray-900">Hoạt động gần đây</h3>
        </div>
        <div className="p-6">
          <div className="flex items-center justify-center py-8 text-gray-400">
            <div className="text-center">
              <svg className="w-12 h-12 mx-auto mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <p className="text-sm">Chưa có hoạt động nào</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function QuickActionCard({
  title,
  description,
  href,
  icon,
}: {
  title: string;
  description: string;
  href: string;
  icon: string;
}) {
  return (
    <Link href={href} className="card-hover p-5 block">
      <div className="w-10 h-10 rounded-lg bg-govone-100 text-govone-600 flex items-center justify-center mb-3">
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d={icon} />
        </svg>
      </div>
      <h3 className="font-medium text-gray-900 text-sm mb-1">{title}</h3>
      <p className="text-xs text-gray-500">{description}</p>
    </Link>
  );
}
