import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card } from "@/components/ui/card";
import { useToast } from "@/components/ui/use-toast";
import { supabase } from "@/integrations/supabase/client";
import { Loader2, Youtube, Sparkles, Copy, CheckCircle2 } from "lucide-react";

const Index = () => {
  const [url, setUrl] = useState("");
  const [summary, setSummary] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [copied, setCopied] = useState(false);
  const { toast } = useToast();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!url.trim()) {
      toast({
        title: "Error",
        description: "Please enter a YouTube URL",
        variant: "destructive",
      });
      return;
    }

    setIsLoading(true);
    setSummary("");
    
    try {
      const { data, error } = await supabase.functions.invoke('summarize-youtube', {
        body: { url }
      });

      if (error) throw error;

      if (data.success) {
        setSummary(data.summary);
        toast({
          title: "Success!",
          description: "Summary generated successfully",
        });
      } else {
        throw new Error(data.error || "Failed to generate summary");
      }
    } catch (error) {
      console.error('Error:', error);
      toast({
        title: "Error",
        description: error instanceof Error ? error.message : "Failed to generate summary. Please try again.",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(summary);
    setCopied(true);
    toast({
      title: "Copied!",
      description: "Summary copied to clipboard",
    });
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-4">
      <div className="w-full max-w-4xl space-y-8 animate-in fade-in duration-700">
        {/* University Header */}
        <div className="text-center space-y-2 mb-8">
          <h2 className="text-xl font-semibold text-primary">University of Michigan Capstone</h2>
          <p className="text-lg text-muted-foreground">Team Candles</p>
        </div>

        {/* Header */}
        <div className="text-center space-y-4">
          <div className="flex items-center justify-center gap-3 mb-4">
            <Youtube className="w-12 h-12 text-primary animate-glow" />
            <h1 className="text-5xl font-bold bg-gradient-to-r from-primary to-amber-300 bg-clip-text text-transparent">
              YouTube Summarizer
            </h1>
          </div>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Get instant AI-powered summaries of any YouTube video. Just paste the link and let our intelligent system do the rest.
          </p>
        </div>

        {/* Input Card */}
        <Card className="glass-morphism p-8 shadow-card border-primary/20">
          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="space-y-3">
              <label htmlFor="youtube-url" className="text-sm font-medium text-foreground flex items-center gap-2">
                <Sparkles className="w-4 h-4 text-primary" />
                YouTube URL
              </label>
              <div className="flex gap-3">
                <Input
                  id="youtube-url"
                  type="url"
                  value={url}
                  onChange={(e) => setUrl(e.target.value)}
                  placeholder="https://www.youtube.com/watch?v=..."
                  className="flex-1 h-12 bg-secondary/50 border-border/50 focus:border-primary transition-all duration-300"
                  disabled={isLoading}
                />
                <Button
                  type="submit"
                  disabled={isLoading}
                  className="h-12 px-8 bg-gradient-to-r from-primary to-cyan-500 hover:shadow-glow transition-all duration-300"
                >
                  {isLoading ? (
                    <>
                      <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                      Analyzing
                    </>
                  ) : (
                    <>
                      <Sparkles className="mr-2 h-5 w-5" />
                      Summarize
                    </>
                  )}
                </Button>
              </div>
            </div>
          </form>
        </Card>

        {/* Summary Card */}
        {summary && (
          <Card className="glass-morphism p-8 shadow-card border-primary/20 animate-in slide-in-from-bottom-4 duration-500">
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <h2 className="text-2xl font-semibold flex items-center gap-2">
                  <Sparkles className="w-6 h-6 text-primary" />
                  Summary
                </h2>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={handleCopy}
                  className="border-primary/30 hover:bg-primary/10 transition-all duration-300"
                >
                  {copied ? (
                    <>
                      <CheckCircle2 className="mr-2 h-4 w-4 text-primary" />
                      Copied!
                    </>
                  ) : (
                    <>
                      <Copy className="mr-2 h-4 w-4" />
                      Copy
                    </>
                  )}
                </Button>
              </div>
              <div className="prose prose-invert max-w-none">
                <div className="text-foreground/90 whitespace-pre-wrap leading-relaxed">
                  {summary}
                </div>
              </div>
            </div>
          </Card>
        )}

        {/* Loading State */}
        {isLoading && !summary && (
          <Card className="glass-morphism p-12 shadow-card border-primary/20 animate-pulse">
            <div className="flex flex-col items-center justify-center space-y-4">
              <Loader2 className="h-12 w-12 animate-spin text-primary" />
              <p className="text-muted-foreground text-center">
                Analyzing video and generating summary...
              </p>
            </div>
          </Card>
        )}
      </div>
    </div>
  );
};

export default Index;
