'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import DashboardLayout from '@/components/DashboardLayout';
import FileUpload from '@/components/FileUpload';
import { useToast } from '@/components/Toast';
import { LOAI_THU_TUC_OPTIONS } from '@/types';

const steps = ['Chọn thủ tục', 'Điền thông tin', 'Tải tài liệu', 'Xác nhận'];

export default function NopHoSoPage() {
  const router = useRouter();
  const toast = useToast();
  const [currentStep, setCurrentStep] = useState(0);
  const [submitting, setSubmitting] = useState(false);
  const [form, setForm] = useState({
    loai_thu_tuc: '',
    noi_dung: '',
  });
  const [files, setFiles] = useState<File[]>([]);

  const handleNext = () => {
    if (currentStep === 0 && !form.loai_thu_tuc) {
      toast.warning('Vui lòng chọn loại thủ tục');
      return;
    }
    if (currentStep === 1 && !form.noi_dung.trim()) {
      toast.warning('Vui lòng nhập nội dung');
      return;
    }
    setCurrentStep((prev) => Math.min(prev + 1, steps.length - 1));
  };

  const handleBack = () => {
    setCurrentStep((prev) => Math.max(prev - 1, 0));
  };

  const handleSubmit = async () => {
    setSubmitting(true);
    try {
      // Giả lập gửi API
      await new Promise((resolve) => setTimeout(resolve, 1500));
      toast.success('Nộp hồ sơ thành công!', 'Mã hồ sơ của bạn sẽ được gửi qua email.');
      router.push('/citizen/ho-so');
    } catch {
      toast.error('Nộp hồ sơ thất bại', 'Vui lòng thử lại sau.');
    } finally {
      setSubmitting(false);
    }
  };

  const handleFileUpload = (file: File) => {
    setFiles((prev) => [...prev, file]);
    toast.success('Tải file thành công', file.name);
  };

  const removeFile = (index: number) => {
    setFiles((prev) => prev.filter((_, i) => i !== index));
  };

  return (
    <DashboardLayout>
      <div className="max-w-3xl mx-auto">
        <div className="page-header">
          <div>
            <h1 className="page-title">Nộp hồ sơ hành chính</h1>
            <p className="page-subtitle">
              Điền thông tin và gửi hồ sơ trực tuyến
            </p>
          </div>
        </div>

        {/* Progress steps */}
        <div className="mb-8">
          <div className="flex items-center justify-between">
            {steps.map((label, i) => (
              <div key={i} className="flex items-center flex-1">
                <div className="flex items-center gap-2">
                  <div
                    className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium ${
                      i <= currentStep
                        ? 'bg-govone-600 text-white'
                        : 'bg-gray-100 text-gray-400'
                    }`}
                  >
                    {i < currentStep ? (
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                      </svg>
                    ) : (
                      i + 1
                    )}
                  </div>
                  <span
                    className={`text-sm font-medium hidden sm:inline ${
                      i <= currentStep ? 'text-govone-600' : 'text-gray-400'
                    }`}
                  >
                    {label}
                  </span>
                </div>
                {i < steps.length - 1 && (
                  <div
                    className={`flex-1 h-0.5 mx-4 ${
                      i < currentStep ? 'bg-govone-600' : 'bg-gray-200'
                    }`}
                  />
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Step content */}
        <div className="card p-8 animate-fade-in">
          {/* Step 1: Chọn thủ tục */}
          {currentStep === 0 && (
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-4">
                Chọn loại thủ tục hành chính
              </h3>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                {LOAI_THU_TUC_OPTIONS.map((opt) => (
                  <button
                    key={opt.value}
                    onClick={() => setForm((prev) => ({ ...prev, loai_thu_tuc: opt.value }))}
                    className={`p-4 rounded-xl border text-left transition-all ${
                      form.loai_thu_tuc === opt.value
                        ? 'border-govone-500 bg-govone-50 ring-1 ring-govone-500'
                        : 'border-gray-200 hover:border-gray-300 bg-white'
                    }`}
                  >
                    <p className="text-sm font-medium text-gray-900">{opt.label}</p>
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Step 2: Điền thông tin */}
          {currentStep === 1 && (
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-4">
                Điền thông tin hồ sơ
              </h3>
              <div className="space-y-4">
                <div>
                  <label className="form-label">Loại thủ tục</label>
                  <p className="text-sm text-gray-700 font-medium">
                    {LOAI_THU_TUC_OPTIONS.find((o) => o.value === form.loai_thu_tuc)?.label}
                  </p>
                </div>
                <div>
                  <label className="form-label">Nội dung chi tiết *</label>
                  <textarea
                    className="form-textarea"
                    rows={6}
                    placeholder="Mô tả chi tiết nội dung bạn cần giải quyết..."
                    value={form.noi_dung}
                    onChange={(e) => setForm((prev) => ({ ...prev, noi_dung: e.target.value }))}
                  />
                  <p className="text-xs text-gray-400 mt-1">
                    {form.noi_dung.length}/5000 ký tự
                  </p>
                </div>
              </div>
            </div>
          )}

          {/* Step 3: Tải tài liệu */}
          {currentStep === 2 && (
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-4">
                Tải lên tài liệu đính kèm
              </h3>
              <p className="text-sm text-gray-500 mb-4">
                Tải lên các giấy tờ cần thiết (CCCD, sổ hộ khẩu, giấy tờ liên quan...)
              </p>
              <FileUpload
                onUpload={handleFileUpload}
                accept="image/*,.pdf"
                maxSizeMB={10}
                label="Kéo thả file hoặc click để chọn"
              />
              {files.length > 0 && (
                <div className="mt-4 space-y-2">
                  <p className="text-sm font-medium text-gray-700">
                    Đã chọn {files.length} file(s):
                  </p>
                  {files.map((file, i) => (
                    <div
                      key={i}
                      className="flex items-center justify-between bg-gray-50 rounded-lg px-4 py-2"
                    >
                      <div className="flex items-center gap-2">
                        <svg className="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
                        </svg>
                        <span className="text-sm text-gray-700">{file.name}</span>
                        <span className="text-xs text-gray-400">
                          ({(file.size / 1024 / 1024).toFixed(2)}MB)
                        </span>
                      </div>
                      <button
                        onClick={() => removeFile(i)}
                        className="text-red-500 hover:text-red-700"
                      >
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                        </svg>
                      </button>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* Step 4: Xác nhận */}
          {currentStep === 3 && (
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-4">
                Xác nhận thông tin hồ sơ
              </h3>
              <div className="bg-gray-50 rounded-xl p-6 space-y-3">
                <div>
                  <p className="text-xs text-gray-500 uppercase">Loại thủ tục</p>
                  <p className="text-sm font-medium text-gray-900">
                    {LOAI_THU_TUC_OPTIONS.find((o) => o.value === form.loai_thu_tuc)?.label}
                  </p>
                </div>
                <div>
                  <p className="text-xs text-gray-500 uppercase">Nội dung</p>
                  <p className="text-sm text-gray-700">{form.noi_dung}</p>
                </div>
                <div>
                  <p className="text-xs text-gray-500 uppercase">Tài liệu đính kèm</p>
                  <p className="text-sm font-medium text-gray-900">
                    {files.length} file(s)
                  </p>
                </div>
              </div>
              <div className="bg-yellow-50 border border-yellow-200 rounded-xl p-4 mt-4">
                <div className="flex gap-2">
                  <svg className="w-5 h-5 text-yellow-600 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                  </svg>
                  <div>
                    <p className="text-sm font-medium text-yellow-800">
                      Vui lòng kiểm tra kỹ thông tin trước khi gửi
                    </p>
                    <p className="text-xs text-yellow-700 mt-0.5">
                      Sau khi gửi, bạn sẽ không thể chỉnh sửa hồ sơ cho đến khi cán bộ xử lý.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Navigation buttons */}
          <div className="flex justify-between mt-8 pt-6 border-t">
            {currentStep > 0 ? (
              <button onClick={handleBack} className="btn-secondary">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                </svg>
                Quay lại
              </button>
            ) : (
              <div />
            )}
            {currentStep < steps.length - 1 ? (
              <button onClick={handleNext} className="btn-primary">
                Tiếp theo
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
              </button>
            ) : (
              <button onClick={handleSubmit} className="btn-primary" disabled={submitting}>
                {submitting ? (
                  <span className="flex items-center gap-2">
                    <div className="h-4 w-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                    Đang gửi...
                  </span>
                ) : (
                  <>
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                    Xác nhận gửi
                  </>
                )}
              </button>
            )}
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}
