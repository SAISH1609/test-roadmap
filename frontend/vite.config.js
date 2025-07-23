import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { fileURLToPath, URL } from 'node:url'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  server: {
    host: '0.0.0.0',
    port: parseInt(process.env.PORT || '5173'),
    allowedHosts: [
      'all', // Allow all hosts for Railway
      'frontend-production-25ef.up.railway.app', // Your specific Railway domain
      '.railway.app', // All Railway domains
      'localhost',
      '127.0.0.1'
    ],
  },
  preview: {
    host: '0.0.0.0',
    port: parseInt(process.env.PORT || '4173'),
    allowedHosts: [
      'all', // Allow all hosts for Railway
      'frontend-production-25ef.up.railway.app', // Your specific Railway domain  
      '.railway.app', // All Railway domains
      'localhost',
      '127.0.0.1'
    ],
  },
})
