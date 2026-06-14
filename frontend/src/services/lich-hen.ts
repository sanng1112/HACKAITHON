import api, { getList, getOne, create, remove } from './api';
import type { LichHen, CreateLichHenRequest, QueryParams } from '@/types';

export const lichHenService = {
  async getMyLichHen(params?: QueryParams) {
    return getList<LichHen>('/lich-hen', params as Record<string, unknown>);
  },

  async getAllLichHen(params?: QueryParams) {
    return getList<LichHen>('/lich-hen', params as Record<string, unknown>);
  },

  async getLichHenById(id: string): Promise<LichHen> {
    return getOne<LichHen>(`/lich-hen/${id}`);
  },

  async createLichHen(data: CreateLichHenRequest): Promise<LichHen> {
    return create<LichHen>('/lich-hen', data);
  },

  async updateLichHen(id: string, data: Partial<LichHen>): Promise<LichHen> {
    const res = await api.put<{ success: boolean; data: LichHen }>(`/lich-hen/${id}`, data);
    return res.data.data;
  },

  async huyLichHen(id: string): Promise<void> {
    await remove(`/lich-hen/${id}`);
  },

  async xacNhan(id: string, can_bo_id: string): Promise<LichHen> {
    return this.updateLichHen(id, { trang_thai: 'DA_XAC_NHAN', can_bo_id } as Partial<LichHen>);
  },

  async hoanThanh(id: string): Promise<LichHen> {
    return this.updateLichHen(id, { trang_thai: 'HOAN_THANH' } as Partial<LichHen>);
  },
};
