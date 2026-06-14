'use client';

import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import type { User, LoginRequest, RegisterRequest } from '@/types';
import { authService } from '@/services/auth';

interface AuthContextType {
  user: User | null;
  loading: boolean;
  isAuthenticated: boolean;
  login: (data: LoginRequest) => Promise<void>;
  register: (data: RegisterRequest) => Promise<void>;
  logout: () => void;
  refreshUser: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  // Khôi phục user từ localStorage khi mount
  useEffect(() => {
    const stored = authService.getUserFromStorage();
    if (stored && authService.isAuthenticated()) {
      setUser(stored);
      // Refresh user info in background
      authService.getMe().then(setUser).catch(() => {
        // Nếu lỗi, xoá và redirect về login
        authService.logout();
      });
    }
    setLoading(false);
  }, []);

  const login = useCallback(async (data: LoginRequest) => {
    const result = await authService.login(data);
    setUser(result.user);
  }, []);

  const register = useCallback(async (data: RegisterRequest) => {
    await authService.register(data);
    // Sau khi đăng ký, redirect đến login
  }, []);

  const logout = useCallback(() => {
    setUser(null);
    authService.logout();
  }, []);

  const refreshUser = useCallback(async () => {
    try {
      const freshUser = await authService.getMe();
      setUser(freshUser);
    } catch {
      setUser(null);
    }
  }, []);

  return (
    <AuthContext.Provider
      value={{
        user,
        loading,
        isAuthenticated: !!user,
        login,
        register,
        logout,
        refreshUser,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth(): AuthContextType {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
