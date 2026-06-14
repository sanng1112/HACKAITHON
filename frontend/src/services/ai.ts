import api, { getOne } from './api';
import type {
  OCRResult,
  STTResult,
  NLPResult,
  AutoFillResult,
  AIHealth,
} from '@/types';

export const aiService = {
  async ocrImage(file: File, aggressive = false): Promise<OCRResult> {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('aggressive', String(aggressive));
    const res = await api.post<{ success: boolean; data: OCRResult }>(
      '/ai/ocr',
      formData,
      { headers: { 'Content-Type': 'multipart/form-data' } },
    );
    return res.data.data;
  },

  async sttTranscribe(file: File): Promise<STTResult> {
    const formData = new FormData();
    formData.append('file', file);
    const res = await api.post<{ success: boolean; data: STTResult }>(
      '/ai/stt',
      formData,
      { headers: { 'Content-Type': 'multipart/form-data' } },
    );
    return res.data.data;
  },

  async nlpAnalyze(text: string): Promise<NLPResult> {
    const res = await api.post<{ success: boolean; data: NLPResult }>('/ai/nlp/analyze', {
      text,
    });
    return res.data.data;
  },

  async nlpClassify(text: string): Promise<{ procedure_class: string; procedure_score: number }> {
    const res = await api.post<{ success: boolean; data: { procedure_class: string; procedure_score: number } }>(
      '/ai/nlp/classify',
      { text },
    );
    return res.data.data;
  },

  async autoFill(file: File, targetForm?: string): Promise<AutoFillResult> {
    const formData = new FormData();
    formData.append('file', file);
    if (targetForm) formData.append('target_form', targetForm);
    const res = await api.post<{ success: boolean; data: AutoFillResult }>(
      '/ai/auto-fill',
      formData,
      { headers: { 'Content-Type': 'multipart/form-data' } },
    );
    return res.data.data;
  },

  async getAIHealth(): Promise<AIHealth> {
    return getOne<AIHealth>('/ai/health');
  },

  async ocrAsync(file: File): Promise<{ task_id: string; poll_url: string }> {
    const formData = new FormData();
    formData.append('file', file);
    const res = await api.post<{ success: boolean; data: { task_id: string; poll_url: string } }>(
      '/ai/ocr/async',
      formData,
      { headers: { 'Content-Type': 'multipart/form-data' } },
    );
    return res.data.data;
  },

  async sttFormFill(file: File, formFields: string[]): Promise<{ text: string; mapped_fields: Record<string, string | null> }> {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('form_fields', formFields.join(','));
    const res = await api.post<{ success: boolean; data: { text: string; mapped_fields: Record<string, string | null> } }>(
      '/ai/stt/form-fill',
      formData,
      { headers: { 'Content-Type': 'multipart/form-data' } },
    );
    return res.data.data;
  },
};
