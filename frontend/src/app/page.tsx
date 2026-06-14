'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { AuthProvider, useAuth } from '@/hooks/useAuth';
import { ToastProvider } from '@/components/Toast';
import LoadingSpinner from '@/components/LoadingSpinner';

function HomeContent() {
  const router = useRouter();
  const { user, loading, isAuthenticated } = useAuth();

  useEffect(() => {
    if (loading) return;
    if (!isAuthenticated) {
      router.push('/login');
    } else if (user?.role === 'officer' || user?.role === 'admin') {
      router.push('/officer');
    } else {
      router.push('/citizen');
    }
  }, [loading, isAuthenticated, user, router]);

  if (loading) {
    return <LoadingSpinner fullPage text="Đang tải..." />;
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-govone-50 to-white">
      <LoadingSpinner fullPage text="Đang chuyển hướng..." />
    </div>
  );
}

export default function HomePage() {
  return (
    <ToastProvider>
      <AuthProvider>
        <HomeContent />
      </AuthProvider>
    </ToastProvider>
  );
}
