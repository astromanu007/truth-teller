import { Header } from "@/components/Header";
import { NewsAnalyzer } from "@/components/NewsAnalyzer";
import { Features } from "@/components/Features";
import { TechStack } from "@/components/TechStack";

const Index = () => {
  return (
    <div className="min-h-screen bg-gradient-hero">
      <Header />
      
      {/* Hero Section */}
      <main className="container mx-auto px-4 py-12 md:py-20">
        <div className="text-center mb-12">
          <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-primary/10 border border-primary/20 text-primary text-sm font-medium mb-6">
            <span className="w-2 h-2 rounded-full bg-primary animate-pulse"></span>
            ML-Powered Detection
          </div>
          
          <h1 className="text-4xl md:text-6xl font-extrabold text-foreground mb-4 tracking-tight">
            Detect <span className="text-gradient-primary">Fake News</span>
            <br />in Seconds
          </h1>
          
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Our machine learning model analyzes news articles and headlines to identify 
            potential misinformation with high accuracy and transparency.
          </p>
        </div>

        <NewsAnalyzer />
      </main>

      <Features />
      <TechStack />

      {/* Footer */}
      <footer className="border-t border-border/50 py-8">
        <div className="container mx-auto px-4 text-center">
          <p className="text-sm text-muted-foreground">
            Built with Flask + Scikit-learn • TF-IDF + PassiveAggressiveClassifier
          </p>
          <p className="text-xs text-muted-foreground/60 mt-2">
            Demo frontend - Connect to your Python backend for production use
          </p>
        </div>
      </footer>
    </div>
  );
};

export default Index;
