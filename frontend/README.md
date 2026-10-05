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
3. Deploy the FastAPI backend to Render by creating a Blueprint from this repository; [render.yaml](../render.yaml) defines its setup. Once it is deployed, set the `VITE_API_BASE_URL` environment variable to its public URL including `/api`, for example:

```text
VITE_API_BASE_URL=https://your-render-service.onrender.com/api
```

4. Deploy or redeploy after setting the environment variable.

The Render Blueprint sets `FRONTEND_ORIGINS` to the current Vercel site origin. If your Vercel domain changes, update that value in Render. For local development, copy `.env.example` to `.env.local` and use `http://localhost:8000/api`.

If the backend URL is missing or invalid, the dashboard displays a backend-unavailable message instead of remaining on its loading screen.
