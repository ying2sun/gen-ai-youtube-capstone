import { serve } from "https://deno.land/std@0.168.0/http/server.ts";

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
};

serve(async (req) => {
  if (req.method === 'OPTIONS') {
    return new Response(null, { headers: corsHeaders });
  }

  try {
    const { url } = await req.json();
    console.log('Processing YouTube URL:', url);

    if (!url) {
      throw new Error('YouTube URL is required');
    }

    // Call external summarization API with extended timeout
    console.log('Calling external API for summary');
    
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 120000); // 2 minute timeout
    
    let summary;
    try {
      const apiResponse = await fetch('http://34.229.218.179:8000/summarize', {
        method: 'POST',
        headers: {
          'X-API-Key': 'MixfOlIYTnMm',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          video_url: url,
        }),
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      if (!apiResponse.ok) {
        const errorText = await apiResponse.text();
        console.error('External API error:', apiResponse.status, errorText);
        throw new Error('Failed to generate summary from external API');
      }

      const data = await apiResponse.json();
      summary = data.summary;

      if (!summary) {
        throw new Error('No summary returned from API');
      }

      console.log('Summary generated successfully');
    } catch (fetchError) {
      clearTimeout(timeoutId);
      if (fetchError instanceof Error && fetchError.name === 'AbortError') {
        throw new Error('Request timed out - the video may be too long or the service is busy. Please try again.');
      }
      throw fetchError;
    }

    return new Response(
      JSON.stringify({ 
        success: true, 
        summary
      }),
      { 
        headers: { ...corsHeaders, "Content-Type": "application/json" } 
      }
    );

  } catch (error) {
    console.error("Error in summarize-youtube function:", error);
    return new Response(
      JSON.stringify({ 
        success: false, 
        error: error instanceof Error ? error.message : "Unknown error occurred" 
      }),
      { 
        status: 500,
        headers: { ...corsHeaders, "Content-Type": "application/json" } 
      }
    );
  }
});
