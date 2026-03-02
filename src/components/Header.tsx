import { Shield, Github, LogOut, LayoutDashboard } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "@/hooks/useAuth";

export const Header = () => {
  const navigate = useNavigate();
  const { user, isAdmin, signOut } = useAuth();

  const handleLogout = async () => {
    await signOut();
    navigate("/auth");
  };

  return (
    <header className="border-b border-border/50 bg-card/50 backdrop-blur-xl sticky top-0 z-50">
      <div className="container mx-auto px-4 h-16 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-primary/10 flex items-center justify-center">
            <Shield className="w-5 h-5 text-primary" />
          </div>
          <div>
            <h1 className="text-lg font-bold text-foreground">FakeGuard</h1>
            <p className="text-xs text-muted-foreground hidden sm:block">
              ML-Powered News Verification
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          {user && (
            <span className="text-xs text-muted-foreground hidden md:block">
              {user.email}
            </span>
          )}

          {isAdmin && (
            <button
              onClick={() => navigate("/admin")}
              className="flex items-center gap-2 px-4 py-2 rounded-lg bg-primary/10 hover:bg-primary/20 transition-colors text-sm text-primary font-medium"
            >
              <LayoutDashboard className="w-4 h-4" />
              <span className="hidden sm:inline">Admin</span>
            </button>
          )}

          <a
            href="https://github.com/astromanu007/truth-teller"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-2 px-4 py-2 rounded-lg bg-secondary hover:bg-secondary/80 transition-colors text-sm text-muted-foreground hover:text-foreground"
          >
            <Github className="w-4 h-4" />
            <span className="hidden sm:inline">View Source</span>
          </a>

          {user && (
            <button
              onClick={handleLogout}
              className="flex items-center gap-2 px-4 py-2 rounded-lg bg-secondary hover:bg-secondary/80 transition-colors text-sm text-muted-foreground hover:text-foreground"
            >
              <LogOut className="w-4 h-4" />
              <span className="hidden sm:inline">Logout</span>
            </button>
          )}
        </div>
      </div>
    </header>
  );
};
