import { useState } from "react";
import { Shield, AlertTriangle, CheckCircle, Loader2, Sparkles } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { cn } from "@/lib/utils";

interface PredictionResult {
  prediction: "REAL" | "FAKE";
  confidence: number;
}

export const NewsAnalyzer = () => {
  const [newsText, setNewsText] = useState("");
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState<PredictionResult | null>(null);

  // Simulated ML prediction - replace with actual API call to your Flask backend
  const analyzeNews = async () => {
    if (!newsText.trim()) return;
    
    setIsAnalyzing(true);
    setResult(null);

    // Simulate API call delay
    await new Promise((resolve) => setTimeout(resolve, 1500));

    // Simulated prediction logic based on text patterns
    // In production, this calls your Flask API: POST /predict
    const text = newsText.toLowerCase();
    const fakeIndicators = [
      "breaking:", "shocking", "you won't believe", "secret", "they don't want you to know",
      "miracle", "exposed", "conspiracy", "urgent", "share before deleted"
    ];
    
    const realIndicators = [
      "according to", "study shows", "researchers", "officials said", 
      "reported", "data indicates", "analysis", "evidence", "sources"
    ];

    let fakeScore = fakeIndicators.filter(ind => text.includes(ind)).length;
    let realScore = realIndicators.filter(ind => text.includes(ind)).length;
    
    // Add some randomness for demo variety
    const randomFactor = Math.random() * 0.3;
    const totalScore = (realScore - fakeScore) / Math.max(realScore + fakeScore, 1);
    
    const isFake = totalScore < randomFactor - 0.15;
    const confidence = 65 + Math.random() * 30; // 65-95% confidence

    setResult({
      prediction: isFake ? "FAKE" : "REAL",
      confidence: Math.round(confidence * 10) / 10
    });
    
    setIsAnalyzing(false);
  };

  const clearForm = () => {
    setNewsText("");
    setResult(null);
  };

  return (
    <div className="w-full max-w-3xl mx-auto">
      {/* Input Section */}
      <div className="bg-card rounded-2xl p-6 md:p-8 card-elevated border border-border/50">
        <div className="flex items-center gap-3 mb-6">
          <div className="w-10 h-10 rounded-xl bg-primary/10 flex items-center justify-center">
            <Shield className="w-5 h-5 text-primary" />
          </div>
          <div>
            <h2 className="text-lg font-semibold text-foreground">News Analyzer</h2>
            <p className="text-sm text-muted-foreground">Paste news article or headline to verify</p>
          </div>
        </div>

        <Textarea
          placeholder="Enter a news headline or article text here..."
          value={newsText}
          onChange={(e) => setNewsText(e.target.value)}
          className="min-h-[160px] bg-secondary/50 border-border/50 resize-none text-foreground placeholder:text-muted-foreground focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all"
        />

        <div className="flex gap-3 mt-4">
          <Button
            onClick={analyzeNews}
            disabled={!newsText.trim() || isAnalyzing}
            className="flex-1 bg-primary hover:bg-primary/90 text-primary-foreground font-medium h-12 rounded-xl transition-all duration-200 disabled:opacity-50"
          >
            {isAnalyzing ? (
              <>
                <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                Analyzing...
              </>
            ) : (
              <>
                <Sparkles className="w-5 h-5 mr-2" />
                Check News
              </>
            )}
          </Button>
          
          {(newsText || result) && (
            <Button
              onClick={clearForm}
              variant="outline"
              className="h-12 px-6 rounded-xl border-border/50 hover:bg-secondary/50"
            >
              Clear
            </Button>
          )}
        </div>
      </div>

      {/* Analysis Progress */}
      {isAnalyzing && (
        <div className="mt-6 bg-card rounded-2xl p-6 card-elevated border border-border/50">
          <div className="flex items-center gap-4">
            <div className="relative w-12 h-12">
              <div className="absolute inset-0 rounded-full border-2 border-primary/20"></div>
              <div className="absolute inset-0 rounded-full border-2 border-primary border-t-transparent animate-spin"></div>
            </div>
            <div>
              <p className="font-medium text-foreground">Analyzing content...</p>
              <p className="text-sm text-muted-foreground">Running ML classification model</p>
            </div>
          </div>
          <div className="mt-4 h-1 bg-secondary rounded-full overflow-hidden">
            <div className="h-full bg-primary rounded-full animate-shimmer" 
                 style={{ 
                   width: '100%',
                   backgroundImage: 'linear-gradient(90deg, transparent, hsl(var(--primary)), transparent)',
                   backgroundSize: '200% 100%'
                 }}
            />
          </div>
        </div>
      )}

      {/* Result Display */}
      {result && !isAnalyzing && (
        <div className={cn(
          "mt-6 rounded-2xl p-6 md:p-8 text-center transition-all duration-500 animate-in fade-in slide-in-from-bottom-4",
          result.prediction === "REAL" ? "result-real" : "result-fake"
        )}>
          <div className="flex justify-center mb-4">
            {result.prediction === "REAL" ? (
              <CheckCircle className="w-16 h-16 text-success-foreground" />
            ) : (
              <AlertTriangle className="w-16 h-16 text-danger-foreground" />
            )}
          </div>
          
          <h3 className="text-3xl font-bold mb-2">
            {result.prediction === "REAL" ? "Likely Real" : "Likely Fake"}
          </h3>
          
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-black/20 backdrop-blur-sm">
            <span className="text-sm opacity-90">Confidence Score</span>
            <span className="text-lg font-bold">{result.confidence}%</span>
          </div>

          <p className="mt-4 text-sm opacity-80 max-w-md mx-auto">
            {result.prediction === "REAL" 
              ? "This content appears to be credible based on our analysis. Always verify with multiple sources."
              : "This content shows signs of misinformation. Cross-check with trusted news sources."
            }
          </p>
        </div>
      )}
    </div>
  );
};
