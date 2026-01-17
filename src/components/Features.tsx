import { Brain, Zap, Lock, BarChart3 } from "lucide-react";

const features = [
  {
    icon: Brain,
    title: "Machine Learning",
    description: "PassiveAggressiveClassifier trained on thousands of news articles"
  },
  {
    icon: Zap,
    title: "Instant Analysis",
    description: "Get results in milliseconds with optimized TF-IDF vectorization"
  },
  {
    icon: Lock,
    title: "Privacy First",
    description: "All processing happens locally - no data stored or shared"
  },
  {
    icon: BarChart3,
    title: "Confidence Score",
    description: "Transparent probability scores for informed decision making"
  }
];

export const Features = () => {
  return (
    <section className="py-16 border-t border-border/50">
      <div className="container mx-auto px-4">
        <h2 className="text-2xl font-bold text-center mb-2 text-foreground">How It Works</h2>
        <p className="text-muted-foreground text-center mb-12 max-w-lg mx-auto">
          Powered by traditional machine learning algorithms for reliable, explainable predictions
        </p>
        
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {features.map((feature, index) => (
            <div 
              key={index}
              className="bg-card rounded-xl p-6 border border-border/50 hover:border-primary/30 transition-all duration-300 group"
            >
              <div className="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                <feature.icon className="w-6 h-6 text-primary" />
              </div>
              <h3 className="font-semibold mb-2 text-foreground">{feature.title}</h3>
              <p className="text-sm text-muted-foreground">{feature.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};
