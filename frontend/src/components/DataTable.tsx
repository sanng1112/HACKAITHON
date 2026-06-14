'use client';

import { TableSkeleton } from './LoadingSpinner';
import EmptyState from './EmptyState';

export interface Column<T> {
  key: string;
  header: string;
  render?: (item: T) => React.ReactNode;
  sortable?: boolean;
  className?: string;
  hideOnMobile?: boolean;
}

interface DataTableProps<T> {
  columns: Column<T>[];
  data: T[];
  loading?: boolean;
  error?: string | null;
  emptyTitle?: string;
  emptyDescription?: string;
  onRowClick?: (item: T) => void;
  keyExtractor: (item: T) => string;
  onRefresh?: () => void;
}

export default function DataTable<T>({
  columns,
  data,
  loading = false,
  error = null,
  emptyTitle = 'Không có dữ liệu',
  emptyDescription,
  onRowClick,
  keyExtractor,
  onRefresh,
}: DataTableProps<T>) {
  if (loading) {
    return (
      <div className="card p-6">
        <TableSkeleton rows={5} cols={columns.length} />
      </div>
    );
  }

  if (error) {
    return (
      <div className="card p-6 text-center">
        <div className="text-red-500 mb-2">
          <svg className="w-12 h-12 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
        </div>
        <p className="text-sm text-gray-600 mb-3">{error}</p>
        {onRefresh && (
          <button onClick={onRefresh} className="btn-secondary btn-sm">
            Thử lại
          </button>
        )}
      </div>
    );
  }

  if (data.length === 0) {
    return (
      <div className="card p-6">
        <EmptyState
          title={emptyTitle}
          description={emptyDescription}
        />
      </div>
    );
  }

  return (
    <div className="table-container">
      <table className="table-base">
        <thead>
          <tr className="table-header">
            {columns.map((col) => (
              <th
                key={col.key}
                className={`${col.hideOnMobile ? 'hidden sm:table-cell' : ''} ${col.className || ''}`}
              >
                {col.header}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="table-body">
          {data.map((item) => (
            <tr
              key={keyExtractor(item)}
              className={`${onRowClick ? 'table-row' : ''}`}
              onClick={() => onRowClick?.(item)}
            >
              {columns.map((col) => (
                <td
                  key={col.key}
                  className={`${col.hideOnMobile ? 'hidden sm:table-cell' : ''} ${col.className || ''}`}
                >
                  {col.render ? col.render(item) : (item as Record<string, unknown>)[col.key] as React.ReactNode}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
