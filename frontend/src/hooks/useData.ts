import { useState, useCallback } from 'react';
import type { QueryParams, Pagination } from '@/types';

interface UseListState<T> {
  data: T[];
  loading: boolean;
  error: string | null;
  pagination: Pagination | null;
}

interface UseListReturn<T> extends UseListState<T> {
  fetchData: (params?: QueryParams) => Promise<void>;
  refetch: () => Promise<void>;
  setData: React.Dispatch<React.SetStateAction<T[]>>;
}

export function useList<T>(
  fetchFn: (params?: QueryParams) => Promise<{ data: T[]; pagination?: Pagination }>,
  initialParams?: QueryParams,
): UseListReturn<T> {
  const [state, setState] = useState<UseListState<T>>({
    data: [],
    loading: true,
    error: null,
    pagination: null,
  });
  const [params, setParams] = useState<QueryParams | undefined>(initialParams);

  const fetchData = useCallback(
    async (newParams?: QueryParams) => {
      setState((prev) => ({ ...prev, loading: true, error: null }));
      try {
        const mergedParams = newParams || params;
        const result = await fetchFn(mergedParams);
        setState({
          data: result.data,
          loading: false,
          error: null,
          pagination: result.pagination || null,
        });
      } catch (err: unknown) {
        const message =
          err instanceof Error ? err.message : 'Đã có lỗi xảy ra';
        setState((prev) => ({ ...prev, loading: false, error: message }));
      }
    },
    [fetchFn, params],
  );

  const refetch = useCallback(async () => {
    await fetchData(params);
  }, [fetchData, params]);

  return {
    ...state,
    fetchData,
    refetch,
    setData: (data) => setState((prev) => ({ ...prev, data: data as T[] })),
  };
}

interface UseDetailState<T> {
  data: T | null;
  loading: boolean;
  error: string | null;
}

interface UseDetailReturn<T> extends UseDetailState<T> {
  fetchDetail: (id: string) => Promise<void>;
  refetch: () => Promise<void>;
}

export function useDetail<T>(
  fetchFn: (id: string) => Promise<T>,
): UseDetailReturn<T> {
  const [state, setState] = useState<UseDetailState<T>>({
    data: null,
    loading: true,
    error: null,
  });
  const [currentId, setCurrentId] = useState<string | null>(null);

  const fetchDetail = useCallback(
    async (id: string) => {
      setState((prev) => ({ ...prev, loading: true, error: null }));
      setCurrentId(id);
      try {
        const result = await fetchFn(id);
        setState({ data: result, loading: false, error: null });
      } catch (err: unknown) {
        const message =
          err instanceof Error ? err.message : 'Đã có lỗi xảy ra';
        setState((prev) => ({ ...prev, loading: false, error: message }));
      }
    },
    [fetchFn],
  );

  const refetch = useCallback(async () => {
    if (currentId) {
      await fetchDetail(currentId);
    }
  }, [fetchDetail, currentId]);

  return {
    ...state,
    fetchDetail,
    refetch,
  };
}
