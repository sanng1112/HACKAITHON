# GovOne MVP — Implementation Plan (4 Rounds)

> **Mục tiêu:** Xây dựng MVP GovOne thực tế, có thể demo — không viễn tưởng. ReactJS + NodeJS + FastAPI + VNPT APIs.

**Kiến trúc tổng thể:**

```
┌──────────────────────────────────────┐
│  ROUND 1: REACTJS (Frontend)          │
│  Kiosk UI │ Scan UI │ Dashboard UI   │
└──────────────┬───────────────────────┘
               │ HTTP / WebSocket
┌──────────────▼───────────────────────┐
│  ROUND 2: NODEJS (API Gateway)        │
│  REST API │ WebSocket │ Auth         │
└──────────────┬───────────────────────┘
               │ HTTP
┌──────────────▼───────────────────────┐
│  ROUND 3: FASTAPI (AI Processing)     │
│  OCR │ VNPT APIs │ Rules Engine      │
└──────────────┬───────────────────────┘
               │ SQL / S3
┌──────────────▼───────────────────────┐
│  ROUND 4: INTEGRATION & DEPLOYMENT    │
│  PostgreSQL │ Docker │ CI/CD │ Tests │
└──────────────────────────────────────┘
```

## 📁 Cấu trúc thư mục

```
hackaithon-de-tai-6-govone/
├── frontend/                  ← R1: ReactJS
│   ├── src/components/
│   │   ├── kiosk/             ← Kiosk Voice-first
│   │   ├── scan/              ← Scan OCR
│   │   └── dashboard/         ← Dashboard
│   ├── hooks/                 ← useVoice hook
│   ├── services/              ← API calls
│   └── types/
├── services/                  ← R2: NodeJS
│   ├── gateway/               ← API Gateway
│   └── voice-stream/          ← WebSocket
├── ai-core/                   ← R3: FastAPI
│   ├── app/routers/           ← voice, ocr, dashboard
│   ├── app/services/          ← smartvoice, ocr, ekyc
│   └── app/models/
├── infra/                     ← R4: Integration
│   ├── docker-compose.yml
│   ├── postgres/init.sql
│   ├── nginx/
│   └── tests/
└── .github/workflows/ci.yml
```

---

# ROUND 1: FRONTEND — REACTJS

**Mục tiêu:** 3 giao diện chính: Kiosk Voice-first, Scan OCR, Dashboard.

## Task 1.1: Khởi tạo React + Vite + TypeScript

**Files:**
- Create: `frontend/package.json`, `vite.config.ts`, `tsconfig.json`
- Create: `frontend/src/main.tsx`, `App.tsx`, `types/index.ts`

- [ ] **Step 1: Init project**

```bash
cd "/run/media/sanng/New Volume/HACKAITHON/hackaithon-de-tai-6-govone"
mkdir -p frontend/src/components/kiosk frontend/src/components/scan frontend/src/components/dashboard frontend/src/hooks frontend/src/services frontend/src/types frontend/public
```

```json
// frontend/package.json
{
  "name": "govone-frontend", "private": true, "version": "0.1.0", "type": "module",
  "scripts": { "dev": "vite", "build": "tsc && vite build", "test": "vitest" },
  "dependencies": {
    "react": "^18.3.1", "react-dom": "^18.3.1", "react-router-dom": "^6.26.0",
    "axios": "^1.7.3", "recharts": "^2.12.7"
  },
  "devDependencies": {
    "@types/react": "^18.3.3", "@types/react-dom": "^18.3.0",
    "@vitejs/plugin-react": "^4.3.1", "typescript": "^5.5.3",
    "vite": "^5.4.0", "vitest": "^2.0.5"
  }
}
```

- [ ] **Step 2: Config files**

```typescript
// frontend/vite.config.ts
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
export default defineConfig({
  plugins: [react()],
  server: { port: 3000, proxy: { '/api': 'http://localhost:4000', '/ws': { target: 'ws://localhost:4001', ws: true } } },
})
```

```json
// frontend/tsconfig.json
{ "compilerOptions": { "target": "ES2020", "useDefineForClassFields": true, "lib": ["ES2020", "DOM", "DOM.Iterable"], "module": "ESNext", "skipLibCheck": true, "moduleResolution": "bundler", "allowImportingTsExtensions": true, "resolveJsonModule": true, "isolatedModules": true, "noEmit": true, "jsx": "react-jsx", "strict": true }, "include": ["src"] }
```

- [ ] **Step 3: Types + App + Main**

```typescript
// frontend/src/types/index.ts
export interface DocumentInfo {
  id: string; holderName: string; idNumber: string; dob: string;
  docType: 'CCCD' | 'SoHoKhau' | 'GiayKhaiSinh' | 'GiayXacNhan';
  status: 'pending' | 'processing' | 'verified' | 'failed';
  confidence: number;
  fieldMatches: { field: string; extracted: string; database: string; match: boolean }[];
  scanUrl?: string; createdAt: string;
}
export interface Transaction {
  id: string; citizenName: string; procedure: string; date: string;
  status: 'completed' | 'warning' | 'error'; result: string;
}
export interface KpiData {
  totalTransactions: number; processing: number; completed: number;
  warnings: number; satisfaction: number;
}
export const API_BASE = '/api/v1';
```

```tsx
// frontend/src/main.tsx
import React from 'react'; import ReactDOM from 'react-dom/client'
import App from './App'
ReactDOM.createRoot(document.getElementById('root')!).render(<React.StrictMode><App /></React.StrictMode>)
```

```tsx
// frontend/src/App.tsx
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import KioskPage from './components/kiosk/KioskPage'
import ScanPage from './components/scan/ScanPage'
import DashboardPage from './components/dashboard/DashboardPage'
export default function App() {
  return (<BrowserRouter>
    <Routes>
      <Route path="/" element={<KioskPage />} />
      <Route path="/kiosk" element={<KioskPage />} />
      <Route path="/scan" element={<ScanPage />} />
      <Route path="/dashboard" element={<DashboardPage />} />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  </BrowserRouter>)
}
```

- [ ] **Step 4: Install + verify**

```bash
cd "/run/media/sanng/New Volume/HACKAITHON/hackaithon-de-tai-6-govone/frontend"
npm install 2>&1 | tail -3
npx tsc --noEmit 2>&1 || true
```
