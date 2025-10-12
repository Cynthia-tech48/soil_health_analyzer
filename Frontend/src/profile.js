import { useEffect, useState } from "react";
import { createClient } from "@supabase/supabase-js";

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY
);

export default function Profile() {
  const [results, setResults] = useState([]);

  useEffect(() => {
    const fetchResults = async () => {
      const { data, error } = await supabase
        .from("analysis_results")
        .select("*")
        .order("created_at", { ascending: false });
      if (error) console.error(error);
      else setResults(data);
    };

    fetchResults();
  }, []);

  return (
    <div style={{ padding: "2rem" }}>
      <h1>Analysis Results</h1>
      <ul>
        {results.map((r) => (
          <li key={r.id}>
            {r.name}: {r.soil_health_score}% — {r.health_label}
          </li>
        ))}
      </ul>
    </div>
  );
}
