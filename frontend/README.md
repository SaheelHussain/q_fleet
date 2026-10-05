# Q-Fleet Frontend

The React + Vite dashboard is deployed as a static site on Vercel.

## Local development

```bash
npm ci
npm run dev
```

## Vercel deployment

1. Import the repository into Vercel from GitHub.
2. Set the Vercel project root to the repository root. The root [vercel.json](../vercel.json) builds `frontend` and serves the SPA.
3. Set the `VITE_API_BASE_URL` environment variable to the public FastAPI backend URL, including `/api`, for example:

```text
VITE_API_BASE_URL=https://your-backend.example.com/api
```

4. Deploy or redeploy after setting the environment variable.

The FastAPI backend must be hosted separately from this static Vercel deployment. Set its `FRONTEND_ORIGINS` environment variable to the exact Vercel site origin, such as `https://your-project.vercel.app`. For local development, copy `.env.example` to `.env.local` and use `http://localhost:8000/api`.
