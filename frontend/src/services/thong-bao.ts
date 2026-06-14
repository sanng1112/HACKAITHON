import api, { getList, create, update } from './api';
import type { ThongBao, CreateThongBaoRequest, QueryParams } from '@/types';

export const thongBaoService = {
  async getMyThongBao(params?: QueryParams) {
    return getList<ThongBao>('/thong-bao', params as Record<string, unknown>);
  },

  async getAllThongBao(params?: QueryParams) {
    return getList<ThongBao>('/thong-bao', params as Record<string, unknown>);
  },

  async createThongBao(data: CreateThongBaoRequest): Promise<ThongBao> {
    return create<ThongBao>('/thong-bao', data);
  },

  async markAsRead(id: string): Promise<void> {
    await update(`/thong-bao/${id}/da-doc`, {});
  },

  async markAllAsRead(): Promise<void> {
    await api.post('/thong-bao/mark-all-read');
  },

  async getUnreadCount(): Promise<number> {
    try {
      const { data } = await getList<ThongBao>('/thong-bao', {
        da_doc: false,
        limit: 1,
      } as Record<string, unknown>);
      const total = 0; // fallback
      return total;
    } catch {
      return 0;
    }
  },
};
