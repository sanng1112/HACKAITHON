import api, { getList, getOne, create } from './api';
import type { HoSo, CreateHoSoRequest, HoSoTaiLieu, QueryParams } from '@/types';

export const hoSoService = {
  async getMyHoSo(params?: QueryParams) {
    return getList<HoSo>('/ho-so', params as Record<string, unknown>);
  },

  async getAllHoSo(params?: QueryParams) {
    return getList<HoSo>('/ho-so', params as Record<string, unknown>);
  },

  async getHoSoById(id: string): Promise<HoSo> {
    return getOne<HoSo>(`/ho-so/${id}`);
  },

  async createHoSo(data: CreateHoSoRequest): Promise<HoSo> {
    return create<HoSo>('/ho-so', data);
  },

  async updateHoSo(id: string, data: Partial<CreateHoSoRequest>): Promise<HoSo> {
    const res = await api.put<{ success: boolean; data: HoSo }>(`/ho-so/${id}`, data);
    return res.data.data;
  },

  async uploadTaiLieu(hoSoId: string, file: File): Promise<HoSoTaiLieu> {
    const formData = new FormData();
    formData.append('file', file);
    const res = await api.post<{ success: boolean; data: HoSoTaiLieu }>(
      `/ho-so/${hoSoId}/upload`,
      formData,
      { headers: { 'Content-Type': 'multipart/form-data' } },
    );
    return res.data.data;
  },

  async submitHoSo(id: string): Promise<HoSo> {
    const res = await api.post<{ success: boolean; data: HoSo }>(`/ho-so/${id}/submit`);
    return res.data.data;
  },

  // Officer actions
  async tiepNhan(id: string): Promise<HoSo> {
    const res = await api.put<{ success: boolean; data: HoSo }>(`/ho-so/${id}/tiep-nhan`);
    return res.data.data;
  },

  async pheDuyet(id: string, ghi_chu?: string): Promise<HoSo> {
    const res = await api.put<{ success: boolean; data: HoSo }>(`/ho-so/${id}/phe-duyet`, {
      ghi_chu,
    });
    return res.data.data;
  },

  async tuChoi(id: string, ly_do: string): Promise<HoSo> {
    const res = await api.put<{ success: boolean; data: HoSo }>(`/ho-so/${id}/tu-choi`, {
      ly_do,
    });
    return res.data.data;
  },

  async yeuCauBoSung(id: string, yeu_cau: string): Promise<HoSo> {
    const res = await api.put<{ success: boolean; data: HoSo }>(
      `/ho-so/${id}/yeu-cau-bo-sung`,
      { yeu_cau },
    );
    return res.data.data;
  },
};
