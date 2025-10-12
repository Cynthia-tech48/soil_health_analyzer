import os
from dotenv import load_dotenv
load_dotenv()

# Supabase configuration
SUPABASE_URL = "https://pmfhzmvfrmlsoxhzlgin.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBtZmh6bXZmcm1sc294aHpsZ2luIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MDEwMDIzNiwiZXhwIjoyMDc1Njc2MjM2fQ.kvLsaaKfYOgidDW-E7FvHDrT4Pt2PMHxqJhan_JakKI"

supabase = None
if SUPABASE_URL and SUPABASE_KEY:
    try:
        from supabase import create_client
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("✅ Supabase connection successful:", SUPABASE_URL)
    except Exception as e:
        print("⚠️ Warning: Supabase client import failed:", e)
        supabase = None
else:
    print("❌ Supabase not configured — DB writes disabled.")
