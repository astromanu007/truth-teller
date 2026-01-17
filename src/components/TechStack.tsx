const technologies = [
  { name: "Python", category: "Backend" },
  { name: "Flask", category: "API" },
  { name: "Scikit-learn", category: "ML" },
  { name: "TF-IDF", category: "NLP" },
  { name: "PassiveAggressive", category: "Model" },
  { name: "Pandas", category: "Data" },
];

export const TechStack = () => {
  return (
    <section className="py-12 border-t border-border/50 bg-secondary/30">
      <div className="container mx-auto px-4">
        <p className="text-sm text-muted-foreground text-center mb-6">Built with</p>
        <div className="flex flex-wrap justify-center gap-3">
          {technologies.map((tech, index) => (
            <div 
              key={index}
              className="px-4 py-2 bg-card rounded-lg border border-border/50 flex items-center gap-2"
            >
              <span className="text-xs text-primary font-medium">{tech.category}</span>
              <span className="text-sm text-foreground">{tech.name}</span>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};
