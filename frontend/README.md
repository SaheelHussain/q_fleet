# Q-Fleet Frontend

The React + Vite dashboard is built and served alongside the FastAPI backend in one Vercel deployment.

## Local development

```bash
npm ci
npm run dev
```

## Vercel deployment

1. Import the repository into Vercel from GitHub.
2. Set the Vercel project root to the repository root. Root [vercel.json](../vercel.json) builds the frontend, and root [index.py](../index.py) mounts its output on the FastAPI app.
3. Deploy. The frontend uses the same-origin `/api` path, so no backend URL environment variable is needed.

For local development, the frontend defaults to `http://localhost:8000/api`; run the backend and Vite development server in separate terminals.
