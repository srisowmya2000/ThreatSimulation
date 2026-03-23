#!/bin/bash
source /Users/srisowmyanemani/Mypython/threat-graph-backend/venv/bin/activate
cd /Users/srisowmyanemani/Mypython/threat-graph-backend
/Users/srisowmyanemani/Mypython/threat-graph-backend/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000 &
echo Backend started on port 8000
cd /Users/srisowmyanemani/Mypython/threat-dashboard
npm run dev
