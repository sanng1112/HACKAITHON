import api, { create, getOne } from './api';
import type { LoginRequest, LoginResponse, RegisterRequest, User } from '@/types';

export const authService = {
  async login(data: LoginRequest): Promise<LoginResponse> {
    const res = await api.post<{ success: boolean; data: LoginResponse }>(
      '/auth/login',
      data,
    );
    const loginData = res.data.data;

    // Lưu token & user vào localStorage
    localStorage.setItem('access_token', loginData.access_token);
    localStorage.setItem('refresh_token', loginData.refresh_token);
    localStorage.setItem('user', JSON.stringify(loginData.user));

    return loginData;
  },

  async register(data: RegisterRequest): Promise<User> {
    const result = await create<User>('/auth/register', data);
    return result;
  },

  async getMe(): Promise<User> {
    const user = await getOne<User>('/auth/me');
    localStorage.setItem('user', JSON.stringify(user));
    return user;
  },

  async refreshToken(): Promise<{ access_token: string; refresh_token: string }> {
    const refreshToken = localStorage.getItem('refresh_token');
    const res = await api.post<{
      success: boolean;
      data: { access_token: string; refresh_token: string; expires_in: number };
    }>(
      '/auth/refresh',
      null,
      { headers: { Authorization: `Bearer ${refreshToken}` } },
    );
    const data = res.data.data;
    localStorage.setItem('access_token', data.access_token);
    localStorage.setItem('refresh_token', data.refresh_token);
    return data;
  },

  async changePassword(currentPassword: string, newPassword: string): Promise<void> {
    await api.put('/auth/change-password', {
      current_password: currentPassword,
      new_password: newPassword,
    });
  },

  logout(): void {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
    if (typeof window !== 'undefined') {
      window.location.href = '/login';
    }
  },

  getUserFromStorage(): User | null {
    if (typeof window === 'undefined') return null;
    const stored = localStorage.getItem('user');
    return stored ? JSON.parse(stored) : null;
  },

  isAuthenticated(): boolean {
    if (typeof window === 'undefined') return false;
    return !!localStorage.getItem('access_token');
  },
};
