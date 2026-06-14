import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'GovOne — Hệ thống Quản lý Hành chính Công Thông minh',
  description:
    'GovOne là hệ thống quản lý hành chính công tích hợp AI, phục vụ cả người dân và cán bộ.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="vi">
      <body className="min-h-screen bg-gray-50">
        {children}
      </body>
    </html>
  );
}
